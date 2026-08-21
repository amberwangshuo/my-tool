# -*- coding: utf-8 -*-
"""从 src/style.css + src/markup.html 生成酒馆正则脚本 JSON 与本地预览页。"""
import json, os, re, uuid

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)

css = open(os.path.join(BASE, 'style.css'), encoding='utf-8').read()
css = '\n'.join(l.strip() for l in css.splitlines() if l.strip())
markup = open(os.path.join(BASE, 'markup.html'), encoding='utf-8').read().strip()

SEP = r'(?:\s|<br\s*/?>)*'
FIND = (
    r'<abstract>' + SEP +
    r'<serial>\s*(?:scene|场景|第)?\s*[#№.:：]*\s*([\s\S]*?)\s*</serial>' + SEP +
    r'<time>\s*([\s\S]*?)\s*(?:[｜|]\s*([\s\S]*?)\s*)?</time>' + SEP +
    r'<scene>\s*([\s\S]*?)\s*</scene>' + SEP +
    r'<plot>\s*([\s\S]*?)\s*</plot>' + SEP +
    r'</abstract>'
)

replace_card = '<style>' + css.replace('\n', '') + '</style>' + markup

def script(name, find, repl, sid):
    return {
        "id": sid,
        "scriptName": name,
        "findRegex": "/" + find + "/gi",
        "replaceString": repl,
        "trimStrings": [],
        "placement": [2],
        "disabled": False,
        "markdownOnly": True,
        "promptOnly": False,
        "runOnEdit": True,
        "substituteRegex": 0,
        "minDepth": None,
        "maxDepth": None,
    }

main = script("冥王星 · 剧情摘要 PLUTO", FIND, replace_card,
              "2f1c6a80-5e3b-4c7d-9a11-7d0b5e9c4a01")
clean = script("冥王星 · 残留标签清理",
               r'</?(?:abstract|serial|time|scene|plot|Episode|Pluto_plot_options|Pluto_opt[A-D]|Pluto_note|Pluto_hud|hud_(?:chapter|title|date|week|time|place|echo[1-3]))>', "",
               "2f1c6a80-5e3b-4c7d-9a11-7d0b5e9c4a02")

for fn, obj in (('冥王星-剧情摘要.json', main), ('冥王星-残留标签清理.json', clean)):
    with open(os.path.join(ROOT, fn), 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

# ---- 预览页：用样例数据把同一套 CSS/结构渲染一遍 ----
SAMPLE = [
    "02", "2026-08-26", "18:40-19:30",
    "旧金山湾区·赵泽川车内 → Mission District 葡萄牙餐厅",
    "商陆葵上了赵泽川的车，途中询问斯坦福暑期经济学课程事宜，赵泽川简短回应并推荐了 Sahni 的课。"
    "两人驱车前往商陆葵预约的葡萄牙餐厅。入座后，商陆葵主导点菜和话题节奏，两人围绕暑假安排、"
    "各自成长背景展开初步交流。赵泽川提及北京时一笔带过，商陆葵注意到这一细节但未追问。"
    "席间聊到学业压力，赵泽川称自己十二点前睡觉，商陆葵借此试探提出日后请教作业的可能，"
    "赵泽川回应：「你可以先发过来，我看看再说。」",
]
card = markup
for i, v in enumerate(SAMPLE, 1):
    card = card.replace('$%d' % i, v)

# 验证正则确实能匹配官方 FORMAT 的输出
raw = (
    "<abstract>\n<serial>Scene 02</serial>\n"
    "<time>2026-08-26｜18:40-19:30</time>\n"
    "<scene>旧金山湾区·赵泽川车内 → Mission District 葡萄牙餐厅</scene>\n"
    "<plot>" + SAMPLE[4] + "</plot>\n</abstract>"
)
m = re.search(FIND, raw, re.I)
assert m, "正则未能匹配标准 FORMAT 输出"
assert [m.group(i) for i in range(1, 6)] == SAMPLE, m.groups()
print("regex OK ->", m.groups()[:4])
print("replaceString 长度:", len(replace_card))

open(os.path.join(BASE, 'card.preview.html'), 'w', encoding='utf-8').write(
    '<style>' + css + '</style>\n' + card + '\n')
