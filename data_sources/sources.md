# 数据源规范

更新时间：2026-06-13T20:15:31+08:00

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

## 最近场次已核对公开信息

截至 2026-06-12T17:37:03+08:00，公开页面显示 001、002 已结束，最近两场未开赛世界杯比赛为 003、004：

| 场次 | 比赛 | 阶段 | 场地 | 美东时间 | 北京时间 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| 001 | Mexico vs South Africa | Group A | Mexico City Stadium | 2026-06-11 15:00 ET | 2026-06-12 03:00 +08:00 | 已结束，墨西哥 2-0 南非 |
| 002 | South Korea vs Czechia | Group A | Guadalajara Stadium | 2026-06-11 22:00 ET | 2026-06-12 10:00 +08:00 | 已结束，韩国 2-1 捷克 |
| 003 | Canada vs Bosnia and Herzegovina | Group B | Toronto Stadium | 2026-06-12 15:00 ET | 2026-06-13 03:00 +08:00 | 未开赛 |
| 004 | USA vs Paraguay | Group D | Los Angeles Stadium | 2026-06-12 21:00 ET | 2026-06-13 09:00 +08:00 | 未开赛 |

本次公开盘口来源包括：

- FIFA Scores & Fixtures：官方赛程和未开赛状态核对；FIFA 赛后战报用于墨西哥 vs 南非赛果复核。
- FOX Sports：赛程交叉验证；加拿大 vs 波黑、美国 vs 巴拉圭比赛页赔率和大小球片段；美国赛前文章补充胜平负、让球和大小球。
- ESPN/DraftKings：加拿大 vs 波黑、美国 vs 巴拉圭让球、大小球和胜平负动态片段。
- RotoWire：加拿大 vs 波黑、美国 vs 巴拉圭赛前情报、盘口和阵容观察。
- Covers/Kalshi、CBS Sports/FanDuel：加拿大 vs 波黑、美国 vs 巴拉圭的胜平负、大小球、阵容和天气交叉验证。
- U.S. Soccer、Guardian：美国 vs 巴拉圭赛前状态、Chris Richards 可用性、Paraguay/Enciso 情报交叉验证。
- Guardian/ESPN：韩国 vs 捷克赛后比分交叉验证。

本次伤停/情报更新要点：

- 墨西哥 vs 南非：实际 2-0，稳健比分精准命中。
- 韩国 vs 捷克：实际 2-1，分歧比分精准命中；小球判断偏差。
- 加拿大：Covers 临场前仍列 Alphonso Davies doubtful、Moise Bombito out；RotoWire 早期认为部分加拿大伤员可能接近复出，需以临场名单为准。Haris Tabakovic doubtful，Dzeko/Sunjic 预计可用。盘口偏小球，但公开前瞻存在 2-1 大球分歧。
- 美国：Chris Richards 已恢复完整训练并表示可出战，U.S. Soccer/Guardian 显示美国 26 人可供选择；Julio Enciso 状态仍不明或 doubtful，偏利好美国但盘口仍只是轻微热门或接近平手。

用户后续提供盘口文本或截图时，仍以用户提供的最新快照为最高优先级。

## 2026-06-13 查询更新

截至 2026-06-13T17:56:56+08:00，003、004 已完成赛后核对，最近四场未开赛比赛仍为 005-008：

| 场次 | 比赛 | 阶段 | 场地 | FIFA/当地时间 | 北京时间 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| 008 | Qatar vs Switzerland | Group B | San Francisco Bay Area Stadium | 2026-06-13 19:00 UTC / 12:00 PT | 2026-06-14 03:00 +08:00 | 未开赛 |
| 007 | Brazil vs Morocco | Group C | New York New Jersey Stadium | 2026-06-13 22:00 UTC / 18:00 ET | 2026-06-14 06:00 +08:00 | 未开赛 |
| 005 | Haiti vs Scotland | Group C | Boston Stadium | 2026-06-14 01:00 UTC / 21:00 ET | 2026-06-14 09:00 +08:00 | 未开赛 |
| 006 | Australia vs Turkiye | Group D | BC Place Vancouver | 2026-06-14 04:00 UTC / 21:00 PT | 2026-06-14 12:00 +08:00 | 未开赛 |

本次公开信息核对：

- FIFA Scores & Fixtures、FIFA Match Centre：赛程和官方开球时间优先来源；美国 4-1 巴拉圭使用 FIFA 赛后战报核对。
- ESPN、Guardian、AP：加拿大 1-1 波黑赛后比分和关键进球交叉验证。
- Al Jazeera、FOX Sports、场馆/票务页面：四场未开赛赛程交叉验证；Australia vs Turkiye 以 FIFA/FOX/BC Place 21:00 PT、04:00 UTC 口径为准。
- FOX Sports/FanDuel、Oddschecker、Action Network、RotoWire、Covers：公开胜平负、让球、大小球和赛前情报来源。
- 用户未提供盘口截图或文本，本次盘口使用公开页面快照；后续如有用户盘口，以用户快照覆盖。

## 2026-06-13 17:56 再次预测修正

本次按用户“尽可能真实靠谱”的要求，在不改变最近四场场次范围的前提下，重新收敛比分区间：

- Qatar vs Switzerland：瑞士方向维持，但从 0-3 调整为更常见的 0-2，分歧为 0-1。
- Brazil vs Morocco：巴西浅热、小球略热，Neymar 缺阵与摩洛哥防反并存；主线从 1-1/摩洛哥爆冷调整为巴西 1-0，分歧 1-1。
- Haiti vs Scotland：苏格兰胜出方向维持；考虑盘口对大 2.5 的轻微支持和海地反击，主线从 0-2 调整为 1-2。
- Australia vs Turkiye：土耳其浅热、小球偏热；主线从 1-2 调整为 0-1，分歧从澳大利亚反杀调整为 1-1。
- Al Jazeera 对 Australia vs Turkiye 的本地时间口径存在与 UTC 不完全匹配的展示问题；本项目继续以 FIFA、FOX/FOX One、BC Place/Socceroos 官方口径的 2026-06-13 21:00 PT / 2026-06-14 04:00 UTC / 北京时间 2026-06-14 12:00 为准。

## 2026-06-13 20:15 再次查询更新

本次按用户“最近四场再预测、尽量精准”的要求，再次核对 005-008 四场未开赛比赛：

- FIFA Scores & Fixtures / Match Centre：确认最近四场仍为 008 Qatar vs Switzerland、007 Brazil vs Morocco、005 Haiti vs Scotland、006 Australia vs Turkiye，当前均未开赛。
- Guardian 当日赛程页：交叉验证四场开球时间和观察点，强调 Brazil vs Morocco 有冷门/平局风险、Scotland 需防 Haiti 反击、Turkey 纸面更强但 Australia 不宜低估。
- FOX Sports/FanDuel、Oddschecker、Covers/Kalshi、RotoWire：补充胜平负、让球和大小球快照；用户未提供盘口截图或文本，本次仍以公开盘口为准。
- 最新情报修正：Qatar vs Switzerland 将分歧比分从 0-1 上调到 0-3；Brazil vs Morocco 将主线从 Brazil 1-0 Morocco 调整为 1-1；Haiti vs Scotland 维持 1-2；Australia vs Turkiye 维持 0-1。
