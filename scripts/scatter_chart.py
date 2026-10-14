"""One chart for a category and two quantitative fields; no discarded metrics."""
import math
from PIL import Image,ImageDraw
from collage import Scene,ease

class ScatterChart:
 def __init__(self,cfg,textures,font):
  self.cfg=cfg;self.rows=cfg['data'];self.s=Scene(1920,1080,textures,font);p=self.s.palette;self.colors=[p['primary']]
  theme=cfg.get('theme',{});title=theme.get('text');self.start=1.9 if title else .9;self.reveal=float(cfg.get('reveal_seconds',6.3));self.final=None
  if title and theme.get('source') not in ('user','user_delegated'):raise ValueError('Title requires user authorization')
  if not self.rows:raise ValueError('Empty scatter data')
  s=self.s;s.paper((1875,-40,100,1200),'accent',seed=84);s.paper((-40,960,660,200),'secondary',seed=53);self.bg=s.image.copy();self.title=Image.new('RGBA',(1920,1080))
  if title:
   s.image=self.title;size=82
   while s.font(size,True,'headline').getlength(title)>1630:size-=1
   s.paper((90,44,min(1720,max(1080,int(s.font(size,True,'headline').getlength(title))+80)),139),'secondary',seed=2,amplitude=12)
   c=p['secondary'];rgb=[int(c[i:i+2],16) for i in (1,3,5)];fill=p['ink'] if sum(v*k for v,k in zip(rgb,(.2126,.7152,.0722)))>155 else p['paper']
   s.text(title,(119,58),size,fill=fill,bold=True,role='headline');self.title=s.image.copy()
  s.image=Image.new('RGBA',(1920,1080));cardtop=245 if title else 95;s.paper((76,cardtop,1770,1002-cardtop),'paper',seed=12,amplitude=15);s.paper((115,cardtop-14,180,30),'accent',seed=24,amplitude=5)
  left,right,top,bottom=230,1680,365 if title else 220,865;xa,ya=cfg['x_axis'],cfg['y_axis']
  for axis in [xa,ya]:
   if axis['max']<=axis['min']:raise ValueError('Invalid scatter axis')
  px=lambda v:left+(float(v)-xa['min'])/(xa['max']-xa['min'])*(right-left)
  py=lambda v:bottom-(float(v)-ya['min'])/(ya['max']-ya['min'])*(bottom-top)
  for v in xa['ticks']:
   x=px(v);s.line([(x,top),(x,bottom)],p['grid'],1);s.text(f'{v:.{xa.get("precision",0)}f}',(x,bottom+22),26,fill=p['muted'],anchor='mt')
  for v in ya['ticks']:
   y=py(v);s.line([(left,y),(right,y)],p['grid'],1);s.text(f'{v:.{ya.get("precision",2)}f}',(left-24,y),26,fill=p['muted'],anchor='rm')
  s.line([(left,top),(left,bottom),(right,bottom)],p['primary'],3);s.text(ya['label'],(145,top-66),30,bold=True);s.text(xa['label'],(955,946),30,bold=True,anchor='mt');self.stages=[s.image.copy()]
  self.positions=[];occupied=[]
  for row in self.rows:
   xv,yv=float(row[xa['field']]),float(row[ya['field']])
   if not math.isfinite(xv+yv) or not xa['min']<=xv<=xa['max'] or not ya['min']<=yv<=ya['max']:raise ValueError('Nonfinite or out-of-range scatter value')
   self.positions.append((px(xv),py(yv)))
  for i,row in enumerate(self.rows):
   x,y=self.positions[i];name=str(row[cfg.get('category_field','name')]);detail=f"{row[xa['field']]}{xa.get('value_suffix','')} · {row[ya['field']]}{ya.get('value_suffix','')}";width=max(s.font(29,True).getlength(name),s.font(24).getlength(detail));height=65
   candidates=cfg.get('label_offsets',{}).get(str(i))
   offsets=[candidates] if candidates else [(22,-30),(22,20),(-width-22,-30),(-width-22,-75),(22,-75),(-width/2,25),(-width/2,-85)]
   chosen=None
   for dx,dy in offsets:
    box=(x+dx,y+dy,x+dx+width,y+dy+height)
    if not (110<=box[0] and box[2]<=1800 and top-12<=box[1] and box[3]<930):continue
    if any(not(box[2]+8<a or box[0]-8>c or box[3]+6<b or box[1]-6>d) for a,b,c,d in occupied):continue
    if any(box[0]-13<ox<box[2]+13 and box[1]-13<oy<box[3]+13 for k,(ox,oy) in enumerate(self.positions) if k!=i):continue
    chosen=box;break
   if chosen is None:raise ValueError(f'Label placement needs explicit label_offsets for {name}; do not omit it or split charts')
   occupied.append(chosen);s.image=self.stages[-1].copy();bx,by,ex,ey=chosen
   target=(max(bx,min(ex,x)),max(by,min(ey,y)))
   if math.dist((x,y),target)>30:s.line([(x,y),target],p['muted'],1)
   s.dot((x,y),13,p['secondary']);s.dot((x,y),9,p['primary']);s.text(name,(bx,by),29,bold=True,fill=p['primary']);s.text(detail,(bx,by+35),24,fill=p['ink']);self.stages.append(s.image.copy())
 def frame(self,t):
  if self.final is not None and t>=self.start+self.reveal:return self.final
  beat=math.floor(t*12)/12;progress=max(0,min(1,(beat-self.start)/self.reveal));n=min(len(self.rows),int(progress*len(self.rows)))
  im=self.bg.copy();im.alpha_composite(self.title,(-int(1750*(1-ease((beat-.05)/.6))),0));im.alpha_composite(self.stages[n],(0,int(1050*(1-ease((beat-(.75 if self.cfg.get('theme',{}).get('text') else .1))/.7)))))
  if progress>=1:self.final=im
  return im
