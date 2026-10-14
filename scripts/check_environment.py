#!/usr/bin/env python3
"""Report rendering prerequisites without silently substituting a different design."""
import platform,sys,shutil,json,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
font=root/'assets/fonts/NotoSansSC.ttf';modules={}
for name in ['PIL','numpy']:
 try:m=__import__(name);modules[name]={'available':True,'version':m.__version__}
 except ImportError:modules[name]={'available':False}
codec='swift' if platform.system()=='Darwin' and shutil.which('swiftc') else 'ffmpeg' if shutil.which('ffmpeg') else None
print(json.dumps({'renderer_version':'2.3','python':sys.version.split()[0],'os':platform.system(),'modules':modules,'bundled_font':font.is_file(),'font_sha256':hashlib.sha256(font.read_bytes()).hexdigest() if font.is_file() else None,'encoder':codec,'ready':all(x['available'] for x in modules.values()) and all((root/'assets/fonts'/name).is_file() for name in ['NotoSansSC.ttf','NotoSerifSC.ttf','BarlowCondensed-Bold.ttf']) and codec is not None},ensure_ascii=False))
