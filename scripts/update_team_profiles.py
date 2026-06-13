from __future__ import annotations

import re
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path


MATCH_SCHEDULE_URL = "https://www.fifa.com/en/articles/match-schedule-fixtures-results-teams-stadiums"
FINAL_DRAW_URL = "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/final-draw-results"
QUALIFIED_TEAMS_URL = "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/world-cup-2026-who-has-qualified"
JINA_PREFIX = "https://r.jina.ai/http://r.jina.ai/http://"


@dataclass(frozen=True)
class Team:
    key: str
    zh: str
    code: str
    confed: str
    filename: str
    positioning: str
    watch: tuple[str, str, str]
    aliases: tuple[str, ...] = ()

    @property
    def names(self) -> tuple[str, ...]:
        return (self.key, *self.aliases)


GROUPS: dict[str, tuple[str, str, str, str]] = {
    "Group A": ("Mexico", "South Africa", "South Korea", "Czechia"),
    "Group B": ("Canada", "Bosnia and Herzegovina", "Qatar", "Switzerland"),
    "Group C": ("Brazil", "Morocco", "Haiti", "Scotland"),
    "Group D": ("USA", "Paraguay", "Australia", "Türkiye"),
    "Group E": ("Germany", "Curaçao", "Côte d'Ivoire", "Ecuador"),
    "Group F": ("Netherlands", "Japan", "Sweden", "Tunisia"),
    "Group G": ("Belgium", "Egypt", "IR Iran", "New Zealand"),
    "Group H": ("Spain", "Cabo Verde", "Saudi Arabia", "Uruguay"),
    "Group I": ("France", "Senegal", "Iraq", "Norway"),
    "Group J": ("Argentina", "Algeria", "Austria", "Jordan"),
    "Group K": ("Portugal", "Congo DR", "Uzbekistan", "Colombia"),
    "Group L": ("England", "Croatia", "Ghana", "Panama"),
}


TEAMS: dict[str, Team] = {
    "Mexico": Team(
        "Mexico",
        "墨西哥",
        "MEX",
        "CONCACAF",
        "mexico.md",
        "东道主之一，小组首战已结束，主场环境和公众期待都会放大比赛波动。",
        ("主场优势与主场压力需要一起评估。", "若盘口过热，需保留小胜或冷门风险。", "中前场创造力与防线回追速度是后续判断重点。"),
    ),
    "South Africa": Team(
        "South Africa",
        "南非",
        "RSA",
        "CAF",
        "south-africa.md",
        "非洲区参赛队，首战已结束，后续更依赖防守组织和反击质量抢分。",
        ("面对强队时防线站位和二点球保护很关键。", "反击效率和定位球质量决定爆冷空间。", "若早早失球，比赛可能被拉到不利节奏。"),
    ),
    "South Korea": Team(
        "South Korea",
        "韩国",
        "KOR",
        "AFC",
        "south-korea.md",
        "亚洲强队，小组首战已结束，技术速度和转换效率是主要优势。",
        ("边路推进和前场转换速度需要重点观察。", "面对身体对抗强的队伍时，定位球防守是风险点。", "核心攻击手状态会直接影响小胜上限。"),
        ("Korea Republic",),
    ),
    "Czechia": Team(
        "Czechia",
        "捷克",
        "CZE",
        "UEFA",
        "czechia.md",
        "欧洲参赛队，身体对抗、定位球和中路推进是主要比赛抓手。",
        ("需要观察中后场对抗和定位球进攻质量。", "如果能压慢节奏，平局和小比分空间会上升。", "面对速度型对手时边路保护是关键。"),
        ("Czech Republic",),
    ),
    "Canada": Team(
        "Canada",
        "加拿大",
        "CAN",
        "CONCACAF",
        "canada.md",
        "东道主之一，主场加成明显，但首战压力和伤停信息需要临场复核。",
        ("高压和纵向推进是主要优势来源。", "边路核心可用性会影响进攻上限。", "主场热度高时，需要警惕盘口高估。"),
    ),
    "Bosnia and Herzegovina": Team(
        "Bosnia and Herzegovina",
        "波黑",
        "BIH",
        "UEFA",
        "bosnia-and-herzegovina.md",
        "欧洲参赛队，通常更适合低位防守、支点推进和定位球争取结果。",
        ("中锋支点和二点球争夺会影响反击质量。", "若能压低节奏，受让方向更有价值。", "锋线伤停和老将体能要在赛前复核。"),
        ("Bosnia",),
    ),
    "Qatar": Team(
        "Qatar",
        "卡塔尔",
        "QAT",
        "AFC",
        "qatar.md",
        "亚洲参赛队，控球组织和比赛节奏管理是争取出线的基础。",
        ("需要观察中场控球能否抵消身体对抗劣势。", "如果先丢球，阵地进攻效率会被放大检验。", "对阵欧洲和东道主球队时，防线横移是风险点。"),
    ),
    "Switzerland": Team(
        "Switzerland",
        "瑞士",
        "SUI",
        "UEFA",
        "switzerland.md",
        "欧洲稳定型球队，纪律性和比赛管理能力通常较强。",
        ("防守结构和中场硬度是主要下限。", "面对低位队伍时，破密集效率需要观察。", "盘口偏浅时，平局风险不能忽略。"),
    ),
    "Brazil": Team(
        "Brazil",
        "巴西",
        "BRA",
        "CONMEBOL",
        "brazil.md",
        "南美传统强队，个人能力和边路爆点会带来高热度。",
        ("强队热度容易抬高盘口预期。", "前场个人能力强，但防守转换仍需复核。", "若早进球，大比分上限会明显提升。"),
    ),
    "Morocco": Team(
        "Morocco",
        "摩洛哥",
        "MAR",
        "CAF",
        "morocco.md",
        "非洲强队，防守纪律和快速转换是主要竞争力。",
        ("中后场结构稳定性是小组出线关键。", "面对控球强队时反击质量决定冷门空间。", "定位球攻防和边路速度需要重点记录。"),
    ),
    "Haiti": Team(
        "Haiti",
        "海地",
        "HAI",
        "CONCACAF",
        "haiti.md",
        "中北美参赛队，小组赛可能更多处在受压和反击角色。",
        ("防线抗压和门将表现会显著影响比分。", "如果能在转换中制造第一球，冷门空间会增加。", "盘口缺失时应降低信心等级。"),
    ),
    "Scotland": Team(
        "Scotland",
        "苏格兰",
        "SCO",
        "UEFA",
        "scotland.md",
        "欧洲参赛队，身体对抗、边路传中和定位球是常见得分路径。",
        ("比赛节奏越硬，越有利于发挥对抗优势。", "面对技术型球队时，中场保护和边路回防是风险点。", "平局与小比分路径需要重点评估。"),
    ),
    "USA": Team(
        "USA",
        "美国",
        "USA",
        "CONCACAF",
        "usa.md",
        "东道主之一，主场优势明显，但热门压力和阵型稳定性需要复核。",
        ("主场环境会提高进攻主动性。", "阵型切换和防线身后空间是主要风险。", "若盘口只给浅让，需要保留平局路径。"),
        ("United States",),
    ),
    "Paraguay": Team(
        "Paraguay",
        "巴拉圭",
        "PAR",
        "CONMEBOL",
        "paraguay.md",
        "南美参赛队，防守韧性和转换冲击适合制造低比分阻击。",
        ("低位防守质量会决定受让价值。", "反击单点状态会影响爆冷概率。", "小球盘下，1-0 或 1-1 路径需要重点评估。"),
    ),
    "Australia": Team(
        "Australia",
        "澳大利亚",
        "AUS",
        "AFC",
        "australia.md",
        "亚洲参赛队，身体对抗和定位球能力是稳定拿分基础。",
        ("定位球攻防和禁区对抗是关键。", "面对技术型强队时，中场移动速度是风险。", "若领先，比赛可能转向低节奏守优势。"),
    ),
    "Türkiye": Team(
        "Türkiye",
        "土耳其",
        "TUR",
        "UEFA",
        "turkiye.md",
        "欧洲参赛队，进攻天赋和比赛情绪波动并存。",
        ("前场创造力能提高大球上限。", "防线稳定性和犯规控制需要赛前复核。", "若盘口过深，冷门和平局风险会抬升。"),
        ("Turkey",),
    ),
    "Germany": Team(
        "Germany",
        "德国",
        "GER",
        "UEFA",
        "germany.md",
        "欧洲传统强队，控球推进和压迫能力会带来强队定位。",
        ("面对低位队伍时，破密集效率是首要观察点。", "防线身后空间和转换防守不可忽略。", "强队盘口下，需要区分赢球与赢盘。"),
    ),
    "Curaçao": Team(
        "Curaçao",
        "库拉索",
        "CUW",
        "CONCACAF",
        "curacao.md",
        "中北美参赛队，小国首次级别舞台带来低预期和高情绪收益。",
        ("防守抗压和门将表现会决定比分区间。", "转换效率是制造冷门的主要路径。", "资料样本少时，预测信心应主动下调。"),
        ("Curacao", "CuraÃ§ao"),
    ),
    "Côte d'Ivoire": Team(
        "Côte d'Ivoire",
        "科特迪瓦",
        "CIV",
        "CAF",
        "cote-d-ivoire.md",
        "非洲强队，身体条件、边路速度和中前场冲击力突出。",
        ("边路推进和反抢质量是主要优势。", "面对纪律性强的队伍时，阵地战耐心需要观察。", "大球和小胜路径都需要结合盘口判断。"),
        ("Cote d'Ivoire", "Ivory Coast"),
    ),
    "Ecuador": Team(
        "Ecuador",
        "厄瓜多尔",
        "ECU",
        "CONMEBOL",
        "ecuador.md",
        "南美参赛队，身体强度和中场覆盖能力是主要竞争力。",
        ("中场抢断和纵向推进决定比赛主动权。", "面对欧洲强队时，防线纪律是核心风险。", "若盘口偏浅，平局路径需要保留。"),
    ),
    "Netherlands": Team(
        "Netherlands",
        "荷兰",
        "NED",
        "UEFA",
        "netherlands.md",
        "欧洲强队，整体推进、边翼宽度和后场出球质量较重要。",
        ("控球优势能否转化为禁区机会是重点。", "边翼卫身后空间需要防反击。", "热门场次要区分控场和大胜。"),
    ),
    "Japan": Team(
        "Japan",
        "日本",
        "JPN",
        "AFC",
        "japan.md",
        "亚洲强队，技术细腻、整体移动和转换速度具备竞争力。",
        ("高位逼抢和肋部配合是主要进攻线索。", "面对高大球队时，定位球防守是风险点。", "如果控球被限制，需要观察替补冲击力。"),
    ),
    "Sweden": Team(
        "Sweden",
        "瑞典",
        "SWE",
        "UEFA",
        "sweden.md",
        "欧洲参赛队，身体对抗、直接进攻和定位球威胁突出。",
        ("定位球进攻可显著改变小比分走势。", "面对技术流球队时，中场覆盖速度是风险。", "低节奏比赛中平局概率需要提高。"),
    ),
    "Tunisia": Team(
        "Tunisia",
        "突尼斯",
        "TUN",
        "CAF",
        "tunisia.md",
        "非洲参赛队，防守组织和比赛韧性通常较强。",
        ("压低节奏有利于制造小比分。", "进攻端效率决定能否从平局走向胜局。", "若盘口不完整，应降低大方向信心。"),
    ),
    "Belgium": Team(
        "Belgium",
        "比利时",
        "BEL",
        "UEFA",
        "belgium.md",
        "欧洲强队，个人能力和前场创造力仍是主要优势。",
        ("前场球星状态会影响进球上限。", "防线年龄结构和回追速度需要复核。", "强队热度下，赢球和穿盘要分开判断。"),
    ),
    "Egypt": Team(
        "Egypt",
        "埃及",
        "EGY",
        "CAF",
        "egypt.md",
        "非洲参赛队，前场单点能力和防守组织并重。",
        ("核心攻击点可用性是最大变量。", "防守阵型完整时，小比分抗衡能力较强。", "若先丢球，阵地进攻效率会被放大检验。"),
    ),
    "IR Iran": Team(
        "IR Iran",
        "伊朗",
        "IRN",
        "AFC",
        "iran.md",
        "亚洲参赛队，身体对抗、防守纪律和定位球是稳定基本盘。",
        ("压低节奏和定位球是抢分重点。", "面对速度型对手时，边路回防是风险。", "盘口偏小球时，需重视一球胜负路径。"),
        ("Iran",),
    ),
    "New Zealand": Team(
        "New Zealand",
        "新西兰",
        "NZL",
        "OFC",
        "new-zealand.md",
        "大洋洲参赛队，身体对抗和定位球是主要得分路径。",
        ("防守抗压时间越长，爆冷价值越高。", "定位球和长传二点球是进攻关键。", "面对强队时，盘口信心应保持谨慎。"),
    ),
    "Spain": Team(
        "Spain",
        "西班牙",
        "ESP",
        "UEFA",
        "spain.md",
        "欧洲强队，控球、压迫和肋部配合是主要优势。",
        ("控球优势能否转化为高质量射门是重点。", "面对低位密集时，早进球非常关键。", "强队热门场次需警惕小胜不穿盘。"),
    ),
    "Cabo Verde": Team(
        "Cabo Verde",
        "佛得角",
        "CPV",
        "CAF",
        "cabo-verde.md",
        "非洲参赛队，世界杯新面孔，防守韧性和反击效率决定上限。",
        ("小组首战面对强队时，防线抗压是核心。", "反击第一脚质量决定能否制造威胁。", "资料样本有限时，预测信心要下调。"),
        ("Cape Verde",),
    ),
    "Saudi Arabia": Team(
        "Saudi Arabia",
        "沙特阿拉伯",
        "KSA",
        "AFC",
        "saudi-arabia.md",
        "亚洲参赛队，比赛强度和前场速度是主要观察方向。",
        ("面对南美/欧洲强队时，中后场抗压是风险。", "转换速度能否形成有效射门是关键。", "若先失球，比赛可能变得开放。"),
    ),
    "Uruguay": Team(
        "Uruguay",
        "乌拉圭",
        "URU",
        "CONMEBOL",
        "uruguay.md",
        "南美强队，对抗、压迫和锋线终结能力具备高下限。",
        ("高强度对抗能压制多数对手节奏。", "前场终结效率决定能否打穿盘口。", "犯规控制和牌面风险需要关注。"),
    ),
    "France": Team(
        "France",
        "法国",
        "FRA",
        "UEFA",
        "france.md",
        "欧洲顶级强队，阵容深度、速度和转换质量突出。",
        ("强队轮换与首发选择会影响盘口判断。", "边路速度和禁区终结是主要优势。", "面对防守型球队时，早进球决定大胜空间。"),
    ),
    "Senegal": Team(
        "Senegal",
        "塞内加尔",
        "SEN",
        "CAF",
        "senegal.md",
        "非洲强队，身体能力、防守硬度和转换冲击兼具。",
        ("中后场对抗能决定比赛下限。", "反击效率和边路速度是爆冷来源。", "面对强队时，小比分受让路径值得关注。"),
    ),
    "Iraq": Team(
        "Iraq",
        "伊拉克",
        "IRQ",
        "AFC",
        "iraq.md",
        "亚洲参赛队，防守韧性和团队纪律是主要基础。",
        ("防守阵型完整性是第一观察点。", "反击和定位球决定进球来源。", "若盘口资料缺失，应降低预测信心。"),
    ),
    "Norway": Team(
        "Norway",
        "挪威",
        "NOR",
        "UEFA",
        "norway.md",
        "欧洲参赛队，前场终结能力和身体条件具备高上限。",
        ("核心前锋状态会直接改变进球预期。", "阵地推进质量决定能否支撑热门定位。", "防守转换和中场保护仍需赛前复核。"),
    ),
    "Argentina": Team(
        "Argentina",
        "阿根廷",
        "ARG",
        "CONMEBOL",
        "argentina.md",
        "卫冕冠军和南美强队，控场能力、经验和关键球处理是主要优势。",
        ("强队热度高，需要区分赢球与大胜。", "老将体能和轮换策略要赛前复核。", "若先入球，比赛管理能力会显著提高胜率。"),
    ),
    "Algeria": Team(
        "Algeria",
        "阿尔及利亚",
        "ALG",
        "CAF",
        "algeria.md",
        "非洲参赛队，前场单点和中场对抗能力是主要线索。",
        ("核心边锋或攻击手状态影响进攻上限。", "防线集中度会决定能否抗衡强队。", "若盘口给到深受让，小比分路径需要关注。"),
    ),
    "Austria": Team(
        "Austria",
        "奥地利",
        "AUT",
        "UEFA",
        "austria.md",
        "欧洲参赛队，高强度压迫和整体纪律是主要竞争力。",
        ("压迫质量能决定比赛主动权。", "若前场逼抢失效，防线身后空间会被放大。", "小组中面对非欧洲对手时节奏适应很关键。"),
    ),
    "Jordan": Team(
        "Jordan",
        "约旦",
        "JOR",
        "AFC",
        "jordan.md",
        "亚洲参赛队，世界杯新面孔，防守反击和纪律性是主要基础。",
        ("防守抗压时间和门将发挥很关键。", "反击第一脚和定位球是主要进球路径。", "资料样本少时，必须降低信心等级。"),
    ),
    "Portugal": Team(
        "Portugal",
        "葡萄牙",
        "POR",
        "UEFA",
        "portugal.md",
        "欧洲强队，阵容深度和前场创造力会带来高热度。",
        ("轮换选择会影响小组赛盘口强度。", "面对低位队伍时，边路和肋部破密集是重点。", "强队热门场次需警惕只小胜。"),
    ),
    "Congo DR": Team(
        "Congo DR",
        "刚果民主共和国",
        "COD",
        "CAF",
        "congo-dr.md",
        "非洲参赛队，身体条件和反击冲击是主要竞争力。",
        ("防守组织能否承受强队压迫是核心。", "转换推进和定位球会决定冷门概率。", "面对控球强队时，犯规和牌面风险需关注。"),
        ("DR Congo", "Democratic Republic of the Congo", "Congo"),
    ),
    "Uzbekistan": Team(
        "Uzbekistan",
        "乌兹别克斯坦",
        "UZB",
        "AFC",
        "uzbekistan.md",
        "亚洲参赛队，世界杯新面孔，整体纪律和中场硬度是主要看点。",
        ("小组首秀心态和抗压能力是最大变量。", "中场对抗质量会影响反击效率。", "资料样本有限时，盘口信心要保守。"),
    ),
    "Colombia": Team(
        "Colombia",
        "哥伦比亚",
        "COL",
        "CONMEBOL",
        "colombia.md",
        "南美强队，身体对抗、前场创造力和比赛韧性兼具。",
        ("中前场创造力决定能否打穿低位。", "防守转换和情绪控制是风险点。", "面对新军时，强弱差和盘口热度要分开评估。"),
    ),
    "England": Team(
        "England",
        "英格兰",
        "ENG",
        "UEFA",
        "england.md",
        "欧洲强队，阵容深度和定位球质量通常带来高下限。",
        ("强队热门下，穿盘比赢球更难判断。", "中前场组合和首发平衡需要赛前复核。", "面对克罗地亚等经验队，小比分风险要保留。"),
    ),
    "Croatia": Team(
        "Croatia",
        "克罗地亚",
        "CRO",
        "UEFA",
        "croatia.md",
        "欧洲经验型强队，中场控制和淘汰赛经验是主要资产。",
        ("中场控节奏能力会影响小比分走势。", "老将体能和轮换策略要赛前复核。", "面对强队时，平局和加时型思路需保留。"),
    ),
    "Ghana": Team(
        "Ghana",
        "加纳",
        "GHA",
        "CAF",
        "ghana.md",
        "非洲参赛队，身体对抗、速度和转换冲击是主要优势。",
        ("边路速度和反击终结是进攻关键。", "防守纪律决定能否把比赛留在小比分。", "若先入球，受让和冷门价值会提升。"),
    ),
    "Panama": Team(
        "Panama",
        "巴拿马",
        "PAN",
        "CONCACAF",
        "panama.md",
        "中北美参赛队，防守纪律和身体对抗是小组抢分基础。",
        ("防线抗压能力会决定比分上限。", "定位球和反击是主要进球来源。", "面对欧洲强队时，盘口信心要保守。"),
    ),
}


def fetch_markdown(url: str) -> str:
    req = urllib.request.Request(
        JINA_PREFIX + url,
        headers={"User-Agent": "SoccerMatchBetting-team-profile-updater/1.0"},
    )
    with urllib.request.urlopen(req, timeout=45) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_schedule(markdown: str) -> list[dict[str, str]]:
    date_re = re.compile(r"#### \*\*(?P<date>[A-Za-z]+, \d+ [A-Za-z]+ 2026)\*\*")
    match_re = re.compile(
        r"\[(?P<match>[^\]]+)\]\(https://www\.fifa\.com/en/match-centre/match/[^\)]+\)"
        r"\s*[–-]\s*\*\*(?P<group>Group [A-L])\*\*\s*[–-]\s*_(?P<stadium>[^_]+)_"
    )
    date_matches = list(date_re.finditer(markdown))
    rows: list[dict[str, str]] = []
    for idx, date_match in enumerate(date_matches):
        start = date_match.end()
        end = date_matches[idx + 1].start() if idx + 1 < len(date_matches) else len(markdown)
        section = markdown[start:end]
        date_en = date_match.group("date")
        date_obj = datetime.strptime(date_en, "%A, %d %B %Y")
        for match in match_re.finditer(section):
            rows.append(
                {
                    "date": date_obj.strftime("%Y-%m-%d"),
                    "date_en": date_en,
                    "group": match.group("group"),
                    "match": match.group("match").strip(),
                    "stadium": match.group("stadium").strip(),
                }
            )
    return rows


def teams_in_match(row: dict[str, str]) -> tuple[str, str]:
    group_teams = GROUPS[row["group"]]
    raw = row["match"]
    found: list[str] = []
    for team_key in group_teams:
        meta = TEAMS[team_key]
        if any(name in raw for name in meta.names):
            found.append(team_key)
    if len(found) != 2:
        raise ValueError(f"Could not identify two teams for fixture: {row}")
    return found[0], found[1]


def status_for(match_text: str) -> str:
    return "已结束" if re.search(r"\d+\s*[-–]\s*\d+", match_text) else "未开赛"


def build_team_fixtures(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    fixtures: dict[str, list[dict[str, str]]] = {team: [] for team in TEAMS}
    for order, row in enumerate(rows):
        team_a, team_b = teams_in_match(row)
        enriched = {**row, "order": str(order), "status": status_for(row["match"])}
        fixtures[team_a].append(enriched)
        fixtures[team_b].append(enriched)
    missing = [team for team, team_rows in fixtures.items() if len(team_rows) != 3]
    if missing:
        raise ValueError(f"Teams without exactly three group fixtures: {missing}")
    return fixtures


def group_for(team_key: str) -> str:
    for group, teams in GROUPS.items():
        if team_key in teams:
            return group
    raise KeyError(team_key)


def write_team_file(team: Team, fixtures: list[dict[str, str]], timestamp: str) -> str:
    group = group_for(team.key)
    opponents = [TEAMS[name].zh for name in GROUPS[group] if name != team.key]
    first = sorted(fixtures, key=lambda row: (row["date"], int(row["order"])))[0]
    fixture_rows = "\n".join(
        f"| {row['date']} | {row['match']} | {row['stadium']} | {row['status']} |"
        for row in sorted(fixtures, key=lambda item: (item["date"], int(item["order"])))
    )
    watch_rows = "\n".join(f"- {item}" for item in team.watch)
    content = f"""# {team.zh}国家队

team_en: {team.key}
team_code: {team.code}
confederation: {team.confed}
last_updated: {timestamp}

## 基础记录

- 所属小组：{group}
- 小组对手：{'、'.join(opponents)}
- 首场比赛：{first['match']}（FIFA 官方日期 {first['date']}，{first['stadium']}，{first['status']}）
- 队伍定位：{team.positioning}

## 小组赛程

| FIFA 官方日期 | 比赛 | 场地 | 状态 |
| --- | --- | --- | --- |
{fixture_rows}

## 当前资料状态

- 已更新：参赛队归属、小组对手、三场小组赛、首战状态。
- 尚需单场赛前更新：最终大名单、预计首发、伤停/停赛、赛前发布会、盘口快照。
- 盘口说明：本文件不维护盘口；胜平负、亚洲让球、大小球只在具体比赛文件中记录。

## 预测观察点

{watch_rows}

## 资料来源

- FIFA 官方赛程文章：{MATCH_SCHEDULE_URL}
- FIFA 最终抽签结果：{FINAL_DRAW_URL}
- FIFA 已晋级球队页面：{QUALIFIED_TEAMS_URL}
- 查询时间：{timestamp}
"""
    path = Path("tournaments/2026-world-cup/teams") / team.filename
    path.write_text(content, encoding="utf-8", newline="\n")
    return str(path)


def write_index(timestamp: str) -> str:
    lines = [
        "# 2026 世界杯参赛队伍索引",
        "",
        f"last_updated: {timestamp}",
        "",
        "## 说明",
        "",
        "- 本目录按 2026 FIFA World Cup 48 支参赛队维护静态队伍档案。",
        "- 单场盘口、赛前情报和复盘仍以 `matches/`、`daily/`、`reviews/` 下的比赛文件为准。",
        "- 本次索引使用 FIFA 官方赛程与抽签页面核对小组和小组赛程。",
        "",
        "## 小组索引",
        "",
        "| 小组 | 队伍 |",
        "| --- | --- |",
    ]
    for group, team_keys in GROUPS.items():
        links = []
        for team_key in team_keys:
            team = TEAMS[team_key]
            links.append(f"[{team.zh}]({team.filename})")
        lines.append(f"| {group} | {'、'.join(links)} |")
    lines.extend(
        [
            "",
            "## 资料来源",
            "",
            f"- FIFA 官方赛程文章：{MATCH_SCHEDULE_URL}",
            f"- FIFA 最终抽签结果：{FINAL_DRAW_URL}",
            f"- FIFA 已晋级球队页面：{QUALIFIED_TEAMS_URL}",
            f"- 查询时间：{timestamp}",
            "",
        ]
    )
    path = Path("tournaments/2026-world-cup/teams/index.md")
    path.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    return str(path)


def main() -> None:
    timestamp = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
    schedule = fetch_markdown(MATCH_SCHEDULE_URL)
    rows = parse_schedule(schedule)
    if len(rows) != 72:
        raise ValueError(f"Expected 72 group-stage fixtures, parsed {len(rows)}")
    fixtures = build_team_fixtures(rows)
    Path("tournaments/2026-world-cup/teams").mkdir(parents=True, exist_ok=True)
    written = [write_team_file(team, fixtures[team_key], timestamp) for team_key, team in TEAMS.items()]
    written.append(write_index(timestamp))
    print(f"Updated {len(written)} team files/index records")
    for item in written:
        print(item)


if __name__ == "__main__":
    main()
