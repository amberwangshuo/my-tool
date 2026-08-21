# -*- coding: utf-8 -*-
"""生成「剧情选项」正则脚本。轨道分类 A-D 在这里定义。"""
import json, os, re

BASE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(BASE)

# 四条航向 = 四种轨道解算结果，编码的是选项类型本身，不是装饰
TRAJ = [
    ('A', 'STABLE ORBIT',    '稳定轨道'),   # 顺应当前气氛推进
    ('B', 'CLOSE APPROACH',  '近点接近'),   # 情感升温
    ('C', 'PERTURBATION',    '摄动'),       # 意外转折
    ('D', 'ESCAPE VELOCITY', '逃逸速度'),   # 搞事情
]

# 内联事件里不出现 '<' 与 '&'，避免过任何 HTML 解析器时被截断
CLICK = ("var t=document.getElementById('send_textarea');"
         "if(t){var q=this.querySelector('.plo-text');"
         "if(q){t.value=q.innerText.trim();"
         "t.dispatchEvent(new Event('input',{bubbles:true}));t.focus();}}"
         "var p=this.parentNode.querySelectorAll('.plo-opt');"
         "for(var i=p.length;i--;){p[i].classList.remove('is-picked');}"
         "this.classList.add('is-picked');")
KEYS = "if(event.key==='Enter'||event.key===' '){event.preventDefault();this.click();}"

def opt(i, key, en, zh):
    return ('<div class="plo-opt" role="button" tabindex="0" onclick="%s" onkeydown="%s">'
            '<span class="plo-key">%s</span>'
            '<span class="plo-cap"><span>%s</span><i>%s</i>'
            '<b>&#8629; 载入</b><em>&#8629; 已载入</em></span>'
            '<span class="plo-text">$%d</span></div>' % (CLICK, KEYS, key, en, zh, i))

MARKUP = (
    '<details class="plo-log" open><summary class="plo-sum">'
    '<span class="plo-tease"><span class="plo-mark">&#10209;</span>'
    '<span class="plo-tz"><b>PLUTO</b>航向</span>'
    '<span class="plo-dust">&#8902; &#730; &#65377;</span></span>'
    '<div class="plo-head"><span class="plo-mark">&#10209;</span>'
    '<span class="plo-brand">冥王星<b>PLUTO</b></span><span class="plo-rule"></span>'
    '<span class="plo-no">TRAJECTORY A&#8211;D</span></div>'
    '<div class="plo-hint"><span class="plo-k">SELECT</span>'
    '<span class="plo-hv">点击任意一条载入输入框</span><span class="plo-chev"></span></div>'
    '</summary><div class="plo-body"><div class="plo-list">'
    + ''.join(opt(n + 1, *t) for n, t in enumerate(TRAJ)) +
    '</div><div class="plo-sep"></div>'
    '<p class="plo-note"><span class="plo-nm">&#10209;</span>$5'
    '<span class="plo-nd">&#8902; &#730; &#65377;</span></p></div></details>'
)

S = r'(?:\s|<br\s*/?>)*'
def tag(name, n):
    return '<Pluto_opt%s>' % name + r'\s*([\s\S]*?)\s*' + '</Pluto_opt%s>' % name + S

FIND = (
    '<Episode>' + S +
    r'(?:<details>' + S + r'(?:<summary>[\s\S]*?</summary>' + S + r')?)?' +
    '<Pluto_plot_options>' + S +
    ''.join(tag(n, i) for i, (n, _, _) in enumerate(TRAJ)) +
    r'(?:<Pluto_note>\s*([\s\S]*?)\s*</Pluto_note>' + S + r')?' +
    '</Pluto_plot_options>' + S + r'(?:</details>' + S + r')?</Episode>'
)

css = '\n'.join(l.strip() for l in open(os.path.join(BASE, 'opt.style.css'), encoding='utf-8'
                                        ).read().splitlines() if l.strip())
# 两张卡的调色板必须一致，漂移就报错
base = open(os.path.join(BASE, 'style.css'), encoding='utf-8').read()
for token in ('#f2f5fb', '#9aa6bd', '#8fcadb', 'rgba(143,202,219,.5)', 'rgba(127,168,207,.22)'):
    assert token in css and token in base, token

script = {
    "id": "2f1c6a80-5e3b-4c7d-9a11-7d0b5e9c4a03",
    "scriptName": "冥王星 · 剧情选项 PLUTO",
    "findRegex": "/" + FIND + "/gi",
    "replaceString": '<style>' + css.replace('\n', '') + '</style>' + MARKUP,
    "trimStrings": [], "placement": [2], "disabled": False,
    "markdownOnly": True, "promptOnly": False, "runOnEdit": True,
    "substituteRegex": 0, "minDepth": None, "maxDepth": None,
}
json.dump(script, open(os.path.join(ROOT, '冥王星-剧情选项.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=2)

# ---- 自检：拿预设模板的原样输出跑一遍 ----
SAMPLE = [
    "商陆葵把话题接了下去，顺着赵泽川推荐的那门课往下问，问他当年选课时是怎么权衡的，语气轻，像是随口一提。",
    "商陆葵在结账时抢先把卡递了出去，抬眼笑说：「下次你请。」把「下次」两个字轻轻放在了桌上。",
    "餐厅门口撞见赵泽川的旧识，对方叫出一个商陆葵没听过的称呼，赵泽川的神色第一次出现了停顿。",
    "商陆葵一本正经地掏出手机，说要给这顿饭打个分，当场编了一套满分十分的评价体系，从餐前面包开始逐项打分。",
    "每一个 Pluto 都有它的 Charon。",
]
raw = ("<Episode>\n<details>\n<summary> 📋 CHOIR的行动建议 </summary>\n<Pluto_plot_options>\n"
       + '\n'.join('<Pluto_opt%s>%s</Pluto_opt%s>' % (t[0], SAMPLE[i], t[0])
                   for i, t in enumerate(TRAJ))
       + "\n<Pluto_note>%s</Pluto_note>\n</Pluto_plot_options>\n</details>\n</Episode>" % SAMPLE[4])
m = re.search(FIND, raw, re.I)
assert m, "正则未能匹配预设模板输出"
assert list(m.groups()) == SAMPLE, m.groups()

# 不带 details/summary 的精简模板也要能匹配
raw2 = raw.replace("<details>\n", "").replace("<summary> 📋 CHOIR的行动建议 </summary>\n", "").replace("</details>\n", "")
assert re.search(FIND, raw2, re.I), "精简模板匹配失败"

# 内联事件不能含 '<' 或 '&'
assert '<' not in CLICK and '&' not in CLICK and '<' not in KEYS and '&' not in KEYS
print("options regex OK, 两种模板都匹配；replaceString", len(script["replaceString"]))

card = MARKUP
for i, v in enumerate(SAMPLE, 1):
    card = card.replace('$%d' % i, v)
open(os.path.join(BASE, 'opt.preview.html'), 'w', encoding='utf-8').write(
    '<style>' + css + '</style>\n' + card + '\n')
