# 特来电 PPT 模板 · 设计规格（嵌入式参考）

> 合并自 `biz-ppt-template-skill`，供 `ima-to-ppt` 自闭环使用。

## 品牌色

```text
品牌青：#00A6CB
品牌线青：#00A7CB
主题强调青：#00AFD2
深蓝强调：#007DA4
浅青：#76D1E0
标题候选青：#77FCFC
白色：#FFFFFF
警示橙：#F79646
```

## 字体

- 中文/标题/标语：微软雅黑
- 英文/数字：微软雅黑 或 Calibri
- Bold 需同时设置 paragraph 级 + run 级

## 中文字体修复（关键！）

```python
from lxml import etree
from pptx.oxml.ns import qn

def set_chinese_font(run, font_name="微软雅黑"):
    rPr = run._r.get_or_add_rPr()
    for tag in ['a:latin', 'a:ea', 'a:cs']:
        el = rPr.find(qn(tag))
        if el is None:
            el = etree.SubElement(rPr, qn(tag))
        el.set('typeface', font_name)
```

## 版式映射

| 用途 | Master | Layout | 操作方式 |
|:----|:-----:|:------:|:--------|
| 封面页 | Master[0] | Layout[0] `标题幻灯片` | 替换占位符文字 |
| 内容页 | Master[0] | Layout[6] `4_标题幻灯片` | 代码添加文本框 |
| 空白页 | Master[0] | Layout[4] `空白` | 特殊用途 |

## 标题层级

| 层级 | 用途 | 字号 | 颜色 |
|:---:|------|:---:|:----:|
| H1 | 主标题 | **29.65pt** Bold | #FFFFFF |
| H2 | 封面副标题 | **18pt**（段落词Bold） | 77FCFC |
| H3 | 章节副标题 | **14.8pt** Bold | 77FCFC |
| H4 | 段落标签 | **16pt** Bold | 00A7CB |
| Body | 正文 | **14pt** | E5E5E5 |
| Body-Small | 引出问题/脚注 | **13.5pt** Italic | F79646 |

## 品牌区坐标（1600x900 基准）

- 顶部横线+插头：x=58.3, y=74.8
- Logo：x=1090.0, y=37.3, 228×117px
- 标语"充电 领域"：x=1253.1, y=60.5, 12.7pt, #00A6CB
- 闪电图标：x=1313.3, y=66.4, 31×31px

## 间距

- 主标题 y=0.30in | 副标题 y=1.11in | 内容区 y=1.70in
- 所有文字框 margin 清零
- 段落间距：同类型 Pt(6)，不同类型 Pt(10)
