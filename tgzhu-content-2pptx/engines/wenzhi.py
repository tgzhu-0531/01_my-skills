# -*- coding: utf-8 -*-
"""
wenzhi.py — 文质风引擎（奶油纸暖色 / Warm Editorial）
奶油纸底 #F7F4EE + 品牌青 #00A5C8 + 暖金 #C99322 + 宋体标题 + 柔和阴影卡片。
暴露统一版式原语：cover / section_header / timeline / two_column / card_grid / summary / bottom_gold
"""
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree
from common import (WHITE, SP_UNIT, SP_GROUP, SP_CARD_BODY, SP_RUN_DEF,
                    tb_box, run_text, rect, add_qr, add_page_number, set_chinese_font,
                    cover_qr, bottom_gold as _gold, cover_line, fit_cover_title,
                    fmt_date_5digit, rounded_card, loop_arrow, loop_return_u,
                    measure_text_width, add_blank, content_card, card_divider,
                    shape_bottom_in, GOLD_LINE_Y, GOLD_TEXT_Y,
                    fit_content_font, fit_single_line, solve_card_fonts, fit_gaps,
                    vcenter, CANVAS_TOP, CANVAS_BOT,
                    layout_loop_page, layout_timeline, layout_card_grid, layout_compare,
                    layout_value_grid, layout_profile_warning, layout_six_step,
                    layout_talent_strip, layout_transition_rows, layout_hero_questions,
                    layout_two_column, layout_summary)

import math
import re

WEN_BG   = RGBColor(0xF7, 0xF4, 0xEE)   # 米白背景（ChatGPT：更柔和暖白）
WEN_DEEP = RGBColor(0x30, 0x48, 0x5B)   # 深蓝灰（卡片标题主焦点 / 页底结论正文）
WEN_CARD = RGBColor(0xFB, 0xF8, 0xF2)   # 暖白卡底（贴近背景，去 UI 白卡感）
WEN_TEAL = RGBColor(0x00, 0xA5, 0xC8)   # 主青（结构：章节标签/编号/卡结论/时间轴点/分隔线）
WEN_GOLD = RGBColor(0xC9, 0x93, 0x22)   # 暖金（页面结论/关键词，唯一点睛色，替代原赤陶橙）
WEN_AMBER= RGBColor(0xC0, 0x8A, 0x2D)   # 琥珀金（金额/投入，第三级强调，不与青/陶土撞）
WEN_INK  = RGBColor(0x19, 0x19, 0x19)   # 近黑标题
WEN_BODY = RGBColor(0x4D, 0x50, 0x54)   # 正文灰（ChatGPT 调色板）
WEN_MUTE = RGBColor(0x77, 0x7A, 0x7E)   # 辅助灰（ChatGPT 调色板）
WEN_LINE = RGBColor(0xE8, 0xE2, 0xD4)   # 分隔线
WEN_CARD_LINE = RGBColor(0xDD, 0xD8, 0xCE)  # 内容卡极淡边框（0.75pt 感，去 UI 感）
WEN_RULE = RGBColor(0xD0, 0xC8, 0xB8)  # hero 下划线淡暖灰（退到背景层）
WEN_FAINT= RGBColor(0xF0, 0xEB, 0xE0)  # 卡内极浅分隔线（松散内容的"底线"）
WEN_TAUPE= RGBColor(0xB0, 0xA6, 0x92)  # 连接线 / 箭头（浅底 → 深色，颜色退线宽进）
WEN_SOFT = RGBColor(0xEF, 0xEB, 0xE2)  # 次级卡底（旧态 / 降温）
WEN_DIM  = RGBColor(0x8A, 0x8A, 0x8A)  # 降温文字（否定项）
WEN_SEP  = RGBColor(0xD8, 0xD2, 0xC4)  # 段落间浅色微分隔线（浅色几何锚定，介于 FAINT 与 LINE 之间）

# 浅底箭头线宽（2026-07-31 用户拍板：以企业风深底 2pt 为参考，文质浅底调细）
WEN_ARROW_W = Pt(1.5)

# ═══════════════════════════════════════════
# 文质风皮肤（布局骨架的视觉参数，2026-07-31 架构：布局在 common.layout_*，皮肤在本层）
# ═══════════════════════════════════════════
WENZHI_SKIN = {
    "bg": WEN_BG,
    "fonts": {"head": "宋体", "body": "微软雅黑", "mute": WEN_MUTE},
    "cap":  {"size": 14, "bold": True, "color": WEN_TEAL},
    "node": {"size": 16, "bold": True, "color": WEN_TEAL, "sub_size": 12, "sub_color": WEN_MUTE},
    "card": {"title_size": 16, "title_color": WEN_DEEP, "sub_size": 12, "sub_color": WEN_MUTE,
             "body_size": 12, "body_color": WEN_BODY, "concl_color": WEN_TEAL,
             "num_color": WEN_TEAL,
             "line": WEN_CARD_LINE, "line_w": 0.75,
             "shadow_alpha": 6000, "shadow_blur": 110000, "shadow_dist": 23000},
    "arrow": {"color": WEN_TAUPE, "w": WEN_ARROW_W},   # 浅底 → 深色细线
    "timeline": {"axis": WEN_LINE, "dot": WEN_TEAL, "date_size": 13, "date_color": WEN_TEAL,
                 "event_size": 14, "event_color": WEN_BODY, "arrow": False},
    # 定义对比（左 hero 墨色 + 右透明青边卡；neg_badge=text 文本✕）
    "compare": {
        "hero_size": 48, "hero_color": WEN_INK,
        "en_size": 18, "en_color": WEN_TEAL, "en_italic": False,
        "cn_size": 20, "cn_color": WEN_INK,
        "bullet_size": 14, "bullet_color": WEN_BODY, "bullet_mark": "bar", "mark_color": WEN_TEAL,
        "summary_size": 14, "summary_color": WEN_TEAL,
        "header_size": 18, "header_color": WEN_TEAL,
        "neg_badge": "text", "neg_kw_size": 12, "neg_kw_color": WEN_DIM,
        "neg_desc_size": 12, "neg_desc_color": WEN_DIM,
        "neg_badge_bg": None, "neg_badge_color": None,
        "pos_bg": None, "pos_border": WEN_CARD_LINE,
        "pos_kw_size": 20, "pos_kw_color": WEN_TEAL,
        "pos_desc_size": 14, "pos_desc_color": WEN_TEAL,
        "div": WEN_LINE, "right_card": True, "inner_div": WEN_LINE,
    },
    # 价值网格（value_grid 求解器版：正文≥12 智能算、间距区间弹性、D1/D2+方块、无箭头）
    "value_grid": {
        "num_size": 20, "num_color": WEN_TEAL, "title_size": 18, "title_color": WEN_TEAL,
        "body_size": 12, "body_color": WEN_BODY, "tag_size": 14, "tag_color": WEN_TEAL,
        "tag_align": "center", "div": WEN_LINE, "d1": True, "mark": True,
        "gap_h": 0.33, "gap_v": 0.16, "solve": True,
        "sp_range": dict(top=(0.08, 0.12), band_to_d1=(0.12, 0.16), d1_to_body=(0.12, 0.16),
                         para=(0.10, 0.14), body_to_d2=(0.12, 0.16), d2_to_concl=(0.10, 0.14),
                         concl_to_bot=(0.06, 0.10)),
        "domains": dict(body=(12, 16), title=(14, 18), num=(16, 20), concl=(11, 14)),
        "line": WEN_CARD_LINE, "line_w": 1.25,
    },
    # 画像（暖白卡 + 青标题线 + 暖金结论）
    "profile": {
        "card_bg": WEN_CARD, "title_size": 18, "title_color": WEN_TEAL, "title_line": WEN_TEAL,
        "role_size": 12, "role_color": WEN_BODY, "dot": WEN_TEAL, "col_threshold": 8,
        "warn_kw_size": 18, "warn_kw_color": WEN_TEAL,
        "warn_desc_size": 12, "warn_desc_color": WEN_BODY, "mark": WEN_TEAL,
        "faint_div": WEN_FAINT, "strong_div": WEN_LINE,
        "concl_bar": WEN_GOLD, "concl_size": 14, "concl_color": WEN_GOLD,
    },
    # 转型对照（transition_rows：旧态浅底降温 / 新态青边高亮）
    "transition": {
        "from_bg": WEN_SOFT, "from_color": WEN_DIM,
        "to_color": WEN_TEAL, "line": WEN_CARD_LINE,
    },
    "tail_bar": WEN_TAUPE,
    "line_spacing": 1.2,
}

# 内容区基准（视觉修正后顶边 1.88；底部金句线在 6.35）
X0, CW_FULL = 0.80, 11.73            # 内容区 0.80 → 12.53
Y_TOP, Y_BOT = 1.88, 6.20
XR = X0 + CW_FULL                    # 12.53

HEAD_FONT = "宋体"
BODY_FONT = "微软雅黑"
PAGE_W = 13.333

# ═══════════════════════════════════════════
# 文质风角色排版规格（封面+时间轴视觉经验沉淀）
# 把"主标题 / 副标题 / 金句"等角色的字号·加粗·字体·颜色从函数内硬编码
# 收口为声明式规格，函数统一走 _role() 引用，渲染结果保持不变。
#   · 主标题：一律 INK 近黑 + 宋体；青只留给结构线与内页核心观点，不抢主标题
#   · 副标题：分两型——封面说明语=MUTE 灰退后；内页核心观点=TEAL 青+bold
#   · 金句：一律 TERRA 赤陶 + bold，整页唯一暖色点睛（与三级强调"陶土=结论"对齐）
# ═══════════════════════════════════════════
WEN_TYPOGRAPHY = {
    "hero":       (52, True,  HEAD_FONT),   # 封面主标题
    "h1":         (36, True,  HEAD_FONT),   # 内页主标题（36pt 减压）
    "sub_cover":  (22, False, BODY_FONT),   # 封面副标/说明语
    "sub_label":  (16, True,  BODY_FONT),   # 内页核心观点（结构强调）
    "sub_lead":   (16, False, BODY_FONT),   # 内页副标-说明（同行灰）
    "gold":       (16, True,  BODY_FONT),   # 金句/结论（暖金 WEN_GOLD 粗体，四风格统一 16pt）
    "date":       (13, True,  BODY_FONT),   # 时间轴日期
    "title_card": (20, True,  BODY_FONT),  # 卡片标题（黑体，消宋体感）
    "body":       (14, False, BODY_FONT),   # 正文
    "tag":        (14, False, BODY_FONT),   # 封面标签组
}
WEN_PALETTE = {
    "hero":       WEN_INK,
    "h1":         WEN_INK,
    "sub_cover":  WEN_MUTE,
    "sub_label":  WEN_TEAL,
    "sub_lead":   WEN_MUTE,
    "gold":       WEN_GOLD,
    "date":       WEN_TEAL,
    "title_card": WEN_DEEP,
    "body":       WEN_BODY,
    "tag":        WEN_MUTE,
}

def _role(tf, role, text, align=PP_ALIGN.LEFT, space_after=SP_RUN_DEF, first=False):
    """按文质风角色规格渲染一段文本：字号/加粗/字体取自 WEN_TYPOGRAPHY，
    颜色取自 WEN_PALETTE；自动套中文（衬线/雅黑）字体修复。"""
    size, bold, font = WEN_TYPOGRAPHY[role]
    color = WEN_PALETTE[role]
    p = run_text(tf, text, size, bold, color, align, space_after, first)
    for r in p.runs:
        r.font.name = font
        set_chinese_font(r, font)
    return p

def _head(tf, text, size, bold, color, align=PP_ALIGN.LEFT, space_after=Pt(0), first=True):
    """标题用宋体（衬线出版感）。
    ⚠️ first 默认 True：文本框首段必须复用 paragraphs[0]，否则会多出一个
    空段落把文字整体下顶（原实现漏传，导致所有标题偏低）。"""
    p = run_text(tf, text, size, bold, color, align, space_after, first)
    r = p.runs[-1]
    r.font.name = HEAD_FONT
    set_chinese_font(r, HEAD_FONT)
    return p

def _h1_render(tf, h1):
    """内页主标题（宋体衬线）：若以英文缩写开头，缩写以小一号(92%)独立 run 渲染，
    收窄中英文间距（ChatGPT 建议）；其余整段宋体。颜色取 WEN_PALETTE['h1']。"""
    color = WEN_PALETTE["h1"]
    size = WEN_TYPOGRAPHY["h1"][0]
    p = tf.paragraphs[0]
    m = re.match(r'^([A-Za-z][A-Za-z0-9.]*)[ \u00a0]+(.*)$', h1)
    if m:
        r1 = p.add_run(); r1.text = m.group(1)
        r1.font.size = Pt(int(round(size * 0.92))); r1.font.bold = True
        r1.font.name = HEAD_FONT; r1.font.color.rgb = color; set_chinese_font(r1, HEAD_FONT)
        r2 = p.add_run(); r2.text = " " + m.group(2)
        r2.font.size = Pt(size); r2.font.bold = True
        r2.font.name = HEAD_FONT; r2.font.color.rgb = color; set_chinese_font(r2, HEAD_FONT)
    else:
        _role(tf, "h1", h1, PP_ALIGN.LEFT, Pt(0), first=True)

def _center_x(w):
    return (PAGE_W - w) / 2.0

def _accent_box(slide):
    """右上角极淡青色竖条（品牌暗示）。"""
    rect(slide, 11.0, 0, 2.333, 7.5, fill=WEN_TEAL, line=None)
    # 用低透明度近似 rgba(0,167,203,0.04)
    srgb = slide.shapes[-1].fill.fore_color._xFill.find(qn('a:srgbClr'))
    if srgb is not None:
        a = etree.SubElement(srgb, qn('a:alpha'))
        a.set('val', '400')  # ~0.04

def _shadow_card(slide, x, y, w, h):
    """白底卡片 + 极淡边线 + 柔和阴影（floating card）。"""
    return rounded_card(slide, x, y, w, h, WEN_CARD, adj=0.04, line=WEN_CARD_LINE, line_w=1.0)

# ═══════════════════════════════════════════
# 版式原语
# ═══════════════════════════════════════════
def cover(slide, title, subtitle, tags=None, total=1, n=1):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = WEN_BG
    _accent_box(slide)
    # 主标题（宋体衬线 hero）：字号智能算，占屏≤72%；框高紧贴字高(修 v2 框矮 bug)
    title_pt = fit_cover_title(title, 52, min_pt=28)
    title_tf = cover_line(slide, 0.8, 1.55, 11.73, title, title_pt,
                          WEN_PALETTE["hero"], True, PP_ALIGN.CENTER, font=HEAD_FONT)
    accent_y = shape_bottom_in(title_tf) + 0.18
    rect(slide, _center_x(1.0), accent_y, 1.0, 0.04, fill=WEN_TEAL, line=None)
    sub_tf = cover_line(slide, 0.8, accent_y + 0.04 + 0.20, 11.73, subtitle, 22,
                        WEN_PALETTE["sub_cover"], False, PP_ALIGN.CENTER)
    if tags:
        cover_line(slide, 0.8, shape_bottom_in(sub_tf) + 0.16, 11.73,
                   " · ".join(tags), 14, WEN_PALETTE["tag"], False, PP_ALIGN.CENTER)
    cover_qr(slide, "wenzhi")
    add_page_number(slide, n, total, WEN_MUTE)

def section_header(slide, h1, label, sub, n=None, total=None):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = WEN_BG
    _accent_box(slide)
    h1sz = WEN_TYPOGRAPHY["h1"][0]
    lh1 = h1sz * 1.2 / 72.0
    # 实测标题行数（长标题会折行），按真实文字底定位青线，避免写死坐标导致贴标题/压标题
    rows1 = max(1, math.ceil(measure_text_width(h1, h1sz) * 1.03 / 11.73))
    tf = tb_box(slide, 0.8, 0.45, 11.73, rows1 * lh1 + 0.05)
    _h1_render(tf, h1)
    title_bottom = 0.45 + rows1 * lh1
    line_y = title_bottom + 0.12
    rect(slide, 0.8, line_y, 0.9, 0.05, fill=WEN_TEAL, line=None)
    label_y = line_y + 0.10
    # label + sub 同行内联于 label_y（距青线底 0.10，不再贴线/焊死）
    if label:
        tf = tb_box(slide, 0.8, label_y, 11.73, 0.34)
        p = _role(tf, "sub_label", label, PP_ALIGN.LEFT, Pt(0), first=True)
        base_p = p
    else:
        base_p = None
    if sub:
        if base_p is not None:
            r = base_p.add_run()
        else:
            tf = tb_box(slide, 0.8, label_y, 11.73, 0.34)
            r = tf.paragraphs[0].add_run()
        r.text = " " + sub
        r.font.size = Pt(WEN_TYPOGRAPHY["sub_lead"][0]); r.font.bold = WEN_TYPOGRAPHY["sub_lead"][1]
        r.font.name = BODY_FONT; r.font.color.rgb = WEN_PALETTE["sub_lead"]
        set_chinese_font(r, BODY_FONT)
    if n and total:
        add_page_number(slide, n, total, WEN_MUTE)

def _run_emph(tf, text, size, kw_teal, kw_amber, base_color):
    """正文内核心词三级强调（视觉修正④）：
       - 青 #00A7CB = 主体（公司/产品）
       - 琥珀金 #C08A2D = 金额/投入
       - 每词本段仅高亮首次出现（落实"整页一公司只强调一次"）
    其余保持正文色。"""
    import re
    all_kw = list(kw_teal) + list(kw_amber)
    all_kw.sort(key=len, reverse=True)        # 长词优先，避免子串提前截断
    pat = re.compile("(" + "|".join(re.escape(k) for k in all_kw) + ")")
    parts = pat.split(text)
    p = tf.paragraphs[0]
    seen = set()
    for part in parts:
        if not part:
            continue
        r = p.add_run()
        r.text = part
        r.font.size = Pt(size)
        r.font.name = BODY_FONT
        r.font.bold = False
        r.font.color.rgb = base_color
        if part not in seen:
            if part in kw_teal:
                r.font.bold = True; r.font.color.rgb = WEN_TEAL
            elif part in kw_amber:
                r.font.bold = True; r.font.color.rgb = WEN_AMBER
            seen.add(part)
        set_chinese_font(r, BODY_FONT)

def timeline(slide, items, emphasis_teal=None, emphasis_amber=None, n=None, total=None, gold=None, gold_kw_a=()):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = WEN_BG
    _accent_box(slide)
    axis_x = 1.6
    top, bottom = 2.2, 6.2
    rect(slide, axis_x - 0.01, top, 0.02, bottom - top, fill=WEN_LINE, line=None)
    step = (bottom - top) / max(1, len(items))
    for i, it in enumerate(items):
        y = top + step * i + step / 2
        rect(slide, axis_x - 0.07, y - 0.07, 0.14, 0.14, fill=WEN_TEAL, line=None, rounded=True)
        tf = tb_box(slide, 0.2, y - 0.2, 1.15, 0.4)
        run_text(tf, fmt_date_5digit(it["time"]), 13, True, WEN_TEAL, PP_ALIGN.RIGHT, Pt(0), True)
        tf = tb_box(slide, 2.0, y - 0.2, 10.5, 0.45)
        # 金额（amt）：追加琥珀加粗后缀 " ｜ 40亿$"，落实"金额高亮"DNA
        disp = it["text"]
        amber = list(emphasis_amber or [])
        if it.get("amt"):
            disp = it["text"] + "　｜　" + it["amt"]
            amber.append(it["amt"])
        if emphasis_teal or amber:
            _run_emph(tf, disp, 14, emphasis_teal or [], amber, WEN_BODY)
        else:
            run_text(tf, disp, 14, False, WEN_BODY, PP_ALIGN.LEFT, Pt(0), True)
    if gold:
        bottom_gold(slide, gold, n=n, total=total, kw_a=gold_kw_a)
    elif n and total:
        add_page_number(slide, n, total, WEN_MUTE)

def two_column(slide, left, right, n=None, total=None, h=4.1, gold=None):
    """双栏：公共骨架 layout_two_column（透明底+青边框）。"""
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = WEN_BG
    _accent_box(slide)
    ye = 6.10 if gold else 6.30
    layout_two_column(slide, WENZHI_SKIN, {"columns": [left, right]}, y0=2.30, y_end=ye)
    if gold:
        bottom_gold(slide, gold, n=n, total=total)
    elif n and total:
        add_page_number(slide, n, total, WEN_MUTE)
def card_grid(slide, cards, cols=2, n=None, total=None):
    """卡片网格：公共骨架 layout_card_grid（透明底+青边框）。"""
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = WEN_BG
    _accent_box(slide)
    layout_card_grid(slide, WENZHI_SKIN, cards, cols=cols, y0=1.65, y_end=6.38)
    if n and total:
        add_page_number(slide, n, total, WEN_MUTE)
def summary(slide, title, sub, metrics=None, quote=None, n=None, total=None):
    """总结页：公共骨架 layout_summary。"""
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = WEN_BG
    _accent_box(slide)
    layout_summary(slide, WENZHI_SKIN, {"title": title, "sub": sub,
                                        "metrics": metrics or [], "quote": quote},
                   y0=1.70, y_end=6.30)
    if n and total:
        add_page_number(slide, n, total, WEN_MUTE)
def bottom_gold(slide, text, n=None, total=None, kw_a=()):
    # 机制委托 common.bottom_gold（已强制 MIDDLE + 共享金句坐标 GOLD_TEXT_Y，根治散落硬编码）；
    # 文质 DNA：暖金 WEN_GOLD 唯一点睛色 + 16pt 粗体（四风格统一 16pt；金句上方无分隔线）
    _gold(slide, text, color=WEN_GOLD, size=16, bold=True,
          text_y=GOLD_TEXT_Y, page_color=WEN_MUTE,
          n=n, total=total, kw_a=kw_a)


# ═══════════════════════════════════════════
# 文质风本地助手（版式原语共用）
# ═══════════════════════════════════════════
def nlines(text, size, w):
    return max(1, math.ceil(measure_text_width(text, size) * 1.03 / w))

def block(s, x, y, w, text, size=12, color=WEN_BODY, gap=0.10, bar=None, bold=False, kw_teal=(), kw_amber=()):
    """悬挂式段落：可选左侧细竖线（文质风"引文"语言）；可选核心词高亮（kw_teal/kw_amber，最多2色、克制）。"""
    tx, tw = (x + 0.16, w - 0.16) if bar else (x, w)
    h = nlines(text, size, tw) * (size * 1.2 / 72.0)
    if bar:
        rect(s, x, y + 0.02, 0.022, h, fill=bar)
    tf = tb_box(s, tx, y, tw, h + 0.08)
    if kw_teal or kw_amber:
        _run_emph(tf, text, size, list(kw_teal), list(kw_amber), color)
    else:
        run_text(tf, text, size, bold, color, PP_ALIGN.LEFT, Pt(0), True)
    return y + h + gap

def card_title(s, x, y, w, text, size=20, underline=True):
    """卡内标题 + 青细线（头身分界）；黑体 + 深蓝灰（文质 DNA：标题=主焦点）"""
    tf = tb_box(s, x, y, w, size * 1.3 / 72.0 + 0.06)
    p = run_text(tf, text, size, True, WEN_DEEP)
    for r in p.runs:
        r.font.name = BODY_FONT; set_chinese_font(r, BODY_FONT)
    if underline:
        rect(s, x, y + size * 1.3 / 72.0 + 0.10,
             min(w, measure_text_width(text, size) + 0.24), 0.022, fill=WEN_TEAL)

def wcard(s, x, y, w, h, fill=WEN_CARD, line=WEN_CARD_LINE):
    """文质风白卡：柔边 + 小圆角（adj 0.03，克制不软）"""
    return rounded_card(s, x, y, w, h, fill, adj=0.03, line=line, line_w=1.0)

def dedupe_accent(s):
    """section_header 与组件型原语都会画右上角 accent_box，去掉重复的（保留最先绘制的）"""
    hits = [sh for sh in s.shapes
            if sh.left == Inches(11.0) and sh.top == 0 and sh.width == Inches(2.333)]
    for sh in hits[1:]:
        sh._element.getparent().remove(sh._element)

def _body_hl(tf, text, hl, size=12, color=WEN_BODY, hl_color=WEN_TEAL):
    """正文 + 加粗青尾句（同段混合 run，用于「描述 + 结论尾句」紧凑排布，对齐企业风角色卡两行结构）。"""
    p = tf.paragraphs[0]
    for t, bold, c in ((text, False, color), (hl, True, hl_color)):
        if not t:
            continue
        r = p.add_run()
        r.text = t
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.name = BODY_FONT
        r.font.color.rgb = c
        set_chinese_font(r, BODY_FONT)

def add_page(prs, h1, label, sub):
    """新增空白页并绘制页眉（section_header 已含背景 + 右上角 accent）。"""
    s = add_blank(prs)
    section_header(s, h1, label, sub)
    return s


# ═══════════════════════════════════════════
# 文质风 · 整页富原语（FDE 沉淀：内容→版式原语）
#   每个原语自含 section_header + 底部金句，生成器只传内容。
# ═══════════════════════════════════════════
def cover_story(prs, title, subtitle, tags, author, n, total):
    """封面：原生 cover + 作者行 + 公众号二维码。"""
    s = add_blank(prs)
    cover(s, title, subtitle, tags=tags, total=total, n=n)
    tf = tb_box(s, X0, 4.65, CW_FULL, 0.28)
    run_text(tf, author, 14, False, WEN_MUTE, PP_ALIGN.CENTER, Pt(0), True)
    add_qr(s, (13.333 - 0.95) / 2, 5.50, 0.95)   # 公众号居底
    tf = tb_box(s, X0, 6.58, CW_FULL, 0.26)
    run_text(tf, "扫码关注「天戈朱」", 12, False, WEN_MUTE, PP_ALIGN.CENTER, Pt(0), True)
    return s

def timeline_page(prs, h1, label, sub, items, emphasis_teal=None, emphasis_amber=None,
                  gold=None, n=None, total=None):
    """时间轴：公共骨架 layout_timeline（竖线+圆点；强调词高亮走 items kw_teal/kw_amber）。"""
    s = add_page(prs, h1, label, sub)
    items2 = []
    for it in items:
        d = {"date": it["time"], "text": it["text"]}
        if emphasis_teal:
            d["kw_teal"] = emphasis_teal
        if emphasis_amber:
            d["kw_amber"] = emphasis_amber
        items2.append(d)
    layout_timeline(s, WENZHI_SKIN, items2, y0=2.20, y_end=6.20)
    dedupe_accent(s)
    if gold:
        bottom_gold(s, gold, n, total)
    elif n and total:
        add_page_number(s, n, total, WEN_MUTE)
def definition_compare(prs, h1, hero, hero_en, hero_cn, bullets, compare_header,
                      negatives, positive, gold, n=None, total=None):
    """定义对比：公共骨架 layout_compare（左 hero+要点 / 右透明青边卡对比；bullets 支持 (text,kw) 高亮）。"""
    s = add_page(prs, h1, None, None)   # 无副标题：hero 区已承载全称+译名
    layout_compare(s, WENZHI_SKIN, {
        "hero": hero, "hero_en": hero_en, "hero_cn": hero_cn,
        "bullets": bullets,
        "summary": None,
        "right": {"header": compare_header,
                  "negatives": [{"kw": kw, "desc": d} for kw, d in negatives],
                  "positive": {"kw": "FDE", "desc": positive}},
    }, y0=1.85, y_end=6.20)
    if gold:
        bottom_gold(s, gold, n, total)
    elif n and total:
        add_page_number(s, n, total, WEN_MUTE)
def value_grid(prs, h1, label, sub, items, gold, n=None, total=None):
    """四大核心价值：公共骨架 layout_value_grid（loop=False 纯并列；求解器/间距区间已固化进 WENZHI_SKIN）。"""
    s = add_page(prs, h1, label, sub)
    layout_value_grid(s, WENZHI_SKIN, items, y0=1.80, y_end=6.48, loop=False)
    if gold:
        bottom_gold(s, gold, n, total)
    elif n and total:
        add_page_number(s, n, total, WEN_MUTE)
def feedback_loop(prs, h1, label, sub, intro, loop_nodes, loop_cap, role_title, role_cap,
                  roles, notes, gold, n=None, total=None):
    """反馈闭环：公共骨架 layout_loop_page（①闭环 ②双卡⇄ ③说明文本）。"""
    s = add_page(prs, h1, label, sub)
    y0 = Y_TOP
    if intro:
        block(s, X0, Y_TOP, CW_FULL, intro, 14, WEN_MUTE, gap=0.0, bar=WEN_TAUPE)
        y0 = 2.48
    layout_loop_page(s, WENZHI_SKIN, {
        "cap1": "① " + loop_cap,
        "nodes": [n if isinstance(n, dict) else {"name": n} for n in loop_nodes],
        "cap2": "② " + role_cap + "：" + role_title,
        "cards": [{"title": it["cn"], "sub": it["en"], "desc": it["desc"], "concl": it.get("hl")}
                  for it in roles],
        "cap3": "③ 三点说明",
        "tail": list(notes),
    }, y0=y0, y_end=6.40)
    if gold:
        bottom_gold(s, gold, n, total)
    elif n and total:
        add_page_number(s, n, total, WEN_MUTE)
def six_step(prs, h1, label, sub, step_cap, steps, cards, bottom_note, gold, n=None, total=None):
    """六步流程：公共骨架 layout_six_step（步骤条+U 型回流+三栏卡+说明）。"""
    s = add_page(prs, h1, label, sub)
    layout_six_step(s, WENZHI_SKIN, {
        "cap": step_cap, "steps": steps,
        "cards": [{"title": c["t"], "lines": c["lines"]} for c in cards],
        "note": bottom_note,
    }, y0=1.90, y_end=6.30)
    if gold:
        bottom_gold(s, gold, n, total)
    elif n and total:
        add_page_number(s, n, total, WEN_MUTE)
def talent_strip(prs, h1, label, sub, intro, items, gold, n=None, total=None):
    """人才长条：公共骨架 layout_talent_strip（intro+全宽横条）。"""
    s = add_page(prs, h1, label, sub)
    layout_talent_strip(s, WENZHI_SKIN, {"intro": intro, "items": items}, y0=Y_TOP, y_end=6.30)
    if gold:
        bottom_gold(s, gold, n, total)
    elif n and total:
        add_page_number(s, n, total, WEN_MUTE)
def profile_warning(prs, h1, label, sub, left, right, gold, n=None, total=None):
    """画像告诫：公共骨架 layout_profile_warning（非对称双卡+两级分隔+结论）。"""
    s = add_page(prs, h1, label, sub)
    left2 = {"title": left["title"],
             "roles": [nm for (_x, _y, nm) in left.get("roles_grid", [])]
                      + ([left["long"]] if left.get("long") else []),
             "conclusion": left["conclusion"]}
    right2 = {"title": right["title"],
              "warns": [{"kw": kw, "desc": desc} for (kw, desc, _wy) in right["warns"]],
              "conclusion": right["conclusion"]}
    layout_profile_warning(s, WENZHI_SKIN, {"left": left2, "right": right2},
                           y0=1.95, y_end=6.20)
    if gold:
        bottom_gold(s, gold, n, total)
    elif n and total:
        add_page_number(s, n, total, WEN_MUTE)
def transition_rows(prs, h1, label, sub, intro, rows, gold, n=None, total=None):
    """转型对照：公共骨架 layout_transition_rows（旧态→新态，行高自适应）。"""
    s = add_page(prs, h1, label, sub)
    y0 = Y_TOP
    if intro:
        block(s, X0, Y_TOP, CW_FULL, intro, 14, WEN_MUTE, gap=0.0, bar=WEN_TAUPE)
        y0 = 2.42
    layout_transition_rows(s, WENZHI_SKIN, {
        "cap": None,
        "rows": [{"from": it["from"], "to_title": it["to"], "to_lines": it["lines"]}
                 for it in rows],
    }, y0=y0, y_end=6.40)
    if gold:
        bottom_gold(s, gold, n, total)
    elif n and total:
        add_page_number(s, n, total, WEN_MUTE)
def hero_questions(prs, h1, label, sub, lead, questions, signature, n=None, total=None):
    """结语问答：公共骨架 layout_hero_questions + 二维码（氛围装饰留引擎层）。"""
    s = add_page(prs, h1, label, sub)
    layout_hero_questions(s, WENZHI_SKIN, {"lead": lead, "questions": questions,
                                           "signature": signature}, y0=1.88, y_end=6.30)
    add_qr(s, (13.333 - 1.05) / 2.0, 4.62, 1.05)
    tf = tb_box(s, X0, 5.76, CW_FULL, 0.26)
    run_text(tf, "扫码关注「天戈朱」", 12, False, WEN_MUTE, PP_ALIGN.CENTER, Pt(0), True)
    add_page_number(s, n or 10, total or 10, WEN_MUTE)
