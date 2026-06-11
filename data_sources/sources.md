# 数据源规范

更新时间：2026-06-11T12:31:36+08:00

## 数据源优先级

### 1. 官方赛程和官方比分

优先使用 FIFA 官方页面核对赛程、开球时间、赛事阶段和实际比分。

- FIFA Scores & Fixtures: https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/scores-fixtures
- FIFA match schedule article: https://www.fifa.com/en/articles/match-schedule-fixtures-results-teams-stadiums

### 2. 用户提供的盘口

用户粘贴的盘口文本或截图是盘口记录的最高优先级来源。

记录时必须保留：

- 用户提供时间
- 原始盘口文本摘要
- 胜平负
- 亚洲让球
- 大小球
- 是否完整

### 3. 公开赛程和赔率页面

当用户未提供盘口时，可使用公开页面补充赛程、胜平负赔率或盘口趋势。

可用作交叉检查的公开页面：

- FOX Sports World Cup schedule: https://www.foxsports.com/stories/soccer/2026-world-cup-schedule-all-games-dates-matchups-how-watch
- FOX Sports FIFA World Cup schedule: https://www.foxsports.com/soccer/fifa-world-cup/schedule
- ESPN World Cup schedule: https://www.espn.com/soccer/schedule/_/league/fifa.world

公开页面的盘口可能不完整，尤其是亚洲让球和大小球。缺失时必须标注 `盘口状态：部分缺失` 或 `盘口状态：缺失`。

### 4. 球队和赛前情报

球队情报可参考：

- 官方国家队名单
- FIFA 球队页面
- 主流体育媒体伤停新闻
- 赛前发布会
- 可靠记者或官方协会公告

情报记录必须区分：

- 已确认
- 多方报道
- 单一来源
- 未确认

## 冲突处理

如果不同来源出现冲突：

- 赛程和实际比分以官方来源为准。
- 盘口以用户提供的最新快照为准。
- 新闻和伤停信息需要列出冲突来源，不得直接合并为确定结论。

## 最近四场已核对公开信息

截至 2026-06-11T12:31:36+08:00，公开页面显示最近四场未开赛世界杯比赛为：

| 场次 | 比赛 | 阶段 | 场地 | 美东时间 | 北京时间 |
| --- | --- | --- | --- | --- | --- |
| 001 | Mexico vs South Africa | Group A | Mexico City Stadium | 2026-06-11 15:00 ET | 2026-06-12 03:00 +08:00 |
| 002 | South Korea vs Czechia | Group A | Guadalajara Stadium | 2026-06-11 22:00 ET | 2026-06-12 10:00 +08:00 |
| 003 | Canada vs Bosnia and Herzegovina | Group B | Toronto Stadium | 2026-06-12 15:00 ET | 2026-06-13 03:00 +08:00 |
| 004 | USA vs Paraguay | Group D | Los Angeles Stadium | 2026-06-12 21:00 ET | 2026-06-13 09:00 +08:00 |

本次公开盘口来源包括：

- 365Scores/BetMGM：四场胜平负和部分大小球。
- RotoWire：墨西哥 vs 南非、加拿大 vs 波黑、美国 vs 巴拉圭的多家胜平负汇总和赛前情报。
- BetInAsia：墨西哥 vs 南非的亚洲让球和大小球公开片段。
- SBG Global：加拿大 vs 波黑的胜平负、让球和大小球。
- Pinnacle 公开页面片段：韩国 vs 捷克、美国 vs 巴拉圭的胜平负、让球和大小球。
- FOX Sports：赛程交叉验证，加拿大 vs 波黑比赛页的胜平负和大小球片段。

用户后续提供盘口文本或截图时，仍以用户提供的最新快照为最高优先级。
