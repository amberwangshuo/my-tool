# 冥王星 · 剧情摘要美化正则

把预设 `PLOT_SUMMARY_GUIDANCE` 输出的 `<abstract>` 块渲染成一张**深空观测记录卡**。
夜间配色，无 emoji，强调色只用冥王星表面的褐金。整条标题栏是折叠开关（原生 `<details>`，不依赖 JS），
收起后只保留编号与曝光时段两行索引。

## 安装

1. 酒馆 → **扩展 → 正则 (Regex)** → 导入 `冥王星-剧情摘要.json`
2. 可选：再导入 `冥王星-残留标签清理.json`，用于流式输出未闭合时兜底隐藏裸标签
3. 两个脚本都作用于 **AI 输出**，且勾选了 **仅格式显示 (markdownOnly)** —— 不改动发给模型的上下文，
   模型仍能读到完整的 `<abstract>` 结构，不影响后续总结的连贯性

> 若同时启用，把"残留标签清理"拖到"剧情摘要"**下方**，保证主脚本先匹配。

## 自定义

`replaceString` 开头的 `<style>` 里，所有可调项都是 `.plu-log` 上的变量：

| 变量 | 默认 | 说明 |
| --- | --- | --- |
| `--plu-a` | `1` | 底片不透明度。改成 `.3` 即半透明，聊天背景图会透上来 |
| `--plu-tan` | `#c9a882` | 强调色（编号、四角刻线、顶部漏光） |
| `--plu-ice` | `#7fa8cf` | 发丝线与微光 |
| `--plu-ink` | `#e6eaf3` | 正文冷白 |
| `--plu-serif` | 宋体系 | 正文字体，回退到苹方而非 SimSun |

**默认收起**：把 `src/markup.html` 里的 `<details class="plu-log" open>` 去掉 ` open`，重新 `python3 src/build.py`。

底部星屑那行在结构末尾的 `.plu-star` 里，换成别的颜文字直接替换字符即可。

## 兼容性

- `<time>` 里的 `｜` 会被拆成 `DATE` / `TIME` 两个字段，等宽数字对齐；半角 `|` 同样识别
- `<serial>` 中的 `Scene` / `场景` / `第` / `#` / `№` 前缀会被剥掉，只留编号
- 标签之间允许空白与 `<br>`
- 移动端 430px 以下自动收窄留白、隐藏英文副标
- 折叠用原生 `<details>/<summary>`，`summary` 是 `details` 的首个子元素；星点、弦月、胶片颗粒
  全部走 `.plu-log` 的背景层，四角取景刻线由 `::after` 内嵌边框 + 四角 mask 切出 —— 装饰不占 DOM
- 键盘可聚焦折叠开关，聚焦态为褐金描边；`prefers-reduced-motion` 下关闭全部动效

## 开发

```
python3 src/build.py          # 由 src/style.css + src/markup.html 生成两个 JSON（含正则自检）
python3 src/build_preview.py  # 生成 preview.html
```

改样式请改 `src/style.css`，不要直接编辑 JSON。
