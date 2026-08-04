# tgzhu-content-2pptx

> 从文章/链接/知识库中筛选资料，基于内容与听众角色，交互确认后生成 PPT 的技能包。
> 内置 **4 套视觉风格**（企业风 / 锋芒风 / 文质风 / 商务风），统一版式原语，换风格零成本。

---

## 一、目录结构

```
tgzhu-content-2pptx/
├── README.md                  # 本文件：目录说明 + 四风格对称度总览
├── SKILL.md                   # 工作流入口（采集→大纲→风格→生成→微调）
│
├── assets/
│   └── qrcode.jpg             # 二维码（封面/结论页自动放置）
│
├── engines/                   # ★ 生成引擎层（四风格 + 共享基件，固化）
│   ├── common.py              # 共享：品牌色/间距规则/tb_box/run_text/set_chinese_font/qr/页码
│   ├── enterprise.py          # 企业风：克隆 templates/enterprise.pptx + 版式原语
│   ├── fengmang.py            # 锋芒风：纯黑高对比，代码绘制
│   ├── wenzhi.py              # 文质风：奶油纸暖色，代码绘制
│   └── business.py            # 商务风：McKinsey 咨询布局（白底深字+浅灰卡底+品牌青竖线+金高亮），空白画布代码绘制，不依赖模板
│
├── templates/
│   └── enterprise.pptx        # 企业风母版（烧录 Logo+标题线+深蓝渐变）；仅供企业风克隆
│
├── styles/                    # 风格设计参考稿（HTML，给人看，运行时不加载）
│   ├── README.md              # 4 风格总说明
│   ├── fengmang.html          # 锋芒风视觉稿
│   └── wenzhi.html            # 文质风视觉稿
│
└── specs/                     # 风格设计规格（Markdown，引擎的事实来源）
    ├── enterprise.md          # 企业风规格（品牌色/字体/版式/坐标/字号）
    └── business.md            # 商务风规格（MckEngine 布局/配色/层级）
```

---

## 二、四风格「资源对称度」对比

四种风格在 **模板 / 设计稿 / 规格文档 / 引擎** 四个维度上的配套情况：

| 风格 | 模板 / 母版 | 设计稿 (HTML) | 规格文档 (md) | 引擎 | 风格定义位置 | 视觉特征 |
|:----:|:----------:|:------------:|:------------:|:----:|:-----------:|---------|
| 💎 企业风 | ✅ `templates/enterprise.pptx` | — | ✅ `specs/enterprise.md` | `enterprise.py` | 模板 + 规格文档 | 深蓝渐变 + 品牌青 + Logo 标题线 |
| 🖤 锋芒风 | — | ✅ `styles/fengmang.html` | — | `fengmang.py` | 代码 + HTML 稿 | 纯黑高对比 + 巨号粗体 + 青边框 |
| 🤎 文质风 | — | ✅ `styles/wenzhi.html` | — | `wenzhi.py` | 代码 + HTML 稿 | 奶油纸暖色 + 宋体标题 + 柔阴影 |
| 📊 商务风 | — | — | ✅ `specs/business-constraints.md` | `business.py` | 代码 + 规格文档 | 白底深字 + 浅灰卡底 + 品牌青竖线 + 金高亮行 |

**对称规律（便于理解）**
- **模板类**：企业风靠「母版 pptx」克隆，品牌视觉烧录在背景图里 → 改视觉要改 `templates/`。
- **设计稿类**：锋芒/文质靠「HTML 参考稿」定义视觉，运行时由引擎代码绘制 → 改视觉看 `styles/*.html` + 改 `engines/*.py`。
- **规格文档类**：企业/商务的配色、字号、坐标都抽成了 `specs/*.md`，其他引擎读它对齐。
- **引擎类**：四种风格全部在 `engines/` 下，暴露**同一组版式原语**，互不依赖。

> 历史注记：商务风早期只有 `business.py` 一个纯代码引擎、无独立规格文档，是四风格中唯一「既无模板、也无 HTML 稿」的；`specs/business.md` 已补齐，目录层面现已完全对称。

---

## 三、各目录职责

| 目录 | 职责 | 谁改它 |
|:----|:----|:----|
| `engines/` | 真正的「生成器」，把内容映射成 pptx 形状 | 调风格/版式时改 |
| `templates/` | 企业风克隆基底（含品牌背景图） | 换企业风母版时改 |
| `styles/` | 锋芒/文质的可视化设计稿（HTML），**不参与运行** | 定视觉方向时看 |
| `specs/` | 引擎的权威规格（配色/字号/坐标），改引擎先对齐这里 | 调参数时查 |
| `assets/` | 二维码等共享素材 | 换二维码时改 |

---

## 四、统一版式原语

四个引擎暴露同一组原语，调用时只把抓取的内容填进对应原语：

```
cover / section_header / timeline / two_column / card_grid / summary / bottom_gold
```

换风格无需重写映射逻辑，只需切换 `import` 的引擎模块：

```python
sys.path.insert(0, "<skill>/engines")
import fengmang as eng   # 换成 enterprise / wenzhi / business 即换风格
prs = eng.blank_deck()
s = eng.add_blank(prs); eng.cover(s, "标题", "副标题", tags=[...])
# ... section_header / card_grid / two_column / timeline / bottom_gold
```

---

## 五、快速开始（以 FDE 文章为例）

```bash
# 生成 6 页「跨部门分享」PPT，切换风格改最后一个参数
python gen_fde_styles.py fengmang     # 锋芒风
python gen_fde_styles.py enterprise    # 企业风
python gen_fde_styles.py wenzhi        # 文质风
python gen_fde_styles.py business        # 商务风（空白画布，白底深字，不依赖模板）
```

> 详细工作流、间距规则、交互确认步骤见 `SKILL.md`。

---

## 六、依赖与安装

生成需要 Python 运行时与以下包：

| 依赖 | 用途 | 版本要求 |
|:----|:----|:--------|
| `python-pptx` | 读写 `.pptx`、绘制形状与文本 | ≥ 0.6.23 |
| `lxml` | python-pptx 的底层 XML 依赖 | — |

**agent 的缺依赖处理**：运行时若探测到上述包缺失，会**提示用户是否安装**，按用户确认执行——
- 用户确认安装：装入隔离环境后重试生成；
- 用户拒绝：停止并说明所需依赖，不静默跳过、不直接抛错。

**手动安装**（如需自行准备环境）：

```bash
pip install python-pptx lxml
```

> 技能包自带的模板、二维码、四引擎无需额外安装，开箱即用。

---

## 七、参考文件索引

- `README.md` — 本文件：目录结构、四风格对称度、依赖与索引总览
- `SKILL.md` — 工作流与生成约束（采集 → 大纲 → 风格 → 生成 → 微调）
- `specs/enterprise.md` — 企业风设计规格
- `specs/business.md` — 商务风（McKinsey 咨询）设计规格
- `styles/fengmang.html` / `styles/wenzhi.html` — 锋芒风 / 文质风设计稿
- `engines/common.py` — 四风格共享基件（颜色 / 间距 / 文本工具 / 二维码 / 页码）
- `engines/{enterprise,fengmang,wenzhi,business}.py` — 四风格生成引擎（统一版式原语）
- `references/runner-example-enterprise.py` / `references/runner-example-fengmang.py` / `references/runner-example-wenzhi.py` — **per-article runner 范式参考样例**（企业风 / 锋芒风 / 文质风，内容一致；展示如何把内容映射到版式原语、各引擎 API 差异如何适配；文质风示范 `(prs, ...)` 整本构建范式：common.blank_deck 建画布 → 富原语/低级原语 → prs.save）
- `templates/enterprise.pptx` — 企业风克隆模板（商务风不依赖模板）
- `assets/qrcode.jpg` — 二维码
