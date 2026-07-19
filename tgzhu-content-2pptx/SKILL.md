---
name: tgzhu-content-2pptx
description: "从IMA知识库/公众号链接/本地文件/粘贴内容中筛选指定资料，基于内容与听众角色，通过逐页交互确认生成PPT的完整工作流。支持teld风/锋芒风/文质风/商务风四种视觉风格。每一步都带着交互，用户确认后才推进。"
agent_created: true
---

# 内容 → PPTX 完整工作流

## 概述

从多源内容（IMA 知识库 / 公众号链接 / 本地文件 / 粘贴内容）中筛选指定资料，基于内容提炼主题，按听众角色预设大纲规则生成 PPT 内容，逐页交互确认后生成 PPTX。

支持 **4 种视觉风格**：teld 风（深蓝渐变）· 锋芒风（纯黑高对比）· 文质风（奶油纸暖色）· 商务风（白底深字）。

## ⚠️ 强制约束

**AI 执行本技能时，必须严格按以下 Step 1~4 的顺序和交互节点执行，不得跳过、合并（除非明确标注"合并"）、提前或自行发挥。**

具体规则：
1. 执行**必须先读 SKILL.md 全文**，按步骤执行
2. **严禁跳过任何交互节点**（弹窗/提问/等待输入/等待确认）
3. **严禁在用户没有提供内容的情况下**直接生成大纲或 PPT
4. **严禁在用户没有确认的情况下**修改文件或生成 PPT
5. 每个步骤完成后必须输出当前状态，然后进入下一步
6. 如果用户要求"跳过某步"，问"确认跳过？"后才可跳过
7. 当用户直接说"生成PPT"或"做一份PPT"等指令时，从 Step 1-A 开始执行

## 核心原则

**每一步都带交互，用户确认后才推进。** 流程如下：

```
弹窗1（来源）→ 用户选 → 用户打字输入内容 → AI获取 → 弹窗2（听众+页数）
   ↑单问题    ↑              ↑              ↑自动    ↑2问(带推荐)
          ↓
  Step 2 审内容 → 弹窗3（选模板）→ 弹窗4（最终确认）→ 用户确认 → 生成PPTX
   ↑预览确认   ↑弹窗（AskUserQuestion）  ↑弹窗（AskUserQuestion）
```

红色规则（任何情况不能碰）：
1. ❌ 用户没确认 → 不改文件
2. ❌ 用户没确认 → 不生成 PPT
3. ✅ 生成后 → 必须告知文件路径

---

## Step 1：选文件 + 定听众 · 分阶段连续提问

### 触发

用户说"生成PPT"、"做个分享"、"做一份PPT"或加载此技能时触发。

### 弹窗 1：来源（单问题）— 必须用 AskUserQuestion

加载完成后，先输出技能启动提示，然后用 **AskUserQuestion 弹窗**提问：

> **输出提示：** "tgzhu-content-2pptx 已就绪，开始制作这份 PPT。"

> **问题 1（选项）：** "你打算如何提供材料？"

| 选项 | 说明 | 用户下一步 |
|:----|:----|:---------:|
| 1\. **IMA 知识库**（推荐） | 从你的 IMA 个人知识库中选择已有文章/文件 | 弹出知识库列表让选 |
| 2\. **提供链接** | 提供 `mp.weixin.qq.com/s/...` 公开链接 | AI 文字回复"请把链接发给我" |
| 3\. **粘贴内容** | 直接把文字粘贴到对话中 | AI 文字回复"请把内容粘贴过来" |
| 4\. **用示例大纲** | 使用 skill 自带的示例大纲快速起步 | 直接跳到弹窗 2 |
| 5\. **本机文件地址** | 提供本地文件路径（多个文件/大文件/PDF 时用） | AI 文字回复"请提供文件路径" |

**关键点：**
- ❌ **不再弹第二个问题**让用户选择"输入链接/粘贴文字/输入文件路径"（选项冗余）
- ✅ 用户选完来源后，AI 用**普通文字**告诉用户怎么提供具体内容
- ✅ 用户用**直接打字**的方式在聊天框输入链接/粘贴文字/文件路径（不是弹窗）

### AI 获取内容（自动执行）

收到具体内容后，AI 自动执行：
1. 用对应工具（WebFetch / Read / `mcp__ima-mcp__*`）获取完整内容
2. 解析文章：标题、作者、核心观点、关键段落
3. **基于内容量评估**，为页数推荐做准备
4. 在脑中形成"这份内容大概能做几页"的判断

### 弹窗 2：听众 + 页数（带推荐）

内容就绪后，先输出提示，再一次性连续问两个问题：

> **输出提示：** "内容已获取（约 X 千字，N 个核心观点）。最后确认两个信息："

> **问题 D1：** "这份 PPT 的听众是谁？"

| 听众角色 | 大纲风格 | 内容侧重 |
|:--------|:--------|:--------|
| **研发团队** | 技术深度 | 架构、代码、数据流程、五层体系 |
| **产品/业务** | 应用价值 | 案例效果、能力边界、选型建议 |
| **管理层** | 结论先行 | 核心观点、ROI、建议方案 |
| **跨部门分享** | 通俗易懂 | 案例贯穿、类比说明、一句话结论 |

> **问题 D2：** "做多少页？请在下方选择推荐方案，或在输入框中输入你想要的页数"
> 
> 用户可接受推荐页数 / 自定义页数（如输入"4"表示4页，"8"表示8页）

**⚠️ 歧义避让规则（2026-07-18 更新）：**

**核心原则：用户输入数字 → 直接作为页数；用户点击选项 → 使用选项对应页数。**

由于 AskUserQuestion 工具无法区分"用户点击了第N个选项"和"用户在自定义框输入了数字N"，必须通过以下方式消除歧义：

1. **选项数量 ≤ 3 个**（不超过选项序号 1-3），避免序号 4/5/6 撞上用户输入的常用页数
2. **选项标签不以纯数字开头**，改用描述性文字（如"精简版（约6页）"而非"6页精简版"）
3. **用户输入任何数字 → 直接作为页数**，不视为选择选项

### 执行流程

```
弹窗1（来源+内容输入） → 用户填写 → AI自动获取内容
  ↓
弹窗2（听众+页数） → 用户回答 → 生成大纲
  ↓
进入 Step 2：审内容
```

### 注意

- **必须先有内容才能推荐页数**，所以听众+页数放在"弹窗 2"
- **选项 4（用示例大纲）** 时，弹窗 1 只问来源，内容框可跳过；弹窗 2 仍可调听众/页数
- 用户在弹窗 2 接受推荐页数 → 直接生成大纲

### 产出

`outline.md`（大纲）+ `content.md`（详细内容稿），按听众角色和确认页数生成。

**注意：** 两个文件将在 Step 2 中用"文件名超链（正文中）+ present_files（产物区）"双重方式展示给用户。生成后先不要展示，进入 Step 2 再按规则输出。

### ⚠️ 内容丰富度要求

每页内容必须有充足的原文干货支撑标题，不得只写骨架：

| 规则 | 不够（骨架） | 够（血肉） |
|:----|:-----------|:----------|
| **核心数据** | "8 个媒体槽" | 列出 8 个媒体槽的具体内容：hero 图、2 支 mp4、截图、SVG…… |
| **表格** | 一句话总结 | **原文表格直接搬到 PPT 中**（如 AST 状态转移表） |
| **关键数字** | "3 轮封顶" | 写清楚：3 轮封顶 + 不收敛标 needs-human |
| **真实案例** | "有实际案例" | 展开讲：截图发现 9 页遮挡 → 自动修复 → 复检通过 |
| **对比逻辑** | "和模板库不同" | 列出 6 个对比维度：起点/密度/素材/渲染/质量/交付 |

**强制规则：**
1. 原文中的**表格**必须完整保留，不能简化成文字
2. 原文中的**关键数字**不能丢（如具体数量、版本号、时间）
3. 原文中的**真实案例**要展开讲（什么场景、怎么解决、结果如何）
4. 原文中的**对比表**要原样保留
5. 每页至少要有 1 个"撑得住"的核心论据（数据/案例/表格/对比）

### ⚠️ 内容充实度检查清单

提取每页内容时，按以下顺序检查原文**实际存在**的论据：

```
① 核心论点 —— 这页要讲什么（原文有）
② 数据支撑 —— 原文中涉及的数字/数量/版本
③ 案例支撑 —— 原文中展开的具体案例
④ 对比/表格 —— 原文中的对比/表格/结构
⑤ 金句结论 —— 原文中的总结性语句（→ 开头）
```

**核心原则：不延伸、不创作、只搬运原文。**

- 如果某页原文支撑不足 3 条论据 → **不独立成页**，合并到相邻主题页
- 宁可总页数少，也不要内容单薄的页面
- 禁绝掺入原文没有的"创作性内容"

### ⚠️ 图片处理策略

AI 工具无法从文章 Web 页面提取配图（只取文字）。策略：

| 场景 | 做法 |
|:----|:----|
| **原文配图** | 内容稿中标注 **`【图：原文配图位置说明】`** 占位 |
| **封面配图** | 可选：用 ImageGen 生成新图 或 留占位 |
| **复杂信息图** | 走 baoyu-infographic 生成 或 留占位 |

**生成 PPTX 时：** 含占位的页面用文本框标记 `【图：XXX】`，用户打开 PPTX 后把图贴到对应位置。

---

## Step 2：审内容 · 预览确认

### ⚠️ 核心规则：预览→发现问题→讨论修改

**生成大纲和内容稿后，一次性交给用户预览，不用逐页确认。**

### 交互流程

```
生成大纲 + 内容稿
  → 展示给用户（系统自动将文件名转为可点击预览链接）
  → 用户检查
  → 有问题：用户指出第几页，讨论修改
  → 没问题：用户说"下一步"、"OK"、"确认"
      ↓
  进入下一步（Step 3）
```

### 规则

1. **一次性生成完整大纲和内容稿**（outline.md + content.md），不用逐页生成
2. **展示给用户**：先在回复正文中用文字写出文件名（如 `outline.md` 和 `content.md`），系统会自动转为可点击的预览链接。**不要只靠 present_files 的"查看所有产物"链接**，必须确保文字正文中包含文件名的超链，让用户可直接点击预览
3. **展示后**：再调用 present_files 将文件注册到产物区作为备选访问入口
4. **用户指出问题**：说"第X页要改……"或"整体调整……"
5. **口头讨论**，只改确认要改的页
6. **用户说"下一步"、"OK"、"确认"** 后，大纲和内容稿定稿，进入 Step 3

### 产出

`outline.md`（大纲）+ `content.md`（详细内容稿）

---

## Step 3：选模板 · 风格确定（弹窗）

### 交互内容

内容确认后，**必须用 AskUserQuestion 弹窗**向用户提问：

> **问题：** "内容已全部确认。请选择视觉风格："

**选项：**

1. **💎 teld 风**（深蓝渐变）— 默认，深蓝渐变底色 + 网格底纹 + 圆角卡片，匹配公司品牌
2. **🖤 锋芒风**（纯黑高对比）— 纯黑底 + 品牌青边框 + 巨号粗体，技术分享场景
3. **🤎 文质风**（奶油纸暖色）— 奶油纸底 + 衬线字体 + 柔和阴影，培训文档场景
4. **📊 商务风**（白底深字）— 白底深字咨询风格，商业汇报场景

### 执行（teld 科技路线）— 模板克隆优先

> ⚠️ **核心技术原则：模板克隆是唯一可靠的样式统一方案，代码绘制不可控。**

**版式选择（2026-07-16 实战验证）：**

| 用途 | Layout | 说明 |
|:----|:-----:|:----|
| **封面** | `Layout[0]` 标题幻灯片 | 自带 logo + 标题装饰线 + 品牌组 |
| **内容页** | `Layout[6]` 4_标题幻灯片 | 自带 logo + 标题线 + 品牌组，**0 占位符**（无"单击此处"残留）|

**正确做法（2026-07-16 实战验证）：**

1. **模板克隆**：`shutil.copy2(TEMPLATE_PATH, OUTPUT_PATH)` 克隆技能包内置模板 `references/teld-template.pptx`
   ```python
   # 模板路径应指向 skill 内部（不依赖项目根目录的外部文件）
   import os
   SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
   TEMPLATE_PATH = os.path.join(SKILL_DIR, "references/teld-template.pptx")
   ```
2. **删除范例页**：将模板自带的 4 页范例全部删除
3. **封面占位符处理**：必须用 **XML 删除**方式彻底移除占位符节点，不能只 `shape.text=""`：
   ```python
   sldXml = s1._element
   spTree = sldXml.find(qn('p:cSld')).find(qn('p:spTree'))
   to_remove = []
   for sp in spTree.findall('p:sp', {'p':'http://schemas.openxmlformats.org/presentationml/2006/main'}):
       nvSpPr = sp.find('p:nvSpPr', nsmap)
       if nvSpPr is not None:
           nvPr = nvSpPr.find('p:nvPr', nsmap)
           if nvPr is not None and nvPr.find('p:ph', nsmap) is not None:
               to_remove.append(sp)
   for sp in to_remove:
       spTree.remove(sp)
   ```
4. **封面布局**（全 textbox，不用占位符）：
   - **标题**：y=0.4（与内容页统一），22pt Bold 白色左对齐，宽度 8.3in 避开右上 logo
   - **副标题**：y=2.5，28pt Bold 品牌青 #77FCFC 居中
   - **第二行小字**：y=3.2，14pt 灰色居中
   - **装饰线**：5in 宽 2pt 高，居中 y=3.8
   - **日期**：y=4.2，13pt 灰色居中
   - **QR 码**：底部（详见二维码章节）
5. **内容页标题**：使用 `add_header()` 工具函数，所有标题统一在 **y=0.4（标题装饰带内部），22pt Bold**，与封面同位置
6. **内容页智能布局**（以 P2 为间距基准）：
   ```
   标题装饰线结束             y≈0.97
   ↓ 间距 0.18in
   金句/总览（橙色）          y=1.15  
   ↓ 间距 0.55in
   首张表格                   y=1.7
   ```
   后续所有内容页（P3/P4）严格对齐此间距。
   页面底部的留白区域用 **金句收尾**（14pt 金色 #C9A227 居中）。
7. **字体设置**：所有中文字符必须用 `set_chinese_font(run)` 同时设置 `a:latin` + `a:ea` + `a:cs`
8. **Bold 设置**：paragraph 级 + run 级双重设置
9. **表格字号**：Header **12pt Bold**，Row **11pt**，行高 **0.42in**（按行数动态计算）
10. **字号/颜色/坐标规范**：参考 `references/teld-design-spec.md`
11. **其他风格**：参考 `references/styles/README.md`

**`add_header()` 函数参考：**
```python
def add_header(slide, title):
    """内容页标题 — Layout[6] 自带 logo+标题线，只需加文字
       标题位置 y=0.4（标题装饰带内部），与封面统一
    """
    tf = tb_box(slide, 0.6, 0.4, 8.0, 0.5)
    run_text(tf, title, 22, True, WHITE)
```

**`add_qr()` (teld 专用) — 底中优先 → 底右备选：**
```python
def add_qr_teld(slide, img_path):
    """teld 模板专用 QR：底中优先 → 底右备选（永远不右上，右上已有 logo）"""
    positions = [
        (6.12, 5.55, 0.9, 0.9),     # 底中（优先）
        (11.5, 5.6, 0.85, 0.85),    # 底右（备选）
    ]
    pick = positions[0]  # 默认底中
    for pos in positions:
        if not _overlaps(slide, pos[0], pos[1], pos[2], pos[3]):
            pick = pos; break
    qx, qy, qw, qh = pick
    lx = qx; ly = qy + qh + 0.04
    label = "扫码关注「天戈朱」"
    slide.shapes.add_picture(img_path, Inches(qx), Inches(qy), width=Inches(qw), height=Inches(qh))
    tf = tb_box(slide, lx - 0.4, ly, qw + 0.8, 0.2)
    run_text(tf, label, 8, False, LIGHT_GRAY, PP_ALIGN.CENTER)
```

### teld 内容区视觉规则（强制，huashu 哲学 | 2026-07-16 新增，仅 teld 风格生效）

> ⚠️ **以下规则在 teld 风格下必须执行，不可跳过。** "增强"一词已修正为"强制"。

> 借鉴 huashu-design 的"反 slop"原则：**少框、分层、有视觉锚点**。以下规则只在 teld 风格生效，锋芒/文质/商务风忽略。

**1. 去框化原则**
- 一个页面出现 **4+ 个矩形框**会显平淡、像清单 → 改为**纯排印分层**
- 字号层级差 > 2 阶：hero 大字（36pt）→ 标题（18-22pt）→ 主文（13pt）→ 副文（10pt）
- 关键术语/数字用放大 + 品牌色单独成视觉焦点

**2. 装饰线规则**
- 模板自带的标题线保留
- **用户说"线去掉" = 删整条线**，不是去边框（初版误用 connector 替代矩形，线仍在）
- 封面色线变淡：`LINE_MUTED = #66C5DC`，1.5pt（原 #00A7CB 3pt 太粗太亮）
- 需要手绘装饰线时用 **connector**（无 shape 外框问题）：

```python
def add_deco_line(slide, x, y, w, color, width=Pt(2.5)):
    from pptx.enum.shapes import MSO_CONNECTOR
    line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
        Inches(x), Inches(y), Inches(x + w), Inches(y))
    line.line.color.rgb = color; line.line.width = width
    return line

def add_accent_bar_v(slide, x, y, h, color, width=Pt(2.5)):
    from pptx.enum.shapes import MSO_CONNECTOR
    line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
        Inches(x), Inches(y), Inches(x), Inches(y + h))
    line.line.color.rgb = color; line.line.width = width
    return line
```

**3. 子主题 / 小标题（section heading）**
- 页面内"什么是 Skill"这类小节标题：用 **16pt Bold 品牌青 #00A7CB**（不是 11pt label）
- 关键术语（如 "Skill"）单独放大：**20pt Bold 品牌青**，成视觉焦点

**4. 顶部锚点金句（"→" 开头）**
- 位置固定在 **y=1.15**（与 P2/P3 一致），**不要因"居中"需求移动它**
- 用户说"正文居中"指的是**正文块**（不含顶部锚点），不是移动这个金句

**5. 正文区垂直 + 水平居中（内容不足一页时）**
- 顶部锚点保持在 y=1.15 不动
- 内容区可用高度：标题线 y≈0.97 → 页码 y=7.2，共 6.23in
- 把**正文块**（不含顶部锚点）作为整体在剩余空间里计算上下边距并居中
- 三列水平也居中：页面宽 13.332，三列总宽 12.0 → 左起 **0.666**
- 底部金句紧贴正文块下方（间距 0.3in），不再悬空

**6. 大数字当视觉锚点（Top N / 要点页）**
- 三列推荐 / 要点页：每列用 **36pt Bold 品牌青** 大数字 01/02/03（既是内容也是视觉锚点）
- 数字下方：标题 18pt Bold 白 + 标签 10pt 橙 + 描述 13pt 灰 + 12pt 白

**7. 底部金句（收尾）**
- 去掉金色竖线（accent bar），改 **金色 14pt 居中**
- 例：`run_text(tf_g, "做一次，沉淀标准化流程 → 再做一次，直接复用", 13, True, GOLD_HL, PP_ALIGN.CENTER)`

**关键纠偏经验：**
- "线去掉" = 删整条线，不是去边框
- "正文居中" = 移动正文块，不是移动顶部锚点金句
- "去框 > 多框"：一个页面框太多会显平淡

### 执行（锋芒风路线 — 纯黑高对比，2026-07-16 新增）

> ⚠️ **锋芒风无现成模板，从空白 Presentation() 构建**——纯黑底 + teal 点缀 + 巨号粗体。

**正确做法（2026-07-16 实战验证）：**

1. **从空白开始**：`Presentation()`，16:9 画布（不依赖任何模板）
2. **每页设置纯黑背景**：`set_bg_black(slide)`，填充 `#000000`
3. **版式选择**：全部用默认空白版式 `prs.slide_layouts[6]`（即"Blank"空白版式，0 占位符），**不能用 teld 模板的 Layout[6]**，因为那会带入 teld 品牌元素（Logo、装饰线等）
4. **封面布局**（全 textbox）：
   - **主标题**：y=2.0，**40pt Bold** 白色居中（巨号粗体）
   - **副标题**：y=3.4，22pt Bold 品牌青 #00A7CB 居中
   - **装饰线**：teal 3pt 高，居中 y=4.2
   - **说明文字**：y=4.6，14pt 灰色居中
   - **日期**：y=5.0，12pt 浅灰居中
   - **QR 码**：底部 y=5.85（详见二维码章节）
5. **内容页标题**：使用 `add_header()`，**28pt Bold** 白色 + teal 下划线 y=1.05
6. **内容页布局**：
   ```
   标题下划线结束              y≈1.05
   ↓ 间距 0.25in
   引语/锚点（橙色 →）         y=1.3，16pt Bold 橙
   ↓ 间距 0.65in
   正文/表格                   y=1.95~5.0
   ↓ 间距 0.25in
   底部金句（teal 20pt 居中）  y=5.0，height 0.5
   ↓ 间距 0.35in
   QR 码                       y=5.85
   ```
7. **表格规范**：
   - 表头底色：`HEADER_TEAL = #1F2A2E`（贴近黑底，不抢戏）
   - 表头文字：**居中**，白色 11pt Bold
   - 分组行底色：`DARK_CARD = #151515`
   - 普通行底色：`#0A0A0A`
   - 分组名文字：teal #00A7CB Bold
8. **字体设置**：所有中文用 `set_chinese_font(run)`，微软雅黑
9. **Bold 设置**：paragraph 级 + run 级双重设置
10. **QR 码**：P1 + Pn 放，固定底部居中（6.12, 5.85），0.85×0.85 in
11. **底部金句**与 QR 码必须留 **0.3in 以上间隙**，防止重叠

**配色常量：**
```python
BLACK       = RGBColor(0x00, 0x00, 0x00)
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
TEAL        = RGBColor(0x00, 0xA7, 0xCB)   # 装饰线/子主题/大数字
HEADER_TEAL = RGBColor(0x1F, 0x2A, 0x2E)   # 表头底色
DARK_CARD   = RGBColor(0x15, 0x15, 0x15)
MID_LINE    = RGBColor(0x33, 0x33, 0x33)
LIGHT_GRAY  = RGBColor(0xAA, 0xAA, 0xAA)
BODY_GRAY   = RGBColor(0xCC, 0xCC, 0xCC)
ORANGE      = RGBColor(0xF7, 0x96, 0x46)   # 引语
GOLD        = RGBColor(0xC9, 0xA2, 0x27)   # 底部金句
```

**`add_header()` 函数参考：**
```python
def add_header(slide, title):
    """锋芒风标题区：28pt Bold + teal 下划线"""
    tf = tb_box(slide, 0.8, 0.35, 11.5, 0.7)
    run_text(tf, title, 28, True, WHITE)
    add_teal_line(slide, 0.8, 1.05, 3.0)  # 3in teal 下划线
```

**`add_qr_fengmang()` 函数参考：**
```python
def add_qr_fengmang(slide, img_path):
    """锋芒风 QR：底部居中（与内容保留 0.3in 以上间隙）"""
    qx, qy, qw, qh = 6.12, 5.85, 0.85, 0.85
    slide.shapes.add_picture(img_path, Inches(qx), Inches(qy), width=Inches(qw), height=Inches(qh))
    tf = tb_box(slide, qx-0.4, qy+qh+0.04, qw+0.8, 0.2)
    run_text(tf, "扫码关注「天戈朱」", 8, False, LIGHT_GRAY, PP_ALIGN.CENTER)
```

### 执行（文质风路线）

1. 从空白 `Presentation()` 开始，设置 16:9 画布
2. 背景色设为奶油纸色 `#F5F0E8`
3. 所有内容页使用 Layout[6] `4_标题幻灯片`（空白，代码添加文本框）
4. 表格隔行背景用**柔暖色 `#EFEBE2`**，不用纯白（不刺眼）
5. 结尾金句文本框宽度控制在 **10.8 in 以内**（避免与页码重叠）

### 视觉强化规则

**封面（仅一句话时）：**
- 副标题**居中显示**（水平 + 垂直）
- 字号建议 28pt Bold 突出
- 颜色：品牌青 #77FCFC
- 装饰线 5in，居中

**内容页核心结论（"→" 开头行）：**
- 字号加大到 16pt
- 颜色用品牌金 #C9A227 或警示橙 #F79646
- 加粗显示
- 与正文 13pt 浅灰形成视觉对比

**内容页间距基准（teld 风格）：**
```
标题装饰线结束              y≈0.97
↓ 间距 0.18in
金句/总览（橙色 → 开头）    y=1.15  
↓ 间距 0.55in
首张表格                    y=1.7
↓
页面底部金句收尾            14pt 金色居中
```

**teld 内容区视觉规则（强制，huashu 哲学）：** 详见上方"teld 内容区视觉规则"小节——
去框化（4+ 框显平淡）、装饰线变淡 #66C5DC/1.5pt、子主题 16pt Bold teal、关键术语 20pt、顶部锚点固定 y=1.15 不移动、正文区整体居中、大数字 36pt 当视觉锚点、底部金句金色居中。

**页面底部：**
- 留白区域用 **金句收尾**（14pt 品牌金 #C9A227，居中）
- QR 码：仅 P1 + Pn，底中优先 → 底右备选（teld 专用逻辑）

### 无模板时的通用风格

- 画布：16:9
- 背景：深蓝径向渐变（#000C18 → #17375E）
- 标题：白色 36pt Bold，微软雅黑
- 副标题/章节标签：青色 18pt
- 正文：浅灰 14pt
- 强调：品牌青色 #00A7CB

---

## Step 4：生成确认 · 是否生成 PPTX

### 交互内容（弹窗）

所有配置就绪后，**必须用 AskUserQuestion 弹窗**展示最终确认信息并询问用户是否开始生成。禁止只用文字展示。

**弹窗内容：**

| 标题 | 选项 |
|:----|:----|
| **准备生成 PPT，确认以下信息：** | 选项 1：**确认生成**（点击后立即执行） |
| 文件来源：{来源简述} | 选项 2：**暂不生成**（返回修改） |
| 听众：{听众角色} | |
| 总页数：{页数} 页 | |
| 模板：{视觉风格} | |
| 输出格式：.pptx | |

**选项说明：**
- **确认生成** → 执行 PPT 生成操作
- **暂不生成** → 回到 Step 3 或之前的步骤，等待用户进一步调整

**在用户点击"确认生成"之前，禁止执行任何生成操作。**

### 红色规则 4：文字零添加（2026-07-16 新增）

> **PPT 页面上的文字必须严格等于用户提供的原文范围，不得自行补充。**

具体约束：
- ❌ 不得在卡片/列表中添加原文没有的 bullet 条目
- ❌ 不得添加原文没有的收尾金句、总结句
- ❌ 不得对原文进行"展开解释"或"补充说明"
- ✅ 用户原文有多少字，PPT 就只展示多少字
- ✅ 表格/对比表等结构化内容按原文原样搬运

**违反案例（2026-07-16 实战教训）：**
用户提供三段式框架（理解/实操/驾驭各一行文字）→ AI 在卡片中自行添加了"模型如何理解指令""什么场景擅长"等 bullet 条目 → 被用户指出"不要随意发挥"。

### 生成后通知

PPT 生成完成后，**必须向用户提示文件位置**：

1. **正文中输出文件名超链**：在回复正文中用反引号写出文件名（如 `充电站电损管控.pptx`），系统会自动转为可点击的预览链接
2. **调用 present_files** 将生成的 PPTX 文件注册到产物区
3. **输出格式**：

```markdown
✅ PPT 已生成

请点击 `{文件名}.pptx` 预览下载

- 总页数: N 页
- 听众: {听众角色}
- 模板: {视觉风格}

提示：文件在 PowerPoint 中可直接编辑文字。
如需美化排版，可在 PowerPoint 中进一步调整。
```

---

## 公众号二维码 · 通用增强

### 资产

技能包自带 `assets/tgzhu_qrcode.jpg`，**所有生成脚本默认在封面页和结论页放上二维码**。

### 位置规格

| 参数 | 值 |
|:-----|:---|
| 位置 | 底部中间（x=6.12 in） |
| 尺寸 | 1.1 × 1.1 in |
| 垂直位置 | y=5.85 in |
| 下方提示 | "扫码关注「天戈朱」" 9pt 灰字居中 |

### 替换为用户自己的二维码

```bash
# 替换 assets/tgzhu_qrcode.jpg 为你自己的公众号二维码
# 建议：PNG 透明底、正方形、≥338×338 像素
cp my_qrcode.jpg C:/Users/tgzhu/.workbuddy/skills/tgzhu-content-2pptx/assets/tgzhu_qrcode.jpg
```

### 二维码智能避让（2026-07-16 新增 | 2026-07-16 v2 更新）

> ⚠️ `add_qr()` **必须在页面所有内容绘制完成后再调用**，否则检测不到冲突位置。

**通用 QR 函数（适用于文质风/锋芒风/商务风）：**
```python
def _overlaps(slide, x, y, w, h):
    """AABB 碰撞检测，margin=0.1 in"""
    margin = 0.1
    for shp in slide.shapes:
        try:
            sx = shp.left / 914400; sy = shp.top / 914400
            sw = shp.width / 914400; sh = shp.height / 914400
            if sw < 0.01 or sh < 0.01: continue
            if (sx - margin < x + w and sx + sw + margin > x and
                sy - margin < y + h and sy + sh + margin > y):
                return True
        except: continue
    return False

### QR 函数选择（按风格强制，2026-07-16 修正）

> ⚠️ **不同风格必须使用对应的 QR 函数，不得混用。** 删除易混淆的通用版本，每种风格只暴露一个函数。

| 风格 | 函数 | 规则 |
|:-----|:-----|:-----|
| **teld 风** | `add_qr_teld()` | **底中(6.12,5.55)→底右(11.5,5.6)**，永远不进右上（右上已有 logo） |
| **锋芒风** | `add_qr_fengmang()` | 固定底部居中 (6.12, 5.85) |
| **文质风/商务风** | `add_qr_wenzhi()` | 底中→底右→右上智能避让 |

**teld 风专用 QR 函数（底中优先 → 底右备选）：**
teld 模板右上已有 logo + 品牌组，**QR 码永远不进入右上区域**。
```python
def add_qr_teld(slide, img_path):
    """teld 专用：底中优先 → 底右备选"""
    positions = [
        (6.12, 5.55, 0.9, 0.9),     # 底中（优先）
        (11.5, 5.6, 0.85, 0.85),    # 底右（备选）
    ]
    pick = positions[0]
    for pos in positions:
        if not _overlaps(slide, pos[0], pos[1], pos[2], pos[3]):
            pick = pos; break
    qx, qy, qw, qh = pick
    slide.shapes.add_picture(img_path, Inches(qx), Inches(qy), width=Inches(qw), height=Inches(qh))
    tf = tb_box(slide, qx-0.4, qy+qh+0.04, qw+0.8, 0.2)
    run_text(tf, "扫码关注「天戈朱」", 8, False, LIGHT_GRAY, PP_ALIGN.CENTER)
```

**锋芒风专用 QR 函数（固定底部居中，保留 0.3in 间隙）：**
锋芒风无模板 logo，QR 固定底部居中。
```python
def add_qr_fengmang(slide, img_path):
    """锋芒风专用：底部居中，y=5.85（与金句保留 0.3in 间隙）"""
    qx, qy, qw, qh = 6.12, 5.85, 0.85, 0.85
    slide.shapes.add_picture(img_path, Inches(qx), Inches(qy), width=Inches(qw), height=Inches(qh))
    tf = tb_box(slide, qx-0.4, qy+qh+0.04, qw+0.8, 0.2)
    run_text(tf, "扫码关注「天戈朱」", 8, False, LIGHT_GRAY, PP_ALIGN.CENTER)
```

### 二维码只放第一页和最后一页

按用户要求（2026-07-16 确认）：**仅 P1（封面）和 Pn（结论页）** 放二维码，其他页面不加。

### 跳过二维码（不想用时）

在 `gen-*.py` 脚本顶部注释掉 `QR_PATH` 那行，或将 `qr_bottom()` 调用注释掉。

---

## 依赖与安装

### 内置依赖（解压即用）
此技能包自带以下资源，无需额外安装：
- `references/teld-template.pptx` — **teld 风格模板**（含 Logo+渐变+品牌线），模板克隆必须使用此路径
- Mck PPT Design Engine（67 种布局、三层防损）
- teld 锋芒风 / 文质风 HTML 模板
- teld 品牌规范、示例内容

### 外部依赖（需单独安装）

| 依赖 | 安装命令 | 用途 |
|:----|:--------|:----|
| **Huashu Design** | `npx skills add alchaincyf/huashu-design` | 设计方向顾问、HTML 风格生成 |
| **Python** | `pip install python-pptx lxml` | PPTX 生成引擎 |
| **Node.js** | 需 ≥22.x | Huashu 的 html2pptx.js 转换 |

> 换电脑时，把 `tgzhu-content-2pptx/` 解压到 `~/.workbuddy/skills/`，再按上表单独安装 Huashu 即可。

## 参考文件

### references/
此技能包含以下参考文件，需要时加载：

- `examples/ai-agent-engineering-share.yaml` — **结构参考**（非内容源），展示一套完整的大纲结构示例
- `examples/outline.md` + `examples/content.md` — **模板文件（只读）**，完整版13页大纲与内容稿
- `references/teld-design-spec.md` — teld 模板设计规格（品牌色/字体/版式/坐标/字号）

### 视觉风格（4 套内置）

| 风格 | 文件 | 场景 |
|:----|:----|:----|
| 💎 **teld 风**（深蓝渐变）| `references/styles/` + `slide-deck/test-hybrid/` | 默认，公司正式汇报 |
| 🖤 **锋芒风**（纯黑高对比）| `references/styles/teld-fengmang.html` | 技术分享、产品发布 |
| 🤎 **文质风**（奶油纸暖色）| `references/styles/teld-wenzhi.html` | 内部培训、文档指南 |
| 📊 **商务风**（白底深字）| `references/mck-ppt/` (MckEngine 67 种布局) | 商业汇报、战略提案 |

详细风格说明见 `references/styles/README.md`。

---

## 关键教训（实战沉淀）

### 文件采集
- IMA MCP 的 `get_knowledge_base_list` 需传 `type=KBT_MINE_KB` 参数
- 文件内容通过 `fetch_media_content` 获取，只传 `media_id`

### 内容交互
- **先口头讨论，不动文件**，确认后才写入
- 逐页确认，防止后期推翻整篇重来

### PPT 生成
- `run.font.name` 只设 latin，中文走主题默认宋体 → 必须用 `set_chinese_font()` 同时设 `a:latin` + `a:ea` + `a:cs`
- Bold 需同时设 paragraph 级 + run 级
- 模板克隆是唯一可靠的样式统一方案，代码绘制不可控
- **封面占位符必须 XML 删除**（`spTree.remove(sp)`），`shape.text=""` 和 `tf.clear()` 无法彻底清除
- **内容页必须用 Layout[6]（4_标题幻灯片）**，自带 logo+标题线，Layout[4]（空白）无品牌元素
- **所有页标题统一 y=0.4，22pt Bold**，封面与内容页一致
- **标题线→金句间距 0.18in，金句→表格 0.55in**，全篇对齐 P2 基准
- **teld QR 规则**：底中优先→底右备选，永远不进入右上区域（右上已有 logo）
- **表格字号**：Header 12pt Bold，Row 11pt，行高 0.42in
- **teld 视觉增强（仅 teld 风格）**：去框化（4+ 矩形框显平淡→纯排印分层）；装饰线变淡 #66C5DC/1.5pt；子主题 16pt Bold teal；关键术语 20pt teal；顶部锚点金句固定 y=1.15 不因"居中"移动；正文块整体上下左右居中；大数字 36pt teal 当视觉锚点；底部金句金色居中无竖线
- **teld 常见误读**：用户说"线去掉"=删整条线（不是去边框）；"正文居中"=移动正文块（不是移动顶部锚点金句）

### 锋芒风
- **锋芒风无现成模板**，从空白 Presentation() 构建，每页手动 set_bg_black(slide)
- **版式**：统一用 `prs.slide_layouts[6]`（空白版式"Blank"），封面也用它。**不可用 teld 模板的 Layout[6]**，否则带入品牌元素
- **标题**：28pt Bold 白色 + teal 下划线（不是 teld 的 22pt）
- **封面主标题**：40pt Bold 白色居中
- **表格表头**：底色 #1F2A2E（贴近黑底），文字居中，分组行 #151515，普通行 #0A0A0A
- **配色层级**：teal #00A7CB 只做装饰线/子主题/大数字，不要大面填充
- **QR 码**：固定底部居中 (6.12, 5.85)，0.85x0.85 in，与底部金句保留 0.3in 以上间隙
- **锋芒风常见误读**：纯黑底上表头应"轻于正文重于背景"，#1F2A2E 是安全选择
