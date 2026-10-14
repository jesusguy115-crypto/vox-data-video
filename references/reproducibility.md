整表单图规则优先：见 [single-chart.md](single-chart.md)。禁止未经用户要求拆为多张图或多个面板。

# 不同 AI 与设备复现

旧版只提供风格说明和绘图原语，代理会自行写场景；同样的数据可以出现不同标题纸条、图例、轴刻度、字形和入场。这不是 Skill 安装就能消除的差异。新版本提供统一模板和渲染入口。

## 常用图表必须执行同一入口

对于适配 line/bar/pie/combo/packed_circle 的标准 16:9 场景，调用 `scripts/render_video.py`，不要另写一份“相似”绘图代码。把用户选择与归一化数据填入 scene.json。用户未选择配色仍默认经典纸黄；想复现黑白朱红需明确设置 `palette_id:"mono-vermilion"`。同一表格但不同配色参数不等于同一次设计。

安装要包含完整目录，不只是 SKILL.md。开始检查：

```sh
python scripts/check_environment.py
python -m pip install -r requirements.txt
python scripts/render_video.py --scene examples/two-series-line.json --cache work/video-cache --preview-only
python scripts/render_video.py --scene examples/two-series-line.json --cache work/video-cache --out outputs/example.mp4 --report work/render.json
```

只有缺失依赖时才安装。通用模板使用随仓库附带的 Noto Sans SC（中文标注）、Noto Serif SC（主标题）和 Barlow Condensed Bold（百分比）字体，字号、可变字体字重、标题宽度、纸张种子、轴尺度、系列颜色、动画时间由同一代码和场景决定。不要自行换字体、调整图例位置或替换纸材质。用户明确要求不同版式时才改，记录所改参数。许可证和来源见 assets/fonts/。

`examples/two-series-line.json` 固定吴艳妮/中岛瞳数据、黑白朱红与秒单位；`assets/layout-reference.jpg` 是这一例子的完整帧。其他 AI 可以先运行示例，再比较自己的输出，不把参考图的数据移植到新任务。

渲染报告记录模板指纹、场景和字体 SHA256、Pillow 版本、配色与实际耗时。保存报告在 work/；不把这些技术信息写进视频。模型与用户输入必须仍核对原表数字，模板不会替代数据理解。

## 环境不支持时

有 Python/Pillow/NumPy、完整资源以及 Swift/AVFoundation 或 FFmpeg 才能执行。豆包或其他平台能否执行本地脚本取决于该会话工具；不能通过“安装了 Skill”就推定具备执行权限或工具。

没有脚本执行能力、缺字体或缺编码器时，明确说当前不能复现模板，保留场景/预览，不声称已经按统一模板完成，也不悄悄用图片生成或另一套画法替代。

Mac 原生直接编码路径已实测；FFmpeg 路径提供跨系统实现，但本机没有 FFmpeg，尚未在 Linux/Windows 实机运行验证。相同模板和参数旨在保持可见布局与运动一致；不同解码器/编码器和字库底层版本仍可能有轻微像素或压缩差异，不保证 MP4 字节完全一致。

用户认可的原版柱线图使用 render_classic.py＋classic_collage.swift，必须与 Python 简化模板区分。原版是 macOS 系统字形路径；通用角色字体是随包路径，不强行宣称两者一致。新配色菜单用经典纸黄与30支NBA球队 Logo 派生色。普通任务不先渲染示例，只有首次安装验收或用户明确要求复现时才运行示例。

用户认可的原版柱线图使用 render_classic.py＋classic_collage.swift，必须与 Python 简化模板区分。原版是 macOS 系统字形路径；通用角色字体是随包路径，不强行宣称两者一致。新配色菜单用经典纸黄与30支NBA球队 Logo 派生色。普通任务不先渲染示例，只有首次安装验收或用户明确要求复现时才运行示例。
