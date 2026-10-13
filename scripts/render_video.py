#!/usr/bin/env python3
"""Render a normalized chart scene with cached textures/templates and direct encoding."""
from pathlib import Path
import argparse,json,time,hashlib,subprocess,sys,platform,shutil
import PIL
from PIL import Image
from video_templates import ChartVideo

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--scene',required=True);ap.add_argument('--out');ap.add_argument('--cache',required=True);ap.add_argument('--font');ap.add_argument('--encoder');ap.add_argument('--backend',choices=['stream','png'],default='stream');ap.add_argument('--preview-only',action='store_true');ap.add_argument('--report');args=ap.parse_args()
 started=time.perf_counter();cfg=json.loads(Path(args.scene).read_text());cache=Path(args.cache).resolve();cache.mkdir(parents=True,exist_ok=True);scripts=Path(__file__).resolve().parent
 fps=int(cfg.get('fps',30));duration=float(cfg.get('duration',14));count=round(fps*duration);w,h=int(cfg.get('width',1920)),int(cfg.get('height',1080))
 if fps<=0 or fps>120 or count<=0 or w<=0 or h<=0 or w%2 or h%2:raise ValueError('Invalid dimensions/fps/duration')
 if w/h!=16/9:raise ValueError('Built-in templates use 16:9; use custom scene for other aspect ratios')
 out=Path(args.out).resolve() if args.out else None
 if not args.preview_only and (out is None or out.exists()):raise ValueError('Choose a new --out path')
 scheme=cfg.get('palette_id','classic-paper');palette_file=cfg.get('palette_file')
 key=hashlib.sha256((scheme+(Path(palette_file).read_text() if palette_file else '')+(scripts/'make_paper.py').read_text()+(scripts.parent/'references/palettes.json').read_text()).encode()).hexdigest()[:16]
 paper=cache/('paper-'+key)
 if not (paper/'palette.json').exists():
  cmd=[sys.executable,str(scripts/'make_paper.py'),'--out',str(paper),'--width','1920','--height','1080','--scheme',scheme]
  if palette_file:cmd+=['--palette-file',palette_file]
  subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL)
 font=Path(args.font).resolve() if args.font else scripts.parent/'assets/fonts/NotoSansSC.ttf'
 if not font.is_file():raise RuntimeError('Missing bundled font; install the complete skill. Do not silently substitute font.')
 scene=ChartVideo(cfg,paper,font)
 if duration<scene.start+scene.reveal+.5:raise ValueError('Duration must allow complete data reveal and reading hold')
 def frame(t):
  im=scene.frame(t)
  return im if (w,h)==im.size else im.resize((w,h),Image.Resampling.LANCZOS)
 previews=cache/('preview-'+hashlib.sha256(Path(args.scene).read_bytes()).hexdigest()[:12]);previews.mkdir(exist_ok=True)
 for name,t in [('entry',.7),('middle',scene.start+scene.reveal/2),('final',duration-1/fps)]:frame(t).convert('RGB').save(previews/(name+'.jpg'),quality=92)
 prepared=time.perf_counter();encoder_seconds=0;render_seconds=0
 if args.preview_only:
  print(json.dumps({'previews':str(previews),'seconds':round(prepared-started,3)}));return
 out.parent.mkdir(parents=True,exist_ok=True)
 ffmpeg=None
 if args.encoder:encoder=Path(args.encoder).resolve()
 elif platform.system()!='Darwin' and shutil.which('ffmpeg'):
  ffmpeg=shutil.which('ffmpeg');encoder=None
 else:
  if platform.system()!='Darwin':raise RuntimeError('FFmpeg is required on this platform. Preserve previews; do not silently redraw with another engine.')
  source=scripts/('encode_stream.swift' if args.backend=='stream' else 'encode_frames.swift');binary_key=hashlib.sha256(source.read_bytes()).hexdigest()[:16];encoder=cache/('encoder-'+args.backend+'-'+binary_key)
  if not encoder.exists():subprocess.run(['swiftc','-O','-module-cache-path',str(cache/'swift-cache'),str(source),'-o',str(encoder)],check=True)
 encoding_started=time.perf_counter();compile_seconds=encoding_started-prepared
 if args.backend=='stream':
  command=([ffmpeg,'-v','error','-f','rawvideo','-pixel_format','bgra','-video_size',f'{w}x{h}','-framerate',str(fps),'-i','pipe:0','-frames:v',str(count),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(out)] if ffmpeg else [str(encoder),str(out),str(w),str(h),str(fps),str(count)])
  proc=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  last=None;data=None
  try:
   for i in range(count):
    t0=time.perf_counter();im=frame(i/fps)
    if im is not last:data=im.tobytes('raw','BGRA');last=im
    render_seconds+=time.perf_counter()-t0;proc.stdin.write(data)
   proc.stdin.close();proc.stdin=None;stdout,stderr=proc.communicate(timeout=120)
  except BaseException:
   proc.kill();proc.wait();raise
  if proc.returncode:raise RuntimeError(stderr.decode(errors='replace'))
  print(stdout.decode().strip())
  if ffmpeg:subprocess.run([ffmpeg,'-v','error','-i',str(out),'-vf',f'select=eq(n\\,0)+eq(n\\,{count//2})+eq(n\\,{count-1})','-frames:v','3','-f','null','-'],check=True)
 else:
  if ffmpeg:raise RuntimeError('Use stream backend with FFmpeg')
  folder=cache/('frames-'+hashlib.sha256(str(out).encode()).hexdigest()[:12]);folder.mkdir(exist_ok=True)
  for i in range(count):frame(i/fps).convert('RGB').save(folder/f'frame_{i:06d}.png')
  render_seconds=time.perf_counter()-encoding_started;t0=time.perf_counter();subprocess.run([str(encoder),str(folder),str(out),str(fps)],check=True);encoder_seconds=time.perf_counter()-t0
 finished=time.perf_counter();report={'renderer_version':'2.0','renderer_sha256':hashlib.sha256((scripts/'video_templates.py').read_bytes()+(scripts/'collage.py').read_bytes()+(scripts/'make_paper.py').read_bytes()).hexdigest(),'scene_sha256':hashlib.sha256(Path(args.scene).read_bytes()).hexdigest(),'font_sha256':hashlib.sha256(font.read_bytes()).hexdigest(),'pillow_version':PIL.__version__,'palette_id':scheme,'series_colors':scene.colors,'backend':args.backend,'frames':count,'width':w,'height':h,'fps':fps,'duration':duration,'prepare_seconds':round(prepared-started,3),'compile_seconds':round(compile_seconds,3),'render_seconds':round(render_seconds,3),'render_encode_seconds':round(finished-encoding_started,3),'total_seconds':round(finished-started,3),'temporary_frame_files':0 if args.backend=='stream' else count,'previews':str(previews),'output':str(out)}
 if args.report:Path(args.report).write_text(json.dumps(report,ensure_ascii=False,indent=2))
 print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
