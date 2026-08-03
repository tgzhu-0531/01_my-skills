# 文质风排版约束（唯一权威源）

> 引用：`engines/wenzhi.py` 按此表渲染。
> 无模板 — 从空白 `Presentation()` 构建，奶油纸底 + 宋体标题。
> 本文档是「知识沉淀层」：风格 DNA → 字号角色 → 强调语义 → 布局铁律 → 版式原语，逐层收敛。

---

## 0. 分层架构

| 层 | 落点 | 职责 |
|:--|:--|:--|
| L0 规格层 | 本文件 `specs/wenzhi-constraints.md` | 配色语义 / 字号角色 / 强调语义 / 布局铁律 / 原语坐标目录 |
| L1 引擎原语层 | `engines/wenzhi.py` | `WEN_TYPOGRAPHY`/`WEN_PALETTE`/`_role` 声明式规格 + `block`/`card_title`/`wcard` 本地助手 + 8 个整页富原语 |
| L2 生成器层 | `gen_fde_wenzhi.py`（业务侧） | 只做「内容 → 原语」映射，**不含任何布局坐标** |
| L3 文档同步 | `SKILL.md` §3/§5.3 | 调用骨架与「文质风现已具备富原语」说明 |

设计原则：视觉规则从代码逻辑剥离为声明式规格；富版式沉淀为引擎原语，生成器薄到只剩内容。

---

## 1. 风格 DNA

### 配色（含语义角色，非裸色值）

| 角色 | 色值 | 语义 | 用途 |
|:--|:--|:--|:--|
| 背景 | `#F7F4EE` | 奶油纸底（暖化） | 页面底色 |
| 卡片底 | `#FFFFFF` | 白卡 | 柔边白卡 |
| 品牌青 | `#00A5C8` | **结构色** | 装饰线 / 时间轴圆点 / 标签 / 核心观点 / 三级强调「主体」 |
| 深蓝灰 | `#30485B` | **卡标题主色** | 卡片标题（2026-08-01 微调：卡标题青→深蓝灰，字号不加大、靠颜色拉层级） |
| 暖金 | `#C99322` | **结论色（唯一点睛）** | 底部金句 / 卡内结论钩子；三级强调「结论」（原赤陶橙 #D97757 已退役） |
| 琥珀金 | `#C08A2D` | **第三级强调** | 金额 / 投入（不与青、暖金撞） |
| 近黑 | `#191919` | 标题 | 主标题 / hero（宋体） |
| 正文 | `#4D5054` | 正文 | 段落（原 #4A4A4A） |
| 次要 | `#777A7E` | 退后 | 副标题 / 页码 / 说明语（原 #666666） |
| 降温 | `#8A8A8A` | 否定 | 对比卡否定项（✕） |
| 卡边框 | `#DDD8CE` | 卡片边线 0.75pt + 6% 影 | 卡内细分隔 / 卡框 |
| 分隔线 | `#E8E2D4` | 主分隔线色 | 结论上 D2 通栏 |
| hero 下划线 | `#D0C8B8` | 退到背景层 | hero 区下方淡暖灰满宽线 |
| 卡内底线 | `#F0EBE0` | 松散内容底线 | 极浅分隔 |
| 连接线/箭头 | `#B0A692` | 颜色退、线宽进 | 流程连线（浅底→深色的暖灰） |
| 次级卡底 | `#EFEBE2` | 旧态/降温 | 过渡页「旧态」块 |

### 字体

| 角色 | 字体 |
|:--|:--|
| 标题 / hero | **宋体**（衬线出版感） |
| 正文 / 标签 | 微软雅黑 |

---

## 2. 字号角色表（`WEN_TYPOGRAPHY` + `WEN_PALETTE`）

角色 → (字号, 加粗, 字体) → 颜色。函数统一走 `_role()` 渲染，禁止在版面函数里写裸 `52/40/18` 等魔法数字。

| 角色 | 字号 | 加粗 | 字体 | 颜色 | 语义 |
|:--|:--:|:--:|:--|:--|:--|
| hero | 52 | 是 | 宋体 | INK | 封面主标题 |
| h1 | 36 | 是 | 宋体 | INK | 内页主标题（原 40pt 已减压） |
| sub_cover | 22 | 否 | 雅黑 | MUTE | 封面副标/说明语（退后） |
| sub_label | 16 | 是 | 雅黑 | TEAL | 内页核心观点（结构强调） |
| sub_lead | 16 | 否 | 雅黑 | MUTE | 内页副标-说明（同行灰） |
| gold | 16 | 是 | 雅黑 | WEN_GOLD（暖金 #C99322） | 金句/结论（唯一点睛；原 18pt+TERRA 已统一/退役） |
| date | 13 | 是 | 雅黑 | TEAL | 时间轴日期 |
| title_card | 20 | 是 | 宋体 | TEAL | 卡片标题 |
| body | 14 | 否 | 雅黑 | BODY | 正文 |
| tag | 14 | 否 | 雅黑 | MUTE | 封面标签组 |

**铁律**：主标题一律 INK+宋体（青只留给结构线与内页核心观点，不抢主标题）；副标题分两型（封面灰退后 / 内页青提结构）；金句一律 暖金 WEN_GOLD+粗体。

---

## 3. 三级强调语义（正文内核心词高亮）

经 `_run_emph` 实现，规则：

1. **青 `#00A5C8` = 主体**（公司 / 产品 / 谁）；
2. **琥珀金 `#C08A2D` = 金额 / 投入**；
3. **暖金 `#C99322` = 结论**（页面唯一暖色点睛，不用于正文内高亮；原赤陶橙 #D97757 已退役）。

约束（用户确认的设计铁律）：
- **最多 2 种高亮色**；
- **只取主题最贴近的少数词**，克制不滥（滥则乱）；
- **每词本段仅高亮首次出现**（落实"整页一公司只强调一次"）；
- 其余文字保持正文色。

---

## 4. 布局铁律（专家级，强制）

1. **Hero 文字框「贴字」**：框宽=实测字宽+0.12，框高=字号行高+0.08；禁止写死大框把空白顶下去（曾因 2.30×1.55 大框把下划线和正文挤到下方、中间留大段空白）。
2. **两栏卡片「自动均布」**：内容按卡高 `(卡内高−内容总高)/(段数−1)` 均分间隙铺满整卡，杜绝底部大段空白（曾硬编码步进导致底部留 ~1.6″ 白）。
3. **左右两栏留白 0.35″**（专业两栏间距），非紧贴也非分离。
4. **副标题可空**：不是每页必须有副标题/金句；空则 `label=None, sub=None`，引擎加 None 守卫（不渲染任何 run，杜绝 "None" 字面或引号残留）。
5. **正文字号 ≥12pt 底线**（不是上限）：内容少→向上放大更大气，内容多→收到底线 12，绝不小于 12；禁止手工指定固定字号，走 `common.solve_card_fonts` 智能求解。
6. **尺寸实测算**：卡宽/文本框宽用 `measure_text_width` 算最长行真实宽度，禁换行、禁撑满；取测算中间值，不在"太窄↔撑满"两极端横跳。
7. **红线一·不贴线**：每行文字距任何线（分隔线/卡框/页脚线）≥ 0.10″。
8. **红线二·不越界**：卡片/形状 ≤ 13.333 × 7.502，生成后必跑 `validate_deck`。
9. **间距智能 + 层级**：上下间距按内容量智能算（内容少→放大、多→收紧，区间 0.10~0.16″）；层级：标题↔正文 > 段落↔段落 > 段内行距（下限逐级递减）。

---

## 5. 版式原语目录（`engines/wenzhi.py`）

> **2026-07-31 重构完成**：本表全部原语（除封面/氛围装饰）函数签名保留，**函数体已改调公共骨架**（`common.layout_*` + `WENZHI_SKIN` 皮肤），布局几何以骨架为准，本表只保留内容结构约定；文质风专属数值（金句坐标/求解器区间/网格）固化在 `WENZHI_SKIN` 与 §7。

### 基础原语（组件型，不自带标题/金句）
`cover` · `section_header` · `timeline`（→`layout_timeline`） · `two_column`（→`layout_two_column`） · `card_grid`（→`layout_card_grid`） · `summary`（→`layout_summary`） · `bottom_gold`
> 组件型需调用方先 `section_header` 再组合；`timeline` 自带 accent，与 section_header 同页时需 `dedupe_accent`。

### 整页富原语（自带 section_header + 底部金句，生成器直接调）
| 原语 | 用途 | 内容参数要点 |
|:--|:--|:--|
| `cover_story(prs, title, subtitle, tags, author, n, total)` | 封面 | 封面 + 作者行 + 二维码 |
| `timeline_page(prs, h1, label, sub, items, emphasis_teal, emphasis_amber, gold, n, total)` | 时间轴 | items=[{time,text}]；emphasis 走三级强调 |
| `definition_compare(prs, h1, hero, hero_en, hero_cn, bullets, compare_header, negatives, positive, gold, n, total)` | 定义对比 | 左 hero 贴字 + 悬挂引注；右卡自动均布对比（透明底+青边框）；**无副标题**。**2026-07-31 迁移公共骨架 `common.layout_compare`**（`WENZHI_SKIN['compare']`：hero 墨 48 / en 青 18 / bullet bar 引注 / neg_badge="text" / right_card=True / pos 青）|
| `value_grid(prs, h1, label, sub, items, gold, n, total)` | 价值网格 | items=[{num,title,points,tag}]，2×2 纯并列（去箭头）。**约束求解版**：走 `common.solve_card_fonts`（正文 12~16 从上限向下试、≥12 底线；标题 14~18 / 数字 16~20 / 结论 11~14），间距区间：卡顶 0.08~0.12 / 带→D1 0.12~0.16 / D1→正文 0.12~0.16 / 段间 0.10~0.14 / 正文→D2 0.12~0.16 / D2→结论 0.10~0.14 / 结论→卡底 0.06~0.10（v8 实测值在区间内）；段间不画线、青方块 0.09″ 分段；网格 1.80→6.48、卡间 0.16、卡高 2.26。**2026-07-31 迁移公共骨架 `common.layout_value_grid`（loop=False）**：以上数值全部固化进 `WENZHI_SKIN['value_grid']`（gap_h 0.33/gap_v 0.16/solve True/D1+方块/tag 左对齐）|
| `feedback_loop(prs, h1, label, sub, intro, loop_nodes, loop_cap, role_title, role_cap, roles, notes, gold, n, total)` | 反馈闭环 | 闭环四节点 + Palantir 双角色 + 三点说明。**v3 规则全面对齐企业风 work_people**：三块编号 ①②③（14pt 青 bold 引导）；卡一律透明底+青边框 1.25pt（content_card，取代旧白底 wcard）；节点 16pt MIDDLE（支持 {name,sub} 双行）；角色卡两段式 cn16青+en12灰 → D1 青短线 → desc+结论尾句（`_body_hl` 青 bold 混合 run）；⇄ 22pt 青；回流缝 0.22；intro 12pt 全宽 1 行（内容密度高时底线字号单行） |
| `six_step(prs, h1, label, sub, step_cap, steps, cards, bottom_note, gold, n, total)` | 六步流程 | 六步流程条 + 三栏白卡 |
| `talent_strip(prs, h1, label, sub, intro, items, gold, n, total)` | 人才长条 | items=[{num,title,lines}]，全宽 4 条横向长条 |
| `profile_warning(prs, h1, label, sub, left, right, gold, n, total)` | 画像告诫 | 非对称双卡；left={title,roles_grid,long,conclusion}，right={title,warns,conclusion} |
| `transition_rows(prs, h1, label, sub, intro, rows, gold, n, total)` | 转型对照 | rows=[{from,to,lines}]，旧态降温→新态白卡 |
| `hero_questions(prs, h1, label, sub, lead, questions, signature, n, total)` | 结语问答 | 宋体三问 + 青短线 + 落款 + 二维码 |

### 本地助手（版式原语共用）
`block`(悬挂式段落+可选高亮) · `card_title`(卡标题+青细线) · `wcard`(柔边白卡) · `nlines`(实测换行) · `dedupe_accent` · `add_page`

---

## 6. 卡片 / 双栏

- 白底 `#FFFFFF` + 柔色分隔线 `#E8E2D4`，圆角 `rounded=True` adj=0.03，line_w=1.0。
- 对比卡：透明底 `fill.background()` + 品牌青边框 1.25pt（用边框界定区域，替代填充，与"青做结构"DNA 一致）。
- 双栏 gutter 0.35″；分隔线暖灰（浅底→深色）。

## 7. 封面 / 内容页 / 金句

- 封面：标题 52pt 宋体 + 青短线居中 + 副标 22pt 灰 + 标签行；作者行居上文字块与二维码正中；二维码底中 `size≈0.95`，下方"扫码关注「天戈朱」"。
- 内容页标题：h1 36pt 宋体（y 0.45，原 40pt 已减压）+ 青线作标题下划线（y 1.02，紧贴标题读作"下划线"，2026-08-01 方案A）；label/sub 同行内联（sub_cover 退后 / sub_label 青提结构），**整行 y 1.24**（距青线底 ~0.17″ 空气；原 1.30/线 1.18 已弃用）。
- 底部金句：16pt 暖金 `#C99322` 粗体居中，文字 y=6.65（共享常量 GOLD_TEXT_Y；**金句上方无分隔线**，见 SKILL §4.2.2 通用规则）；内容区底上限 6.48″。与二维码保留 ≥0.3″ 间隙。

## 8. 表格

- 隔行背景 `#EFEBE2` 柔暖色（不用纯白）。
