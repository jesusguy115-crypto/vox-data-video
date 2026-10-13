# Hanabi 样式目录


主题与强调效果遵守 theme-and-caption.md：目录中的重点圈线、标题、数字卡等是有用户授权时的可选动效；无主题只展开图表。选图不授权推测叙事意图。

2026-10-13 检查的 125 个样式，归为 39 个数据关系家族。选图先看 hanabi-selection.md；具体输入陷阱看 hanabi-input-and-motion.md。用途判断是本技能的研究归纳，格式状态是官网核实情况。

## comparison · 类别间大小或单期排序

需要：类别、数值、单位。
避免：完整占比组成不默认用排名图；三角/象形是外观变体，不能按图形面积误读高度。
Vox 动画：逐条贴入、固定零基线、重点数字纸卡。

| 样式 | 输入与核实状态 |
|---|---|
| [动态柱状图](https://hanabi.cn/h2/visualisation/dynamic_column_chart) | 网站指引：2列；语义字段为类别、数值、单位；涉及大小的数值为非负。 |
| [棒棒糖图](https://hanabi.cn/h2/visualisation/lollipop_chart) | 网站指引：2列；语义字段为类别、数值、单位 |
| [动态排名图](https://hanabi.cn/h2/visualisation/barchartrace) | 网站指引：2列；语义字段为类别、数值、单位；涉及大小的数值为非负。 |
| [基础柱状图](https://hanabi.cn/h2/visualisation/column_chart) | 网站指引：2列；语义字段为类别、数值、单位 |
| [三角柱形图](https://hanabi.cn/h2/visualisation/triangular_bar_chart) | 网站指引：2列；语义字段为类别、数值、单位 |
| [象形柱图](https://hanabi.cn/h2/visualisation/pictorial_column_chart) | 网站指引：2列；语义字段为类别、数值、单位；涉及大小的数值为非负。 |
| [基础条形图](https://hanabi.cn/h2/visualisation/bar_chart) | 网站指引：2列；语义字段为类别、数值、单位 |
| [象形条形图](https://hanabi.cn/h2/visualisation/pictorial_bar_chart) | 网站指引：2列；语义字段为类别、数值、单位；涉及大小的数值为非负。 |
| [迷你柱状图](https://hanabi.cn/h2/visualisation/column_sparkline) | 类别、数值、单位 |

## grouped_comparison · 同类别内比较多个系列

需要：类别、系列、数值。
避免：系列太多时分面；各面板尺度须可比较。
Vox 动画：按系列贴入，最后圈出组内差异。

| 样式 | 输入与核实状态 |
|---|---|
| [分组柱状图](https://hanabi.cn/h2/visualisation/grouped_column_chart) | 类别、系列、数值 |
| [分组条形图](https://hanabi.cn/h2/visualisation/grouped_bar_chart) | 类别、系列、数值 |
| [分组条形图（新）](https://hanabi.cn/h2/visualisation/grouped_bar_chart3) | 类别、系列、数值 |
| [分面条形图](https://hanabi.cn/h2/visualisation/grouped_bar_chart2) | 类别、系列、数值 |

## stacked_composition · 多个整体的构成与总量

需要：类别/组、可相加的组成值、共同分母。
避免：百分比与绝对堆叠不能混用；不同单位不能相加。
Vox 动画：整组建立后逐块展开，标总量或份额。

| 样式 | 输入与核实状态 |
|---|---|
| [堆叠条形图](https://hanabi.cn/h2/visualisation/stacked_bar_chart) | 类别/组、可相加的组成值、共同分母；涉及大小的数值为非负。 |
| [堆叠柱状图](https://hanabi.cn/h2/visualisation/stacked_column_chart) | 类别/组、可相加的组成值、共同分母；涉及大小的数值为非负。 |
| [百分比堆叠柱状图](https://hanabi.cn/h2/visualisation/percentage_stacked_column_chart) | 类别/组、可相加的组成值、共同分母；涉及大小的数值为非负。 |
| [百分比堆叠条形图](https://hanabi.cn/h2/visualisation/percentage_stacked_bar_chart) | 类别/组、可相加的组成值、共同分母；涉及大小的数值为非负。 |
| [分组堆叠柱状图](https://hanabi.cn/h2/visualisation/column_clustered_stacked) | A横轴；C起非负数值，B用于组别的具体映射需核实。 |

## dual_axis_combo · 同对象的两指标叠加

需要：类别/时间、柱或线系列、左右轴单位。
避免：轴缩放不能制造相关性；保留用户指定柱线叠加。
Vox 动画：柱先展开、线后绘出、贴短解释标签。

| 样式 | 输入与核实状态 |
|---|---|
| [动态双轴折线图](https://hanabi.cn/h2/visualisation/dynamic_line_dou_chart) | A横轴；B左轴；C右轴，三列。 |
| [折线柱状图](https://hanabi.cn/h2/visualisation/combo_dual_axes_chart) | A类别、B右轴折线、C左轴柱形；可在控件调整映射。 |
| [分组折线柱状图](https://hanabi.cn/h2/visualisation/line_grouped_bar) | 文字沿用三列柱线说明；控件支持柱/线数据范围。 |
| [堆叠折线柱状图](https://hanabi.cn/h2/visualisation/line_stacked_bar) | 文字沿用三列柱线说明；控件支持柱/线数据范围。 |

## line_trend · 有序连续趋势与节点标注

需要：有序横轴、数值系列、可选节点文字。
避免：纯类别不自动连线；真实缺失和插值须区分。
Vox 动画：纸页固定、线按顺序画出、节点注释贴入。

| 样式 | 输入与核实状态 |
|---|---|
| [动态折线图](https://hanabi.cn/h2/visualisation/dynamic_line_chart) | 有序横轴、数值系列、可选节点文字 |
| [带标签折线图](https://hanabi.cn/h2/visualisation/labeled_line) | 官网数据指引为空；以下是按图形结构归纳的自绘字段：有序横轴、数值系列、可选节点文字 |
| [折线图（带标注)](https://hanabi.cn/h2/visualisation/line_with_notes) | 有序横轴、数值系列、可选节点文字 |
| [折线图](https://hanabi.cn/h2/visualisation/line_chart) | 有序横轴、数值系列、可选节点文字 |
| [迷你折线图](https://hanabi.cn/h2/visualisation/spark_line) | 有序横轴、数值系列、可选节点文字 |
| [阶梯折线图](https://hanabi.cn/h2/visualisation/stepped_line_chart) | 有序横轴、数值系列、可选节点文字 |

## ranking_over_time · 多对象的时序数值/排名变化

需要：对象、真实时间、多期值或名次。
避免：两列单期数据不构造假时间；名次轴方向及并列名次需清楚。
Vox 动画：稳定身份标签、按真实时间运动，关键时点停留。

| 样式 | 输入与核实状态 |
|---|---|
| [动态条形图](https://hanabi.cn/h2/visualisation/dynamic_bar_chart) | A颜色组、B对象；C起列头为时间，单元格为非负值。 |
| [动态折线排名图](https://hanabi.cn/h2/visualisation/dynamic_line_rank_chart) | A横轴，B起每列一个系列，网站建议少于九线。 |
| [动态对比条形图](https://hanabi.cn/h2/visualisation/diverging_bar) | A颜色组、B对象；后续为多期非负值。 |

## heatmap · 二维分类矩阵中的强度

需要：X维、Y维、格值、色阶单位。
避免：缺失不是零；不能只靠颜色不给图例。
Vox 动画：逐行格片揭开、重点格圈线。

| 样式 | 输入与核实状态 |
|---|---|
| [笛卡尔热力图](https://hanabi.cn/h2/visualisation/heatmap_cartesian) | 官网数据指引为空；以下是按图形结构归纳的自绘字段：X维、Y维、格值、色阶单位 |

## tree_structure · 父子关系的结构

需要：层级路径、可选叶值。
避免：节点位置不代表量；网络不是树。
Vox 动画：父级先贴入、分支展开、聚焦一个子树。

| 样式 | 输入与核实状态 |
|---|---|
| [水平树状图](https://hanabi.cn/h2/visualisation/horizontal_tree) | 前列层级名称，末列叶值，层数不固定。 |
| [径向树状图](https://hanabi.cn/h2/visualisation/radial_tree) | 前列层级名称，末列叶值。 |
| [垂直树状图](https://hanabi.cn/h2/visualisation/vertical_tree) | 前列层级名称，末列叶值。 |

## parallel_coordinates · 同对象多指标关系

需要：对象/组、多个数值维度。
避免：不同尺度需轴标或标准化；交叉太多会难读。
Vox 动画：先建轴，再画重点对象，其他线弱化。

| 样式 | 输入与核实状态 |
|---|---|
| [平行坐标系](https://hanabi.cn/h2/visualisation/parallel_chart) | A组/图例；B起数值轴，每行一个对象，网站建议至少四列。 |

## regression · 两个数值的拟合关系

需要：成对X/Y样本、明确拟合方式。
避免：拟合不代表因果；不凭少量点给可靠预测。
Vox 动画：先散点、后拟合线、注明计算与范围。

| 样式 | 输入与核实状态 |
|---|---|
| [线性回归图](https://hanabi.cn/h2/visualisation/scatter_linear_regression) | A为X，B为Y。 |

## diverging_comparison · 基准两侧或两群体对比

需要：共同类别、正负系列或左右群体。
避免：左边视觉方向不等于数据为负；人口年龄层须真实。
Vox 动画：共同基线固定，两边展开，圈差异。

| 样式 | 输入与核实状态 |
|---|---|
| [发散堆叠条形图](https://hanabi.cn/h2/visualisation/diverging_stacked_bar) | 共同类别、正负系列或左右群体 |
| [发散堆叠柱形图](https://hanabi.cn/h2/visualisation/diverging_stacked_column) | 共同类别、正负系列或左右群体 |
| [双向柱状图](https://hanabi.cn/h2/visualisation/bidirectional_bar_chart) | 网站指引：3列；语义字段为共同类别、正负系列或左右群体；涉及大小的数值为非负。 |
| [蝴蝶图](https://hanabi.cn/h2/visualisation/butterfly_chart) | 网站指引：3列；语义字段为共同类别、正负系列或左右群体；涉及大小的数值为非负。 |
| [人口金字塔](https://hanabi.cn/h2/visualisation/population_pyramid_chart) | 官网数据指引为空；以下是按图形结构归纳的自绘字段：共同类别、正负系列或左右群体 |

## candlestick · 每期的开高低收

需要：时间、开盘、收盘、最低、最高。
避免：普通单值趋势不能伪造OHLC；验证最低/最高覆盖开收。
Vox 动画：时间顺序逐根出现，贴关键波动说明。

| 样式 | 输入与核实状态 |
|---|---|
| [K线图](https://hanabi.cn/h2/visualisation/k_line_chart) | 日期、开盘、收盘、最低、最高五列。 |

## sets · 集合交集的规模

需要：集合名称组合、交集数。
避免：互斥份额不是交集；交集计数口径需一致。
Vox 动画：集合纸片建立后揭示交叠值。

| 样式 | 输入与核实状态 |
|---|---|
| [韦恩图](https://hanabi.cn/h2/visualisation/venn_chart) | 前列集合名称组合，末列交集值。 |

## geographic_distribution · 地区空间差异

需要：同层级地区、数值、可选多期时间。
避免：绝对人口/总量宜气泡，强度/率宜分级色；行政面积不是值。
Vox 动画：地图纸页固定、地区逐项着色或气泡出现。

| 样式 | 输入与核实状态 |
|---|---|
| [静态地图热力图（分省）](https://hanabi.cn/h2/visualisation/static_choropleth_map_provincial) | 同层级地区、数值、可选多期时间 |
| [静态地图气泡图（分省）](https://hanabi.cn/h2/visualisation/static_bubble_map_provincial) | 同层级地区、数值、可选多期时间 |
| [动态地图热力图](https://hanabi.cn/h2/visualisation/dynamic_choropleth_map) | 同层级地区、数值、可选多期时间 |
| [动态地图气泡图](https://hanabi.cn/h2/visualisation/dynamic_bubble_map) | 同层级地区、数值、可选多期时间；涉及大小的数值为非负。 |
| [静态地图热力图](https://hanabi.cn/h2/visualisation/static_choropleth_map) | 同层级地区、数值、可选多期时间 |
| [静态地图气泡图](https://hanabi.cn/h2/visualisation/static_bubble_map) | 同层级地区、数值、可选多期时间；涉及大小的数值为非负。 |
| [动态地图热力图（分省）](https://hanabi.cn/h2/visualisation/dynamic_choropleth_map_provincial) | 同层级地区、数值、可选多期时间 |
| [动态地图气泡图（分省）](https://hanabi.cn/h2/visualisation/dynamic_bubble_map_provincial) | 同层级地区、数值、可选多期时间 |

## event_timeline · 事件按时间与文字发展

需要：时间/日期、标题、事件、可选左右位置。
避免：不是数值趋势；不要编造事件时间。
Vox 动画：轴线展开、事件纸卡依次贴入。

| 样式 | 输入与核实状态 |
|---|---|
| [动态时间轴（新）](https://hanabi.cn/h2/visualisation/dynamic_timeline_chart2) | 官网数据指引为空；以下是按图形结构归纳的自绘字段：时间/日期、标题、事件、可选左右位置 |
| [动态时间轴图](https://hanabi.cn/h2/visualisation/dynamic_timeline_chart) | 五列时间轴：年份/时间小标题/框内文字/具体节点/事件。 |
| [时间轴](https://hanabi.cn/h2/visualisation/timeline_chart) | 位置时间、标题、事件、左右位置四列。 |

## progress_comparison · 独立指标的达成/进度

需要：对象、实际比例或目标/实际/区间。
避免：各环分母独立，不把同整体组成误画成独立目标达成；须明确100%含义。
Vox 动画：轮廓固定后弧/水位/实际条展开，贴目标说明。

| 样式 | 输入与核实状态 |
|---|---|
| [得分环](https://hanabi.cn/h2/visualisation/ring_gauge) | A为时间/右下文字，B起各项数值。 |
| [对比环形图](https://hanabi.cn/h2/visualisation/grouped_donut_chart) | 网站指引：2列；语义字段为对象、实际比例或目标/实际/区间；涉及大小的数值为非负。 |
| [水波图](https://hanabi.cn/h2/visualisation/liquid_fill_gauge) | 网站指引：2列；语义字段为对象、实际比例或目标/实际/区间；涉及大小的数值为非负。 |
| [子弹图](https://hanabi.cn/h2/visualisation/bullet_graph_chart) | A类别、B目标、C实际，E起区间带；D的角色未解释。 |
| [子弹图（竖）](https://hanabi.cn/h2/visualisation/bullet_vertical_chart) | A类别、B目标、C实际，E起区间带；D未解释。 |
| [对比环形图(半环)](https://hanabi.cn/h2/visualisation/grouped_donut_chart_half) | 网站指引：2列；语义字段为对象、实际比例或目标/实际/区间；涉及大小的数值为非负。 |
| [自定义水波图](https://hanabi.cn/h2/visualisation/custom_liquid_fiil_gauge) | 网站指引：2列；语义字段为对象、实际比例或目标/实际/区间；涉及大小的数值为非负。 |

## boxplot · 多组样本的分布

需要：类别和每组多个原始样本值。
避免：单个均值不能生成四分位数；说明异常值与须线规则。
Vox 动画：箱体先建立，再中位数/须线，圈分布差异。

| 样式 | 输入与核实状态 |
|---|---|
| [箱型图](https://hanabi.cn/h2/visualisation/box_plot) | A组名、B原始样本值，同组可多行。 |

## hierarchical_radial · 层级化的份额结构

需要：层级路径、末级非负值。
避免：父子汇总不得重复计数；没有层级不加层级。
Vox 动画：由父到子展开，聚焦一条层级路径。

| 样式 | 输入与核实状态 |
|---|---|
| [动态玫瑰图（环）](https://hanabi.cn/h2/visualisation/dynamic_stacked_rose_chart) | 前列为层级路径，末列非负值；动态时间映射说明不足，需确认实际表头。 |
| [动态玫瑰图](https://hanabi.cn/h2/visualisation/dynamic_stacked_rose_chart2) | 前列为层级路径，末列非负值；动态时间映射说明不足，需确认实际表头。 |
| [多级饼图](https://hanabi.cn/h2/visualisation/mult_level_pie_chart) | 前列为层级路径，末列非负值；动态时间映射说明不足，需确认实际表头。 |
| [多级环图](https://hanabi.cn/h2/visualisation/mult_level_donut_chart) | 前列为层级路径，末列非负值；动态时间映射说明不足，需确认实际表头。 |
| [交互旭日图](https://hanabi.cn/h2/visualisation/sunburst_chart) | 一级、二级、三级、数值四列。 |
| [旭日图](https://hanabi.cn/h2/visualisation/sunburst) | 层级路径各列，末列非负值，层数可变。 |
| [玫瑰图](https://hanabi.cn/h2/visualisation/stacked_rose_chart) | 前列为层级路径，末列非负值；动态时间映射说明不足，需确认实际表头。 |
| [玫瑰图(环)](https://hanabi.cn/h2/visualisation/stacked_rose_chart2) | 前列为层级路径，末列非负值；动态时间映射说明不足，需确认实际表头。 |

## rose · 类别在径向上编码大小的外观变体

需要：类别、非负值、明确半径/面积编码。
避免：普通组成优先饼图；不同半径同时改变面积，不用于细差精比。
Vox 动画：扇片顺序展开后稳住尺度，直接标数值。

| 样式 | 输入与核实状态 |
|---|---|
| [动态基础玫瑰图（环）](https://hanabi.cn/h2/visualisation/dynamic_rose_chart2) | 网站指引：2列；语义字段为类别、非负值、明确半径/面积编码；涉及大小的数值为非负。 |
| [动态基础玫瑰图](https://hanabi.cn/h2/visualisation/dynamic_rose_chart) | 网站指引：2列；语义字段为类别、非负值、明确半径/面积编码；涉及大小的数值为非负。 |
| [动态基础玫瑰图（半环）](https://hanabi.cn/h2/visualisation/dynamic_rose_chart3) | 网站指引：2列；语义字段为类别、非负值、明确半径/面积编码；涉及大小的数值为非负。 |
| [动态基础玫瑰图（半环竖）](https://hanabi.cn/h2/visualisation/dynamic_rose_chart4) | 网站指引：2列；语义字段为类别、非负值、明确半径/面积编码；涉及大小的数值为非负。 |
| [动态扇形玫瑰图](https://hanabi.cn/h2/visualisation/dynamic_quarter_rose_chart) | 网站指引：2列；语义字段为类别、非负值、明确半径/面积编码；涉及大小的数值为非负。 |
| [基础玫瑰图(环)](https://hanabi.cn/h2/visualisation/rose_chart2) | 网站指引：2列；语义字段为类别、非负值、明确半径/面积编码；涉及大小的数值为非负。 |
| [基础玫瑰图](https://hanabi.cn/h2/visualisation/rose_chart) | 网站指引：2列；语义字段为类别、非负值、明确半径/面积编码；涉及大小的数值为非负。 |
| [扇形玫瑰图](https://hanabi.cn/h2/visualisation/quarter_rose_chart) | 网站指引：2列；语义字段为类别、非负值、明确半径/面积编码；涉及大小的数值为非负。 |
| [基础玫瑰图(半环)](https://hanabi.cn/h2/visualisation/rose_chart3) | 网站指引：2列；语义字段为类别、非负值、明确半径/面积编码；涉及大小的数值为非负。 |
| [基础玫瑰图(半环竖)](https://hanabi.cn/h2/visualisation/rose_chart4) | 网站指引：2列；语义字段为类别、非负值、明确半径/面积编码；涉及大小的数值为非负。 |

## waterfall · 阶段数值变化或净贡献

需要：阶段顺序、level/delta口径、起终值。
避免：网站输入阶段实际值计算差，不能当成增减量累加。
Vox 动画：逐步连接阶段，再贴终值及净变化。

| 样式 | 输入与核实状态 |
|---|---|
| [动态瀑布图](https://hanabi.cn/h2/visualisation/dynamic_waterfall_chart) | A阶段名、B阶段实际值；网站自动计算相邻差。 |
| [瀑布图](https://hanabi.cn/h2/visualisation/waterfall_chart) | A阶段名、B实际值，自动计算相邻差。 |

## pie_donut · 一个整体的少量互斥类别份额

需要：类别、非负值、完整共同分母。
避免：重叠类别/独立百分比/负值不可闭合；不规则外观影响精度。
Vox 动画：按角度揭开扇片、贴外侧类别值、重点份额纸卡。

| 样式 | 输入与核实状态 |
|---|---|
| [基础饼图](https://hanabi.cn/h2/visualisation/pie_chart) | 网站指引：2列；语义字段为类别、非负值、完整共同分母；涉及大小的数值为非负。 |
| [不规则饼图](https://hanabi.cn/h2/visualisation/irregular_pie_chart) | 网站指引：2列；语义字段为类别、非负值、完整共同分母；涉及大小的数值为非负。 |
| [环图](https://hanabi.cn/h2/visualisation/donut_chart) | 网站指引：2列；语义字段为类别、非负值、完整共同分母；涉及大小的数值为非负。 |
| [半圆环图](https://hanabi.cn/h2/visualisation/semi_circle_donut_chart) | 网站指引：2列；语义字段为类别、非负值、完整共同分母；涉及大小的数值为非负。 |
| [扇形饼图](https://hanabi.cn/h2/visualisation/quarter_pie_chart) | 网站指引：2列；语义字段为类别、非负值、完整共同分母；涉及大小的数值为非负。 |

## funnel · 顺序阶段的留存/转化

需要：有顺序阶段、各阶段量、共同人群口径。
避免：普通排名不能因为递减就称漏斗；需实际转化过程。
Vox 动画：逐层贴入并标阶段率。

| 样式 | 输入与核实状态 |
|---|---|
| [漏斗图](https://hanabi.cn/h2/visualisation/funne_chart) | 网站指引：2列；语义字段为有顺序阶段、各阶段量、共同人群口径；涉及大小的数值为非负。 |

## circle_packing · 类别大小的面积展示

需要：类别、非负值、可选真实时间。
避免：半径须按面积换算；空隙不代表未分配份额。
Vox 动画：圆纸片按面积出现，重点对象加标签。

| 样式 | 输入与核实状态 |
|---|---|
| [动态圆堆图](https://hanabi.cn/h2/visualisation/dynamic_packed_circle_chart) | B为非负值，C起列头用于时点文字；A包含颜色组信息，详细映射需核实。 |
| [圆堆图](https://hanabi.cn/h2/visualisation/packed_circle_chart) | 类别、非负值、可选真实时间；涉及大小的数值为非负。 |

## treemap · 很多类别或层级的面积组成

需要：类别/层级路径、非负大小值。
避免：比较小差异不如条；面积与值成比例，父子别重复。
Vox 动画：矩形/多边形块贴入，重点块注释。

| 样式 | 输入与核实状态 |
|---|---|
| [动态树图](https://hanabi.cn/h2/visualisation/dynamic_treemap) | B为非负值，后续表头用于时点文字；逐期布局需核实。 |
| [树图](https://hanabi.cn/h2/visualisation/treemap) | 网站指引：2列；语义字段为类别/层级路径、非负大小值；涉及大小的数值为非负。 |
| [双层树图](https://hanabi.cn/h2/visualisation/multilevel-treemap) | 三列，末列为非负值；前两列用于层级。 |
| [沃罗诺伊树图](https://hanabi.cn/h2/visualisation/voronoi-treemap-rect) | 网站指引：2列；语义字段为类别/层级路径、非负大小值；涉及大小的数值为非负。 |
| [沃罗诺伊图](https://hanabi.cn/h2/visualisation/voronoi-treemap-circle) | 网站指引：2列；语义字段为类别/层级路径、非负大小值；涉及大小的数值为非负。 |

## area_trend · 量随时间累积、组成或范围

需要：有序时间、可加系列或下上界。
避免：堆叠与区间语义不同；河流图曲线不适合精确读取单项。
Vox 动画：时间方向揭开填充，重点时间贴注释。

| 样式 | 输入与核实状态 |
|---|---|
| [堆叠面积图](https://hanabi.cn/h2/visualisation/stacked_area_chart) | 有序时间、可加系列或下上界；涉及大小的数值为非负。 |
| [基础面积图](https://hanabi.cn/h2/visualisation/area_chart) | 有序时间、可加系列或下上界 |
| [河流图](https://hanabi.cn/h2/visualisation/stream_graph) | 有序时间、可加系列或下上界；涉及大小的数值为非负。 |
| [百分比堆叠面积图](https://hanabi.cn/h2/visualisation/percentage_stacked_area_chart) | 有序时间、可加系列或下上界；涉及大小的数值为非负。 |
| [区间面积图](https://hanabi.cn/h2/visualisation/range_area_chart) | 网站指引：3列；语义字段为有序时间、可加系列或下上界 |

## radar · 同对象多维轮廓

需要：指标、对象系列、同量纲或明确归一化。
避免：任意混单位会误导；多边形面积不是总体能力。
Vox 动画：轴稳定，逐对象轮廓展开，重点维度标注。

| 样式 | 输入与核实状态 |
|---|---|
| [雷达图](https://hanabi.cn/h2/visualisation/radar_chart) | 指标、对象系列、同量纲或明确归一化；涉及大小的数值为非负。 |
| [柱形雷达图](https://hanabi.cn/h2/visualisation/radar_bar_chart) | 指标、对象系列、同量纲或明确归一化；涉及大小的数值为非负。 |
| [星型雷达图](https://hanabi.cn/h2/visualisation/radar_star_chart) | 指标、对象系列、同量纲或明确归一化；涉及大小的数值为非负。 |

## wordcloud · 词语权重的概览

需要：词语、频次/权重。
避免：字体尺寸不是精确比例；普通数字类别优先其他图。
Vox 动画：词片有序贴入，突出核实高频词。

| 样式 | 输入与核实状态 |
|---|---|
| [词云](https://hanabi.cn/h2/visualisation/wordcloud) | 网站指引：2列；语义字段为词语、频次/权重；涉及大小的数值为非负。 |

## range · 类别的上下界

需要：类别、起/下界、终/上界。
避免：不是两时点变化，须先区分区间与配对值。
Vox 动画：范围纸条展开，端点稳定标注。

| 样式 | 输入与核实状态 |
|---|---|
| [区间条形图](https://hanabi.cn/h2/visualisation/range_bar_chart) | 网站指引：3列；语义字段为类别、起/下界、终/上界 |
| [区间柱状图](https://hanabi.cn/h2/visualisation/range_column_chart) | 网站指引：3列；语义字段为类别、起/下界、终/上界 |

## paired_change · 同对象的两个端点变化

需要：类别、前值、后值、时点/条件。
避免：需要配对同对象；不要把不确定性范围当前后变化。
Vox 动画：前点建立、后点出现、连接两点。

| 样式 | 输入与核实状态 |
|---|---|
| [哑铃图](https://hanabi.cn/h2/visualisation/dumbbell_plot2) | 网站指引：3列；语义字段为类别、前值、后值、时点/条件 |
| [哑铃图（竖）](https://hanabi.cn/h2/visualisation/dumbbell_chart) | 网站指引：3列；语义字段为类别、前值、后值、时点/条件 |

## polar_line · 有周期或极轴语义的系列

需要：极轴/周期类别、径向值。
避免：任意类别闭合线会制造循环；不同维度需同尺度。
Vox 动画：先轴、后径向线、贴周期重点。

| 样式 | 输入与核实状态 |
|---|---|
| [动态极坐标折线图](https://hanabi.cn/h2/visualisation/dynamic_radial_line) | 极轴/周期类别、径向值；涉及大小的数值为非负。 |
| [极坐标折线图](https://hanabi.cn/h2/visualisation/radial_line) | 极轴/周期类别、径向值；涉及大小的数值为非负。 |

## polar_bar · 周期/径向类别大小

需要：极轴类别、非负径向值。
避免：不是普通饼图份额；径向长度与面积不要混淆。
Vox 动画：由内向外展开，直接标值。

| 样式 | 输入与核实状态 |
|---|---|
| [极坐标柱状图](https://hanabi.cn/h2/visualisation/radial_column_chart) | 网站指引：2列；语义字段为极轴类别、非负径向值；涉及大小的数值为非负。 |

## radial_comparison · 同心弧条类别或堆叠比较

需要：类别、值、共同角度尺度、可选组成。
避免：外圈弧长天生更长；不用视觉长度代替数值。
Vox 动画：沿弧路径展开、标数值与尺度。

| 样式 | 输入与核实状态 |
|---|---|
| [基础玉珏图](https://hanabi.cn/h2/visualisation/radial_bar_chart) | 网站指引：2列；语义字段为类别、值、共同角度尺度、可选组成；涉及大小的数值为非负。 |
| [玉珏图(线)](https://hanabi.cn/h2/visualisation/radial_bar_chart2) | 网站指引：2列；语义字段为类别、值、共同角度尺度、可选组成；涉及大小的数值为非负。 |
| [堆叠玉珏图](https://hanabi.cn/h2/visualisation/stacked_radial_bar_chart) | 官网数据指引为空；以下是按图形结构归纳的自绘字段：类别、值、共同角度尺度、可选组成 |

## bubble · X/Y关联加第三量，或随时间移动

需要：对象、X、Y、大小、可选颜色/真实时间。
避免：数量大小映射面积；显式半径与面积字段要区分。
Vox 动画：先坐标、后圆纸片，多期才沿真实时间移动。

| 样式 | 输入与核实状态 |
|---|---|
| [动态气泡图](https://hanabi.cn/h2/visualisation/dynamic_bubble_chart) | 默认六列：名称、颜色组、时间、X、Y、面积大小；可调映射。 |
| [气泡图](https://hanabi.cn/h2/visualisation/bubble_chart) | 说明称五列，列出X/Y/名称/半径；控件另含颜色映射。 |

## scatter · 两个数值的关联

需要：成对X/Y、可选对象名。
避免：类别占比表不是散点；不能推断因果。
Vox 动画：坐标固定，点出现，圈重点区间。

| 样式 | 输入与核实状态 |
|---|---|
| [基础散点图](https://hanabi.cn/h2/visualisation/scatter_plot) | X、Y两列，第三列可选名称。 |

## network · 节点与联系强弱

需要：源、目标、权重、可选边描述/节点组。
避免：网络不自动代表流程或层级；力布局运动不是数据变化。
Vox 动画：节点先建立，边后画，随后冻结布局。

| 样式 | 输入与核实状态 |
|---|---|
| [关系力导向图](https://hanabi.cn/h2/visualisation/force_directed_graph) | 来源节点、目标节点、关系权重、边描述四列。 |
| [分组力导向图](https://hanabi.cn/h2/visualisation/grouped_force_directed_graph) | 来源节点、目标节点、关系权重三列。 |

## histogram · 一个数值变量的样本分布

需要：原始样本、分箱规则。
避免：不要把类别频数当原样本重新分箱。
Vox 动画：分箱尺度固定，箱柱展开，贴密集区说明。

| 样式 | 输入与核实状态 |
|---|---|
| [直方图](https://hanabi.cn/h2/visualisation/histogram) | 两列输入，其中B为原始样本；网站按箱数/箱宽分布。 |

## geographic_flow · 地点间的时序流量

需要：时间、源地区、目标地区、非负流量。
避免：线条粗细是流量，不是距离；须真实地点匹配。
Vox 动画：地图固定，路径画出，流量变化只用真实时间。

| 样式 | 输入与核实状态 |
|---|---|
| [动态地图流向图](https://hanabi.cn/h2/visualisation/dynamic_flow_map) | 时间、来源省份、目标省份、非负流量四列。 |

## gantt · 任务/活动起止与并行

需要：任务名、开始时间、结束时间。
避免：时间范围不能当上下数值范围；验证结束不早于开始。
Vox 动画：日期轴固定，任务纸条展开。

| 样式 | 输入与核实状态 |
|---|---|
| [甘特图](https://hanabi.cn/h2/visualisation/time_bar_chart) | 任务名、开始、结束三列，后两列为时间。 |

## flow · 节点之间的流量和连接

需要：源、目的、非负权重。
避免：桑基用于流量，弦用于互联结构；检查总入出及重复边。
Vox 动画：先节点/外环，再流带，重点流向纸卡。

| 样式 | 输入与核实状态 |
|---|---|
| [桑基图](https://hanabi.cn/h2/visualisation/sankey_diagram) | 来源、目的、非负流量三列。 |
| [弦图](https://hanabi.cn/h2/visualisation/chordDiagram) | 来源、目的、非负流量三列。 |
