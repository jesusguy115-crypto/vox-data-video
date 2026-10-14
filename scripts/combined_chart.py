"""Shared categorical combo renderer: stepped bars and line in one plot."""
import math
from PIL import Image,ImageDraw
from video_templates import ChartVideo

class CombinedChart(ChartVideo):
 def px(self,row,i):
  if self.cfg.get('x_axis',{}).get('type')!='category':return super().px(row,i)
  return self.left+(i+.5)/len(self.rows)*(self.right-self.left)
 def bar_width(self):return min(190,(self.right-self.left)/len(self.rows)*.46)
 def _bar(self,im,i,fraction):
  x,y=self.positions[0][i];w=max(1,int(self.bar_width()));h=int((self.bottom-y)*fraction)
  if h<=0:return
  series=self.series[0];material=series.get('materials',{}).get(str(self.rows[i][self.cfg['x_axis']['field']]),series.get('material','accent'))
  key=(material,w,h)
  if key not in self.bar_tiles:self.bar_tiles[key]=self.s.textures[material].resize((w,h),Image.Resampling.BILINEAR)
  im.alpha_composite(self.bar_tiles[key],(int(x-w/2),int(self.bottom-h)))
 def _node(self,im,j,i):
  x,y=self.positions[j][i];series=self.series[j];d=ImageDraw.Draw(im)
  if j==0:
   self._bar(im,i,1);d.text((x,y-20),self.value_label(self.rows[i][series['field']])+series.get('value_suffix',''),font=self.s.font(48 if len(self.rows)<=4 else 35,True,'number'),fill=self.colors[j],anchor='ms')
  else:
   d.ellipse((x-11,y-11,x+11,y+11),fill=self.p['paper']);d.ellipse((x-7,y-7,x+7,y+7),fill=self.colors[j])
   if series.get('show_values',True):d.text((x+self.bar_width()/2+20,y),self.value_label(self.rows[i][series['field']])+series.get('value_suffix',''),font=self.s.font(43 if len(self.rows)<=4 else 30,True,'number'),fill=self.colors[j],anchor='lm')
 def frame(self,t):
  if t>=self.start+self.reveal:return super().frame(t)
  page=self.chart.copy();beat=math.floor(t*12)/12;n=len(self.rows);stagger=min(.5,1.5/max(1,n-1))
  for i in range(n):
   q=max(0,min(1,(beat-self.start-i*stagger)/1.1));step=[0,.12,.32,.58,.82,1][min(5,int(q*6))]
   if q>=1:self._node(page,0,i)
   elif step:self._bar(page,i,step)
  line_start=1.1+(n-1)*stagger;q=max(0,min(1,(beat-self.start-line_start)/max(.5,self.reveal-line_start)))
  if q>0:
   pos=q*(n-1);index=min(n-1,int(pos));points=self.positions[1][:index+1]
   if index<n-1:
    a,b=self.positions[1][index:index+2];fraction=pos-index;points=points+[(a[0]+(b[0]-a[0])*fraction,a[1]+(b[1]-a[1])*fraction)]
   d=ImageDraw.Draw(page)
   if len(points)>1:d.line(points,fill=self.p['paper'],width=11);d.line(points,fill=self.colors[1],width=5)
   for i in range(index+1):self._node(page,1,i)
  return self._compose(page,t)
