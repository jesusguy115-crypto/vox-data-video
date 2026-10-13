# 用户认可的原版柱线拼贴与跳切

来源是用户明确满意的 chart-collage-readable.mp4 原工程。保留其 CoreGraphics/CoreText 版式、凝缩数字字体、纹理柱、半色调篮球、旋转胶带、撕纸、大字分层入场、折线描绘与手绘圈；不能为了速度换成 Noto 字体的简化图表。

`classic_collage.swift` 直接来自原工程，新增字体/文字/纸层缓存，省掉逐帧 PNG 与重复编写场景。柱子分六拍从 0 到目标高度：0、12%、32%、58%、82%、100%，每拍约 0.1 秒，逐柱错开约 0.18 秒；字体与最终尺度不抖动，原数值只在落位后出现。折线与手绘圈按 12fps 离散拍绘制，输出仍为 30fps。标题纸片沿用原版离散节奏。

```sh
python scripts/render_classic.py --scene work/classic-scene.json --out outputs/video.mp4 --report work/classic-render.json
```

输入字段：players（字符串数组）、points_per_possession（数字数组）、efg_percent（百分数点，46.6而非0.466）、title_lines（两行用户标题或明确委托的标题）、duration（默认12）、show_emphasis（默认false）。用户主题确实要求最高值比较才设置 show_emphasis=true，图中最大值由数据计算，不写死布伦森。无主题不得添加结论卡/圈线；本版本须明确标题后使用，其他无主题图走通用模板。

原轴固定为每回合得分0–1.2、有效命中率0–60%，超范围不能默默裁切或随意改轴。最多12个类别，更密的对象需调整原版布局。原图 footer 的样本说明、重建说明已去除。真实表格百分比替代旧视频点位估算。

此入口需要 macOS CoreGraphics/CoreText，并沿用系统 PingFang SC 与 Helvetica Neue Condensed Black，才能保留用户满意的字形。其他环境不能执行时明确说明，不偷偷换简化渲染器。没有分发系统字体文件；随包资源只有生成的纸张材质。已有统一 Noto 模板继续用于其他图表。

原版风格4K/30fps/12秒本次实际渲染+编码约13.5秒；这是机器导出计时，首次编译、数据理解、对话与核查另计。不要把1080p简化模板的2.6秒与这套4K原工程混用。
