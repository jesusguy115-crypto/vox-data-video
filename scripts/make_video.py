#!/usr/bin/env python3
"""Table -> deterministic scene -> preview -> video, with end-to-end timings."""
from pathlib import Path
import argparse,csv,json,subprocess,sys,time,hashlib,math,platform,re,os

def nice_axis(values,zero=False):
 lo,hi=min(values),max(values);span=hi-(0 if zero else lo)
 if span<=0:span=max(abs(hi)*.2,1)
 raw=span/6;power=10**math.floor(math.log10(raw));step=next(x*power for x in [1,2,2.5,5,10] if x*power>=raw)
 low=0 if zero else math.floor((lo-span*.06)/step)*step;high=math.ceil((hi+span*.06)/step)*step
 ticks=[round(low+i*step,10) for i in range(round((high-low)/step)+1)]
 return {'min':low,'max':high,'ticks':ticks,'precision':max(0,-math.floor(math.log10(step)))}

def read_image(path,cache,scripts):
 if platform.system()!='Darwin':raise RuntimeError('Image input needs macOS OCR or a verified table JSON/CSV. No silent transcription fallback.')
 source=scripts/'ocr_table.swift';key=hashlib.sha256(source.read_bytes()).hexdigest()[:12];binary=cache/('ocr-'+key)
 if not binary.exists():subprocess.run(['swiftc','-O','-module-cache-path',str(cache/'swift-cache'),str(source),'-o',str(binary)],check=True)
 tokens=json.loads(subprocess.check_output([str(binary),str(path)]));tokens=[t for t in tokens if t['text'].strip() not in ['↑','↓','↕','↔']];groups=[]
 for item in sorted(tokens,key=lambda x:(x['y'],x['x'])):
  if item['confidence']<.2:raise ValueError('Low-confidence OCR: verify source before rendering')
  if not groups or abs(item['y']-sum(x['y'] for x in groups[-1])/len(groups[-1]))>max(.009,item['height']*.5):groups.append([])
  groups[-1].append(item)
 grid=[[x['text'].strip() for x in sorted(g,key=lambda x:x['x'])] for g in groups]
 # Remove spreadsheet column-letter chrome and standalone row-number cells.
 if grid and all(re.fullmatch(r'[A-Z]\s*[↑↓↕↔]?',x) for x in grid[0]):grid.pop(0)
 width=max(map(len,grid))
 if all(r and r[0].isdigit() and int(r[0])==i+1 for i,r in enumerate(grid)):grid=[r[1:] for r in grid]
 if not grid or any(len(r)!=len(grid[0]) for r in grid):
  (cache/'ocr-unverified.json').write_text(json.dumps({'tokens':tokens,'rows':grid},ensure_ascii=False,indent=2));raise ValueError('OCR cell grid ambiguous; verify cached rows once, never guess missing cells')
 return {'columns':grid[0],'rows':grid[1:],'ocr':True}

def plan(table,chart,theme,palette,metric,unit):
 columns=table['columns'];rows=table['rows']
 if not rows or any(len(r)!=len(columns) for r in rows):raise ValueError('Nonrectangular or empty table')
 # Deduplicate columns only when header and every cell are identical.
 keep=[]
 for j,col in enumerate(columns):
  if not any(col==columns[k] and all(r[j]==r[k] for r in rows) for k in keep):keep.append(j)
 columns=[columns[k] for k in keep];rows=[[r[k] for k in keep] for r in rows]
 def number(x):
  v=float(str(x).strip().replace(',','').rstrip('%'))
  if not math.isfinite(v):raise ValueError('Nonfinite data')
  return v
 def year(x):
  try:return str(x).strip().isdigit() and 1000<=int(x)<=3000
  except (ValueError,TypeError):return False
 common={'preserve_value_labels':True,'palette_id':palette,'width':1920,'height':1080,'fps':30,'duration':14,'value_precision':2,'theme':{'text':theme,'source':'user' if theme else 'user_delegated'},'highlight':None,'extra_info_cards':False,'production_captions':False}
 ylabel=(metric or '数值')+(f'（{unit}）' if unit else '')
 if len(columns)>2 and all(year(c) for c in columns[1:]):
  years=list(map(int,columns[1:]));data=[{'name':str(r[0]),'values':{str(y):str(r[j+1]) for j,y in enumerate(years)}} for r in rows]
  for r in data:
   for v in r['values'].values():number(v)
  chosen=chart if chart!='auto' else 'packed_circle' if len(data)>=8 else 'line'
  if chosen=='packed_circle':return {**common,'chart_type':chosen,'data':data,'years':years,'reveal_seconds':10,'theme':common['theme'] if theme else {'text':'各类历年数值变化','source':'user_delegated'}},'多对象多时期；圆面积编码非负数值，避免密集折线'
  if chosen!='line':raise ValueError('Selected chart incompatible with time-wide table')
  converted={'columns':['年份']+[r['name'] for r in data],'rows':[[y]+[r['values'][str(y)] for r in data] for y in years]}
  return plan(converted,'line',theme,palette,metric,unit)
 if len(columns)>=2 and all(year(r[0]) for r in rows):
  if chart not in ('auto','line'):raise ValueError('Chart incompatible with series table')
  data=[{'x':int(r[0]),**{f'v{j}':str(r[j]) for j in range(1,len(columns))}} for r in rows];values=[number(r[j]) for r in rows for j in range(1,len(columns))]
  return {**common,'chart_type':'line','data':data,'x_axis':{'field':'x','label':str(columns[0])},'y_axis':{**nice_axis(values),'label':ylabel},'series':[{'name':str(columns[j]),'field':f'v{j}'} for j in range(1,len(columns))],'theme':common['theme'] if theme else {'text':'历年数值变化','source':'user_delegated'}},'时间序列共用同一尺度'
 if len(columns)==2:
  vals=[number(r[1]) for r in rows];shares=('占比' in str(columns[1]) or '%' in str(columns[1]) or '比例' in str(columns[1])) and abs(sum(vals)-100)<.1 and min(vals)>=0
  chosen=chart if chart!='auto' else 'pie' if shares and len(rows)<=8 else 'bar';data=[{'name':str(r[0]),'value':str(r[1]).rstrip('%')} for r in rows]
  if chosen=='pie':
   if not shares:raise ValueError('Pie requires verified whole proportions; use an explicit normalized scene for other whole data')
   return {**common,'chart_type':'pie','data':data,'category_field':'name','value_field':'value','value_suffix':'%','complete_whole':True,'categories_mutually_exclusive':True,'theme':common['theme'] if theme else {'text':'各类占比分布','source':'user_delegated'}},'完整占比、少量类别'
  if chosen!='bar':raise ValueError('Chart incompatible with category-value table')
  return {**common,'chart_type':'bar','data':data,'category_field':'name','value_field':'value','value_axis':{**nice_axis(vals,True),'label':ylabel},'theme':common['theme'] if theme else {'text':'各类数值对比','source':'user_delegated'}},'类别与单指标的大小比较'
 raise ValueError('Complex data needs a verified normalized scene; never silently substitute a chart')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--table',required=True);ap.add_argument('--out');ap.add_argument('--work',required=True);ap.add_argument('--chart',choices=['auto','line','bar','pie','packed_circle'],default='auto');ap.add_argument('--cache');ap.add_argument('--no-theme',action='store_true');ap.add_argument('--theme');ap.add_argument('--palette',default='classic-paper');ap.add_argument('--metric');ap.add_argument('--unit');ap.add_argument('--preview-only',action='store_true');a=ap.parse_args()
 started=time.perf_counter();work=Path(a.work).resolve();work.mkdir(parents=True,exist_ok=True);scripts=Path(__file__).resolve().parent;path=Path(a.table);shared=Path(a.cache or os.environ.get('VOX_VIDEO_CACHE',str(Path.home()/'Documents/Codex/.vox-video-cache' if (Path.home()/'Documents/Codex').is_dir() else Path.home()/'.cache/vox-data-video'))).resolve();shared.mkdir(parents=True,exist_ok=True)
 if path.suffix.lower()=='.json':table=json.loads(path.read_text())
 elif path.suffix.lower() in ('.csv','.tsv'):
  with path.open(newline='',encoding='utf-8-sig') as f:grid=list(csv.reader(f,delimiter='\t' if path.suffix=='.tsv' else ','))
  table={'columns':grid[0],'rows':grid[1:]}
 elif path.suffix.lower() in ('.png','.jpg','.jpeg','.webp'):table=read_image(path,shared,scripts)
 elif path.suffix.lower()=='.xlsx':
  from read_table import xlsx
  document=xlsx(path)
  if document['warnings']:raise ValueError('Spreadsheet requires formula/error verification: '+str(document['warnings']))
  sheets=[s for s in document['sheets'] if s['state']=='visible']
  if len(sheets)!=1:raise ValueError('Select the sheet explicitly before processing a multi-sheet workbook')
  cells={}
  for cell in sheets[0]['cells']:
   letters,row=re.fullmatch(r'([A-Z]+)([0-9]+)',cell['cell']).groups();column=0
   for letter in letters:column=column*26+ord(letter)-64
   cells[int(row),column]=cell['value']
  maximum_row=max(r for r,c in cells);maximum_column=max(c for r,c in cells)
  grid=[[cells.get((r,c)) for c in range(1,maximum_column+1)] for r in range(1,maximum_row+1)]
  if any(v is None for row in grid for v in row):raise ValueError('Blank/merged cells require verification')
  table={'columns':grid[0],'rows':grid[1:]}
 else:raise ValueError('Supply JSON/CSV/TSV/XLSX/image')
 read=time.perf_counter();cfg,reason=plan(table,a.chart,a.theme,a.palette,a.metric,a.unit)
 if a.no_theme:cfg['theme']={'text':None,'source':'not_provided'}
 scene=work/'scene.json';scene.write_text(json.dumps(cfg,ensure_ascii=False,indent=2));planned=time.perf_counter()
 cmd=[sys.executable,str(scripts/'render_video.py'),'--scene',str(scene),'--cache',str(shared)]
 if a.preview_only:cmd+=['--preview-only']
 else:
  if not a.out:raise ValueError('--out required')
  cmd+=['--out',a.out,'--report',str(work/'render.json')]
 subprocess.run(cmd,check=True);end=time.perf_counter();report={'table_read_seconds':round(read-started,3),'planning_seconds':round(planned-read,3),'remaining_pipeline_seconds':round(end-planned,3),'automation_total_seconds':round(end-started,3),'chart':cfg['chart_type'],'reason':reason,'rows':len(table['rows']),'theme_source':cfg['theme']['source'],'excluded':'对话等待、人工核对和首次安装不在自动流程计时内'};(work/'pipeline.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
