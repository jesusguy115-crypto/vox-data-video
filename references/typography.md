# NBA 纸张图表的字体与层级

Vox 并没有唯一一套字形。Dion Lee 的 [By Design 原设计说明](https://dion.studio/By-Design)强调大胆字体、强构图与节奏；John McColgan 的 [Explained 原项目](https://www.mcmotion.art/vox-explained)也说明各主题有自己的视觉语言。下列是对本用户认可纸张分支的中文设计落实，不声称是 Vox 官方字体规定。

通用 editorial 模板：主标题用 Noto Serif SC 900 的粗宋体，强调印刷标题的笔画反差；引题与中文类别用 Noto Sans SC，建立主副层级；百分比用 Barlow Condensed Bold，作为紧凑、清晰的数据数字。只为标题加粗或加撕纸，不等于完成字体设计。不要整张图都用同一款普通黑体。

字体角色固定在 collage.Scene 中。完整字体、来源和 OFL 许可证随包交付，禁止换系统字体后声称与其他代理一致。用户认可的原版 macOS 柱线工程继续沿用其 PingFang SC / Helvetica Neue Condensed Black，见 original-collage.md；这条路径不重新换字。

题目可按原意拆成引题与主标题，但拼接必须等于用户原文。例如“勒布朗”＋“从1打到5”，不能自行加“全能王”等结论。暗色纸用浅字、浅色纸用深字；不为球队颜色牺牲阅读对比度。饼图数值落在扇区内且与底色对比，右侧名称不重复百分比。小于约6%的扇区可使用外侧引导线，避免缩到难以阅读。

动态过程中，数值在对应扇区完整展开后贴入，随后固定，不跳动、不重算原数值。饼图角度可为四舍五入导致的100.01%归一化，标签仍使用用户原始数值。
