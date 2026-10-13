#!/usr/bin/env python3
"""Deterministic reusable paper textures; Pillow and NumPy required."""
import argparse
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter, ImageDraw

def load_palette(scheme='classic-paper',palette_file=None):
    source=Path(palette_file) if palette_file else Path(__file__).resolve().parents[1]/'references/palettes.json'
    data=json.loads(source.read_text())
    # A custom file can contain a single named palette with the same role keys.
    if 'palettes' not in data:return data
    for palette in data['palettes']:
        if scheme in (palette['id'],palette['name'],str(palette['number'])):return palette
    if not palette_file:
        legacy=source.with_name('legacy-palettes.json')
        if legacy.exists():
            for palette in json.loads(legacy.read_text())['palettes']:
                if scheme in (palette['id'],palette['name']):return palette
    raise ValueError('Unknown palette: '+str(scheme))

def rgb(value):
    return tuple(int(value.lstrip('#')[i:i+2],16) for i in (0,2,4))

def generate(out,width=1920,height=1080,seed=424,scheme='classic-paper',palette_file=None):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    palette=load_palette(scheme,palette_file)
    rng=np.random.default_rng(seed);w,h=width,height
    coarse=np.array(Image.fromarray(rng.integers(60,195,(36,64),dtype=np.uint8)).resize((w,h),Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(max(1,w/120)))).astype(float)-128
    medium=np.array(Image.fromarray(rng.integers(85,170,(135,240),dtype=np.uint8)).resize((w,h),Image.Resampling.BICUBIC)).astype(float)-128
    noise=coarse*.10+medium*.07+rng.normal(0,1.8,(h,w))
    roles=[('paper','paper'),('yellow','primary'),('accent','primary'),('secondary','secondary'),('dark','ink'),('back','canvas')]
    materials=[(name,rgb(palette[role])) for name,role in roles]
    materials += [(f'category_{i+1}',rgb(value)) for i,value in enumerate(palette['categorical'])]
    for name,base in materials:
        arr=np.clip(np.array(base)[None,None,:]+noise[:,:,None],0,255).astype(np.uint8)
        im=Image.fromarray(arr);d=ImageDraw.Draw(im,'RGBA')
        for _ in range(max(100,int(w*h/700))):
            x=int(rng.integers(0,w));y=int(rng.integers(0,h));length=int(rng.integers(1,8))
            d.line((x,y,x+length,y+int(rng.integers(-1,2))),fill=(90,74,54,int(rng.integers(5,25))),width=1)
        im.save(out/f'{name}.jpg',quality=95)
    (out/'palette.json').write_text(json.dumps(palette,ensure_ascii=False,indent=2))
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True)
    p.add_argument('--width',type=int,default=1920);p.add_argument('--height',type=int,default=1080);p.add_argument('--seed',type=int,default=424)
    p.add_argument('--scheme',default='classic-paper');p.add_argument('--palette-file')
    a=p.parse_args()
    if min(a.width,a.height)<16:raise SystemExit('Dimensions must be at least 16 pixels.')
    print(generate(a.out,a.width,a.height,a.seed,a.scheme,a.palette_file))
