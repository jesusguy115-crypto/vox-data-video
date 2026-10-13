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

表格读取使用 Python 标准库；材质和画布依赖 Pillow/NumPy。视频优先使用 FFmpeg，macOS 无 FFmpeg 时可使用附带的 Swift/AVFoundation 编码器。中文需有可用字体。详细命令见 `references/rendering.md`。

Vox 是视觉方向参考，本项目不属于 Vox，也不使用其标志。Hanabi 是样式研究参考；仓库不包含其网站代码。使用参考资产时请核对适用的权利。
