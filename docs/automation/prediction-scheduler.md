# 世界杯预测技能定时任务

本项目可以通过 `scripts/prediction_scheduler.py` 创建“轮询式定时任务”：外部定时器每隔几分钟运行一次脚本，脚本会读取 `tournaments/2026-world-cup/matches/` 下的比赛 Markdown 文件，筛选最近四场未开赛比赛，并按最近一场比赛的北京时间提前 1 小时触发项目预测技能。

## 触发逻辑

1. 扫描比赛文件中的 `status` 和 `北京时间` 字段。
2. 只选择 `pre_match` 或 `scheduled` 状态且开赛时间晚于当前时间的比赛。
3. 按开赛时间排序，保留最近四场。
4. 以最近一场比赛的开赛时间减去 `--lead-minutes` 作为触发时间，默认提前 60 分钟。
5. 在默认 15 分钟触发窗口内运行一次预测技能命令。
6. 如配置了 `--notify-command` 或 `SOCCER_SCHEDULER_NOTIFY_COMMAND`，预测命令成功触发后再发送一条提醒。
7. 写入 `.scheduler-state/prediction_scheduler.json`，避免同一场最近比赛重复触发。

> 注意：该脚本只运行项目预测资料更新流程，不提供下注金额建议，不自动投注，也不把预测包装成确定性结论。

## 本地试运行

```bash
python3 scripts/prediction_scheduler.py --dry-run
```

指定一个测试时间，验证是否会在开赛前 1 小时触发：

```bash
python3 scripts/prediction_scheduler.py --dry-run --now 2026-06-12T02:00:00+08:00
```

## 配置实际预测技能命令

默认命令会调用 Codex 并要求使用 `$soccer-match-prediction`：

```bash
codex exec '使用 $soccer-match-prediction 更新最近未开赛的世界杯比赛，优先处理最近四场，并按项目规则输出两组娱乐参考比分。'
```

如果本机 Codex CLI 路径、技能名称或提示词不同，可以通过环境变量覆盖：

```bash
export SOCCER_PREDICTION_COMMAND="codex exec '使用 \$soccer-match-prediction 更新最近未开赛的世界杯比赛，优先处理最近四场，并按项目规则输出两组娱乐参考比分。'"
```

也可以在运行脚本时传入：

```bash
python3 scripts/prediction_scheduler.py --command "codex exec '使用 \$soccer-match-prediction 更新最近未开赛的世界杯比赛，优先处理最近四场。'"
```

## 输出结果和提醒方式

默认情况下，调度器**不会自动把结果提交到 ChatGPT App 对话里**。它是在运行环境的命令行里执行 `codex exec`，因此输出位置取决于你如何启动它：

- 手动运行时：结果直接显示在当前终端。
- 使用 cron 示例时：结果会追加到 `logs/prediction-scheduler.log`。
- 使用 systemd user timer 时：结果可通过 `journalctl --user -u soccer-prediction-scheduler.service` 查看。
- 预测技能本身按项目规则更新比赛 Markdown 文件；ChatGPT App 不会收到主动推送，除非你额外接入通知通道。

如果需要“提醒”，可以配置 `--notify-command` 或环境变量 `SOCCER_SCHEDULER_NOTIFY_COMMAND`。提醒只在预测命令成功触发后发送，提醒文本会同时通过标准输入和 `SOCCER_SCHEDULER_MESSAGE` 环境变量传给通知命令。

本地验证提醒内容：

```bash
python3 scripts/prediction_scheduler.py --dry-run --now 2026-06-12T02:00:00+08:00 --notify-command 'cat'
```

把提醒写入本地日志文件示例：

```bash
python3 scripts/prediction_scheduler.py --notify-command 'mkdir -p logs && cat >> logs/prediction-notify.log'
```

如果想推送到手机、企业微信、Telegram、邮件或其他通知工具，需要把对应工具的 CLI / webhook 包装成 `--notify-command`；本仓库默认不内置第三方推送密钥。

## cron 示例

每 5 分钟检查一次，真正执行时间仍由脚本判断：

```cron
*/5 * * * * cd /workspace/SoccerMatchBetting && /usr/bin/env bash -lc 'mkdir -p logs && python3 scripts/prediction_scheduler.py >> logs/prediction-scheduler.log 2>&1'
```

如需保存日志，请先创建 `logs/` 目录；不要使用批量删除命令清理日志。

## systemd user timer 示例

`~/.config/systemd/user/soccer-prediction-scheduler.service`：

```ini
[Unit]
Description=SoccerMatchBetting prediction scheduler

[Service]
Type=oneshot
WorkingDirectory=/workspace/SoccerMatchBetting
ExecStart=/usr/bin/python3 /workspace/SoccerMatchBetting/scripts/prediction_scheduler.py
```

`~/.config/systemd/user/soccer-prediction-scheduler.timer`：

```ini
[Unit]
Description=Run SoccerMatchBetting prediction scheduler every 5 minutes

[Timer]
OnCalendar=*:0/5
Persistent=true

[Install]
WantedBy=timers.target
```

启用：

```bash
systemctl --user daemon-reload
systemctl --user enable --now soccer-prediction-scheduler.timer
```

## 维护提醒

- 每次新增或更新比赛文件时，务必填写 `status` 与 `北京时间`。
- 赛程、盘口和赛前情报仍必须按 `AGENTS.md` 规则在预测技能执行时联网更新。
- 如果官方赛程变更，以 FIFA 官方赛程和比分页面为准，先更新比赛文件，再依赖调度器触发预测。
