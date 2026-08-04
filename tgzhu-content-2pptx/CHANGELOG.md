# CHANGELOG — tgzhu-content-2pptx

> 本文件只记"**何时、为何**演进"（决策历史）；"**现行规则/约束是什么**"见 `SKILL.md`。
> 格式：按日期倒序；每条 = 类型（新增/修改/修复/重构/验证）· 变更 · 影响章节或函数。
> 起始日期 2026-07-31（更早的迭代历史不再追溯）。
> 维护节奏：**每天收尾时统一总结当天一次**，不必每次改动都记（省时；当天多次改动合并成一条或按类型归并）。

## 2026-08-04

### 修改（双栏页三处收敛：暗边框 + 段落自动均分 + 标题对齐 h1，2026-08-04 收尾）
- **双栏卡边框改近背景暗色（仅企业风·皮肤键驱动）**：原 `layout_two_column` 的 `content_card` 边框直接取 `cd['line']`（企业=`#D2D8DC` 浅灰，深蓝底上偏亮抢戏）→ 改为 `cd.get('two_col_border', cd['line'])`（`two_col_border` 缺省回落原 `line`）。`ENTERPRISE_SKIN['card']` 新增 `two_col_border=RGBColor(0x22,0x40,0x5F)`（中性暗蓝，比背景亮一档、存在不刺眼，契合"颜色退、线宽进"）。锋芒/文质/商务未设此键 → 自动回落各自 `cd['line']`，互不受影响（局部改动不越界）。→ `common.py::layout_two_column` / `enterprise.py::ENTERPRISE_SKIN`
- **双栏框内段落高度自动计算（等框高 + 内容区均匀铺满）**：原右栏 4 行用"固定行距 + 垂直居中"，只聚卡中间、上下留大空当；改为在 `(area_top, area_bot)` 内按段数 `n_items` 均匀切分 `seg=(area_bot-area_top)/n_items`、各行中心落在 `area_top+(j+0.5)*seg`，左 7 行/右 4 行各自等距、同区铺满等高卡（ChatGPT 双栏"定框高后分段自适应"思路落地，消除右栏空荡）。→ `common.py::layout_two_column`
- **双栏页主标题 28pt 对齐 h1（消除跨页跳变）**：原 `enterprise._action_title` 写死 `Pt(20)`，而 `section_header` 的 H1 用 `TYPOGRAPHY['h1']=(28,True)`，混排时同级别标题 20↔28 跳变；改为 `Pt(28)` 与全 deck 主标题一致。→ `enterprise.py::_action_title`
- **双栏卡宽 80% 页宽保底（自动计算为主·不写死）**：原下限 `cw2=max(cw2, 0.70*col_avail)`（70% 列可用宽）在短内容演示下塌成双卡占页宽 62.3% 窄卡；改为「双卡整体 ≥ 页宽 80%」对应单列下限 `pair_min=0.80*PAGE_W; cw2=max(cw2,(pair_min-gap)/2.0)`——内容长仍自动撑到列宽(双卡 88%)，短内容兜底 80%，左右上下始终按 80% 布局。全局改 `layout_two_column`（版式行为·四风格双栏页同受益），契合"卡宽卡高测最大值统一"铁律。→ `common.py::layout_two_column`
- **验证**：重生成 `交付物与职责分工_二栏_引擎版.pptx`（走真实引擎 `new_deck` 克隆模板 + `add_content` 品牌版式 `layout[6]` + `two_column` 传 `left_note/right_note` + `bottom_gold`）；反向读 XML 确认双卡边框 `#22405F`/`1.25pt`、主标题 28pt、左 7 行行距 0.323″ 与右 4 行 0.565″ 各自均匀铺满、不超页；`validate_deck` PASS(0)。
- **遗留（未改·待授权）**：`layout_two_column` 文本框宽 `cw2-2*pad` 与卡内宽 `max_inner+2*pad` 抵消 → 文字宽=框宽零余量，长条目临界换行（演示右栏日期已精简规避）。属第三处改动，超出本次"只改两处"授权，待用户确认后再补文本框缓冲（如 `cw2` 多放 0.1″）。

### 新增（三列专用骨架 layout_three_column + 企业风 three_column 包装，2026-08-04 下午）
- **背景**：P11（附则·施行）原为 `card_grid(cols=2)` 渲染成 2+1，与"三列并排"目标不符；用户要求把三列单独抽一个骨架，参考 ChatGPT 双栏三原则（等框高/自动分段/暗色框线）。
- **新增 `common.py::layout_three_column`**：单排三卡、等宽、等框高，独立于 `layout_card_grid` 的 2×N 网格。几何调整（专家）：卡宽锁定 **页宽 92%**（12.27″，gap 0.35″，单卡 ≈3.86″）——三列比二列更窄，若沿用 80% 单卡内文宽仅 ~2.84″ 必折行，92% 时 ~3.38″ 可读性更好且留 4% 边距；其余原则与双栏/2×2 同源（等框高取本页最大、内容卡内分段、暗边框 `two_col_border`=#22405F、分隔线锚定卡底同行对齐）。
- **三列增强项（已撤销·与 2×2 统一）**：① 标题下青色短下划线；② 结论 `icon`；③ 列间连接线——上述三处为三列专属装饰，2×2(card_grid) 均无。用户要求"保持和 2×2 一样、整洁统一"，故全部去除：`layout_three_column` 删标题下划线块与 icon（结论=纯 `c['hl']`），`connect` 默认 `True`→`False`（列间连接线默认关闭）；`enterprise.three_column` 同步 `connect=False` 并改 docstring 标注"与 2×2 一致（无下划线/无 icon/无连接线）"；P11 runner 删三卡 `icon` 字段。
- **新增 `enterprise.py::three_column` 薄壳**：标题区委托 `section_header`（28pt H1 + 18pt label，与全站一致），再调 `layout_three_column`，并在 `from common import` 增加 `layout_three_column`。
- **调用**：P11 runner 由 `card_grid(cols=2,…)` 改为 `three_column(title,label,cards=[{tag,title,lines,hl}×3], n,total)`（无 icon）；`card_grid` 仍负责 2×2/2×3。
- **验证**：重生成 `互联网平台价格行为规则_企业风_12页_v4.pptx`；反向读 XML 确认 P11 = 三卡 x=0.53/4.74/8.94、宽 3.855″、等距 4.206″、边框 #22405F、**仅剩 3 条卡内底部暗分隔线(#44586C，与 2×2 同源)**、无列间连接线/无标题下划线/无 icon、溢出 0；`validate_deck` PASS(0)。

### 修复（框内「标题↔正文」间距层级倒挂，2026-08-04 晚）
- **问题**：实测 `_v4.pptx` 框内 标题→正文（P11=0.00″ / P10=0.08″）**小于** 段落↔段落（0.22″），违反 `SKILL §4.12-7` 层级「标题↔正文 > 段间 > 行距」。根因：①三列回归——第四轮删标题下划线时把 `yy = gt + BAND_GAP + UNDER_GAP` 误改为 `yy = gt`，标题→正文间距整段丢失；②两骨架 `BAND_GAP`（三列 0.10 / 2×2 0.08）本就 < `BULLET_GAP`(0.22)，原本逆层级；③三列 `card_h` 多算一个 `+ BAND_GAP`（`group_h` 已含首行 `BAND_GAP`），卡高虚高 0.10″。
- **修复（全在 `common.py`，runner 不动，三列与 2×2 统一）**：
  - 三列 `yy = gt` → `yy = gt + BAND_GAP`（恢复标题间距，修回归）。
  - 三列 `card_h` 删多余 `+ BAND_GAP`，与 `card_grid` 公式对齐（`title_band + group_h + 2*VPAD`）。
  - 两骨架 `BAND_GAP` 0.10/0.08 → **0.28**（> `BULLET_GAP` 0.22，立「标题↔正文 > 段间」层级；行距≈0.208 仍最小）。`BULLET_GAP=0.22`、`BODY_LS=1.25` 不动。
- **关于 SKILL「间距区间 0.10~0.16」**：该软指引被更硬的「层级」规则覆盖，且 skill 自身 `BULLET_GAP=0.22` 已超该区间；12pt×1.25 行距≈0.208 使「段间≥0.22、标题↔正文>0.22」无法塞回 0.10~0.16（否则需压垮行距，不可读），故以层级为硬约束、取值 0.28。
- **验证**：重生成 `互联网平台价格行为规则_企业风_12页_v5.pptx`；反向读 XML 确认 P11 标题→正文=0.279″、P10=0.28″，均 > 段落↔段落=0.221/0.22″（层级 True）、溢出 0、`validate_deck` PASS(0)、12 页。
- **约束（重要·同晚发现）**：`BAND_GAP=0.28` 下，**双行 2×2 每卡正文建议 ≤2 条**——3 条卡自然高=2.465″ 会超过双行 `fit_cap`=2.265″（y0=1.6,y_end=6.45,gap=0.32），`ch` 被砍高后正文(顶锚定)与分隔线/结论(卡底锚定)碰撞 → 正文压线重叠 0.12″（实测 P3/P4/P5/P8/P12 共14张3条卡全中招）。**单行/2卡布局（如 P10 行业自律·轻微违法，rows=1，卡高无封顶）不受限，可放3条**。几何上双行2×2 的3条卡物理卡高容不下 `BAND_GAP>0.08`（标题0.41+正文1.07+分隔0.24+结论0.27+内边距0.20=2.185 为下限，加 BAND_GAP 即破上限）。→ 修复方式：把超量页的3条卡合并为2条（忠实合并相关要点），引擎未动；产 `…_v6.pptx`，7个 card_grid 页重叠卡数=0。

### 重构（三列原语 three_column 四风格对齐 + section_header 副标保护，2026-08-04 收尾）
- **问题**：`layout_three_column`（单排三卡骨架）虽在 `common.py` 共享，但只有 **enterprise** 引擎暴露了 `three_column` wrapper；锋芒/文质/商务三引擎既未导入 `layout_three_column`，也无该原语 → 三列页只能企业风用，与"四风格一致"目标不符。另：business/fengmang 的 `section_header` 内部 `r.text = "  " + sub` **未做 None 保护**（wenzhi 已有 `if sub:`、enterprise `sub` 有默认值），three_column 省略副标（传 `sub=None`）会 `TypeError`。
- **修复（引擎层·薄壳，不改骨架几何）**：
  - 锋芒/文质/商务三引擎 `from common import` 增加 `layout_three_column`；各自新增 `three_column(slide, title=None, label=None, cards=None, n=None, total=None, connect=False)` 薄壳，镜像 enterprise：标题区复用本引擎 `section_header`（传 `sub=None` 跳过副标）、再调 `layout_three_column(slide, <本引擎>_SKIN, cards, y0=1.65, y_end=6.45, connect=connect)`；背景与 `card_grid` 同处理（锋芒 `set_bg(BG)` / 文质 `WEN_BG`+`_accent_box` / 商务依赖调用方 `set_bg(WHITE)`）。
  - business/fengmang `section_header` 给 `r.text = "  " + sub`（business）/ `"    " + sub`（fengmang）加 `if sub:` 保护，与 wenzhi/enterprise 一致 → 四风格 `section_header(sub=None)` 均安全。
  - 三列主题色自动对齐：边框/分隔线取各皮肤 `cd.get('two_col_border'/'div_line', cd['line'])` 回落值，序号/结论色取 `num_color`/`concl_color`，无硬编码。
- **SKILL.md 同步**：「已骨架化」清单 12→13（补 `layout_three_column`）；原语表加「单排三列」行（`three_column` / — / `layout_three_column`）；组件型调用约定补 `three_column`（标注四风格均已支持、内部自带 section_header）。
- **验证**：三风格各生成单页三列（3 张 `{tag,title,lines,hl}` 卡），反向读 XML 确认 3 卡 x=0.53/4.74/8.94、宽 3.855″、等宽等距、分隔线锚卡底，与企业风 P11 几何完全一致；导入无异常、文件保存成功。

### 修复（文质风 three_column 重复绘制 _accent_box + Genie Ontology 文质风真本，2026-08-04 收尾）
- **问题（反向读 XML 发现）**：文质风 `three_column` wrapper 顶部无条件 `_accent_box(slide)`，而 `title` 给定时又调 `section_header`（其内也画 `_accent_box`）→ 三列页右上角品牌竖条被画**两次**（双栏页因调用方 `dedupe_accent` 正常，唯三列页漏）。business/fengmang 的 `three_column` 顶部无 `_accent_box`（仅 `set_bg`/依赖调用方），故无此问题。
- **修复**：`wenzhi.three_column` 把 `_accent_box(slide)` 从顶部无条件调用移入 `else`（无 title）分支；`title` 给定时由 `section_header` 统一负责背景+品牌条。几何/视觉零变化，仅消除重复形状。→ `engines/wenzhi.py`
- **真本验证（文质风 10 页）**：用公众号《当语义层不再靠人来建：Databricks Genie Ontology 的第三条路》（小鱼不卡壳 2026-06-24）生成文质风 10 页（`gen_genie_ontology_wenzhi.py` / 产物 `Databricks Genie Ontology 文质风 10页.pptx`）。反向 XML 核查：12 页？实为 10 页；0 溢出；P1/P10 含二维码、页码 1/10…10/10 齐全；**P3/P9 three_column 各 3 张等宽卡@3.855″、accent 仅 1 个（确认重复已消除）**；P2–P8 two_column 各 2 张等宽卡；P9 页级金句@6.65″ 在三列卡(止 6.45″)下方无重叠；`validate_deck` PASS(0)。→ 证明第七轮补的 `three_column` 在文质风真实闭环。
- **沉淀**：runner 存档 `references/runner-example-wenzhi.py`（首个文质风 (prs,...) 整本范式样例，含 cover/two_column/three_column/hero_questions 用法），`py_compile` 通过。README 参考索引可补该样例。

### 修复（P10 重叠 + 封面二维码/署名参数化，2026-08-04 续）
- **P10 重叠（用户报告）**：`hero_questions` 把二维码画在 y=4.62，而本文 `questions` 文案约 70 字 → 渲染成 4 行 36pt 大字(y=2.28→4.88)压住二维码起点。引擎设计假设 questions 是 1–2 行短句。→ 弃用 `hero_questions`，P10 改 `section_header` + 手写居中收尾块（34pt 大字 2 行论点 + 强调短线 + 15pt 金句「压舱石」），无二维码、无重叠。产物 `_v2`。
- **封面硬编码「天戈朱」硬伤（同源）**：`cover()`→`cover_qr`、及 `cover_story`/`hero_questions` 均硬编码「天戈朱」公众号二维码(skill 资产 `assets/qrcode.jpg`)+署名，对其它作者文章是事实错误。→ **引擎参数化（向后兼容，默认仍天戈朱）**：
  - `cover_qr(style, label="天戈朱", qr_path=None)`：`qr_path=False` 整段跳过（不画码不写扫码署名）；否则透传 `qr_path` 给 `add_qr`（None=默认资产）。
  - `cover(..., qr_label="天戈朱", qr_path=None, author=None)`：调 `cover_qr(label=qr_path...)`；`author` 给则在标签下行显作者署名。
  - `cover_story(...)` 改为委托 `cover`（去掉自身硬编码的 add_qr+天戈朱署名）。
  - `hero_questions(...)` 增加 `qr_label="天戈朱"`，署名用 `f"扫码关注「{qr_label}」"`。
  - `validate_deck` 封面二维码检查放宽：无码但封面含「公众号/作者/来源」署名文本时降级为告警（不 fail）；label 分类词检查跳过封面(i==1)。
- **本 deck 应用**：P1 `cover(..., tags=["语义层","Databricks","Agent 时代"], author="小鱼不卡壳 · 公众号文章", qr_path=False)` → 封面显示正确作者、无天戈朱码。`validate_deck` PASS（仅 1 条已豁免告警）。产物 `_v3`（旧文件被 PowerPoint 锁占，递增命名）。
- **沉淀**：`references/runner-example-wenzhi.py` 覆盖为含 `qr_path=False` 封面参数化示例的最新版，`py_compile` 通过。

## 2026-08-01

### 修复（金句统一 + 卡框高重构 + 企业副标题换行，2026-08-01 收尾）
- **金句字号统一 16pt（四风格）**：企业风 `_render_gold`(gold 角色 20pt)、文质 18pt 改为统一 16pt（锋芒/商务本就 16）；企业风 `bottom_gold` 改委托公共 `_gold`(size=16+品牌橙)，与另三风同机制。→ `enterprise.py` / `wenzhi.py` / `common.py::bottom_gold`
- **卡内结论 hl 锁死 14pt、删 auto-fit 13**：原"长文缩到 13pt 保 1 行"造成 13/14 隐形不一致，违背用户"统一"诉求 → 删 `concl_fit`，固定 14pt。→ `common.py::layout_card_grid`
- **卡框高改内容自适应 + 整组居中（消死白/协调）**：原 `ch=(avail-gap)/rows` 固定高、内容带居中留大片死白，卡内上下间距与框间距失调 → 改 `ch=band_h(c)+2*VPAD`(VPAD≈0.16)，整组 2×N 在 `[y0,y_end]` 垂直居中、框间距 0.32 与内部同频。→ `common.py::layout_card_grid`
- **序号框收窄 0.78→0.52(NUM_W)、间距 0.16→0.12(NUM_TITLE_GAP)**：原过宽推远标题+挤窄标题 → 标题可用宽 +0.30″。→ `common.py::layout_card_grid`
- **企业风 P3 页副标题换行修复**：`section_header` 把 `sub` 追加到 label 同行，但 `fit_single_line` 只按 label("核心能力")定框≈1.2″，sub 被塞进窄框软换行 → 改按 `label+sub` 合并宽度定框(≈3.98″)，单行。→ `enterprise.py::section_header`
- **「金句不允许换行」硬规则（代码层）**：新增 `common._guard_one_line()`，生成期对页底 `bottom_gold` 与卡内 `hl` 实测行数，>1 行直接抛错（强制作者精简文案，不靠压字号）；配套精简 GOLD_TL/GOLD_CARDS/卡03 hl 到 1 行。→ `common.py` / `gen_styles_P1_P3.py`
- **SKILL.md 同步**：§4.3.3 五区(数字 22pt/标题 14pt/结论 14pt 锁死)、卡框高内容自适应；§金句区新增"金句禁换行硬红线"与"四风格页底金句统一 16pt 只保留颜色 DNA"。→ `SKILL.md`
- **验证**：重生成 `四风格_P1P3对比_v3.pptx`(12 页)；`_verify_p3v3.py` ALL_OK、OVERFLOW 0；`_geom_p3.py` 四风格卡框高统一 1.86″、行间距 0.31~0.32″、整组居中(首卡顶距y0≈0.37″、行2卡底距金句线0.46~0.54″)、行2卡底≤6.01<6.50；`_check_final.py` FINAL_OK：企业副标题单行(框宽3.98″)、四风格页底金句 16pt 单行。

### 修复（金句分隔线退背景 + 内容卡淡边+真阴影，2026-08-01 收尾·续）
- **金句分隔线（金句上方细线）改极淡贴背景**：原企业/商务用高饱和强调色(橙 `#F79646`/金 `#C9A227`)画分隔线，与下方金句(结论)抢戏，违背"分隔线退背景层"原则；锋芒原用暗青 `#1A4A55`(已较退)、文质 `#E8E2D4`(已对)。统一改为极淡贴背景：`#EDEDED`(企业/商务浅底)、`#ECE7DF`(文质奶油底)、`#141414`(锋芒近黑底，比背景略亮一档)；锋芒 P2 时间轴金句独立传 `line_color=BORDER_DIM` 的遗漏一并修正。→ 四引擎 `bottom_gold` / `timeline` 金句线
- **内容卡边框改极淡 + 真柔和阴影（floating card）**：原边框用亮青(`BIZ_ACCENT`/`BIZ_TEAL`/`BORDER_DIM`)过亮 → 改为极淡贴背景痕（比金句线稍可见，让容器读得出边）：企业/商务 `#D2D8DC`/`#D9D9D9`、文质 `#DED8C8`、锋芒 `#1C1C1C`；新增 `common.add_soft_shadow()`(标准 `<a:outerShdw>`：blur 90000/dist 20000/α 35000/向下) 在 `content_card`/`rounded_card` 自动叠加。阴影判定按"背景是否暗底"(`_soft_shadow_if_light`)：浅底三风格加阴影，锋芒近黑底**不加阴影**、靠 `#111` 卡底与 `#0A0A0A` 背景的填充差自然抬升。→ `common.py` / 四引擎 skin `line`·`pos_border` + 企业显式卡片绘制 + 文质 `_shadow_card`/`wcard`
- **企业金额徽章边框改暗青专色**：原 `badge.line=BIZ_TEAL` 亮青 → `TL_CARD_BORDER #1A5560`(已有"接背景不刺眼"专色)；时间轴节点圆点(实心青、无边框)属图表节点，按"轴线/节点可用品牌色"原则保留。→ `enterprise.py::timeline`
- **关键坑确认**：商务 `full_cleanup` 只剥 **theme** 里的 `outerShdw`，不碰 slide 级形状 → 卡片阴影安全保留（实测 XML 含 `<a:outerShdw>`，PowerPoint 可正常打开，无修复提示）；文质 `_shadow_card` 原名"阴影"实为淡边+填充假阴影，已升级真阴影。→ `business.py::full_cleanup` / `wenzhi.py::_shadow_card`
- **SKILL.md 同步**：§金句区补"金句分隔线退背景层(极淡贴背景色，四风格一致)"；§4 视觉层级补"分隔线/卡片边框极淡贴背景、浅底叠 outerShdw、近黑底靠填充差抬升"；锋芒"品牌青亮边框"→"极淡贴背景边框+近黑底不加阴影"；商务"顶边金色细线"→"顶边极淡细线"。→ `SKILL.md`
- **验证**：重生成 `四风格_P1P3对比_v3.pptx`(12 页)；反向读 XML 确认——四风格金句线=EDEDED/ECE7DF/141414、P3 内容卡边框=D2D8DC/DED8C8/D9D9D9/1C1C1C 且浅底含 `outerShdw`/锋芒无阴影、企业金额徽章=1A5560、OVERFLOW 0；`outerShdw` XML 结构合法(blurRad/dist/dir/alpha 齐全)。

### 修改（设计经验分层沉淀到 skill · 四风格通用，2026-08-01 收尾）
- **背景**：商务风/文质风 P3 经 ChatGPT 评审 + 专家取舍后，收敛出一套"如何布局才克制好看"的通用原则；本次把经验**分层固化进 skill**，确保四风格通用（不只是这两套）。
- **代码层强制（阴影克制）**：`content_card`/`add_soft_shadow`/`_soft_shadow_if_light` 阴影默认 **35000(35%)→8000(8%)**（旧重投影默认已弃用）；个别风格可再调淡（文质 6000）。`validate_deck` 新增 **#6 阴影检查**：扫描 `a:outerShdw` 透明度，>12% 报 WARN（非阻断，避免误伤既有 deck）。→ `common.py`
- **文档层（references/design-principles.md 新增 §9–§13）**：
  - §9 视觉铁律：单强调色收敛（金只点编号+页底结论、卡结论用主色深蓝灰）、层级靠颜色拉不靠字号（卡标题不加大红线）、阴影≤8%、留白节奏。
  - §10 色彩 DNA：三级体系（主70/辅20/强调10）+ **四风格对照表**（企业/锋芒暗底单色青、文质/商务浅底双色青+金/暖金）。
  - §11 组件克制：卡片四级色彩分工、页眉节奏（标题→下划线~0.07″→副标留~0.17″空气、线对齐标题左缘）、底部结论（保留金句+分隔线、**否决独立结论带**）、字体分工（宋体标题/黑体信息）。
  - §12 反模式清单（6 条勿再犯）、§13 验证闭环（**`p:sp` 命名空间坑** + **文件锁坑**：PowerPoint 预览打开时 save 报 PermissionError→改输出文件名 v2/v3）。
- **SKILL.md 同步**：§4.4 末尾加指针，指向 design-principles.md §9–§13（新增风格/原语须先读、不得违反）。→ `SKILL.md`
- **验证**：重生成 `FDE商务风_P3_微调v3.pptx` / `FDE文质风_P3_微调v3.pptx`，`validate_deck` 均 ok=True、无报告（默认变更未影响既有输出：商务/文质显式覆盖 8%/6%）。

### 修复（严格按 skill 生成企业/锋芒 → 抓出 skill 自相矛盾 + 两风格视觉 bug，2026-08-01 下午）
- **背景**：用户要求"忘掉记忆、严格按 skill 代码"重生成企业/锋芒 P3 → 验证闭环抓出 skill 真实漏洞。
- **skill 自相矛盾（代码 vs 文档铁律）**：`common.layout_card_grid` 调 `content_card` 时 `shadow_alpha=cd.get('shadow_alpha', 35000)`——**回退默认仍是 35%**，与 design-principles §11"阴影≤8%"直接冲突（商务/文质皮肤显式配 8000/6000 才正常，企业/锋芒皮肤漏配→回退 35%）。一行修复：默认 35000→8000。→ `common.py`
- **锋芒卡框不可见**：`FENG_CARD_LINE` 三阶调亮 `#1C1C1C`→`#2A2A2A`→**`#444444`**（黑底 #0A0A0A 上亮度差 ~60%，可见不抢戏）。→ `fengmang.py`
- **企业内容页背景全白（根因=python-pptx save 时注入 noFill）**：`add_content()` 用 layout[6] 带白底 → 改 `layout[8]`（仅标题，主体继承母版渐变）；但 save() 序列化时仍对内容页注入 `<bg><bgPr><noFill/></bgPr></bg>` 覆盖母版（内存中创建时不存在，**save 才写**）→ 新增 `enterprise.clean_no_fill_bg(pptx_path, skip_slides)` 文件后处理（zip 重读写回，删含 noFill 的 cSld:bg），生成器 save 后必调。→ `enterprise.py` / `gen_enterprise_p3.py`
- **验证**：`FDE企业风_P3_skill_v3.pptx` / `FDE锋芒风_P3_skill_v3.pptx` validate ok=True；XML 确认企业 slide2 无 `<cSld:bg>`（渐变透出）、锋芒边框 #444444。

### 修复（企业 12 页内容页背景全白——生成脚本漏调 clean_no_fill_bg，2026-08-01 下午）
- **用户反馈**"企业风第1页对、第2页不对（缺克隆的右上 logo/标题线）"。
- **诊断纠偏**：① 先误查 `references/teld-template.pptx`，用户纠正正确克隆源=`templates/enterprise.pptx`（`common.template_path()` 指向）；② 两模板均为**占位符空壳**（1 页 2 占位符，无 logo/标题线）→ 这两样本就不在克隆源里，克隆不出来；③ **真正根因**=`gen_fde_enterprise_12.py` save() 后**漏调 `clean_no_fill_bg()`** → 内容页(P2~P12)被 noFill 覆盖全白，封面 first_slide 复用模板不受影响 → 观感"第1页对、第2页起都不对"。
- **修复**：脚本 save 后加 `eng.clean_no_fill_bg(OUT, skip_slides=(1,))`，重生成 12 页；XML 验证 slide1/2/3 均无 noFill、背景正常。
- **经验（强）**：① 诊断"某页不像模板"先反查该页 `<cSld:bg>` 是否被 noFill 覆盖，再谈元素缺失；② 排查克隆源必须先看 `template_path()` 代码指向，勿凭文件名/glob 猜。→ `gen_fde_enterprise_12.py` / `SKILL.md §5.1`

### 修改（金句上方分隔线删除，四风格通用规则，2026-08-01 下午）
- **用户拍板**：所有风格通用——页底金句上方细分隔线一律去掉（含 P2 时间轴等所有走 `bottom_gold` 的金句）；**卡内结论上方 `card_divider` 保留**（非金句装饰，属卡内结构）。
- **代码**：`common.bottom_gold` 删除画线行（原 `rect(...,0.02,fill=line_color)`），`line_color/line_y` 参数弃用保留签名（兼容四引擎薄壳传参），docstring 更新。→ `common.py`
- **文档**：SKILL.md §4.2.2 金句区改写"金句上方无分隔线（覆盖'退背景层'旧做法）" + GOLD_LINE_Y 标注弃用 + 商务风段去"顶边极淡细线"；design-principles.md §11.3 重写（无分隔线 + card_divider 保留声明）；specs/wenzhi-constraints.md 金句行同步。→ `SKILL.md` / `references/design-principles.md` / `specs/wenzhi-constraints.md`
- **验证**：重生成 5 文件（商务 P3 v4 因 v3 被 PowerPoint 锁、文质/企业/锋芒 P3 v3、企业 12 页）；反向验证 22 页金句线残留=0、金句文字(y≈6.65)全在；validate_deck 四 P3 全 ok，企业 12 页报 6 处历史遗留"疑似换行"（页3/7/8/10 长文本框宽不足，非本次引入）。

### 修改（知识审计补漏：DNA 旧值全量同步 + 收尾，2026-08-01 傍晚）
- **背景**：用户要求"检查今天一天讨论的知识是否全部沉淀到 skill，遗漏以专家角色分层补"。
- **审计发现 17 处遗漏**：SKILL.md 10 处（§4.2.2 文质金句色仍写赤陶 #D97757；§4.3.1 文质强调色旧值；§4.3.3 文质分隔线 1.18 旧值；§5.0 企业二维码"右上已有 logo"过时描述；§5.1 企业画布来源写 layout[6]/"自带 logo 标题线"（实为 layout[8]+空壳模板+必调 clean_no_fill_bg）、底部金句"金色"（实为品牌橙）；§5.3 文质背景 #F5F0E8 旧值、赤陶橙旧值、FENG_CARD_LINE #1C1C1C 旧值、金句线 6.55/6.70 旧值）、design-principles 1 处（§10.2 锋芒卡边框 #1C1C1C）、specs 4 处（文质整表 #F5F0E8/#D97757/#4A4A4A/#666666 + h1 40pt/青线 1.12；企业金句 20pt、value_loop 卡边框 #00AFD2）、CHANGELOG 后续轮次缺失。
- **分层补齐**：规则层（SKILL.md §4.2.2/§4.3.1/§4.3.3/§5.0/§5.1/§5.3 全量同步今日定稿值）、原则层（design-principles §10.2 锋芒 #444444）、明细层（specs 文质配色表+三级强调+标题坐标、企业金句 16pt+卡边 #D2D8DC）、记录层（本 CHANGELOG 今日 4 条收尾）。
- **验证**：grep 复核 SKILL.md/design-principles/specs 无残留旧值（#D97757/#1C1C1C/#F5F0E8/layout[6]/金句线 6.55 均清零）。

### 重构
- **信息架构下沉**：Step 3 内的「调用约定铁律 + 双卡页选型 + 调用骨架代码」整体下沉为第 4 章末尾新增的 **§4.13「原语调用参考（分类 + 调用骨架）」**；Step 3 只保留一行指针，恢复为纯"用户交互"节奏。→ `SKILL.md` Step 3 / §4.13
- **公共层抽取（去重四风格）**：新增 `measure_text_height` + `tb_box_hug`（框高=文字实测高+gap，紧贴文字）、`COVER_QR` 坐标表 + `cover_qr(slide, style)`（封面二维码坐标驱动）、`bottom_gold(...)`（金句机制统一，新增 `bold` 参数保留各风格 DNA）。→ `common.py` / §4.8 §4.9 §4.10 §4.12-6
- **变更历史外置**：把散落在 SKILL.md 正文的日期尾注/「用户拍板」戳全部剥离到本文件，SKILL.md 只留"现行规则"。→ `SKILL.md` 全文 / `CHANGELOG.md`
- **§4/§5 分层重构（通用层/专属层）**：SKILL.md 第 4 章由"规则主题平铺"重组为"按生成模型分层"——§4 跨风格通用层（4.1 生成模型脊 / 4.2 页面类型约束 首页·内容页·结束页 / 4.3 内容页场景目录 / 4.4 跨风格通用原则 / 4.5 视觉增强 / 4.6 骨架×皮肤 / 4.7 原语调用参考），§5 风格专属层（5.0 跨风格专属参数对照：双栏分隔线色 + 封面二维码坐标 / 5.1~5.4 四风格）。抽走四风格专属参数、消 §10 悬空引用与 §4.12-6 伪编号、统一内部引用。→ `SKILL.md` §4 §5

### 新增
- **金句契约**：`timeline / two_column / card_grid / summary` 等内容原语统一加 `gold=None` 参数——传金句文本即自动渲染（含页码），不传则不画。根治"组件型原语缺金句"类 bug。→ `fengmang.py` / `wenzhi.py` / `business.py`
- **（首页迭代）`fit_font_to_width` + `shape_bottom_in` + `NATURAL_LH`**：新增"按宽反解单行最大字号"helper（封面主标题智能缩字保不换行）、"取形状实际框底"helper（flow 布局按前一元素底推导下一元素 y）、微软雅黑自然行高常量 1.35（PIL 实测）。→ `common.py`

### 修复
- **锋芒 `_glow` 超页**：右上角带底色硬边矩形（R=15.40 > 13.333，违红线二）→ 删除 `_glow` 函数及所有调用。→ `fengmang.py`
- **锋芒封面重构**：`cover()` 改左上对齐大标题 54pt（给内容区更大空间）；`section_header` 改用 `tb_box_hug`。→ `fengmang.py`
- **锋芒 `cover` 实参写反**：`tb_box_hug` 的 `color`/`bold` 参数顺序颠倒（潜伏 bug，首次执行即崩溃）→ 修正为 `(pt, color, bold)`。→ `fengmang.py`
- **四风格封面缺二维码**：各 `cover()` 未画封面二维码 → 锋芒/文质/商务补 `cover_qr`，企业风走等价 `add_qr_enterprise`。→ 四引擎 `cover()`
- **`layout_compare` 正解描述框撑破换行**：文质分支正解描述框按单行定高，长文本折行溢出 0.03″ → 改按内容行数自适应高度 + `word_wrap`。→ `common.py::layout_compare`
- **frontmatter 自相矛盾**：description 写"逐页交互确认"，Step 2 正文却明确"不用逐页确认" → 统一为"分步"。→ `SKILL.md` frontmatter
- **调用骨架二维码画两遍**：四风格 `cover()` 已内置封面二维码，旧骨架却在 `cover()` 外又手动 `add_qr` → 删除并加注"已内置勿外调"。→ §4.13
- **调用骨架缺 `gold=` 契约**：旧骨架 `timeline/two_column/card_grid` 未体现金句参数（缺金句 bug 的根因写法）→ 全部补 `gold=` 示例。→ §4.13
- **（首页迭代）企业封面主标题换行**：hero 写死 36pt，长副标题(13.15″)超内容区(12.13″)换行 → 改用 `fit_font_to_width` 智能缩至 33pt 单行。→ `enterprise.py::cover`
- **（首页迭代）`measure_text_height` 测高偏小致"框没包住文字"**：默认 1.2 且未计字形自然行高，54pt 大字框比真实渲染矮 ~0.11″、底部笔画被压 → 加 `max(SP_LINE, NATURAL_LH=1.35)` 地板，默认改走 `SP_LINE`；`tb_box_hug` 默认行距同步 `SP_LINE`。跨风格所有单行 hug 受益。→ `common.py`
- **（首页迭代）锋芒封面下划线嵌入标题**：分隔线 y 硬编码 2.02，54pt 标题实际框底 2.05~2.16 → 下划线压进标题底 0.03~0.11″。改由 `shape_bottom_in(title)` 推导 y（flow 布局），彻底消除碰撞。→ `fengmang.py::cover`
- **（首页迭代）锋芒封面灰字看不清**：纯黑底副标题 #999(6.9:1)偏暗、标签 #666(仅3.4:1)投屏几乎不可见 → 副标题→#CCC(12:1)、标签→#B3B3B3(9:1)；新增暗底对比强制规则。→ `fengmang.py` / §4.5

### 修改
- **行距数值统一**：§4.10 写 `line_spacing = 1.2` 与 §4.3 `SP_LINE = 1.22` 打架（代码真值 1.22）→ §4.10 统一为 1.22 并标注单一事实源。→ §4.10
- **§4.9 措辞纠偏**："每个引擎 cover() 必调 cover_qr" 对企业风不成立（企业风走 `add_qr_enterprise`）→ 改为分风格说明。→ §4.9

### 验证
- `FDE崛起_三风格对比_P1-P3_v2.pptx`（9 页）`validate_deck` **PASS**：三封面均有二维码、零越界、无单行折行；框高实测=文字高+gap（标题 1.00″=54pt 行高+0.10）。
- 四引擎 import 全部干净，企业风 12 页路径未回归。
- **（首页迭代）`四风格封面对比_v2.pptx`（4 页）`validate_deck` PASS**：反向读 XML——企业 hero 33pt 单行(12.06≤12.13)；锋芒标题居中、框底 2.163 vs 下划线 2.283 间隙 +0.12″ 不重叠、副标题#CCC/标签#B3B3B3 均居中；每页二维码标签 1 个、零越界。

### 重构（封面"包住+居中"公共化）
- **封面文本"包住+居中"提为公共原语**：新增 `cover_line`（框高=实测字高+2×gap、强制 `vertical_anchor=MIDDLE`、支持 `font`/`cy`）+ `fit_cover_title`（max_w=`min(内容区宽, 页宽×COVER_TITLE_MAX_W_RATIO=0.72)`）；四引擎 `cover()` 全改调，根治锋芒/商务"框没包住/不居中"、文质框比字矮（0.85<0.975）bug。→ `common.py` / §4.2.1
- **主标题占屏上限 72% 强制**：`fit_cover_title` 以 `页宽×0.72` 为宽上限反解单行最大字号，长标题自动缩字（企业 36→33pt/71.3%），禁裸 `fit_font_to_width(max_w=内容区宽)` 顶满。→ `common.py` / §4.2.1

### 修改（P2 内容页：金句/高亮/金额/坐标统一）
- **金句区强制 MIDDLE+bold 统一**：`common.bottom_gold` 默认 `bold=True` + 强制 `MIDDLE`，四风格 `_gold` 调用不得改 anchor/传 `bold=False`；落实 SKILL §4.2.2。
- **正文关键词高亮公共化（防平淡）**：新增 `emph_runs`（整段去重、最多 2 色 青/金）；修 `layout_timeline` 旧 dead code（`for seg in (kw_t+kw_a): pass`）改为接 `kw_teal/kw_amber`；四风 `timeline` 接 kw、企业走 `emph_runs`、文质走 `_run_emph`，落实"全文字最多 2 主题高亮、整页去重"。
- **金额即内容（amt）**：`layout_timeline` 加 `amt` 支持（追加"｜{amt}"琥珀加粗后缀）；文质 `timeline` 同逻辑；企业风走专属金额徽章；生成脚本 `TL_ITEMS` 补 `amt`（OpenAI 40亿$/AWS 10亿$/微软 25亿$）。
- **金句坐标共享常量**：`common` 新增 `GOLD_LINE_Y=6.50 / GOLD_TEXT_Y=6.65`（由页底反推，基准=企业风已验收 6.65），四风格 `bottom_gold`/时间轴统一改用、消除此前 6.20/6.35/6.38/6.50 离散硬编码（"后三风离底太远"）。

### 修复（P2 复验：锋芒重叠/文质贴底/商务不居中）
- **锋芒副标与时间线重叠**：`section_header` 返回副标底，`timeline` 增 `y0` 参数（默认 2.10=副标底+0.22 呼吸），根治重叠；时间框窄换行实测为重叠拥挤所致，根治后 6 条均 1 行。
- **文质标题线贴脸/金句贴底**：线 y 1.12→1.30、副标 1.30→1.50；`bottom_gold` text_y 原 6.70→统一走 `GOLD_TEXT_Y=6.65` 防贴底。
- **商务副标不居中**：副标 `tb_box` TOP→MIDDLE + `timeline` 接 kw。
- **金额丢失/金句截断**：上轮 `GOLD_TL` 被截短丢"75 亿"前半句 → 恢复含"75 亿美元"全文并经 `bottom_gold(..., kw_a=["75 亿美元"])` 高亮；企业金额框消失因生成脚本未传 `amt` → 补传。

### 验证（四风格 P1+P2 对比件）
- **`四风格_P1P2对比_v3.pptx`（8 页）**：反向验证（_diag_p2b.py，XML 直读）四风格 P2 金句均含"75 亿美元"(✓)、金额 40/10/25 亿$ 均呈现(✓)、金句 top 统一 6.65(✓)、锋芒副标底 1.88 vs 时间轴竖线顶 2.10 间隙 0.22(✓ 不重叠)、零越界；ALL_OK。
- 四引擎 import 全干净；`validate_deck` PASS。

### 规则沉淀（SKILL.md §4.2.1 / §4.2.2 补）
- §4.2.1：封面"包住+居中"公共原语 `cover_line` 强制 + 主标题占屏≤72% 强制。
- §4.2.2：① 正文关键词高亮（防平淡）5 条约束；② 金句区强制 MIDDLE+bold；③ 金额即内容（amt 琥珀高亮、金句关键数字不截断、kw_a 高亮）；④ 金句坐标统一共享常量 `GOLD_LINE_Y/GOLD_TEXT_Y`（基准企业 6.65）。

### 修复（金句首段空行）
- **`common.bottom_gold` 金句首段空行**：`run_text` 未传 `first=True` → 追加到新建段落、首段留空，金句文本因 MIDDLE 居中被下压半行。P2 走 `emph_runs`（写入首段）故未暴露，P3（无 kw）走 `run_text` 才显形（反向验证发现"FDE 的价值"金句首字符前多出空行）。→ 改 `first=True`，金句回到框内真正居中。→ `common.py`

### 验证（四风格 P1~P3 对比件）
- **`四风格_P1P3对比_v1.pptx`（12 页）**：四风格各 P1 封面 / P2 行业趋势时间轴 / P3 FDE 四种能力（2×2 卡片）。反向验证：bg 正确（企业 INHERIT 蓝 / 锋芒 #0A0A0A / 文质 #F5F0E8 / 商务 #FFFFFF）；P2 金句含"75 亿美元"+amt 40/10/25 亿$ 呈现、P3 金句"FDE 的价值…"均 ctr+bold+top 6.65；零越界；ALL_OK。

### 修复（P3 卡片页：副标题错位 / 序号两行 / 压线重叠）
- **副标题错位**：企业 `section_header` 原把 `sub` 当页底金句（`_render_gold`）渲染在 y=6.65，与设计意图（标题下副标题）相悖且压到金句 → 改为标题下**单行**副标题（label 青粗 + sub 灰内联）；锋芒原把 label/sub 写进两个段落强拆两行 → 改为同一段内联一行。四风格副标题统一为"核心能力 从发现需求到沉淀产品"单行（与文质/商务一致）。
- **序号 01~04 与标题两行**：`layout_card_grid` 原 tag 在 `y+0.20`、title 在 `y+0.50` 错行 → 改为**同一行**（tag 用 `concl_color` 强调色、title 用 `title_color`，均加粗）。
- **压线/重叠（四风格通病）**：原骨架写死金句分隔线 `y+ch-0.36`、金句文字 `y+ch-0.30`，而正文按整行宽度估折行数算高（常低估）→ 正文末行压分隔线、金句文字距卡底仅 0.04″（<红线 0.10）。重写 `layout_card_grid`：**卡片高度由内容驱动**（按真实折行数实测每行高累加 + 缓冲）、整组在 `[y0,y_end]` 内垂直居中；金句分隔线/文字**跟在正文之后**留安全间距，金句文字距卡底 ≥0.10″、整组距金句线(6.50) ≥0.10″。
- **`run_text` 首段空行坑（四引擎通病）**：锋芒/商务 `section_header` 追加 sub run 时 `run_text(..., first=False)` 默认新建空首段 → 文本框首段留 `\n`、副标被推成两行。补 `first=True`（锋芒另补 `set_chinese_font` import）。→ 四引擎 `section_header` / `common.py::run_text` 注释加注。

### 验证（四风格 P1~P3 对比件 v2）
- **`四风格_P1P3对比_v2.pptx`（12 页）**：_verify_p3.py 全绿——四风格副标题均顶部单行（y 0.95~1.5，无 `\n`、无页底）；序号+标题已合并同一行；每卡金句文字距卡底 = 0.12″（≥0.10，不压线）；卡底距金句线 0.16~0.28″（≥0.10）；全局 0 越界；P2 金句"75 亿美元"四页均在；ALL_OK。

### 修复（P3 卡片页五区量化：对照 ChatGPT 参考 + 复盘）
- **用户复盘分类（P3 框内五区 vs SKILL §4.3.3）**：① 5 个真 BUG：序号 12pt 应 28pt、结论 12pt 应 16pt、结论 LEFT 应 CENTER、结论不粗应粗、正文缺"·"前缀；② 4 处 SKILL 约束不明确：垂直居中实现方式未说、行距无量化值、01 与标题间距、自适应求解释义、禁换行与长结论矛盾；③ 2 处风格偏差（v2 仅"同行"未达 ChatGPT 量级感）。
- **`layout_card_grid` 五区重写（核心）**：① 序号 `run_text(28pt 自适应, True, concl_color, LEFT, MIDDLE)` 于固定宽 `NUM_W=0.78`，`NUM_TITLE_GAP=0.16`；② 标题 `run_text(16pt, True, title_color, LEFT, MIDDLE)` 与序号**同行 MIDDLE 居中对齐**；③ 正文 `run_text("· "+ln, 12pt, False, body_color, LEFT)` 每行 bullet 前缀、行距 `BODY_LS∈[1.20,1.40]` 量化；④ `card_divider` 分隔线（内容↔结论间）；⑤ 结论 `run_text(concl_fit(hl), True, concl_color, CENTER, MIDDLE)` **居中加粗**，自适应收 1 行（下限 14pt，消除长结论折 2 行顶高）。
- **卡高自适应求解**：在「序号字号(28→22) × 正文行距」两自由度上循环，取第一个能装进 `[y0,y_end]` 的最大组合（content_h 按真实折行实测累加 +0.06 缓冲）；最终四风格均取 **28pt**、卡底 6.30~6.37″ 全在金句线 6.50 之上。
- **页眉紧凑化（释放垂直预算）**：锋芒 `section_header` 30→26pt、线距 0.18→0.12、副标 y 收；文质分隔线 1.30→1.18、副标 1.50→1.24；`card_grid` y0 调 1.60(企业)/1.65(锋芒)/1.65(文质)/1.50(商务)，y_end=6.38（距金句线 0.12，满足红线）。
- **结论自适应 `concl_fit`**：长结论（如 card03"FDE 交付的不是一个功能，而是一套能够持续运行的业务闭环"24 汉字）16pt 下折 2 行顶高 → 判定后逐 pt 收缩至 14pt 收 1 行（下限 14pt），其余卡保持 16pt。

### 验证（四风格 P1~P3 对比件 v3）
- **`四风格_P1P3对比_v3.pptx`（12 页）**：_verify_p3v3.py 全绿——四风格序号均 **28pt 粗**(✓)、标题 **16pt 粗 MIDDLE**(✓)、正文 **8 行 "·" bullet**(✓)、结论 **居中加粗**(card03 因过长自适应 14pt、余 16pt，均 MIDDLE+CENTER)(✓)、**OVERFLOW 0**(✓)、卡底 6.30~6.37″ < 金句线 6.50(✓)；整本 P2 金句"75 亿"四页在(✓)、金额徽章在(✓)；ALL_OK: True。

### 规则沉淀（SKILL.md §4.3.3 / §4.2.2 重写）
- §4.3.3 卡片五区**量化**：序号 28pt(自适应≥22pt) 强调色粗居左 + 标题 16pt 粗 MIDDLE 同行 + 正文 12pt "·" bullet 行距 1.3 + 分隔线 + 结论 16pt 居中加粗(自适应收 1 行≥14pt)；补卡高自适应求解说明、页眉须紧凑前提、旧三 bug 注记。
- §4.2.2 `card_grid` 红线条目补全：序号 28pt MIDDLE 同行 / 正文 bullet / 结论居中加粗 16pt / 卡高自适应求解 / 页眉紧凑；并明示"布局由内容驱动、禁写死卡高"。

### 重构/修复（P3 卡片"小字大留白"二次迭代 — 覆盖上条 28/16 取值）
- **`layout_card_grid` 删"取最大能装字号"求解器**：改固定舒适小字号（序号 22 / 标题 14 / 正文 12 底线 / 结论 14）+ **卡框高 = 网格分配高、内容带卡内垂直居中** → 上下留白由字号与文案长度决定，而非顶满卡片（上条 28/16 取值被本迭代覆盖）。
- **根因实测（关键）**：子弹文案 34~61 字（如"真正可持续的模式应形成闭环：…沉淀为组件、Skill 和流程。"61 字 ≈ 8.6″），卡文字列仅 5.23″ 宽 → 12pt 下必然折 2 行；**缩字号不改"一行装不下"事实，故留白出不来**。用户拍板"缩短文案到 1 行"。
- **`gen_styles_P1_P3.py` CARDS**：每条 bullet 改写为 ≤17 字 1 行金句（保留原意，标题/结论不动）；`BULLET_GAP/DIV_GAP/CONCL_GAP` 微调为 0.10 更透气。
- **验证（`_verify_p3v3.py` 预期改 22/14/14）**：四风格卡内上下留白 **0.33/0.26″**、内容占卡高 **71~74%**（原 93%）；序号 22pt 粗 / 标题 14pt 粗 MIDDLE / 8 行 1‑line bullet / 结论 14pt(长文 13) 粗 MIDDLE 居中；OVERFLOW 0、卡底 6.38 < 金句线 6.50；ALL_OK。
- **经验**：卡片"紧凑/换行"根因常是**文案过长**而非字号；2×2 宽胖卡里长中文 bullet 必折行，缩字号救不了，须缩短文案到 1 行或放宽卡宽。下次此类迭代先量 bullet 字数再定方案。

### 验证（第八轮：锋芒风全本生成，确认 three_column 等四风格对齐生效，2026-08-04 收尾）
- **背景**：第七轮补齐锋芒/文质/商务的 `three_column` wrapper + `section_header` 副标 `None` 保护后，需真本验证锋芒风能整本跑通、且 P11 三列真实渲染（此前三列仅企业风有 wrapper）。
- **新增 `references/runner-example-fengmang.py`（锋芒风 per-article runner 范式）**：镜像企业风 `runner-example-enterprise.py`，适配锋芒 API 差异——`cover(title, subtitle, tags, total, n)` 无 `subtitle2/date_str` → `tags` 承载副标与文号；`section_header` 顺序（title, label, sub）；`definition_compare` 签名与企业风一致；`two_column` 无自带页眉须先 `section_header`。内容与企业风 `_v6` **完全一致**（同款 2 行卡合并，规避双行 2×2 压线）。
- **验证**：生成 `互联网平台价格行为规则_锋芒风_12页.pptx`；`validate_deck` PASS(0)、OVERFLOW 0；反向读 XML 确认 12 页、封面含二维码、12 页均有页码；2×2 网格页（P2/3/4/5/8/12）各 **4 张等宽卡（宽 5.17″）**、P10 单列 2 卡；**P11 = 3 张等宽卡（宽 3.855″）**，与企业风 P11 几何一致 → `three_column` 四风格真实可用；P6 `definition_compare`、P7/P9 `two_column` 正常。
- **沉淀**：两份 runner 作为「per-article runner 范式」参考样例存入 `references/`（企业风 + 锋芒风），README §七 参考索引已登记；四风格对齐经真本验证闭环。

## 2026-07-31

### 重构（架构里程碑）
- **布局骨架 × 皮肤分层**：布局几何只写一份在 `common.layout_*`（骨架，不引用具体色值/字体）；四风格只提供皮肤（`SKIN_*` dict：配色/字体/字号/箭头/卡样式）。确立"**企业风为布局样板**"——新场景先在企业风调通 → 公共骨架定稿 → 文质/锋芒/商务换皮肤自动生效。→ `common.py` / `SKILL.md` §4.12-8
- **引擎层全部改调骨架**：文质 12 原语 + 企业 6 富原语 + 锋芒/商务基础原语，**原函数签名全保留、业务脚本零改动**；`enterprise.timeline` 卡片式（homePlate+徽章+虚线）为定稿特色保留在引擎层。→ 四引擎
- **skill 清理**：删项目级旧版 skill 与 `__pycache__`/旧引擎/旧样式残留；`design-principles.md` 从时间轴流水账重写为规则体系；全 skill 清理 PX（P1~P10）耦合引用。

### 新增
- **骨架化 12 个 `layout_*`**：`loop_page / timeline / card_grid / compare / value_grid / profile_warning / six_step / talent_strip / transition_rows / hero_questions / two_column / summary`。→ `common.py`
- **公共布局规则（用户拍板，进 SKILL.md §4.12-7）**：红线①每行文字距线 ≥0.10″、红线②形状不越界（≤13.333×7.5，生成后必跑 `validate_deck`）、间距按内容量智能算（0.10~0.16 弹性）、正文 ≥12pt 底线智能求解（禁手工写死）、行带高取行内最大字号、箭头随底色（深底 2pt / 浅底 1.5pt）、复合页用编号小标题①②③、两卡协同用 ⇄ 符号。
- **约束求解器**：`solve_card_fonts`（字号联立求解：正文≥底线优先最大 → 标题 → 数字 → 结论）+ `fit_gaps`（单卡间距区间弹性分配）。→ `common.py`
- **公共机制**：`measure_text_width` / `content_card` / `card_divider` / `loop_arrow` / `loop_return_u` / `fit_single_line` / `rounded_card` / `vcenter` / `auto_gap` / `set_leading` + 画布常量 `CANVAS_*`。→ `common.py`

### 验证
- `四风格骨架试点v4.pptx`（12 骨架 × 4 皮肤 = 48 页）`validate_deck` **PASS**；文质业务回归 PASS（P4 求解 20/18/14/14 与定稿一致）。

## 2026-08-03（数据中台企业风 10 页实战 → 通用规则定稿）

### 重构（卡宽卡高通用铁律，覆盖全风格全带框页）
- **`layout_two_column` 通用化**：删每风格各写一份（仅企业风曾 bespoke），改为 `common.layout_two_column` 薄壳委托；每栏宽=最长行实测+2*pad→本页 maxW 统一封顶列宽、栏高=标题+条目+note→maxH，左右成对水平居中。→ `common.py` / `enterprise.py`
- **`common.fmt_date_5digit` 扩展**：兼容 `.` 与 `/` 分隔、月日零补→5 位（8.31→08.31），带后缀仅格式化日期部分；所有 timeline 受益。
- **通用铁律确立（用户拍板）**：所有风格、所有带框页（card_grid / two_column / compare / value_grid / profile_warning / transition 等）的**卡宽卡高均由内容实测算、取本页最大值统一**，禁止写死半幅/写死高度。`layout_card_grid`：卡宽 `cw2 = min(max_inner*1.04 + 2*pad, col_avail)`（col_avail 仅作 cap 非取值、下限 3.0）、卡高 `ch = max(card_h(c))` 四卡等高+溢出封顶 fit_cap。四风格回归：two_column 均宽 3.52、card_grid 均宽 3.65，均居中。→ `common.py` / §4.3.3

### 修复（card_grid 内部节奏三处 bug，用户复核指出）
- **bullet 段距黏连**：`BULLET_GAP 0.10→0.22″`、`BODY_LS 1.35→1.25`（行距 0.208），段距≥行距不黏连；bullet 框高=行高（去 +0.04 缓冲）；卡宽补 `*1.04` 安全余量使最长行单行不折。
- **P6 触红线压金句**：根因是宽度漏 1.04 余量→最长行折 2 行→卡变高；改后按本页最大内容统一卡高、封顶 fit_cap，卡底统一 3.83″/6.38″（金句区 6.65″，间距 >2″）。
- **P8/P10 分隔线贴正文+总结区留空**：正文顶锚+结论底锚分离→改 `[正文+分隔线+结论]` 整组在剩余高度内垂直居中（body→divider 0.11″、divider→hl 0.12″、hl→卡底 0.10″ 三段均匀）。

### 修复（card_grid 同行分隔线对齐，用户点名 P5-04/P10-04）
- **问题**：分隔线=正文末行底+固定间距，随 bullet 行数浮动；同行 3 行卡与 2 行卡错开 0.24″（P5 行2 03=5.92″/04=5.68″）。P9(two_column) 因锚定卡底故同行对齐（用户要"参照 P9 右侧框"）。
- **方案（用户拍板 A，非 min/max）**：分隔线/结论**锚定卡底固定偏移**（`hl_y=卡底-VPAD-concl_h`、`div_y=hl_y-CONCL_GAP`），与 two_column 同源、与 bullet 行数解耦。min 会重叠正文不可用、max 后处理脆弱（依赖同行最长卡）。→ `common.layout_card_grid` ②③→④
- **结果**：P5/P10 同行分隔线均对齐（行1=3.33″、行2=5.88″，组内差 0）；纯 2 行页（P4/P7/P8）行为不变、无回归。→ §4.2.2 / §4.3.3

### 验证
- 企业风 deck `数据中台建设专项技术要求_企业风.pptx`（10 页）：`validate_deck` **PASS(0)**；反向 XML 核查三处 bug + 分隔线对齐全部确认修复。
- 四风格回归（临时文件已删）：two_column 均宽 3.52 居中、card_grid 均宽 3.65 居中，规则全风格一致生效。

### 文档沉淀
- SKILL.md §4.3.3 / §4.2.2 重写：智能宽度（通用铁律）、卡框高（本页最大内容带→四卡等高）、分隔线锚定卡底（与 two_column 同源）；覆盖旧 `cw=max_chars*(14/72)/2+0.39` 公式与"跟在正文之后"旧写法。→ `SKILL.md`

### 卡宽下限 70%·col_avail（2026-08-03 收尾·第二波）
- `common.py::layout_card_grid` 卡宽下限由写死常量 `3.0` 改为 `max(0.70*col_avail, 3.0)`：短内容页（如 P10 2×2 四卡内容短）抬到 70% 列宽，防塌成窄卡 + 左右大留白（实测 3.0″ 仅占内容区 54%、02 标题"人员配备（V0→VP）"临界折行）；`3.0` 绝对兜底护窄列（2×3 列宽仅 3.7″，70% 仅 2.59″<3.0 锁 3.0 不回退）。→ P10 卡宽 3.0→3.99″、网格占 71%、02 标题单行；P4 长内容页(4.37″)不变、P8 2×3 回退 3.0″；`validate_deck` PASS。

### two_column 70% 对齐 + 结论分隔线（2026-08-03 收尾·第三波）
- `common.py::layout_two_column` 卡宽下限由写死 `3.2` 改为 `0.70*col_avail`(≈3.99)：消除「两列页不达标、大留白」残留（P2/P9 实测 56%~66% → 70% 统一）；P9 标题框 2.93→3.39″，"职责分工（甲方 A / 乙方 R）"单行不再折行。→ 与 card_grid 70% 口径一致，所有风格 two_column 同步受益。
- 文质风 `wenzhi.two_column` 增加 `notes=[左结论,右结论]` 参数并转发至骨架；gen `P2/P9` 两列框补结论（开发范围→四大范围界定交付边界 等）+ 锚定卡底分隔线，与 card_grid 的 hl 同源。→ `validate_deck` PASS。
- `common.py::layout_card_grid` 标题字号由写死 `14` 改为读皮肤 `card.title_size`(=16，与 two_column 同源)，字体 `body_f`→`head_f`：消除两列/多列标题「16 vs 14 + 雅黑/宋体」不统一；过窄 2×3 卡(P8)按「本页最长标题可装下的最小字号≥14」整页统一收缩（禁逐卡参差）。→ 反向 XML 确认 P5 多列标题 14→16pt 与 P2 两列统一、P8 全 14 齐；企业风+文质风 `validate_deck` PASS(0)。
