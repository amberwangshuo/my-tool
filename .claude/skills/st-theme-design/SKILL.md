---
name: st-theme-design
description: 酒馆(SillyTavern)UI主题美化设计手册。当用户想设计、修改或讨论酒馆主题美化(theme JSON/custom_css)时使用。包含设计工作流、审美方法论、CSS选择器技术清单、已交付作品档案。
---

# 酒馆主题美化设计手册

本手册蒸馏自对 5 份社区高水平主题的深度学习（《in time》、NAKARI 白/夜双版、《紧紧相依的心》、《自定义小说[全屏改]》），以及为 amber 交付《不可译》的完整设计过程。你是设计师，用户是甲方。

## 一、工作流程（务必遵守）

1. **需求访谈**（用 AskUserQuestion 分两轮）：
   - 第一轮：世界观隐喻方向 / 明暗色调 / 技术路线 / 使用设备
   - 第二轮：字体气质 / 装饰密度 / 主题命名 / 文案分配
2. **出提案**：先给完整设计提案（隐喻映射表 + 视觉基调 + 技术方案），甲方拍板后再写代码
3. **交付三件套**：主题 JSON（SendUserFile）+ HTML 可视化验收预览（Artifact，模拟手机效果）+ 归档进仓库 `themes/`
4. **预留返工**：不同酒馆版本 DOM 有差异，请甲方实测后发截图微调

## 二、审美方法论（最重要）

**好的美化不是换颜色换圆角，而是把整个聊天界面重新叙事成另一个东西（世界观隐喻）。** 参考案例：
- 音乐专辑（三段式卡片、底栏按钮改成 L/O/V/E 字母）
- 异地恋共享歌单（楼层数→"相距X公里"，计时器→"一起听了X小时"）
- 网文阅读器（名字→"作/"，楼层→"章"，token→"字数"，编辑按钮→"摘抄"）
- 辞典（《不可译》：每楼一页词条，重roll→"另一种译法"，思维链→Tacenda）

隐喻确定后，把**每个 UI 功能都翻译成该世界观下的行为**，尤其是元数据三件套、思维链标题、输入框占位符、翻页按钮、加载动画、分割线。

配色纪律：夜色主题用"一冷一暖"两支点缀色防闷（如月光银 #AEB8C4 + 叶隙金 #C4AD8B）；正文用暖白 #ECE9E4 而非冷白。

## 三、技术路线

| 路线 | 特点 |
|---|---|
| 纯CSS流 | 零图床依赖永不裂图，靠字体/符号(❝❞《》﹥)/线条/文案营造质感 |
| 图片框架流 | 华丽但依赖图床(iili.io/postimg)，需反复调百分比适配 |
| 混合流(推荐) | 骨架纯CSS + 装饰用 **SVG data-URI 内嵌**，有图的效果、无图床的风险 |

字体：zeoseven 接口 `@import url("https://fontsapi.zeoseven.com/{id}/main/result.css")`
已验证 id：**292=霞鹜文楷(LXGW WenKai)**，214=更纱黑体 Sarasa UI SC，285=Noto Serif CJK，371=BabelStone Han

## 四、JSON 结构

主题 = 平铺字段 + `custom_css` 大字符串。关键字段：`name`, `main/italics/underline/quote_text_color`, `blur_tint_color`(面板底色), `chat_tint_color`, `user/bot_mes_blur_tint_color`(常设透明,CSS里自己画), `font_scale`(0.75~1), `chat_width`(50~68), `avatar_style`, `chat_display:1`, `noShadows:true`, `fast_ui_mode:true`, timer/timestamps/mesID/token 四开关全开（供叙事化包装用）。用 Python json.dump(ensure_ascii=False) 生成。

## 五、CSS 选择器技术清单（社区验证过的写法）

**骨架模板**（每个主题都要）：
- `:root` 顶部设"甲方调整区"：全中文变量（--卡片透明度、--输入框文案、--思维链标题…），甲方不懂CSS也能改
- `#chat` 高度：`calc(100dvh + var(--bottomFormBlockSize))`；`#sheld` top/height 用 `var(--bottomFormBlockSize)` 配套；`#form_sheld {position:absolute; bottom:0}` 底栏悬浮
- `.drawer-content` / `#left-nav-panel` / `#right-nav-panel`：`top: var(--抽屉高度)`（约39px）
- 最后一楼间距修复｜@Serein：`.mes.last_mes > *:has(.mesIDDisplay,.mes_timer,.tokenCounterDisplay) {margin/padding-bottom:0}`
- `#chat` 上下柔和渐隐：`mask: linear-gradient(to bottom, transparent 0%, black 4%, black 96%, transparent 100%)`

**消息卡片**：
- `.mes {display:flex; flex-direction:column; position:relative; overflow:visible}`——此时 `.mes::before` 成为第一个 flex 子项（可放词头/标题行），`::after` 是最后一项
- **楼层轮转内容**：`#chat .mes:nth-of-type(9n+1)::before {content:"..."}` ×N 条，不同楼自动换文案（《不可译》招牌）
- user/char 区分：`.mes[is_user="true"]`（换底色、::before 对齐方向、头像左右互换）
- 小头像角章：`.mesAvatarWrapper{position:static}` + `.mes .avatar{position:absolute; top/right; 30px}`
- 图片框架流三段式：`.mes::before` 平铺中段(`repeat-y` + margin-top/bottom 避开透明区) + `.mes::after` 头图尾图双背景(`background-image:url(),url()`, `top center, bottom center`)

**元数据叙事化**（灵魂技巧）：
`.mesIDDisplay/.tokenCounterDisplay/.mes_timer` 用 `::before/::after` 加 content 文案；排序用 `order:1/2/3` + 首项 `margin-left:auto` 推到右侧；`.timestamp::before {content:"收录于 "}`

**思维链**：`.mes_reasoning_header_title {font-size:0}` + `::before {content: var(--思维链标题)}`；`.mes_reasoning_arrow {display:none}`；`.mes_reasoning` 自定底色/左边线/斜体

**翻页按钮**：`.swipeRightBlock {display:contents}` 解除包裹 → `.swipe_left/.swipe_right` absolute 定位 + `::before {content:"文案"}` 替换箭头；`.swipes-counter` absolute + `::before` 前缀

**输入区**：
- `#nonQRFormItems {display:grid; grid-template-columns:auto 1fr auto}`，textarea 占第1行整行(`grid-column:1/4`)，左右按钮组第2行两端
- 占位符打字机｜@墨千尾：原生 placeholder 透明 → `#nonQRFormItems:has(#send_textarea:placeholder-shown)::before {content:var(--输入框文案); width:0; animation: typing steps(N) alternate + 光标 border-right blink}`；聚焦隐藏：`:has(#send_textarea:focus)::before {display:none}`
- QR栏收纳：`#qr--bar {height:0; overflow:hidden}` + `#send_form:hover/:focus-within #qr--bar {height:auto}`

**图标**：FontAwesome 替换 `content:'\f5ad'` 等（'\' 单反斜杠=不设置）；或 `content:""` + background 图片/文字（`.fa-pencil::before {content:"校订"; font-family:霞鹜文楷}`）；顶栏图标平时低透明度、`body:has(.drawer-icon.openIcon)` 时亮起+抽屉铺底

**表单控件全套**：checkbox/radio `appearance:none` 重绘，对勾用 SVG data-URI（`url("data:image/svg+xml,%3Csvg...polyline points='20 6 9 17 4 12'...")`）；滑块 `-webkit-slider-runnable-track` 1px 细线 + `-webkit-slider-thumb` 自绘（radial-gradient 光点或图片），thumb 需 `margin-top` 负值校正

**装饰(纯CSS)**：
- Mångata 光点分割线：`hr {background: radial-gradient(circle, 色 0 1px, transparent 1.8px) 0 50%/11px 6px repeat-x; mask: linear-gradient(90deg,transparent,#000 22%,#000 78%,transparent)}`
- 呼吸加载：`#load-spinner::before {color:transparent; background:多个radial-gradient光斑}` + `@keyframes breathPulse {scale+opacity}`
- 夜色纵深：多层垂直同色投影 `box-shadow: 0 3px 5px rgba(35,35,35,.9), 0 6px 12px .7, ... 0 30px 56px .05`
- 半透卡片：`rgba(11,13,17,0.55)` + `backdrop-filter: blur(6px)`，透出用户自己的背景图
- `color-mix(in srgb, var(--色), transparent N%)` 从两支点缀色派生所有深浅

**杂项**：隐藏滚动条(移动端 display:none / 桌面3px)；`#chat > div.mes.smallSysMes.last_mes.fade {display:none}`；toast 顶部居中毛玻璃；`.completion_prompt_manager_prompt:hover` 左边线+缩进动效；标题包书名号 `h3::before{content:"《"}` `::after{content:"》"}`；警示按钮清单(#delete_button 等8个选择器)统一反色

**致谢惯例**：CSS 头部注释署名+致谢技术来源（@NAKARI @lazyalie @墨千尾 @Serein 等），发布注明"请勿二传或商用"按甲方意愿。

## 六、已交付作品档案

**《不可译》Untranslatable**（2026-08，甲方 amber，成品在本仓库 `themes/不可译-Untranslatable.json`）
- 概念：酒馆=收录不可译之词的辞典；九词轮转楼层（Komorebi/Mångata/Cafuné/Fernweh/Forelsket/Hiraeth/Kilig/Aparima/Iktsuarpok），思维链=Tacenda，输入框=Iktsuarpok 打字机，重roll="前一种译法/另一种译法"，元数据="词条No.X·释义X字·检索Xs"
- 视觉：夜+半透明卡片(透出用户背景)，霞鹜文楷(292)，月光银#AEB8C4+叶隙金#C4AD8B，暖白#ECE9E4，直角2px、细线、辞典排版
- 甲方偏好画像：喜欢有文学性/意象感的世界观隐喻、夜间半透明、手机竖屏、混合流(零图床)、词头+一行释义的克制装饰密度、霞鹜文楷
