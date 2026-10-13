# Vox 数据视频 Skill

从 Excel、CSV 或结构化数据选择合适的可视化图表，并制作带撕纸、纸纹、拼贴与数据动画的 MP4。

## 使用流程

1. 上传表格或清晰的表格截图。
2. 提供视频主题/标题，也可以不设主题。Skill 会先询问；没有主题时只制作动态图表，不自行添加结论、差值卡或重点圈线。
3. 选择配色。提供九套方案，未指定时默认“经典纸黄”。
4. 根据数据结构选图，核对名称、指标、单位和数值，然后制作与验证视频。

默认画面只保留必要的数据标签、坐标轴、单位和图例，以及用户提供的标题。不添加样本数说明卡、读图教学卡和制作说明。

## 安装

将本仓库下载或克隆到 Codex 的 skills 目录，目录名为 `vox-data-video`，确保其中直接包含 `SKILL.md`。

```sh
git clone https://github.com/jesusguy115-crypto/vox-data-video.git "${CODEX_HOME:-$HOME/.codex}/skills/vox-data-video"
```

在 Codex 中调用 `$vox-data-video` 并上传数据。例如：

> 用 $vox-data-video 制作这份表格的视频。主题是“各位置占比”，使用经典纸黄。

## 包含内容

- `SKILL.md`：完整工作流程和交付检查。
- `references/`：数据选图规则、Hanabi 125 种样式/39 个家族研究、多套配色、主题与文字边界、视觉动效和渲染说明。
- `scripts/`：表格读取、图表候选查询、纸张材质、拼贴画布和 macOS 视频编码工具。
- `assets/`：材质方向参考与配色预览。

125 种样式是选图参考目录，不表示已有 125 个开箱即用的视频模板。具体视频由代理按数据编排并渲染。

## 运行条件

表格读取使用 Python 标准库；材质和画布依赖 Pillow/NumPy。视频优先使用 FFmpeg，macOS 无 FFmpeg 时可使用附带的 Swift/AVFoundation 编码器。随包包含统一的 Noto Sans SC 中文字体与许可证。详细命令见 `references/rendering.md`。

Vox 是视觉方向参考，本项目不属于 Vox，也不使用其标志。Hanabi 是样式研究参考；仓库不包含其网站代码。使用参考资产时请核对适用的权利。

## 2.0 快速模板与统一复现

已实现双/多折线、单系列横条、饼图和一柱一线组合模板。适配这些模板时调用同一个渲染入口，不让不同 AI 各写一套相似版式。右侧背景已收窄，标题按文字宽度排版，保留更大的图表空间。

```sh
python scripts/check_environment.py
python -m pip install -r requirements.txt
python scripts/render_video.py --scene examples/two-series-line.json --cache work/video-cache --preview-only
python scripts/render_video.py --scene examples/two-series-line.json --cache work/video-cache --out outputs/example.mp4 --report work/render.json
```

安装依赖只在缺失时进行。示例固定吴艳妮/中岛瞳、黑白朱红、秒单位；参考画面见 `assets/layout-reference.jpg`。同一数据还需同一标题、配色和轴尺度，才能复现相同版式。无脚本执行能力的会话不能仅靠安装 Skill 复现。详细边界见 `references/reproducibility.md`。

直接传帧编码，不写几百张临时 PNG。本机同规格实测：旧流程约 45.8 秒，新流程缓存就绪后约 2.6–4.5 秒；首次编译额外约 21 秒。这只计算导出，不含读表、对话等待与检查。Mac 原生路径已实测；FFmpeg 跨系统路径尚未在 Linux/Windows 实机验证。

字体来自 [Google Fonts 官方 Noto Sans SC](https://github.com/google/fonts/tree/main/ofl/notosanssc)，遵循附带的 SIL Open Font License 1.1。示例用于验证版式，不能替代新任务的数据。

## 2.1 从输入到成片

新增 make_video.py，统一表格读取/截图 OCR、数据规划、参数生成、预览、编码和解码检查。截图 OCR 仅在 macOS 实测；其他环境可输入 JSON/CSV/XLSX。跨任务共享缓存，避免每张表再次编译约21秒。新增动态圆堆模板；用户指定的图形不替换成横条。

```sh
python scripts/make_video.py --table input.png --work work/job --out outputs/video.mp4 --palette classic-paper --chart packed_circle
```

可省略主题、指标和单位，按委托使用通用数据标题，未知单位留空，不臆造具体经济口径；明确不需要标题用 --no-theme。

合成输入实测，缓存就绪，1080p/30fps/14秒：截图从 OCR 到成片约4.6秒，12对象时间宽表到动态圆堆约3.1秒。包含规划和场景，不仅编码；对话等待、代理加载、人工核对与首次编译另计。详细范围见 references/one-pass-workflow.md。
