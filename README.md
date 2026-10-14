# Vox NBA 数据视频 Skill

从 Excel、CSV、JSON 或清晰表格截图选图并制作纸纹、撕纸拼贴和分拍跳切的 MP4。主要服务 NBA 内容。

## 使用

安装完整目录后调用 `$vox-data-video`，上传表格，提供主题、单位与配色；也可明确跳过或不设主题。每个新任务提供一次选择入口，已经回答的内容不重复问。

配色是经典纸黄＋NBA30队官方Logo配色派生方案，未选择时直接默认经典纸黄。可说“湖人”“凯尔特人”等球队名。颜色来源及派生说明见 references/color-palettes.md；Logo不默认置入影片。

## 本版改进

**一张表的全部数据必须在同一张图表中呈现。** 多指标不拆成多面板或轮播独立图；只有用户本次明确要求拆图时例外。数量＋命中率默认同图叠加柱线，两个连续指标可用散点。


- 普通制作复用固定模板，修改数据与参数；把开发、基准测试和仓库维护从出片流程移开。保留视觉质量并缩短整轮等待，不把编码秒数冒充总交付时间。
- 饼图百分比标在扇区内，右侧只放色块和名称；小扇区用邻近引导线。
- 标题、中文标注与数字分角色，完整开源字体和许可证随包；保留用户认可原版4K柱线工程。
- 柱形分拍生长、折线描绘、纸层贴入；保留撕边、纸纹、胶带与大字层级，缩小右侧空黑底。
- 不自行推测对比主题；无主题不加结论收尾。默认无说明卡、制作注脚或水印。
- 统一模板与场景记录供其他代理复用；没有执行能力时明确限制，不偷偷重画。

## 安装

```sh
git clone https://github.com/jesusguy115-crypto/vox-data-video.git "${CODEX_HOME:-$HOME/.codex}/skills/vox-data-video"
```

已安装可在该仓库目录执行 `git pull`。如果目录包含个人修改，先保留修改。安装包含 scripts、references、assets，不只复制 SKILL.md。

Python依赖见 requirements.txt。通用视频由 macOS Swift/AVFoundation 或 FFmpeg直接编码。macOS 原版4K柱线工程使用 CoreGraphics/CoreText 与系统字体；其他平台不能声称已复现该工程。FFmpeg分支尚未在本机跨平台实测。详见 references/reproducibility.md。

Hanabi125样式目录用于数据选图参考，并不表示有125个现成模板。Vox是设计参考，项目不属于Vox或NBA，不包含其网站代码。
