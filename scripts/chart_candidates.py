#!/usr/bin/env python3
"""Recommend chart families from an already interpreted data profile, not column-name guesses."""
import argparse,json,math
from pathlib import Path

CATALOG=Path(__file__).resolve().parents[1]/'references/hanabi-catalog.json'
def recommend(p):
    def result(family,reason,alternatives=(),warnings=()):
        return {'family':family,'reason':reason,'alternatives':list(alternatives),'warnings':list(warnings),'requires_clarification':family is None}
    purpose=p.get('purpose')
    if not purpose:return result(None,'先确认数据表达组成、比较、趋势、关系等哪一种目的。')
    if p.get('locked_chart'):
        return {'locked_chart':p['locked_chart'],'family':None,'reason':'用户已指定图表结构，先核对有效性，保留结构；本工具不替换。','requires_clarification':False,'warnings':[],'alternatives':[]}
    values=p.get('values',[])
    if any(not isinstance(v,(int,float)) or isinstance(v,bool) or not math.isfinite(v) for v in values):
        return result(None,'输入含缺失或非有限数值；先处理口径，空值不能当零。')
    count=p.get('category_count',len(values))
    periods=p.get('time_points',1)
    if periods>1 and not p.get('real_time_confirmed'):
        return result(None,'存在多个时点的声明，但还没有核实真实时间数据。')
    if purpose=='composition':
        if not p.get('mutually_exclusive') or not p.get('complete_whole'):
            return result(None,'组成图需要确认类别互斥和完整共同分母。')
        if any(v<0 for v in values):return result(None,'负值不能直接做闭合组成图。')
        if values and sum(values)<=0:return result(None,'整体为零，无法计算份额。')
        warnings=[]
        if values and p.get('unit') in ('percent','%','fraction'):
            target=1 if p['unit']=='fraction' else 100
            tolerance=count*0.5*10**(-p.get('decimals',2))+1e-8
            if abs(sum(values)-target)>tolerance:return result(None,'份额合计超出四舍五入尾差，先核实分母/漏项。')
            if abs(sum(values)-target)>1e-8:warnings.append('角度按总和闭合，标签保留原值，说明四舍五入尾差。')
        if p.get('hierarchy'):return result('hierarchical_radial','需要表达层级组成。',('treemap',),warnings)
        if periods>1:return result('area_trend','组成随真实时间变化。',('stacked_composition',),warnings)
        if p.get('multiple_wholes'):return result('stacked_composition','比较多个整体的组成。',('pie_donut',),warnings)
        if count<=6 and count>=2:return result('pie_donut','单个完整整体由少量互斥类别组成。',('stacked_composition',),warnings)
        return result('treemap','类别较多，使用面积组成或分组展示。',('comparison',),warnings)
    if purpose=='comparison':
        if p.get('paired'):return result('paired_change','同对象两个条件或时点的配对比较。')
        if p.get('signed') or p.get('two_sided'):return result('diverging_comparison','有基准方向或两侧群体。')
        if p.get('series_count',1)>1:return result('grouped_comparison','同类别多个系列需对比。',('stacked_composition',))
        return result('comparison','重点是类别间大小比较。')
    if purpose=='trend':
        if periods<2:return result(None,'趋势需要至少两个真实时点，不能给单期数据编造时间。')
        return result('line_trend','数值沿真实有序时间变化。',('area_trend',))
    if purpose=='ranking_over_time':
        if periods<2:return result(None,'排名变化需要真实多期数据。')
        return result('ranking_over_time','对象排名/数值沿多期时间变化。')
    if purpose=='association':return result('bubble' if p.get('size_metric') else 'scatter','成对数值指标的关联，不推断因果。')
    if purpose=='distribution':
        if not p.get('raw_samples_confirmed'):return result(None,'尚未确认组内原始样本，不能从均值编造分布。')
        return result('boxplot' if p.get('multiple_groups') else 'histogram','使用原始样本分布，不能只用每组一个均值。')
    if purpose=='progress' and not p.get('denominator_known'):return result(None,'先确认进度的目标或分母。')
    lookup={'flow':'flow','network':'network','sets':'sets','geography':'geographic_distribution','geographic_flow':'geographic_flow',
            'events':'event_timeline','schedule':'gantt','range':'range','hierarchy':'tree_structure','progress':'progress_comparison',
            'matrix':'heatmap','ohlc':'candlestick','waterfall':'waterfall','multivariate':'parallel_coordinates','words':'wordcloud'}
    if purpose in lookup:return result(lookup[purpose],'依据已确认的数据关系选择对应家族。')
    return result(None,'未识别表达目的；请根据数据与用户任务解释关系，不默认柱状图。')

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--profile');ap.add_argument('--query');ap.add_argument('--family')
    a=ap.parse_args();catalog=json.loads(CATALOG.read_text())
    if a.profile:
        output=recommend(json.loads(Path(a.profile).read_text()))
        if output.get('family'):output['family_reference']=catalog['families'][output['family']]
    elif a.query:output=[c for c in catalog['charts'] if a.query in c['name']]
    elif a.family:output={'definition':catalog['families'].get(a.family),'charts':[c for c in catalog['charts'] if c['family']==a.family]}
    else:ap.error('Provide --profile, --query, or --family')
    print(json.dumps(output,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
