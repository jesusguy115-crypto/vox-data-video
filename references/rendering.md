# 执行与交付

所有路径相对当前任务和 Skill 目录解析，不写死作者的 Desktop、运行时或旧球员数据。提取 JSON、材质、场景代码和帧写 work/，最终文件写 outputs/。当前环境有依赖加载工具时先定位运行时；画布和材质脚本需要 Pillow/NumPy，表格提取仅需标准库。

```sh
python scripts/read_table.py '/path/input.xlsx' --out 'work/extracted.json'
python scripts/make_paper.py --out 'work/paper' --width 1920 --height 1080
```

配色由 palettes.json 提供，例如 `--scheme blue-coral`；自定义文件用 `--palette-file work/custom-palette.json`。将生成目录中的 palette.json 读入 scene.json，并用其 ink、paper、primary、secondary、categorical 等角色绘制文字和数据，不能仅给背景换色。accent.jpg 是主强调纸层，yellow.jpg 是兼容别名，颜色随方案改变。

命令路径正确引用，标题与数值通过 JSON 传入，不插入 shell。

保存 scene.json，先记录 theme.text、theme.source、highlight 及 narrative_effects；无用户主题时 theme.text=null、highlight=null、narrative_effects=false。默认 extra_info_cards=false、production_captions=false。再记录包含数据、源单元格、单位、轴范围、顺序、类型、标题、重点、画幅、fps、时长与节拍。使用 scripts/collage.py 的 Scene、ease 和 torn_points 编写短场景脚本。它是材料画布，不替代理解数据，也不限制图表类型；需要时用 Matplotlib/SVG 等绘制精确图形后加入纸层。

中文字体显式定位，macOS 可检查 PingFang/Heiti，其他平台使用已存在的中文字体。测最长文本 bounding box，优先换布局而非缩成小字。先渲染 3–5 张关键帧检查，再生成连续 frame_000000.png…；缓存纹理/字体/纸层，不每帧重新生成。

优先使用 FFmpeg：

```sh
ffmpeg -framerate 30 -i 'work/frames/frame_%06d.png' -c:v libx264 -crf 18 -pix_fmt yuv420p -movflags +faststart 'outputs/data-video.mp4'
```

只有授权重做时覆盖本任务输出。不要删除来源视频或表格。

macOS 无 FFmpeg 时用系统编码器：

```sh
swiftc -module-cache-path 'work/swift-cache' 'scripts/encode_frames.swift' -o 'work/encode-frames'
work/encode-frames 'work/frames' 'outputs/data-video.mp4' 30
```

模块缓存放可写目录。沙箱可能不能访问系统编解码器，按当前权限机制请求执行；不能因沙箱无法解码就断定文件损坏，也不能改变系统权限。编码器检查连续编号、同尺寸、禁止覆盖，并尝试解码开头/中间/结尾。没有编码能力时保留场景与预览，明确限制，不把 GIF/HTML 冒充 MP4。

用实际解码帧检查文字、坐标、柱高、线条和裁切，用源单元格独立核对数值。速度来自复用工具和先检查关键帧，不来自省略验证。先 1080p，用户要求时再定稿 4K。

交付主 MP4 的直接链接和轻量预览。不要仅给 ZIP，不默认生成所有比例与长短多个版本。后续需要再生成。
