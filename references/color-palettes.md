# NBA 球队 Logo 配色

这套 Skill 主要用于 NBA 内容。可选经典纸黄＋NBA 30 队 Logo 配色，不再将旧九套通用方案作为新任务主菜单。**用户没选择时直接用 classic-paper 经典纸黄**，不根据标题或球员自动套球队。

每次新任务提供一次可选入口，用户可说球队中文名、nba-球队ID，或“默认”。已有本次选择不重复问。配色选择不是审批；未选择用默认继续，用户明确说要选色则等待其实际选择。主题和单位可在同一入口询问。默认不随上一次非默认选择改变。

颜色依据2026-10-14读取的 NBA 官方 CDN 主 Logo；来源、原色和文件哈希在 nba-logo-sources.json。SVG 未声明 fill 的路径使用默认黑色。当前 Logo 颜色可能与历史队徽或球衣色不同，不把记忆中的配色当作已查证结果。基于 Logo 原色派生纸底、墨色和同色明暗层级，不声称这些衍生色都是官方品牌色；单色队伍尤其需要层级和直接标签。NBA 官方球队目录 https://www.nba.com/teams 。只提取颜色，不将 Logo 默认放进用户视频，不暗示球队官方出品。

| 球队 | ID | 主色 / 辅色 | 来源 |
|---|---|---|---|
| 老鹰 | `nba-hawks` | #E03A3E / #111111 | [官方 Logo](https://cdn.nba.com/logos/nba/1610612737/primary/L/logo.svg) |
| 凯尔特人 | `nba-celtics` | #008348 / #BB9753 | [官方 Logo](https://cdn.nba.com/logos/nba/1610612738/primary/L/logo.svg) |
| 篮网 | `nba-nets` | #000000 / #737373 | [官方 Logo](https://cdn.nba.com/logos/nba/1610612751/primary/L/logo.svg) |
| 黄蜂 | `nba-hornets` | #00788C / #1D1160 | [官方 Logo](https://cdn.nba.com/logos/nba/1610612766/primary/L/logo.svg) |
| 公牛 | `nba-bulls` | #CD1F43 / #000000 | [官方 Logo](https://cdn.nba.com/logos/nba/1610612741/primary/L/logo.svg) |
| 骑士 | `nba-cavaliers` | #860038 / #BC945C | [官方 Logo](https://cdn.nba.com/logos/nba/1610612739/primary/L/logo.svg) |
| 独行侠 | `nba-mavericks` | #0064B1 / #061922 | [官方 Logo](https://cdn.nba.com/logos/nba/1610612742/primary/L/logo.svg) |
| 掘金 | `nba-nuggets` | #0D2240 / #FFC627 | [官方 Logo](https://cdn.nba.com/logos/nba/1610612743/primary/L/logo.svg) |
| 活塞 | `nba-pistons` | #1D428A / #C8102E | [官方 Logo](https://cdn.nba.com/logos/nba/1610612765/primary/L/logo.svg) |
| 勇士 | `nba-warriors` | #1D428A / #FDB927 | [官方 Logo](https://cdn.nba.com/logos/nba/1610612744/primary/L/logo.svg) |
| 火箭 | `nba-rockets` | #CE0E2D / #FFD520 | [官方 Logo](https://cdn.nba.com/logos/nba/1610612745/primary/L/logo.svg) |
| 步行者 | `nba-pacers` | #0C2340 / #FFD520 | [官方 Logo](https://cdn.nba.com/logos/nba/1610612754/primary/L/logo.svg) |
| 快船 | `nba-clippers` | #12173F / #7D7F95 | [官方 Logo](https://cdn.nba.com/logos/nba/1610612746/primary/L/logo.svg) |
| 湖人 | `nba-lakers` | #542C81 / #FAB624 | [官方 Logo](https://cdn.nba.com/logos/nba/1610612747/primary/L/logo.svg) |
| 灰熊 | `nba-grizzlies` | #5D76A9 / #12173F | [官方 Logo](https://cdn.nba.com/logos/nba/1610612763/primary/L/logo.svg) |
| 热火 | `nba-heat` | #961A31 / #F9A11E | [官方 Logo](https://cdn.nba.com/logos/nba/1610612748/primary/L/logo.svg) |
| 雄鹿 | `nba-bucks` | #00471A / #EDE0C5 | [官方 Logo](https://cdn.nba.com/logos/nba/1610612749/primary/L/logo.svg) |
| 森林狼 | `nba-timberwolves` | #1D428A / #009A44 | [官方 Logo](https://cdn.nba.com/logos/nba/1610612750/primary/L/logo.svg) |
| 鹈鹕 | `nba-pelicans` | #0A2240 / #B4975A | [官方 Logo](https://cdn.nba.com/logos/nba/1610612740/primary/L/logo.svg) |
| 尼克斯 | `nba-knicks` | #1D428A / #F58426 | [官方 Logo](https://cdn.nba.com/logos/nba/1610612752/primary/L/logo.svg) |
| 雷霆 | `nba-thunder` | #057DC1 / #EE3C33 | [官方 Logo](https://cdn.nba.com/logos/nba/1610612760/primary/L/logo.svg) |
| 魔术 | `nba-magic` | #0050B5 / #061922 | [官方 Logo](https://cdn.nba.com/logos/nba/1610612753/primary/L/logo.svg) |
| 76人 | `nba-76ers` | #1D428A / #C8102E | [官方 Logo](https://cdn.nba.com/logos/nba/1610612755/primary/L/logo.svg) |
| 太阳 | `nba-suns` | #E46025 / #000000 | [官方 Logo](https://cdn.nba.com/logos/nba/1610612756/primary/L/logo.svg) |
| 开拓者 | `nba-trail-blazers` | #CF0A2C / #000000 | [官方 Logo](https://cdn.nba.com/logos/nba/1610612757/primary/L/logo.svg) |
| 国王 | `nba-kings` | #592D81 / #63717A | [官方 Logo](https://cdn.nba.com/logos/nba/1610612758/primary/L/logo.svg) |
| 马刺 | `nba-spurs` | #000000 / #C2CCD2 | [官方 Logo](https://cdn.nba.com/logos/nba/1610612759/primary/L/logo.svg) |
| 猛龙 | `nba-raptors` | #BC2126 / #000000 | [官方 Logo](https://cdn.nba.com/logos/nba/1610612761/primary/L/logo.svg) |
| 爵士 | `nba-jazz` | #4E008E / #9E73C1 | [官方 Logo](https://cdn.nba.com/logos/nba/1610612762/primary/L/logo.svg) |
| 奇才 | `nba-wizards` | #002B5C / #E21936 | [官方 Logo](https://cdn.nba.com/logos/nba/1610612764/primary/L/logo.svg) |

完整角色和分类色在 palettes.json，预览在 assets/palette-preview.png。系列身份全片一致；跨球队数据若要每队自身色，需用户选择该方案，否则沿本次选定主题配色。正负/连续量不使用无序分类色。纸张与跳切风格不随配色改变。

legacy-palettes.json 仅保留旧场景复现兼容，不出现在新配色菜单。用户明确复现森林橙等旧片时仍可执行旧 ID；这个兼容例外不把旧方案重新加入 NBA 菜单。
