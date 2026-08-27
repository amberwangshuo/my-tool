---
name: st-theme-design
description: 酒馆(SillyTavern)UI主题美化设计手册。当用户想设计、修改或讨论酒馆主题美化(theme JSON/custom_css)时使用。包含设计工作流、审美方法论、CSS选择器技术清单、已交付作品档案。
---

# 酒馆主题美化设计手册 v2

蒸馏自对 10 份社区高水平主题的深度学习（《in time》、NAKARI 白/夜、《紧紧相依的心》、《自定义小说》、电影三部曲《往日回廊/飞鸟越雪/灰色天空》、SNS动态系《@你的好友更新了一条动态》蓝/青苹果双版），以及为 amber 交付《不可译》的完整设计过程。你是设计师，用户是甲方。

## 一、工作流程（务必遵守）

1. **需求访谈**（用 AskUserQuestion 分两轮）：
   - 第一轮：世界观隐喻方向 / 明暗色调 / 技术路线 / 使用设备
   - 第二轮：字体气质 / 装饰密度 / 主题命名 / 文案分配
2. **出提案**：先给完整设计提案（隐喻映射表 + 视觉基调 + 技术方案），甲方拍板后再写代码
3. **交付三件套**：主题 JSON（SendUserFile）+ HTML 可视化验收预览（Artifact，模拟手机效果）+ 归档进本仓库 `themes/`
4. **预留返工**：不同酒馆版本 DOM 有差异，请甲方实测后发截图微调

## 二、审美方法论（最重要）

**好的美化不是换颜色换圆角，而是把整个聊天界面重新叙事成另一个东西（世界观隐喻）。** 已见案例库：
- 音乐专辑（三段式卡片、底栏按钮改 L/O/V/E）；异地恋共享歌单（楼层→"相距X公里"）
- 网文阅读器（名字→"作/"、楼层→"章"、编辑→"摘抄"）；辞典（《不可译》：每楼一页词条，重roll→"另一种译法"）
- **电影片尾**：卡片头图+片名，"上映/辑录"反色标签章贴时间戳，名字→"—— Directed By"，右上角"THE END."大字+小字副文案，胶片条码字符 𝄃𝄂𝄂𝄀𝄁𝄃𝄂𝄂𝄃 当装饰，加载更多→"上一幕：人生如戏"，按钮文字→"(幸福/像雨落下)"拆成两半分给两个按钮
- **社交动态/朋友圈**：名字下挂 @id 签名，时间戳右上角，每楼正文前嵌一张带相框的"照片"（mes_text::before），元数据带小图标前缀

隐喻确定后，把**每个 UI 功能都翻译成该世界观下的行为**：元数据三件套、思维链标题、输入框占位符、翻页按钮、加载动画、分割线、编辑按钮文字、#show_more_messages、顶栏图标。

**质感谱系**（供甲方选型）：直角文字系（辞典/小说，细线+衬线字）｜胶片系（图片羽化+反色标签+衬线）｜新拟态奶油系（同色双向投影+大圆角+软塌塌）｜夜色纵深系（多层垂直同色投影）｜毛玻璃半透系（backdrop-filter 透背景图）。
配色纪律：夜色用"一冷一暖"两支点缀色防闷；正文暖白 #ECE9E4 而非冷白；浅色系可用低饱和灰字 (#757575/#888)。

## 三、技术路线与系列化

| 路线 | 特点 |
|---|---|
| 纯CSS流 | 零图床依赖永不裂图，靠字体/符号/线条/文案营造质感 |
| 图片框架流 | 华丽但依赖图床(iili.io/catbox.moe/postimg)，需调百分比适配 |
| 混合流(推荐) | 骨架纯CSS + 装饰用 SVG data-URI 内嵌 |

**系列化/变体**：把全部颜色抽成 `:root` 令牌（--theme-bg/--theme-shadow/--accent…），同一份 CSS 换一组令牌值即出新配色版本（如"蓝/青苹果"双版、日/夜双版）——做"三部曲"系列的正确姿势。

字体：zeoseven `@import url("https://fontsapi.zeoseven.com/{id}/main/result.css")`
已见 id：**292=霞鹜文楷**，214=更纱黑体，285=Noto Serif CJK，371=BabelStone Han，**415=文源宋体 WenYuan Serif SC VF**（电影系用，衬线），**3=寒蝉全圆体 ChillRoundF**（圆体可爱系用）。设置 `--mainFontFamily/--monoFontFamily` 或直接 body font-family。

## 四、JSON 结构

主题 = 平铺字段 + `custom_css` 大字符串。关键字段：`name`, 四个 text_color, `blur_tint_color`(面板底色), `chat_tint_color`(顶栏底栏可引用 var(--SmartThemeChatTintColor)), `user/bot_mes_blur_tint_color`(常设透明), `font_scale`, `chat_width`(40~68), `avatar_style`, `chat_display`(0扁平/1气泡→body.bubblechat), `noShadows:true`, `fast_ui_mode:true`, timer/timestamps/mesID/token 四开关全开（供叙事化包装）。可覆写 ST 内部色变量：`--black30a/--black70a/--white50a` 等。用 Python json.dump(ensure_ascii=False) 生成。

## 五、CSS 选择器技术清单

**骨架模板**（每个主题都要）：
- `:root` 顶部"甲方调整区"：全中文变量（--卡片透明度、--输入框文案、--图片高度…），甲方不懂CSS也能改；教学式注释（每个可调项旁写"改这里"）
- `#chat` 高度 `calc(100dvh + var(--bottomFormBlockSize))`；`#sheld` top/height 配套；`#form_sheld {position:absolute; bottom:0}` 或 `{margin:0 auto}`
- `.drawer-content`/`#left-nav-panel`/`#right-nav-panel`：top 对齐顶栏；**手机全屏菜单**：`@media(max-width:600px){ top: var(--bottomFormBlockSize); height: calc(100dvh - var(--bottomFormBlockSize)) }`
- 最后一楼：`.mes.last_mes >*:has(.mesIDDisplay,...)` 清 margin｜@Serein；或 `#chat .mes:last-of-type .mes_block {margin-bottom:70px}`
- `#chat` 上下渐隐 mask；隐藏 `#chat > div.mes.smallSysMes.last_mes.fade`

**消息卡片布局三流派**：
1. flex 纵排 + 绝对定位：`.mes {display:flex; flex-direction:column}`，`::before/::after` 成为首/末 flex 子项（放词头/标题），头像、名字、按钮 absolute 摆位（自由但要调坐标）
2. **Grid 区域布局（最稳）**：`.mes {display:grid; grid-template-columns:45px 1fr; grid-template-areas:"avatar name-date" "avatar reasoning" "text text"}` + **`.mes_block {display:contents}`** 解散包裹层，再给 .mesAvatarWrapper/.ch_name/.mes_text/.mes_reasoning_details 指定 grid-area
3. 默认流微调：只动 padding/order（《自定义小说》路线，兼容性最好）

**头图/图片处理**（.mes_block::before 或 .mes_text::before 插图）：
- 基本式：absolute 或 display:block + background url，padding-top 撑位；`padding-top:50%` 做等比占位
- **双向羽化**：`mask-image: linear-gradient(to bottom,...), linear-gradient(to left,...)` + `mask-composite: intersect`（-webkit- 用 source-in）——图片边缘融进背景
- **椭圆羽化**：`mask-image: radial-gradient(ellipse 100% 70% at center, black 30%, transparent 70%)`
- 相框式：`border: 8px solid 浅色; box-shadow: inset 0 0 0 1px rgba(0,0,0,.1); border-radius:8px`
- **图片填充文字**：`background-image:url() + background-clip:text + color:transparent`，用 background-size/position 调显示区域（大标题神器）
- 图上压字渐变遮罩：`background: linear-gradient(to bottom, transparent, rgba(0,0,0,.5)), url()`
- 面板"色罩+图"：`background-image: linear-gradient(tint,tint), url(img); background-size:cover`

**元数据叙事化**（灵魂技巧）：
- `::before/::after` 加 content 文案；`order` + `margin-left:auto` 排右；`.timestamp::before` 做**反色标签章**：`background:black; color:white; padding:0 5px; font-weight:bold`
- 图标前缀式：`::before {background-image:url(小图标); filter: invert(..)sepia(..)hue-rotate(..)}` 用 filter 给 PNG 调色
- **`:empty {display:none}`** 隐藏没值的元数据
- `#show_more_messages {font-size:0}` + `::before {content:"上一幕：…"}` 改加载更多文案

**名字/标题**：
- `.ch_name {flex-direction:column}` + `.ch_name::before` 大标题（可按 `.mes[is_user]` 分别给 char/user 不同标题）
- `.name_text::after {content:"@id"}` 挂签名；`::before {content:"—— Directed By"}` 挂前缀
- **竖排**：`writing-mode: vertical-rl; text-orientation: upright`（vertical-lr 反向）
- 标题包书名号 `h3::before/::after {content:"《"/"》"}`；`strong::before {content:"﹥/↺/ฅ"}` 做小标记

**思维链**：header_title `font-size:0` + `::before/::after {content:var(--思维链标题)}`（『 』括起有仪式感）；arrow display:none；`.mes_reasoning {max-height:500px; overflow:hidden auto}`｜@咩；grid 布局里给 details 指定 grid-area

**翻页**：`.swipeRightBlock {display:contents}` 或 `{width:100%; justify-content:center}`；swipe 按钮 ::before 换文案/字符；counter 加 `— … —` 前后缀

**输入区**：grid 两行布局；占位符打字机（@墨千尾：width 0→N 动画 + border-right 光标 + :has(:focus) 隐藏）或静态斜体小字；**输入时隐藏按钮组**：`#send_form:has(#send_textarea:focus) { #leftSendForm,... {display:none} }`；QR 收纳 hover 唤出

**图标**：FontAwesome content 码替换；文字当图标（`content:"校订"` 配主题字体）；**Unicode 符号库**：☞☛ ◎◉ ❀✿ ▊ ► ✻ 🕊 ☂︎ ⸝⸝⸝ ❦ ✦ ©；图片图标（隐藏 ::before + 元素本体 background 图，hover scale 1.1）；全局图标统一色：`.fa,.fa-solid:not(排除清单),...{color:X !important}`

**控件质感配方**（三选一保持全套统一）：
- 线性极简：透明底 + 1px 边线/底线，focus 换左边线；装饰边"书脊式"`border-left:5px solid; border-right:3px dotted`
- **新拟态**：`background:#f7faff; box-shadow: 3px 3px 6px 阴影色, -3px -3px 6px #fff`，checked/active 换 `inset`；track 用 inset 凹槽；完整套用于 checkbox/radio/range/button/scrollbar(track+thumb)
- 奶油玻璃：大圆角 + `inset 白高光多层 + 0 0 10px white` 泛光
- 符号勾选框：`appearance:none` + `::after {content:"☞/❀"}`，checked 换 "☛/✿"（零绘制成本）
- SVG data-URI 对勾/下拉箭头（stroke 颜色用 %23 转义）

**装饰(纯CSS)**：光点分割线+mask 渐隐；呼吸加载动画；多层垂直同色投影；半透卡片 backdrop-filter；`color-mix(in srgb, var(--色), transparent N%)` 派生深浅；em 虚线下划线 `repeating-linear-gradient`；strong 两侧 `::before/::after` 花饰

**Toast**：语义色左边框（success 绿 error 红 info 蓝 warning 黄，border-left-width 5~10px），底色统一

**世界书移动端 grid 重排**｜@柏柏：`@media(max-width:700px)` 内 `.wi-card-entry .inline-drawer-header {display:grid; 7列3行}` + 各控件 `display:contents` + 逐个指定 grid-row/column（完整代码见 themes/ 参考归档或按此思路重写）

**楼层轮转**：`#chat .mes:nth-of-type(9n+1)::before {content:"..."}` ×N，不同楼自动换文案（《不可译》招牌）

**致谢惯例**：CSS 头尾注释署名+致谢技术来源（@NAKARI @lazyalie @墨千尾 @Serein @柏柏 @咩 @Junezz 等），发布注明"请勿二传或商用"按甲方意愿。参考主题原文件不入库（尊重"请勿二传"）。

## 六、已交付作品档案

**《不可译》Untranslatable**（2026-08，甲方 amber，本仓库 `themes/不可译-Untranslatable.json`，预览页同目录）
- 概念：酒馆=收录不可译之词的辞典；九词轮转楼层（Komorebi/Mångata/Cafuné/Fernweh/Forelsket/Hiraeth/Kilig/Aparima/Iktsuarpok），思维链=Tacenda，输入框=Iktsuarpok 打字机，重roll="前一种译法/另一种译法"，元数据="词条No.X·释义X字·检索Xs"
- 视觉：夜+半透明卡片(透用户背景)，霞鹜文楷(292)，月光银#AEB8C4+叶隙金#C4AD8B，暖白#ECE9E4，直角2px细线辞典排版
- 甲方偏好画像：喜欢文学性/意象感的世界观隐喻、夜间半透明、手机竖屏、混合流(零图床)、词头+一行释义的克制装饰密度、霞鹜文楷

**⚠ 甲方 amber 硬性禁忌与偏好（2026-08 明确声明，所有交付必须遵守）**
- **非常不喜欢金色/焦糖/暖金系**——永远不作为首要选择；点缀色优先冷色系（月光银蓝/星蓝）
- **不要 emoji**——图标一律用自绘内联 SVG 细线图形或颜文字替代（☀️🌙✦ 这类可能渲染成 emoji 的字符也避免）
- 喜欢"简洁但高级"：透明底、细线、克制排版；喜欢宇宙星空/浩瀚意象（纯 CSS 星野 radial-gradient 星点+微闪烁动画很受用）
- **折叠标签/装饰性英文用真实手写体**——选定 La Belle Aurore（纤细钢笔字）；技巧：Google Fonts css2 加 `&text=所需字符` 拿子集 woff2（仅3KB），base64 内嵌 data URI 进组件，零外链不怕墙；配 `transform: rotate(-1.5deg)` 更像手写；注意子集缺字回退，改标签文字要重新生成子集

**《冥王星星海版》正则套件**（2026-08，甲方 amber，本仓库 `themes/底部打包-冥王星星海版.json` + `themes/选项复制-冥王星星海版.json`，预览页同目录）
- 性质：SillyTavern 正则脚本美化（replaceString HTML 组件），非主题 JSON；底部打包=Snapshot/abstract/Todo/seeds/Events 五标签收进楼底折叠 Tab 面板；选项复制=「CHOIR·行动建议」四选项卡，圆环字母 A-D，点选填入 #send_textarea（剪贴板回退），raw span 查找已改为 wrapper 内 class 作用域（修复原版多楼层 id 串号）
- 视觉：透明底、默认折叠成一条「─── ✧ PLUTO SUMMARY ───」标签线、默认夜间；冷色星蓝点缀、纯 CSS 星野背景、SVG 日月切换图标；解析逻辑沿用原版（DOM 抓取+正则容错+懒加载）
- **正则美化两大坑（2026-08 实战教训，做 replaceString HTML 组件必查）**：①代码围栏 ``` 在 `<details>`/`<Episode>` 等 HTML 包裹层内不被 markdown 解析→渲染失败：findRegex 必须把 AI 输出模板的外壳（`<Episode>`、`<details[^>]*>`、`<summary>…</summary>`）用可选非捕获组一并吞掉；②findRegex 尾部 `\s*` 会吃掉与下一个块（如世界书状态栏 `<ValmontStatus>`）之间的空行→两个代码块粘连：replaceString 必须以 `\n\n` 开头和结尾,保证围栏顶格独立
