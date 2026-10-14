"""Reusable 16:9 collage charts. Input fields/semantics must be supplied by the agent."""
import math
from pathlib import Path
from PIL import Image,ImageDraw,ImageColor
from collage import Scene,ease

class ChartVideo:
 def __init__(self,cfg,textures,font):
  self.editorial=cfg.get('visual_profile')=='editorial';self.bar_tiles={};self.cfg=cfg;self.kind=cfg['chart_type'];self.rows=cfg['data'];self.series=cfg.get('series',[])
  if self.kind not in ('line','bar','pie','combo'):raise ValueError('Unsupported template: '+self.kind)
  if not self.rows:raise ValueError('No data')
  theme=cfg.get('theme',{})
  if theme.get('text') and theme.get('source') not in ('user','user_delegated'):raise ValueError('Title must come from user')
  if cfg.get('highlight') or cfg.get('extra_info_cards') or cfg.get('production_captions'):raise ValueError('Use a custom scene for explicitly requested editorial effects')
  self.has_title=bool(theme.get('text'));self.header_rows=len(cfg.get('title_lines') or [theme.get('text')]) if self.has_title else 0;self.s=Scene(1920,1080,textures,font);self.p=self.s.palette
  self.colors=[x.get('color',self.p['categorical'][i%len(self.p['categorical'])]) for i,x in enumerate(self.series)]
  self.stages={};self.final=None
  self.left,self.right,self.top,self.bottom=230,1690,(350 if self.header_rows==1 else 412 if self.has_title else 250),853
  if self.editorial:self.left,self.right=200,1700
  self.start=1.9 if self.has_title else .9;self.reveal=float(cfg.get('reveal_seconds',6.3))
  self._prepare()
 def empty(self):self.s.image=Image.new('RGBA',(1920,1080))
 def text(self,*args,**kwargs):return self.s.text(*args,**kwargs)
 def axis(self,axis):
  if axis['max']<=axis['min']:raise ValueError('Invalid axis range')
  return axis
 def py(self,v,axis):return self.bottom-(float(v)-axis['min'])/(axis['max']-axis['min'])*(self.bottom-self.top)
 def px(self,row,i):
  axis=self.cfg.get('x_axis',{});field=axis.get('field','year')
  if self.kind=='combo' and axis.get('type')=='category':
   return self.left+65+i/max(1,len(self.rows)-1)*(self.right-self.left-130)
  if self.kind in ('line','combo'):
   values=[float(r[field]) for r in self.rows];lo,hi=min(values),max(values)
   if hi<=lo:raise ValueError('Line needs at least two distinct x values')
   if values!=sorted(values) or len(set(values))!=len(values):raise ValueError('x values must be unique and increasing')
   pad=65 if self.kind=='combo' else 0
   return self.left+pad+(float(row[field])-lo)/(hi-lo)*(self.right-self.left-2*pad)
  return self.left+(i+.5)/len(self.rows)*(self.right-self.left)
 def _prepare(self):
  s,p=self.s,self.p
  team=p.get('id','').startswith('nba-')
  s.begin();s.paper((1875,-80,130,1240),'accent' if team else 'dark',seed=84,amplitude=16);s.paper((-50,930,690,220),'accent',seed=53,amplitude=16);self.bg=s.image.copy()
  self.title_layers=[]
  if self.has_title:
   lines=self.cfg.get('title_lines') or [self.cfg['theme']['text']]
   # Agent can split exact user title into lines, but cannot add text.
   normal=lambda x:''.join(str(x).split()).casefold()
   if normal(''.join(lines))!=normal(self.cfg['theme']['text']):raise ValueError('title_lines must preserve user title')
   if len(lines)>2:raise ValueError('At most two title lines')
   for i,line in enumerate(lines):
    self.empty();size=(54 if i==0 and len(lines)>1 else 82) if self.editorial else (64 if i==0 else 45)
    role='headline' if self.editorial and (i>0 or len(lines)==1) else 'body'
    while s.font(size,True,role).getlength(line)>1690:size-=1
    width=int(s.font(size,True,role).getlength(line))+80
    box=((1920-width)//2 if len(lines)==1 else 92,65,width,110) if i==0 else (101,191,width,73)
    if self.editorial:
     box=(92,35,width,88) if i==0 and len(lines)>1 else (92,140 if i else 45,min(1690,max(width,1080)),136)
    material=self.cfg.get('title_materials',[p.get('title_material','secondary') if team else 'dark','accent'])[i]
    base=p['ink'] if material=='dark' else p['secondary'] if material=='secondary' else p['primary']
    lum=sum(v*k for v,k in zip(ImageColor.getrgb(base),(.2126,.7152,.0722)));title_fill=p['ink'] if lum>155 else p['paper']
    s.paper(box,material,seed=2+i*2,amplitude=11);s.text(line,(box[0]+30,box[1]+10),size,fill=title_fill,bold=True,role=role);self.title_layers.append(s.image.copy())
  self.empty();card_top=235 if self.header_rows==1 else 296 if self.has_title else 90
  s.paper((76,card_top,1770,994-card_top),'paper',seed=12,amplitude=15)
  s.paper((118,card_top-14,180,32),'accent',seed=24,amplitude=5);s.paper((1620,977,160,29),'dark',seed=35,amplitude=5)
  if self.editorial:
   s.paper((1590,card_top-11,180,31),'accent',seed=84,amplitude=4)
   s.paper((120,card_top-9,155,25),'accent',seed=81,amplitude=4)
  if self.kind=='pie':self._prepare_pie();self.chart=s.image.copy();return
  if self.kind=='bar':self._prepare_bar();self.chart=s.image.copy();return
  if not self.series:raise ValueError('Series required')
  if self.kind=='bar' and len(self.series)!=1:raise ValueError('Bar template supports one series; use custom scene for grouped bars')
  if self.kind=='combo' and [x.get('role') for x in self.series]!=['bar','line']:raise ValueError('Combo requires one bar and one line series')
  yaxis=self.axis(self.cfg['y_axis']);self.yaxis=yaxis
  for tick in yaxis['ticks']:
   y=self.py(tick,yaxis);s.line([(self.left,y),(self.right,y)],fill=p['grid'],width=1);s.text(self.axis_label(tick,yaxis),(self.left-24,y),25,fill=p['muted'],anchor='rm')
  for i,row in enumerate(self.rows):
   x=self.px(row,i)
   if not self.editorial:s.line([(x,self.top),(x,self.bottom)],fill=p['grid'],width=1)
   s.text(str(row[self.cfg['x_axis']['field']]),(x,self.bottom+22),30 if self.editorial else 25,fill=p['ink'] if self.editorial else p['muted'],bold=self.editorial,anchor='mt')
  s.line([(self.left,self.top),(self.left,self.bottom),(self.right,self.bottom)],width=3)
  header_y=self.top-73
  s.text(yaxis.get('label',''),(145,header_y+36 if self.editorial else header_y),24 if self.editorial else 31,bold=not self.editorial);s.text(self.cfg['x_axis'].get('label',''),(960,931),30,bold=True,anchor='mt')
  for j,series in enumerate(self.series):
   x=(145+j*400 if self.editorial else 1280+j*230) if len(self.series)<=2 else 720+j*220
   color=self.colors[j]
   legend_y=header_y+13
   if self.editorial and series.get('role')=='bar':s.rectangle((x,legend_y-10,x+21,legend_y+11),fill=color)
   else:s.line([(x,legend_y),(x+49,legend_y)],fill=color,width=5);s.dot((x+24,legend_y),6,fill=color)
   s.text(series['name'],(x+35 if self.editorial and series.get('role')=='bar' else x+66,legend_y-17),30,bold=True,fill=color if self.editorial else p['ink'])
  if self.kind=='combo':
   rightaxis=self.axis(self.cfg['right_axis']);s.text(rightaxis['label'],(1732,self.top-36),25,fill=self.colors[1],anchor='rt')
   for tick in rightaxis['ticks']:s.text(self.axis_label(tick,rightaxis),(self.right+20,self.py(tick,rightaxis)),25,fill=self.colors[1] if self.editorial else p['muted'],anchor='lm')
   if not self.editorial:s.line([(self.right,self.top),(self.right,self.bottom)],width=2)
  self.positions=[]
  for j,series in enumerate(self.series):
   axis=self.cfg['right_axis'] if self.kind=='combo' and series['role']=='line' else yaxis
   vals=[float(r[series['field']]) for r in self.rows]
   if any(not math.isfinite(v) or not(axis['min']<=v<=axis['max']) for v in vals):raise ValueError('Non-finite value or outside axis')
   if (self.kind=='bar' or series.get('role')=='bar') and axis['min']!=0:raise ValueError('Bar axis must start at zero')
   self.positions.append([(self.px(r,i),self.py(r[series['field']],axis)) for i,r in enumerate(self.rows)])
  self.chart=s.image.copy()
 def axis_label(self,value,axis):return f'{value:.{axis.get("precision",1)}f}'+axis.get('suffix','')
 def _prepare_bar(self):
  cfg,s,p=self.cfg,self.s,self.p
  if len(self.rows)>12:raise ValueError('Use custom layout for more than 12 bars')
  axis=self.axis(cfg['value_axis'])
  if axis['min']!=0:raise ValueError('Bar axis must start at zero')
  self.left,self.right=480,1590
  self.bar_height=min(44,(self.bottom-self.top)/len(self.rows)*.6)
  self.colors=[self.p['primary'] if self.p.get('id','').startswith('nba-') else self.p['ink']];positions=[]
  for i,row in enumerate(self.rows):
   v=float(row[cfg['value_field']])
   if not math.isfinite(v) or not 0<=v<=axis['max']:raise ValueError('Invalid bar value')
   y=self.top+(i+.5)/len(self.rows)*(self.bottom-self.top);x=self.left+v/axis['max']*(self.right-self.left);positions.append((x,y))
   label=str(row[cfg['category_field']])
   if s.font(30,True).getlength(label)>310:raise ValueError('Category label needs custom layout')
   s.text(label,(self.left-25,y),30,bold=True,anchor='rm')
  for tick in axis['ticks']:
   x=self.left+float(tick)/axis['max']*(self.right-self.left);s.line([(x,self.top),(x,self.bottom)],fill=p['grid'],width=1);s.text(self.axis_label(tick,axis),(x,self.bottom+22),25,fill=p['muted'],anchor='mt')
  s.line([(self.left,self.top),(self.left,self.bottom),(self.right,self.bottom)],width=3)
  s.text(axis.get('label',''),(1035,931),30,bold=True,anchor='mt')
  self.positions=[positions];self.series=[{'field':cfg['value_field'],'name':axis.get('label','')}]
 def _prepare_pie(self):
  cfg,s,p=self.cfg,self.s,self.p
  if not cfg.get('complete_whole') or not cfg.get('categories_mutually_exclusive'):raise ValueError('Pie requires confirmed complete whole and exclusive categories')
  field=cfg['value_field'];values=[float(r[field]) for r in self.rows]
  if any(not math.isfinite(v) or v<0 for v in values) or sum(values)<=0:raise ValueError('Pie requires nonnegative finite values and positive total')
  if len(values)>8:raise ValueError('Use a custom layout for more than eight pie categories')
  self.pie_tiles={};self.angles=[];cursor=-90
  for v in values:self.angles.append((cursor,cursor+360*v/sum(values)));cursor+=360*v/sum(values)
  self.pie_box=(340,350 if self.has_title else 230,980,990 if self.has_title else 870)
  self.pie_labels=[]
  cx,cy=(self.pie_box[0]+self.pie_box[2])/2,(self.pie_box[1]+self.pie_box[3])/2;radius=320
  for i,row in enumerate(self.rows):
   y=(410 if self.has_title else 290)+i*77;s.rectangle((1160,y,1186,y+26),fill=p['categorical'][i%len(p['categorical'])]);s.text(str(row[cfg['category_field']]),(1210,y-4),34,bold=True)
   a,b=self.angles[i];theta=math.radians((a+b)/2);span=b-a
   if span<=0:continue
   color=ImageColor.getrgb(p['categorical'][i%len(p['categorical'])]);light=sum(v*k for v,k in zip(color,(.2126,.7152,.0722)))>155
   text=self.value_label(row[field])+cfg.get('value_suffix','');f=s.font(48,True,'number')
   if span<22:
    x=cx+radius*1.12*math.cos(theta);y=cy+radius*1.12*math.sin(theta);fill=p['ink'];leader=[(cx+radius*.96*math.cos(theta),cy+radius*.96*math.sin(theta)),(x,y)]
   else:
    x=cx+radius*.65*math.cos(theta);y=cy+radius*.65*math.sin(theta);fill=p['ink'] if light else '#F7F4E9';leader=None
    while f.getlength(text)>2*radius*.65*math.sin(math.radians(span/2))*.9 and f.size>32:f=s.font(f.size-1,True,'number')
   self.pie_labels.append((b,text,(x,y),f,fill,leader))
 def value_label(self,v):return str(v) if self.cfg.get('preserve_value_labels') else f'{float(v):.{self.cfg.get("value_precision",2)}f}'
 def draw_bar(self,im,x,y):
  width=max(0,int(x-self.left));height=max(1,int(self.bar_height))
  if not width:return
  key=('horizontal',width,height)
  if key not in self.bar_tiles:
   material='accent' if self.p.get('id','').startswith('nba-') else 'dark'
   self.bar_tiles[key]=self.s.textures[material].resize((width,height),Image.Resampling.BILINEAR)
  im.alpha_composite(self.bar_tiles[key],(int(self.left),int(y-self.bar_height/2)))
 def _node(self,im,j,i):
  row=self.rows[i];series=self.series[j];x,y=self.positions[j][i];color=self.colors[j];d=ImageDraw.Draw(im)
  if self.kind=='bar':
   self.draw_bar(im,x,y)
   d.text((x+16,y),self.value_label(row[series['field']])+self.cfg.get('value_suffix',''),font=self.s.font(27,True),fill=color,anchor='lm')
   return
  if series.get('role')=='bar':
   width=min(108 if self.editorial else 70,(self.right-self.left)/len(self.rows)*.55)
   if self.editorial:
    height=max(1,int(self.bottom-y));key=(j,i,height)
    if key not in self.bar_tiles:
     material=series.get('materials',{}).get(str(row[self.cfg['x_axis']['field']]),series.get('material','dark'));self.bar_tiles[key]=self.s.textures[material].resize((int(width),height),Image.Resampling.BILINEAR)
    im.alpha_composite(self.bar_tiles[key],(int(x-width/2),int(y)))
   else:d.rectangle((x-width/2,y,x+width/2,self.bottom),fill=color)
  else:d.ellipse((x-10,y-10,x+10,y+10),fill=self.p['paper']);d.ellipse((x-7,y-7,x+7,y+7),fill=color)
  if self.editorial and series.get('role')=='line' and not series.get('show_values',False):return
  above=not(self.kind=='combo' and series.get('role')=='line')
  if self.kind=='line' and len(self.series)==2:above=y<self.positions[1-j][i][1]
  label_y=y-24 if above else y+24;label_x=x+(38 if self.kind=='line' and i==0 else 0)
  d.text((label_x,label_y),self.value_label(row[series['field']])+series.get('value_suffix',''),font=self.s.font(38 if self.editorial and series.get('role')=='bar' else 25,True),fill=color,anchor='ms' if above else 'mt',stroke_width=0 if self.editorial else 4,stroke_fill=self.p['paper'])
 def stage(self,n):
  if n in self.stages:return self.stages[n]
  im=self.chart.copy();d=ImageDraw.Draw(im)
  if self.kind=='combo':
   for j,series in enumerate(self.series):
    if series.get('role')=='bar':
     for i in range(n):self._node(im,j,i)
  for j,series in enumerate(self.series):
   if self.kind=='line' or series.get('role')=='line':
    pts=self.positions[j][:n]
    if len(pts)>1:
     if self.editorial:d.line(pts,fill=self.p['paper'],width=10,joint='curve')
     d.line(pts,fill=self.colors[j],width=5 if self.editorial else 6,joint='curve')
  for j in range(len(self.series)):
   if self.kind=='combo' and self.series[j].get('role')=='bar':continue
   for i in range(n):self._node(im,j,i)
  self.stages[n]=im;return im
 def frame(self,t):
  total=len(self.rows);progress=max(0,min(1,(t-self.start)/self.reveal))
  if t>=self.start+self.reveal:
   if self.final is None:
    if self.kind=='pie':self.final=self._pie_frame(1)
    else:self.final=self._compose(self.stage(total),t)
   return self.final
  if self.kind=='pie':
   if self.cfg.get('motion_steps_per_second'):
    hz=float(self.cfg['motion_steps_per_second']);progress=max(0,min(1,math.floor(max(0,t-self.start)*hz)/(hz*self.reveal)))
   return self._pie_frame(progress,t)
  if t<self.start:page=self.chart
  elif self.kind=='line' or self.kind=='combo':
   pos=progress*(total-1);index=int(pos);part=pos-index;page=self.stage(index+1).copy();d=ImageDraw.Draw(page)
   for j,series in enumerate(self.series):
    if index+1<total and (self.kind=='line' or series.get('role')=='line'):
     a,b=self.positions[j][index:index+2];d.line([a,(a[0]+(b[0]-a[0])*part,a[1]+(b[1]-a[1])*part)],fill=self.colors[j],width=6)
  else:
   pos=progress*total;index=min(total-1,int(pos));part=[0,.12,.32,.58,.82,1][min(5,int((pos-index)*6))];page=self.stage(index).copy();x,y=self.positions[0][index];self.draw_bar(page,self.left+(x-self.left)*part,y)
  return self._compose(page,t)
 def _pie_frame(self,progress,t=100):
  page=self.chart.copy();d=ImageDraw.Draw(page);end=-90+360*progress
  for i,(a,b) in enumerate(self.angles):
   if end>a:
    if self.editorial:
     x,y,right,bottom=self.pie_box;w,h=right-x,bottom-y
     if i not in self.pie_tiles:self.pie_tiles[i]=self.s.textures['category_'+str(i%len(self.p['categorical'])+1)].resize((w,h),Image.Resampling.BILINEAR)
     mask=Image.new('L',(w,h));ImageDraw.Draw(mask).pieslice((0,0,w,h),a,min(b,end),fill=255);page.paste(self.pie_tiles[i],(x,y),mask);d=ImageDraw.Draw(page);d.pieslice(self.pie_box,a,min(b,end),outline=self.p['paper'],width=4)
    else:d.pieslice(self.pie_box,a,min(b,end),fill=self.p['categorical'][i%len(self.p['categorical'])],outline=self.p['paper'],width=4)
  for b,text,xy,f,fill,leader in self.pie_labels:
   if end>=b-1e-6:
    if leader:d.line(leader,fill=self.p['ink'],width=2)
    d.text(xy,text,font=f,fill=fill,anchor='mm')
  return self._compose(page,t)
 def _compose(self,page,t):
  im=self.bg.copy();beat=math.floor(t*12)/12
  for i,layer in enumerate(self.title_layers):im.alpha_composite(layer,(-int(1700*(1-ease((beat-.05-i*.35)/.55))),0))
  cy=int(1040*(1-ease((beat-(.95 if self.has_title else .1))/.65)));im.alpha_composite(page,(0,cy));return im
