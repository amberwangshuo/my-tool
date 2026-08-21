# -*- coding: utf-8 -*-
"""生成「开头状态栏 · 历史上的今天」正则脚本。"""
import json, os, re

BASE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(BASE)
S = r'(?:\s|<br\s*/?>)*'

def field(name, i):
    return '<hud_%s>' % name + r'\s*([\s\S]*?)\s*' + '</hud_%s>' % name + S

# 年份｜光年｜事件；光年缺省时也能匹配，只丢那一列
def echo(n):
    return ('<hud_echo%d>' % n + r'\s*([^｜|]*?)\s*[｜|]\s*(?:([^｜|]*?)\s*[｜|]\s*)?([\s\S]*?)\s*'
            + '</hud_echo%d>' % n + S)

FIND = ('<Pluto_hud>' + S
        + '<hud_chapter>' + r'\s*(?:chapter|第|章节)?\s*([\s\S]*?)\s*' + '</hud_chapter>' + S
        + ''.join(field(f, i) for i, f in enumerate(('title', 'date', 'week', 'time', 'place')))
        + ''.join(echo(n) for n in (1, 2, 3))
        + '</Pluto_hud>')

ROW = ('<span class="phd-y d%d">$%d</span><span class="phd-ly">$%d</span>'
       '<span class="phd-e">$%d</span>')

MARKUP = (
    '<div class="phd">'
    '<div class="phd-top"><span class="phd-ch">CHAPTER $1</span><span class="phd-line"></span></div>'
    '<div class="phd-title">$2</div>'
    '<div class="phd-meta"><span class="phd-d">$3</span><span class="phd-w">$4</span>'
    '<span class="phd-dot"></span><span class="phd-t">$5</span>'
    '<span class="phd-dot"></span><span class="phd-p">$6</span></div>'
    # 光的旅程：左端恒星（衍射芒+扩散光晕），一束光沿线走向右端的「此刻」，
    # 三个年份是路上的节点 —— 位置由远及近，越远的越暗
    '<div class="phd-sky">'
    '<i class="phd-halo"></i><i class="phd-halo"></i><i class="phd-star"></i>'
    '<span class="phd-beam"><i class="phd-pulse"></i></span>'
    '<span class="phd-node phd-n1"><i></i><b>$7</b></span>'
    '<span class="phd-node phd-n2"><i></i><b>$10</b></span>'
    '<span class="phd-node phd-n3"><i></i><b>$13</b></span>'
    '<span class="phd-earth"><i></i><b>此刻</b></span>'
    '</div>'
    '<div class="phd-cap">今夜抵达的光<i>离开的那年</i></div>'
    '<div class="phd-echo">'
    + ''.join(ROW % (d, 7 + (d - 1) * 3, 8 + (d - 1) * 3, 9 + (d - 1) * 3) for d in (1, 2, 3))
    + '</div></div>'
)

css = '\n'.join(l.strip() for l in open(os.path.join(BASE, 'hud.style.css'), encoding='utf-8'
                                        ).read().splitlines() if l.strip())
assert 'rgba(143,202,219' not in css and '#8fcadb' not in css, '状态栏只用白色'
assert 'emoji' not in css

script = {
    "id": "2f1c6a80-5e3b-4c7d-9a11-7d0b5e9c4a04",
    "scriptName": "冥王星 · 开头状态栏 PLUTO",
    "findRegex": "/" + FIND + "/gi",
    "replaceString": '<style>' + css.replace('\n', '') + '</style>' + MARKUP,
    "trimStrings": [], "placement": [2], "disabled": False,
    "markdownOnly": True, "promptOnly": False, "runOnEdit": True,
    "substituteRegex": 0, "minDepth": None, "maxDepth": None,
}
json.dump(script, open(os.path.join(ROOT, '冥王星-开头状态栏.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=2)

# ---- 自检 ----
SAMPLE = ['03', '近点接近', '2026-08-26', '周三', '18:40', '旧金山湾区 · Mission District',
          '1883', '143', '喀拉喀托火山喷发，声浪三次绕行地球',
          '1920', '106', '美国宪法第十九修正案生效，女性获得选举权',
          '1978', '48', '若望·保禄一世当选教宗，在位仅三十三天']
raw = ('<Pluto_hud>\n<hud_chapter>第03</hud_chapter>\n<hud_title>近点接近</hud_title>\n'
       '<hud_date>2026-08-26</hud_date>\n<hud_week>周三</hud_week>\n<hud_time>18:40</hud_time>\n'
       '<hud_place>旧金山湾区 · Mission District</hud_place>\n'
       + ''.join('<hud_echo%d>%s｜%s｜%s</hud_echo%d>\n' % (n, *SAMPLE[6 + (n - 1) * 3: 9 + (n - 1) * 3], n)
                 for n in (1, 2, 3))
       + '</Pluto_hud>')
m = re.search(FIND, raw, re.I)
assert m, '正则未能匹配状态栏模板'
assert list(m.groups()) == SAMPLE, m.groups()

# 漏掉光年那一列也不能整块塌掉
raw2 = raw.replace('1920｜106｜', '1920｜')
m2 = re.search(FIND, raw2, re.I)
assert m2 and m2.group(10) == '1920' and m2.group(11) is None and '第十九修正案' in m2.group(12)
for ph in ('$7', '$10', '$13'):
    assert MARKUP.count(ph) == 2, ph  # 节点标注与表格第一列同源
print('状态栏正则 OK（缺列容错通过）| replaceString', len(script["replaceString"]))

card = MARKUP
for i, v in enumerate(SAMPLE, 1):
    card = card.replace('$%d' % i, v)
open(os.path.join(BASE, 'hud.preview.html'), 'w', encoding='utf-8').write(
    '<style>' + css + '</style>\n' + card + '\n')
