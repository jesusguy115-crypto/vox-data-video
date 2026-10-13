#!/usr/bin/env python3
"""Run the user-approved original CoreGraphics collage, with cached native compilation."""
from pathlib import Path
import argparse,hashlib,json,os,platform,subprocess,time
from make_paper import load_palette

def main():
 p=argparse.ArgumentParser();p.add_argument('--scene',required=True);p.add_argument('--out',required=True);p.add_argument('--cache');p.add_argument('--width',type=int,default=3840);p.add_argument('--height',type=int,default=2160);p.add_argument('--fps',type=int,default=30);p.add_argument('--palette');p.add_argument('--report');a=p.parse_args()
 started=time.perf_counter()
 if platform.system()!='Darwin':raise RuntimeError('Original collage requires macOS CoreGraphics/CoreText. Do not silently replace with the simpler template.')
 scene=json.loads(Path(a.scene).read_text());players=scene['players'];ppp=scene['points_per_possession'];efg=scene['efg_percent']
 if len(players)!=len(ppp) or len(players)!=len(efg) or not 1<=len(players)<=12:raise ValueError('Series lengths differ or unsupported count')
 if any(not 0<=v<=1.2 for v in ppp) or any(not 0<=v<=60 for v in efg):raise ValueError('Original chart axes: ppp 0–1.2, percent 0–60; adapt explicitly for other scales')
 if len(scene.get('title_lines',[]))!=2:raise ValueError('Supply two user-approved or delegated title lines')
 out=Path(a.out).resolve()
 if out.exists():raise ValueError('Choose a new output path')
 out.parent.mkdir(parents=True,exist_ok=True);scripts=Path(__file__).resolve().parent
 cache=Path(a.cache or os.environ.get('VOX_VIDEO_CACHE',str(Path.home()/'Documents/Codex/.vox-video-cache' if (Path.home()/'Documents/Codex').is_dir() else Path.home()/'.cache/vox-data-video')));cache.mkdir(parents=True,exist_ok=True)
 scheme=a.palette or scene.get('palette_id','classic-paper');texture=scripts.parent/'assets/classic-collage';scene_path=Path(a.scene).resolve()
 if scheme!='classic-paper':
  palette=load_palette(scheme);key=hashlib.sha256((json.dumps(palette,sort_keys=True)+(scripts/'make_paper.py').read_text()).encode()).hexdigest()[:16];texture=cache/('classic-paper-'+key)
  if not (texture/'palette.json').exists():subprocess.run([os.sys.executable,str(scripts/'make_paper.py'),'--out',str(texture),'--scheme',scheme],check=True)
  scene['palette_colors']={role:[int(palette[role][i:i+2],16)/255 for i in (1,3,5)] for role in ['paper','ink','muted','grid','primary','secondary']}
  scene_path=cache/('classic-scene-'+hashlib.sha256(json.dumps(scene,sort_keys=True).encode()).hexdigest()[:16]+'.json');scene_path.write_text(json.dumps(scene,ensure_ascii=False))
 source=scripts/'classic_collage.swift';key=hashlib.sha256(source.read_bytes()).hexdigest()[:16];binary=cache/('classic-'+key)
 if not binary.exists():subprocess.run(['swiftc','-O','-module-cache-path',str(cache/'swift-cache'),str(source),'-o',str(binary)],check=True)
 compiled=time.perf_counter();subprocess.run([str(binary),str(scene_path),str(texture),str(out),str(a.width),str(a.height),str(a.fps)],check=True)
 report={'renderer':'original-classic-collage','renderer_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'compile_seconds':round(compiled-started,3),'render_verify_seconds':round(time.perf_counter()-compiled,3),'automated_total_seconds':round(time.perf_counter()-started,3),'output':str(out)}
 if a.report:Path(a.report).write_text(json.dumps(report,indent=2))
 print(json.dumps(report))
if __name__=='__main__':main()
