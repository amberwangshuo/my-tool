# -*- coding: utf-8 -*-
import os
BASE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(BASE)
css = open(os.path.join(BASE,'style.css'),encoding='utf-8').read()
card = open(os.path.join(BASE,'card.preview.html'),encoding='utf-8').read().split('</style>\n',1)[1].strip()

card2 = card.replace('class="plu-log"', 'class="plu-log" style="--plu-a:1"') \
            .replace('SCENE 02','SCENE 03') \
            .replace('2026-08-26','2026-08-29').replace('18:40-19:30','23:10-23:52') \
            .replace('旧金山湾区·赵泽川车内 → Mission District 葡萄牙餐厅','Palo Alto·商陆葵公寓楼下 → 车内') \
            .replace('商陆葵上了赵泽川的车，途中询问斯坦福暑期经济学课程事宜，赵泽川简短回应并推荐了 Sahni 的课。两人驱车前往商陆葵预约的葡萄牙餐厅。入座后，商陆葵主导点菜和话题节奏，两人围绕暑假安排、各自成长背景展开初步交流。赵泽川提及北京时一笔带过，商陆葵注意到这一细节但未追问。席间聊到学业压力，赵泽川称自己十二点前睡觉，商陆葵借此试探提出日后请教作业的可能，赵泽川回应：「你可以先发过来，我看看再说。」',
                     '把 --plu-a 调回 1，那层偏蓝近黑的底片就回来了。星点、弦月、四角刻线不变，只是卡片从背景里浮出来一层。浅色界面或者背景图太花的时候用这一版。')

card3 = card.replace('<details class="plu-log" open>', '<details class="plu-log">') \
            .replace('SCENE 02','SCENE 01') \
            .replace('2026-08-26','2026-08-24').replace('18:40-19:30','14:05-14:40')

SWATCH = [('#080a10','近黑底','偏蓝，不是纯黑'),('#e6eaf3','冷白正文','夜视下不刺眼'),
          ('#79839b','蓝灰弱字','字段名与注记'),('#8fcadb','冰川青','唯一强调色'),
          ('#7fa8cf','冰蓝','只做发丝线与微光')]
sw = ''.join(
 f'<li><i style="background:{h}"></i><b>{h}</b><span>{n}</span><em>{d}</em></li>' for h,n,d in SWATCH)

html = f'''<title>冥王星剧情摘要卡</title>
<style>
{css}
:root{{--pg:#050609;--pg2:#0a0c12;--ink:#e6eaf3;--dim:#79839b;--tan:#8fcadb;--ice:#7fa8cf;
--mono:ui-monospace,"SFMono-Regular",Menlo,Consolas,monospace;
--sans:"PingFang SC","HarmonyOS Sans SC","Source Han Sans SC","Noto Sans SC","Microsoft YaHei",-apple-system,sans-serif;}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--pg);color:var(--ink);font-family:var(--sans);
background-image:radial-gradient(1px 1px at 8% 12%,rgba(230,238,255,.35),transparent 60%),radial-gradient(1px 1px at 72% 6%,rgba(230,238,255,.25),transparent 60%),radial-gradient(1.4px 1.4px at 91% 41%,rgba(230,238,255,.22),transparent 60%),radial-gradient(1px 1px at 21% 78%,rgba(230,238,255,.2),transparent 60%);
background-attachment:fixed}}
.wrap{{max-width:760px;margin:0 auto;padding:clamp(28px,7vw,64px) clamp(16px,5vw,28px) 72px}}
.eyebrow{{display:flex;align-items:center;gap:10px;font-family:var(--mono);font-size:10px;letter-spacing:.3em;color:rgba(127,168,207,.6)}}
.eyebrow span{{flex:1;height:1px;background:linear-gradient(90deg,rgba(127,168,207,.3),transparent)}}
h1{{margin:16px 0 0;font-size:clamp(26px,6.4vw,38px);font-weight:500;letter-spacing:.14em;text-wrap:balance}}
h1 b{{display:block;font-family:var(--mono);font-size:11px;font-weight:400;letter-spacing:.42em;color:var(--tan);margin-top:12px}}
.lede{{margin:18px 0 0;max-width:34em;font-size:14px;line-height:2;color:#aab3c6;letter-spacing:.02em}}
h2{{margin:56px 0 0;font-family:var(--mono);font-size:10px;font-weight:400;letter-spacing:.3em;color:rgba(143,202,219,.66)}}
h2+p{{margin:8px 0 18px;font-size:12.5px;line-height:1.9;color:var(--dim)}}
.swatches{{list-style:none;margin:14px 0 0;padding:0;display:grid;gap:1px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.06)}}
.swatches li{{display:grid;grid-template-columns:26px max-content 1fr;align-items:center;gap:14px;padding:11px 14px;background:var(--pg2)}}
.swatches i{{width:26px;height:26px;border-radius:2px;box-shadow:inset 0 0 0 1px rgba(255,255,255,.1)}}
.swatches b{{font-family:var(--mono);font-size:11px;font-weight:400;letter-spacing:.1em;color:#ccd4e3}}
.swatches span{{font-size:12.5px;color:#ccd4e3}}
.swatches em{{font-style:normal;font-size:11.5px;color:var(--dim)}}
@media(max-width:520px){{.swatches li{{grid-template-columns:22px 1fr;gap:10px}}.swatches i{{width:22px;height:22px}}.swatches em{{grid-column:2}}}}
footer{{margin-top:64px;padding-top:16px;border-top:1px solid rgba(255,255,255,.06);font-family:var(--mono);font-size:9.5px;letter-spacing:.28em;color:rgba(127,168,207,.38)}}
</style>
<div class="wrap">
<div class="eyebrow">OBSERVATION LOG<span></span>SILLYTAVERN REGEX</div>
<h1>冥王星 · 剧情摘要<b>PLUTO / PLOT SUMMARY</b></h1>
<p class="lede">把每轮剧情总结渲染成一张深空观测记录：编号、曝光时段、观测视场、正文注记。四角是取景刻线，右上角那道弦月是被远日照亮的冥王星。底色透明，直接浮在你的黑背景上；整条标题栏是折叠开关，收起后只剩一行字。</p>

<h2>01 &nbsp;展开态</h2>
<p>透明底，只有星点、弦月与发丝线浮在你自己的聊天背景上。整条标题栏可点击折叠。</p>
{card}

<h2>02 &nbsp;收起态</h2>
<p>框、底、刻线、漏光全部卸掉，只剩一行字。长对话里往回翻，它安静地待在那儿不抢戏。</p>
{card3}

<h2>03 &nbsp;加回底片（可选）</h2>
<p>默认是透明的。如果你的界面不是纯黑，一行变量就能把底片加回来。</p>
{card2}

<h2>04 &nbsp;色板</h2>
<p>整套只有冷白、蓝灰、冰川青三层。强调色只出现在编号、四角刻线、星体弧线和顶部那道亮边。</p>
<ul class="swatches">{sw}</ul>

<footer>⋆ ˚ ｡ ⋆ ° ･ ⟡ ･ ° ⋆ ｡ ˚ ⋆</footer>
</div>
'''
open(os.path.join(ROOT,'preview.html'),'w',encoding='utf-8').write(html)
print('preview.html', len(html))
