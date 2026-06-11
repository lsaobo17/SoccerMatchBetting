# 2026 世界杯比分预测智能体 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建一个中文 Markdown 工作流项目，用于 2026 世界杯赛前资料整理、盘口快照记录、两组比分预测和赛后复盘。

**Architecture:** 第一版不做程序后台，使用 `AGENTS.md` 约束智能体行为，使用 `methodology/` 固化预测和复盘规则，使用 `tournaments/2026-world-cup/` 按日期归档比赛。每场比赛一个 Markdown 文件，每日一个汇总文件，后续查询时先更新资料再预测。

**Tech Stack:** Markdown、Git、Codex/AGENTS.md 工作流、联网资料核对。

---

## File Structure

- Create `AGENTS.md`: 根目录智能体规则，包含禁止批量删除、每次查询更新、盘口优先级、输出格式和娱乐边界。
- Create `README.md`: 项目说明、使用方式、目录说明、风险提示。
- Create `data_sources/sources.md`: 官方赛程、公开赛程/赔率、盘口、球队和比分来源说明。
- Create `methodology/prediction-model.md`: 方案三混合评分模型。
- Create `methodology/review-rules.md`: 赛后命中与偏差复盘规则。
- Create `tournaments/2026-world-cup/tournament.md`: 赛事总览和 Group A 首日赛程记录。
- Create `tournaments/2026-world-cup/teams/*.md`: 首日涉及国家队基础资料占位，供后续持续更新。
- Create `tournaments/2026-world-cup/matches/2026-06-11/*.md`: 2026-06-11 两场比赛模板。
- Create `tournaments/2026-world-cup/daily/2026-06-11.md`: 每日汇总模板。
- Create `tournaments/2026-world-cup/reviews/2026-06-11-review.md`: 赛后复盘模板。

## Task 1: Git 初始化确认

**Files:**
- Existing: `.git/`

- [x] **Step 1: 初始化 git 仓库**

Run: `git init -b main`

Expected: 仓库初始化成功，当前分支为 `main`。

## Task 2: 创建工作流规则和项目说明

**Files:**
- Create: `AGENTS.md`
- Create: `README.md`

- [x] **Step 1: 写入根目录智能体规则**

`AGENTS.md` 必须包含禁止批量删除、中文文档、每次预测前刷新资料、两组比分输出、信心等级、赛后复盘、娱乐参考边界。

- [x] **Step 2: 写入项目 README**

`README.md` 必须说明项目用途、目录结构、使用方式和风险边界。

## Task 3: 创建方法论文档

**Files:**
- Create: `data_sources/sources.md`
- Create: `methodology/prediction-model.md`
- Create: `methodology/review-rules.md`

- [x] **Step 1: 写入资料源规范**

记录官方赛程优先、用户盘口优先、公开页面补充、实际比分官方优先。

- [x] **Step 2: 写入混合评分模型**

记录实力差、近期状态、阵容完整度、战术克制、盘口共识、进球倾向、冷门风险。

- [x] **Step 3: 写入赛后复盘规则**

记录精准命中、方向命中、进球区间命中、未命中，以及偏差原因分类。

## Task 4: 创建 2026 世界杯赛事目录和首日文件

**Files:**
- Create: `tournaments/2026-world-cup/tournament.md`
- Create: `tournaments/2026-world-cup/teams/mexico.md`
- Create: `tournaments/2026-world-cup/teams/south-africa.md`
- Create: `tournaments/2026-world-cup/teams/south-korea.md`
- Create: `tournaments/2026-world-cup/teams/czechia.md`
- Create: `tournaments/2026-world-cup/matches/2026-06-11/001-mexico-vs-south-africa.md`
- Create: `tournaments/2026-world-cup/matches/2026-06-11/002-south-korea-vs-czechia.md`
- Create: `tournaments/2026-world-cup/daily/2026-06-11.md`
- Create: `tournaments/2026-world-cup/reviews/2026-06-11-review.md`

- [x] **Step 1: 创建赛事总览**

写入 2026 世界杯第一版资料规则、Group A 首日两场比赛、更新时间和来源。

- [x] **Step 2: 创建四支首日球队资料文件**

每个球队文件包含基础资料、待更新情报、盘口相关观察、后续记录。

- [x] **Step 3: 创建两场首日比赛文件**

每场文件包含比赛信息、盘口快照、赛前情报、预测评分、推荐比分和赛后复盘模板。

- [x] **Step 4: 创建每日汇总和复盘模板**

每日文件列出最近场次、盘口状态、推荐比分占位；复盘文件列出赛后更新表格。

## Task 5: 验证和提交

**Files:**
- All created Markdown files

- [x] **Step 1: 验证文件结构**

Run: `rg --files`

Expected: 输出包含所有计划文件。

- [x] **Step 2: 检查占位风险词**

Run: `Select-String -Path .\*.md, .\data_sources\*.md, .\methodology\*.md, .\tournaments\2026-world-cup\**\*.md -Pattern ('TO' + 'DO|TB' + 'D') -CaseSensitive:$false`

Expected: 不出现占位风险词。

- [x] **Step 3: 提交初始项目骨架**

Run:

```powershell
git add .
git commit -m "init world cup prediction agent workspace"
```

Expected: 创建首个提交。

## Self-Review

- Spec coverage: 覆盖中文文档、Markdown 工作流、盘口 A 范围、A+B 数据获取、混合评分、两组比分、赛后复盘、按日期归档和 `AGENTS.md` 规则。
- Placeholder scan: 计划文档不使用占位风险词。
- Scope check: 第一版只落地文档和目录骨架，不实现 Web 后台、数据库、自动下注或赔率 API。
