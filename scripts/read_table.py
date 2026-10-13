#!/usr/bin/env python3
"""Extract XLSX/CSV/TSV cells with provenance; never calculate formulas."""
import argparse
import csv
import io
import json
import posixpath
import re
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
BUILTIN = {0:'General',1:'0',2:'0.00',9:'0%',10:'0.00%',14:'mm-dd-yy',
           15:'d-mmm-yy',16:'d-mmm',17:'mmm-yy',18:'h:mm AM/PM',
           19:'h:mm:ss AM/PM',20:'h:mm',21:'h:mm:ss',22:'m/d/yy h:mm'}

def column(i):
    result = ''
    while i:
        i, rem = divmod(i-1, 26)
        result = chr(65+rem)+result
    return result

def number(value):
    if value is None or value == '':
        return None
    try:
        n = float(value)
        return int(n) if n.is_integer() else n
    except ValueError:
        return value

def text(element):
    return ''.join(n.text or '' for n in element.findall('.//m:t', NS))

def xlsx(path):
    warnings = []
    with zipfile.ZipFile(path) as z:
        if sum(i.file_size for i in z.infolist()) > 250_000_000:
            raise ValueError('Workbook uncompressed content exceeds 250 MB; use a suitable streaming reader.')
        wb = ET.fromstring(z.read('xl/workbook.xml'))
        rel = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        targets = {}
        for item in rel:
            if item.get('TargetMode') == 'External':
                continue
            target = item.get('Target','')
            targets[item.get('Id')] = (target.lstrip('/') if target.startswith('/')
                                       else posixpath.normpath('xl/'+target))
        strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            strings = [text(si) for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',NS)]
        formats = dict(BUILTIN)
        styles = [0]
        if 'xl/styles.xml' in z.namelist():
            st = ET.fromstring(z.read('xl/styles.xml'))
            for fmt in st.findall('m:numFmts/m:numFmt', NS):
                formats[int(fmt.get('numFmtId'))] = fmt.get('formatCode')
            styles = [int(x.get('numFmtId','0')) for x in st.findall('m:cellXfs/m:xf',NS)] or [0]
        sheets = []
        for sheet in wb.findall('m:sheets/m:sheet', NS):
            target = targets.get(sheet.get('{'+NS['r']+'}id'))
            if not target or target not in z.namelist():
                warnings.append('Unreadable worksheet relationship: '+sheet.get('name',''))
                continue
            xml = ET.fromstring(z.read(target));cells = []
            for c in xml.findall('m:sheetData/m:row/m:c',NS):
                address = c.get('r');kind = c.get('t','n');v = c.find('m:v',NS);f = c.find('m:f',NS)
                raw = v.text if v is not None else None
                if kind == 's': value = strings[int(raw)] if raw is not None else None
                elif kind == 'inlineStr': value = text(c)
                elif kind == 'b': value = None if raw is None else raw == '1'
                elif kind in ('str','e','d'): value = raw
                else: value = number(raw)
                index = int(c.get('s','0'));fmt = formats.get(styles[index] if index < len(styles) else 0,'Unknown')
                cell = {'cell':address,'value':value,'type':kind,'number_format':fmt}
                if f is not None:
                    cell['formula'] = f.text
                    cell['formula_attributes'] = dict(f.attrib)
                    cell['cached'] = v is not None and raw is not None
                    if not cell['cached']: warnings.append(f"{sheet.get('name')}!{address}: formula has no cached value")
                if kind == 'e': warnings.append(f"{sheet.get('name')}!{address}: {value}")
                cells.append(cell)
            sheets.append({'name':sheet.get('name'),'state':sheet.get('state','visible'),
                           'cells':cells,'merged_ranges':[m.get('ref') for m in xml.findall('m:mergeCells/m:mergeCell',NS)]})
        props = wb.find('m:workbookPr',NS)
        calc = wb.find('m:calcPr',NS)
        if any(n.startswith('xl/externalLinks/') for n in z.namelist()): warnings.append('Workbook contains external links; caches may be stale.')
        return {'source':str(path.resolve()),'format':'xlsx','date_system':1904 if props is not None and props.get('date1904') in ('1','true') else 1900,
                'calculation_properties':dict(calc.attrib) if calc is not None else {},
                'warnings':warnings,'sheets':sheets,'formula_note':'Cached values are not proof of current recalculation.'}

def delimited(path):
    content = path.read_text(encoding='utf-8-sig')
    delimiter = '\t' if path.suffix.lower() == '.tsv' else ','
    try: dialect = csv.Sniffer().sniff(content[:8192], delimiters=',\t;')
    except csv.Error: dialect = None
    reader = csv.reader(io.StringIO(content), dialect) if dialect else csv.reader(io.StringIO(content),delimiter=delimiter)
    cells = []
    for r, values in enumerate(reader,1):
        for c, value in enumerate(values,1):
            # Preserve labels, percentages, leading-zero identifiers and locale ambiguity as text.
            cells.append({'cell':f'{column(c)}{r}','value':value if value != '' else None,
                          'type':'text','number_format':None})
    return {'source':str(path.resolve()),'format':path.suffix[1:].lower(),'warnings':[],
            'sheets':[{'name':path.stem,'state':'visible','cells':cells,'merged_ranges':[]}]}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('input');ap.add_argument('--out',required=True)
    args=ap.parse_args();p=Path(args.input)
    if p.suffix.lower()=='.xlsx':result=xlsx(p)
    elif p.suffix.lower() in ('.csv','.tsv'):result=delimited(p)
    else:raise SystemExit('Supported input: .xlsx, UTF-8 .csv, .tsv. Use an appropriate reader for other formats.')
    out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
    print(f'Extracted {len(result["sheets"])} sheet(s); {len(result["warnings"])} warning(s). See {out}')

if __name__=='__main__':main()
