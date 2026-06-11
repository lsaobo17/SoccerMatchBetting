#!/usr/bin/env python3
"""世界杯赛前预测技能调度器。

设计目标：由 cron/systemd 等外部定时器高频调用本脚本；脚本每次扫描本项目
`tournaments/2026-world-cup/matches/` 下的 Markdown 比赛文件，找出未开赛且最近
的最多四场比赛，并在最近一场开赛前指定提前量（默认 60 分钟）触发一次预测技能命令。

脚本只负责调度，不生成下注建议，不自动下注。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATCHES_DIR = REPO_ROOT / "tournaments" / "2026-world-cup" / "matches"
DEFAULT_STATE_FILE = REPO_ROOT / ".scheduler-state" / "prediction_scheduler.json"
DEFAULT_COMMAND = (
    "codex exec '使用 $soccer-match-prediction 更新最近未开赛的世界杯比赛，"
    "优先处理最近四场，并按项目规则输出两组娱乐参考比分。'"
)
BEIJING_TZ = timezone(timedelta(hours=8))

STATUS_RE = re.compile(r"^status:\s*(?P<status>\S+)", re.MULTILINE)
TITLE_RE = re.compile(r"^#\s+(?P<title>.+?)\s*$", re.MULTILINE)
ROUND_RE = re.compile(r"^-\s*场次：\s*(?P<round>\S+)", re.MULTILINE)
BEIJING_TIME_RE = re.compile(
    r"^-\s*北京时间：\s*(?P<date>\d{4}-\d{2}-\d{2})\s+"
    r"(?P<hour>\d{1,2}):(?P<minute>\d{2})\s*(?P<offset>\+08:00)?",
    re.MULTILINE,
)


@dataclass(frozen=True)
class Match:
    path: Path
    title: str
    round_no: str
    starts_at: datetime

    @property
    def key(self) -> str:
        return f"{self.starts_at.isoformat()}|{self.path.relative_to(REPO_ROOT)}"


def parse_beijing_datetime(match: re.Match[str]) -> datetime:
    year, month, day = (int(part) for part in match.group("date").split("-"))
    hour = int(match.group("hour"))
    minute = int(match.group("minute"))
    return datetime(year, month, day, hour, minute, tzinfo=BEIJING_TZ)


def parse_match_file(path: Path) -> Match | None:
    text = path.read_text(encoding="utf-8")
    status_match = STATUS_RE.search(text)
    if status_match and status_match.group("status") not in {"pre_match", "scheduled"}:
        return None

    time_match = BEIJING_TIME_RE.search(text)
    if not time_match:
        return None

    title_match = TITLE_RE.search(text)
    round_match = ROUND_RE.search(text)
    return Match(
        path=path,
        title=title_match.group("title") if title_match else path.stem,
        round_no=round_match.group("round") if round_match else "未知",
        starts_at=parse_beijing_datetime(time_match),
    )


def load_matches(matches_dir: Path, now: datetime, limit: int) -> list[Match]:
    candidates: list[Match] = []
    for path in sorted(matches_dir.glob("*/*.md")):
        parsed = parse_match_file(path)
        if parsed and parsed.starts_at > now:
            candidates.append(parsed)
    return sorted(candidates, key=lambda item: item.starts_at)[:limit]


def read_state(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def write_state(path: Path, state: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def format_match_list(matches: Iterable[Match]) -> str:
    lines = []
    for item in matches:
        rel_path = item.path.relative_to(REPO_ROOT)
        lines.append(f"- {item.round_no} {item.title}：{item.starts_at.isoformat()}（{rel_path}）")
    return "\n".join(lines)


def run_command(command: str, dry_run: bool) -> int:
    if dry_run:
        print(f"[dry-run] 将执行命令：{command}")
        return 0
    completed = subprocess.run(command, shell=True, cwd=REPO_ROOT, check=False)
    return completed.returncode


def run_notify_command(command: str | None, message: str, dry_run: bool) -> int:
    if not command:
        return 0
    if dry_run:
        print(f"[dry-run] 将发送提醒：{command}")
        print(message)
        return 0

    env = os.environ.copy()
    env["SOCCER_SCHEDULER_MESSAGE"] = message
    completed = subprocess.run(
        command,
        shell=True,
        cwd=REPO_ROOT,
        input=message,
        text=True,
        env=env,
        check=False,
    )
    return completed.returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="按最近四场世界杯比赛时间提前触发预测技能。")
    parser.add_argument(
        "--matches-dir", type=Path, default=DEFAULT_MATCHES_DIR, help="比赛 Markdown 根目录。"
    )
    parser.add_argument(
        "--state-file", type=Path, default=DEFAULT_STATE_FILE, help="防重复触发状态文件。"
    )
    parser.add_argument(
        "--lead-minutes", type=int, default=60, help="提前多少分钟触发预测技能，默认 60。"
    )
    parser.add_argument(
        "--window-minutes", type=int, default=15, help="允许触发窗口，适配 cron 轮询延迟，默认 15。"
    )
    parser.add_argument("--limit", type=int, default=4, help="最近比赛数量，默认 4。")
    parser.add_argument(
        "--command",
        default=os.environ.get("SOCCER_PREDICTION_COMMAND", DEFAULT_COMMAND),
        help="要执行的预测技能命令。",
    )
    parser.add_argument(
        "--notify-command",
        default=os.environ.get("SOCCER_SCHEDULER_NOTIFY_COMMAND"),
        help="预测命令成功触发后执行的提醒命令；提醒文本会通过标准输入和 SOCCER_SCHEDULER_MESSAGE 传入。",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="只打印判断结果，不执行命令、不写入状态。"
    )
    parser.add_argument("--now", help="测试用当前时间，ISO 8601，例如 2026-06-12T02:00:00+08:00。")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    now = datetime.fromisoformat(args.now) if args.now else datetime.now(BEIJING_TZ)
    if now.tzinfo is None:
        now = now.replace(tzinfo=BEIJING_TZ)

    matches = load_matches(args.matches_dir, now=now, limit=args.limit)
    if not matches:
        print("未找到未来未开赛比赛；本次不触发预测技能。")
        return 0

    next_match = matches[0]
    trigger_at = next_match.starts_at - timedelta(minutes=args.lead_minutes)
    trigger_until = trigger_at + timedelta(minutes=args.window_minutes)

    print("最近未开赛比赛：")
    print(format_match_list(matches))
    print(f"计划触发时间：{trigger_at.isoformat()} 至 {trigger_until.isoformat()}")
    print(f"当前时间：{now.isoformat()}")

    if now < trigger_at:
        print("尚未进入触发窗口；本次不执行。")
        return 0
    if now > trigger_until:
        print("已超过触发窗口；本次不执行，等待下一次赛程窗口。")
        return 0

    state = read_state(args.state_file)
    state_key = next_match.key
    if state.get("last_triggered_match") == state_key:
        print("该最近比赛窗口已触发过；本次不重复执行。")
        return 0

    print("进入触发窗口，准备运行预测技能命令。")
    exit_code = run_command(args.command, dry_run=args.dry_run)
    if exit_code != 0:
        print(f"预测技能命令执行失败，退出码：{exit_code}", file=sys.stderr)
        return exit_code

    notify_message = (
        "世界杯预测技能已触发\n"
        f"触发时间：{now.isoformat()}\n"
        f"最近比赛：{next_match.round_no} {next_match.title}\n"
        f"开赛时间：{next_match.starts_at.isoformat()}\n"
        "处理范围：最近未开赛四场比赛，输出仅作娱乐和复盘参考。"
    )
    notify_exit_code = run_notify_command(args.notify_command, notify_message, dry_run=args.dry_run)
    if notify_exit_code != 0:
        print(f"提醒命令执行失败，退出码：{notify_exit_code}", file=sys.stderr)
        return notify_exit_code

    if not args.dry_run:
        write_state(
            args.state_file,
            {
                "last_triggered_match": state_key,
                "last_triggered_at": now.isoformat(),
                "lead_minutes": str(args.lead_minutes),
                "limit": str(args.limit),
            },
        )
    print("预测技能调度完成。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
