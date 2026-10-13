"""Paper-collage primitives. Coordinates are actual output pixels, top-left origin."""
from pathlib import Path
import random
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def ease(value):
    x=min(1,max(0,value));return x*x*(3-2*x)

def torn_points(box,seed=1,amplitude=8,step=13):
    x,y,w,h=box;rng=random.Random(seed);points=[]
    for start,end in [((x,y),(x+w,y)),((x+w,y),(x+w,y+h)),((x+w,y+h),(x,y+h)),((x,y+h),(x,y))]:
        dx=end[0]-start[0];dy=end[1]-start[1];n=max(2,int((abs(dx)+abs(dy))/step))
        for i in range(n):
            px=start[0]+dx*i/n;py=start[1]+dy*i/n
            offset=rng.uniform(-amplitude/2,amplitude/2)
            points.append((px+(offset if dy else 0),py+(offset if dx else 0)))
    return points

class Scene:
    def __init__(self,width,height,textures,font_regular,font_bold=None):
        self.width,self.height=width,height
        folder=Path(textures)
        self.textures={f.stem:Image.open(f).convert('RGBA') for f in folder.glob('*.jpg')}
        palette_file=folder/'palette.json'
        self.palette=json.loads(palette_file.read_text()) if palette_file.exists() else {'ink':'#20282B','paper':'#F2EEE2','secondary':'#C93824','primary':'#FBD32E'}
        for role in ['paper','yellow','dark','back']:
            if role not in self.textures:raise ValueError('Missing paper texture: '+role)
        self.font_regular=str(font_regular);self.font_bold=str(font_bold or font_regular);self.fonts={}
        # Fail early rather than silently replacing Chinese with missing glyph boxes.
        ImageFont.truetype(self.font_regular,24)
        self.begin()

    def begin(self):
        self.image=self.textures['back'].resize((self.width,self.height),Image.Resampling.LANCZOS).copy()
        return self

    def paper(self,box,material='paper',seed=1,amplitude=8,shadow=True):
        x,y,w,h=map(int,box)
        if w<=0 or h<=0:return
        points=torn_points((x,y,w,h),seed,amplitude)
        mask=Image.new('L',self.image.size);ImageDraw.Draw(mask).polygon(points,fill=255)
        if shadow:
            shift=Image.new('L',mask.size);shift.paste(mask,(4,7));shift=shift.filter(ImageFilter.GaussianBlur(5))
            tint=Image.new('RGBA',self.image.size,(0,0,0,0));tint.putalpha(shift.point(lambda a:int(a*.18)))
            self.image=Image.alpha_composite(self.image,tint)
        pad=max(2,int(amplitude)+2)
        layer=self.image.copy();layer.paste(self.textures[material].resize((w+2*pad,h+2*pad),Image.Resampling.BILINEAR),(x-pad,y-pad))
        self.image=Image.composite(layer,self.image,mask)
        ImageDraw.Draw(self.image).line(points+[points[0]],fill=(248,245,232,255),width=1)

    def font(self,size,bold=False):
        key=(int(size),bold)
        if key not in self.fonts:self.fonts[key]=ImageFont.truetype(self.font_bold if bold else self.font_regular,int(size))
        return self.fonts[key]

    def text(self,value,xy,size=32,fill=None,bold=False,anchor='lt'):
        d=ImageDraw.Draw(self.image);f=self.font(size,bold)
        fill=fill or self.palette['ink']
        d.text(xy,str(value),font=f,fill=fill,anchor=anchor)
        return d.textbbox(xy,str(value),font=f,anchor=anchor)

    def line(self,points,fill=None,width=2):
        fill=fill or self.palette['ink']
        ImageDraw.Draw(self.image).line(points,fill=fill,width=int(width),joint='curve')

    def dot(self,xy,radius=5,fill=None):
        fill=fill or self.palette['secondary']
        x,y=xy;ImageDraw.Draw(self.image).ellipse((x-radius,y-radius,x+radius,y+radius),fill=fill)

    def rectangle(self,box,fill=None):
        fill=fill or self.palette['ink']
        ImageDraw.Draw(self.image).rectangle(box,fill=fill)

    def save(self,path):
        p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);self.image.convert('RGB').save(p)
