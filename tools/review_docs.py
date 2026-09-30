"""Read-only content checks plus PDF previews under ignored tmp/."""
from pathlib import Path
import os, re, subprocess, xml.etree.ElementTree as ET
import pdfplumber
from PIL import Image, ImageOps, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
GH=os.environ.get('GH_EXE','gh')
SHA='c4f208931c008a7578a42cdc23d854f77d7de4cc'
def source(path):
    return subprocess.check_output([GH,'api',f'repos/HKUST-MPAS/HKUST-MPAS/contents/{path}?ref={SHA}',
        '-H','Accept: application/vnd.github.raw+json'],text=True,encoding='utf-8')
registries={
    'init':source('src/core_init_atmosphere/Registry.xml'),
    'atmosphere':source('src/core_atmosphere/Registry.xml')+source('src/core_atmosphere/physics/Registry_noahmp.xml')+source('src/core_atmosphere/diagnostics/Registry_soundings.xml')}
for path in (ROOT/'config').glob('namelist.*'):
    known=set(re.findall(r'<nml_option\s+name="([^"]+)"',registries['init' if 'init_atmosphere' in path.name else 'atmosphere']))
    used=set(re.findall(r'^\s*(config_\w+)\s*=',path.read_text(),re.M))
    assert not used-known,(path.name,used-known)
    print('Registry option check:',path.name,len(used))
for path in (ROOT/'config').glob('streams.*'):
    ET.parse(path)
    print('XML check:',path.name)
for path in list((ROOT/'docs').glob('*.md'))+[ROOT/'README.md']:
    content=path.read_text(encoding='utf-8')
    for label,url in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',content):
        if not url.startswith(('http:','https:','#')):
            assert (path.parent/url.split('#')[0]).exists(),(path.name,url)
    for snippet in re.findall(r'```bash\n(.*?)```',content,re.S):
        result=subprocess.run(['wsl.exe','-d','Ubuntu-22.04','--cd','~','bash','-n'],input=snippet,
                              text=True,encoding='utf-8',errors='replace',capture_output=True)
        assert result.returncode==0,(path.name,result.stderr)
print('Local links and Bash syntax: OK')

tmp=ROOT/'tmp'/'pdfs';tmp.mkdir(parents=True,exist_ok=True)
poppler=Path(os.environ['PDFTOPPM_EXE'])
for path in (ROOT/'docs').glob('0*.pdf'):
    with pdfplumber.open(path) as pdf:
        for i,page in enumerate(pdf.pages):
            assert page.extract_text(),(path.name,i)
            bad=[c for c in page.chars if c['x0'] < 38 or c['x1']>page.width-35 or c['top']<25 or c['bottom']>page.height-22]
            assert not bad,(path.name,i,bad[:2])
        print('PDF bounds:',path.name,len(pdf.pages),'pages')
    subprocess.run([str(poppler),'-scale-to','1100','-png',str(path),str(tmp/path.stem)],check=True)
    pages=sorted(tmp.glob(path.stem+'-*.png'))
    for offset in range(0,len(pages),4):
        sheet=Image.new('RGB',(840,1220),'#cbd5df')
        draw=ImageDraw.Draw(sheet)
        for n,p in enumerate(pages[offset:offset+4]):
            im=Image.open(p).convert('RGB');im.thumbnail((406,574))
            x=8+(n%2)*420;y=24+(n//2)*610
            sheet.paste(im,(x,y));draw.text((x,y-16),p.name,fill='black')
        sheet.save(tmp/f'contact-{path.stem}-{offset//4+1}.png')
