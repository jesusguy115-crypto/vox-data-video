# 常用图表快速制作

优先使用 one-pass-workflow.md 的 make_video.py，让读表、选图和参数生成也进入统一自动流程。

默认背景只保留窄边装饰，标题纸条按文字宽度计算，单行标题居中，图表向上扩展。避免旧版大面积右侧黑底造成空洞；其他主题可按数据与画幅调整。

先理解数据并选图，再判断模板是否适合。不能为了使用快模板而改变数据关系。以下五种 16:9 模板已实现：

| chart_type | 支持范围 |
|---|---|
| packed_circle | 多对象、非负值、真实时间宽表；面积比例、固定身份动态圆堆 |
| line | 数字时间轴、共同尺度的折线；少量系列与可读的年度节点 |
| bar | 单系列横条，最多 12 类；数量轴从 0 起 |
| pie | 已确认的互斥类别、完整整体、非负数，最多 8 类；按总和闭合，保留原标签 |
| combo | 同一数字横轴，一组柱形、一组折线；左右轴分别定义，柱轴从 0 起 |

密集数据、长标签、特殊单位编码、更多系列、特殊强调或不同画幅需自定义场景，不硬挤模板。主题、数值、单位和轴范围来自已核对的输入；模板不猜它们。

## 运行

```sh
python scripts/render_video.py --scene work/scene.json --cache work/video-cache --preview-only
python scripts/render_video.py --scene work/scene.json --cache work/video-cache --out outputs/data-video.mp4 --report work/render-timing.json
```

统一脚本一次生成 entry/middle/final 预览并导出，随后核对一次；不默认 preview-only 后再从头执行完整导出。默认使用打包字体。Mac 使用 Swift/AVFoundation；其他系统有 FFmpeg 时使用 rawvideo stdin，保持同一模板画面。，BGRA 帧通过 stdin 直接进入编码器，不写逐帧 PNG；缓存纹理、字体、已完成数据层、最终停留画面和编译后的编码器。本次初次编译额外约 21 秒（首次整段约 25 秒），后续缓存可复用。不要把缓存或二进制提交进 Skill。

用 `--backend png` 可回退到连续 PNG 与原编码器。自动 Swift 编译仅支持 macOS；FFmpeg 跨系统路径尚未在本机实测，不声称所有平台已经测试。

相同已提供的信息不重复问；主题、单位与配色在开始时尽量一次收齐。没有主题仍按原规则只展示图表。无需每次重查风格或全量样式目录。导出计时不包含对话等待、截图转录和检查时间，不承诺固定总交付时间。

## 通用场景字段

`theme={text:null,source:"not_provided"}` 表示无主题；有主题必须 `source:"user"`。可提供最多两行 `title_lines`，拼接后必须保留用户原标题（允许空格变化）。`highlight:null`、`extra_info_cards:false`、`production_captions:false`。模板不添加额外解释卡或自主结论。

`palette_id` 来自配色库，`data` 为核对后的行对象。`value_precision` 指定数值小数位；保持来源精度。`width/height` 默认 1920/1080，`fps` 默认 30，`duration` 默认 14。`reveal_seconds` 默认 6.3；时长需覆盖入场、展开和阅读停顿。

### 折线

```json
{
  "chart_type":"line", "theme":{"text":null,"source":"not_provided"},
  "palette_id":"mono-vermilion", "value_precision":2,
  "x_axis":{"field":"year","label":"年份"},
  "y_axis":{"min":12.4,"max":14,"ticks":[12.4,12.8,13.2,13.6,14],"precision":1,"label":"成绩（秒）"},
  "series":[{"name":"甲","field":"a","color":"#D64732"},{"name":"乙","field":"b","color":"#262626"}],
  "data":[{"year":2024,"a":"12.99","b":"12.74"},{"year":2025,"a":"12.71","b":"12.90"}]
}
```

数字横轴按实际间距映射，必须递增且唯一。缺失值不能静默补齐；有缺失需自定义断线。数字标签只标实际节点，线段插值不作为新数据。

### 横条

`chart_type:"bar"`，`category_field:"name"`，`value_field:"value"`，`value_axis:{min:0,max:40,ticks:[0,10,20,30,40],precision:0,label:"得分"}`，`data:[{name:"甲",value:24},…]`。不自动排序；保存用户顺序。

### 饼图

`chart_type:"pie"`，`category_field:"name"`，`value_field:"value"`，`complete_whole:true`，`categories_mutually_exclusive:true`。仅在确认组成关系后设置这两个布尔值。`value_suffix:"%"` 仅适用于源数据已经为百分数；不自动乘 100。

### 柱线组合

折线字段基础上使用 `chart_type:"combo"`。两个 series 分别设置 `role:"bar"` 和 `role:"line"`；`y_axis` 是柱轴，`right_axis` 是线轴，两者各有 min/max/ticks/precision/label。不要按叙事需要任意调整轴来制造关系。当前模板的右轴图例约定要求柱系列在前、折线系列在后。

## 本机实测口径

同一份 11 年、两系列数据，1920×1080、30fps、14 秒：旧自定义场景 + PNG + 编码约 45.8 秒；预制模板 + 直接编码约 2.6–4.5 秒（编码器已编译，后续版式和字库更新后重复测量）。数值、尺度和视频规格一致，但图层实现和入场细节不同。这是单次本机导出对比，不是跨机器保证，也不是对原先整轮约八分钟聊天耗时的分解。

饼图百分比默认直接放扇区，右侧图例仅色块＋名称；小扇区用近邻引导线。visual_profile=editorial 与 motion_steps_per_second=12 为新入口默认。title_materials 可指定 dark/accent/secondary 两行材料；主标题字体角色见 typography.md。

饼图百分比默认直接放扇区，右侧图例仅色块＋名称；小扇区用近邻引导线。visual_profile=editorial 与 motion_steps_per_second=12 为新入口默认。title_materials 可指定 dark/accent/secondary 两行材料；主标题字体角色见 typography.md。
