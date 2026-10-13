"""Deterministic area-proportional circle packing; changing radii, stable identities."""
import math
from PIL import Image,ImageDraw
from collage import Scene,ease

def pack(radii):
 order=sorted(range(len(radii)),key=lambda i:(-radii[i],i));placed=[];result=[None]*len(radii)
 for i in order:
  r=radii[i]+3
  if not placed:x,y=0.,0.
  else:
   candidates=[]
   for ax,ay,ar in placed:
    for k in range(48):
     a=k*math.tau/48;candidates.append((ax+(ar+r)*math.cos(a),ay+(ar+r)*math.sin(a)))
   for n,(ax,ay,ar) in enumerate(placed):
    for bx,by,br in placed[n+1:]:
     dx,dy=bx-ax,by-ay;dist=math.hypot(dx,dy);ra,rb=ar+r,br+r
     if not dist or dist>ra+rb or dist<abs(ra-rb):continue
     along=(ra*ra-rb*rb+dist*dist)/(2*dist);high=math.sqrt(max(0,ra*ra-along*along));mx,my=ax+along*dx/dist,ay+along*dy/dist
     candidates.extend([(mx-high*dy/dist,my+high*dx/dist),(mx+high*dy/dist,my-high*dx/dist)])
   valid=[(max(math.hypot(x,y)+r,max(math.hypot(a,b)+c for a,b,c in placed)),x*x+y*y,y,x) for x,y in candidates if all(math.hypot(x-a,y-b)>=r+c-.01 for a,b,c in placed)]
   if not valid:raise ValueError('Packing failed')
   _,_,y,x=min(valid)
  placed.append((x,y,r));result[i]=(x,y)
 return result

class PackedVideo:
 def __init__(self,cfg,textures,font):
  self.cfg=cfg;self.rows=cfg['data'];self.years=cfg['years'];self.start=1.2;self.reveal=cfg.get('reveal_seconds',10)
  if not 1<=len(self.rows)<=30:raise ValueError('Packed template supports 1–30 objects')
  if self.years!=sorted(set(self.years)):raise ValueError('Years must increase')
  self.values=[[float(row['values'][str(y)]) for row in self.rows] for y in self.years]
  if any(not math.isfinite(v) or v<0 for col in self.values for v in col):raise ValueError('Circle area needs nonnegative finite values')
  maxima=[max(col[i] for col in self.values) for i in range(len(self.rows))];maximum=max(maxima)
  if maximum<=0:raise ValueError('No positive circle areas')
  radii=[160*math.sqrt(v/maximum) for v in maxima];positions=pack(radii)
  bounds=(min(x-r for (x,y),r in zip(positions,radii)),min(y-r for (x,y),r in zip(positions,radii)),max(x+r for (x,y),r in zip(positions,radii)),max(y+r for (x,y),r in zip(positions,radii)))
  scale=min(1620/(bounds[2]-bounds[0]),710/(bounds[3]-bounds[1]));mx,my=(bounds[0]+bounds[2])/2,(bounds[1]+bounds[3])/2
  self.positions=[(960+(x-mx)*scale,610+(y-my)*scale) for x,y in positions];self.radii=[r*scale for r in radii];self.maximums=maxima
  s=self.s=Scene(1920,1080,textures,font);p=self.p=s.palette;self.colors=[p['categorical'][i%len(p['categorical'])] for i in range(len(self.rows))]
  s.begin();s.paper((1875,-80,130,1240),'dark',seed=84,amplitude=16);s.paper((-50,930,690,220),'accent',seed=53,amplitude=16);self.bg=s.image.copy()
  self.title=None;theme=cfg.get('theme',{})
  if theme.get('text'):
   if theme.get('source') not in ('user','user_delegated'):raise ValueError('Unapproved theme')
   s.image=Image.new('RGBA',(1920,1080));size=60
   while s.font(size,True).getlength(theme['text'])>1520:size-=1
   width=int(s.font(size,True).getlength(theme['text']))+80;x=(1920-width)//2
   s.paper((x,45,width,98),'dark',seed=2,amplitude=11);s.text(theme['text'],(x+40,58),size,fill=p['paper'],bold=True);self.title=s.image.copy()
  s.image=Image.new('RGBA',(1920,1080));s.paper((76,185,1770,818),'paper',seed=12,amplitude=15);s.paper((118,170,180,32),'accent',seed=24,amplitude=5);self.page=s.image.copy();self.states={};self.final=None
 def page_for(self,index,next_index=None,fraction=0):
  exact=next_index is None
  if exact and index in self.states:return self.states[index]
  image=self.page.copy();d=ImageDraw.Draw(image);year=str(self.years[index]) if exact else f'{self.years[index]} → {self.years[next_index]}'
  d.text((1780,203),year,font=self.s.font(40,True),fill=self.p['ink'],anchor='rt')
  for i,row in enumerate(self.rows):
   value=self.values[index][i] if exact else self.values[index][i]*(1-fraction)+self.values[next_index][i]*fraction
   if value<=0:continue
   radius=self.radii[i]*math.sqrt(value/self.maximums[i]);x,y=self.positions[i];color=self.colors[i]
   d.ellipse((x-radius,y-radius,x+radius,y+radius),fill=color,outline=self.p['paper'],width=3)
   rgb=tuple(int(color[j:j+2],16) for j in (1,3,5));ink=self.p['paper'] if .2126*rgb[0]+.7152*rgb[1]+.0722*rgb[2]<135 else self.p['ink']
   size=min(48,max(15,int(radius*.48)))
   while self.s.font(size,True).getlength(row['name'])>radius*1.7 and size>11:size-=1
   d.text((x,y-4 if exact and radius>28 else y),row['name'],font=self.s.font(size,True),fill=ink,anchor='mm')
   if exact and radius>28:d.text((x,y+size*.95),str(row['values'][str(self.years[index])]),font=self.s.font(max(13,size-4)),fill=ink,anchor='mm')
  if exact:self.states[index]=image
  return image
 def frame(self,t):
  if self.final is not None and t>=self.start+self.reveal:return self.final
  image=self.bg.copy();beat=math.floor(t*12)/12
  if self.title:image.alpha_composite(self.title,(-int(1920*(1-ease(beat/.6))),0))
  progress=max(0,min(1,(t-self.start)/self.reveal));position=progress*(len(self.years)-1);index=int(position);part=position-index
  if index==len(self.years)-1 or part<.62:page=self.page_for(index)
  else:page=self.page_for(index,index+1,ease((part-.62)/.38))
  image.alpha_composite(page,(0,int(1080*(1-ease((beat-.45)/.6)))))
  if progress==1:self.final=image
  return image
