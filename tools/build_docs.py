"""Build the three PDFs from their Markdown sources (ReportLab)."""
from pathlib import Path
import re
from html import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, KeepTogether, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4

ROOT = Path(__file__).resolve().parents[1]
class CodeBlock(Preformatted):
    def split(self, availWidth, availHeight):
        return []
styles = getSampleStyleSheet()
styles.add(ParagraphStyle('Body', fontName='Helvetica', fontSize=10.2, leading=14.2,
                         spaceAfter=8, textColor=colors.HexColor('#26364a')))
styles.add(ParagraphStyle('CodeBlock', fontName='Courier', fontSize=8.2, leading=11.4,
                         leftIndent=9, rightIndent=5, spaceBefore=5, spaceAfter=12,
                         backColor=colors.HexColor('#f0f4f8'), borderPadding=8))
for key, size in [('Title',25), ('Heading1',16), ('Heading2',12)]:
    styles[key].fontName='Helvetica-Bold'
    styles[key].fontSize=size
    styles[key].leading=size*1.3
    styles[key].textColor=colors.HexColor('#245e87')
    styles[key].spaceBefore=15
    styles[key].spaceAfter=10
    styles[key].keepWithNext=True

def inline(text):
    text=escape(text)
    def link(match):
        label, url = match.groups()
        if url.startswith('#'):
            url='https://github.com/Liuzh223/MPAS-Urban-Tutorial/blob/main/docs/appendix-dependencies.md'+url
        return f'<link href="{url}" color="#245e87"><u>{label}</u></link>'
    text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link,text)
    text=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',text)
    return re.sub(r'`([^`]+)`',r'<font name="Courier" size="9">\1</font>',text)

def parse(text):
    out=[]; para=[]; code=None
    def flush():
        if para:
            st=ParagraphStyle('ParaLocal',parent=styles['Body'],splitLongWords=False,
                              allowWidows=0,allowOrphans=0,keepWithNext=para[-1].endswith(':'))
            out.append(Paragraph(inline(' '.join(para)), st));para.clear()
    for line in text.splitlines():
        if line.startswith('```'):
            flush()
            if code is None: code=[]
            else:
                # Long code lines use a smaller font without altering command text.
                maximum=max([len(x) for x in code]+[1])
                size=min(8.2, 475/(maximum*0.6))
                if size < 6.2: raise ValueError('Split long command before PDF generation: '+max(code,key=len))
                st=ParagraphStyle('CodeLocal',parent=styles['CodeBlock'],fontSize=size,leading=size*1.42)
                out.append(CodeBlock('\n'.join(code),st));code=None
            continue
        if code is not None: code.append(line);continue
        if not line.strip(): flush();continue
        if line.startswith('<!--'):flush();continue
        if line.startswith('# '):
            flush();out.append(Paragraph(inline(line[2:]),styles['Title']))
        elif line.startswith('## '):
            flush();out.append(Paragraph(inline(line[3:]),styles['Heading1']))
        elif line.startswith('### '):
            flush();out.append(Paragraph(inline(line[4:]),styles['Heading2']))
        elif line.startswith('- '):
            flush();out.append(Paragraph('&#8226; '+inline(line[2:]),styles['Body']))
        else:para.append(line)
    flush()
    for n,flow in enumerate(out):
        if isinstance(flow,Paragraph) and flow.getPlainText()=='References':
            out[n:]=[KeepTogether(out[n:])]
            break
    return out

def footer(canvas,doc):
    canvas.setStrokeColor(colors.HexColor('#d6e1e9'))
    canvas.line(48,45,A4[0]-48,45)
    canvas.setFont('Helvetica',8)
    canvas.setFillColor(colors.HexColor('#617487'))
    canvas.drawString(48,31,'MPAS-URBAN | HONG KONG HEATWAVE 2022')
    canvas.drawRightString(A4[0]-48,31,str(doc.page))

for stem in ('01-installation','02-initialization','03-running'):
    text=(ROOT/'docs'/f'{stem}.md').read_text(encoding='utf-8')
    story=parse(text)
    if stem=='01-installation':
        story.append(PageBreak())
        story.extend(parse((ROOT/'docs'/'appendix-dependencies.md').read_text(encoding='utf-8')))
    out=ROOT/'docs'/f'{stem}.pdf'
    SimpleDocTemplate(str(out),pagesize=A4,rightMargin=48,leftMargin=48,
                     topMargin=40,bottomMargin=60,title=text.splitlines()[0][2:],
                     author='LIU Zhuo, The Hong Kong University of Science and Technology').build(
                         story,onFirstPage=footer,onLaterPages=footer)
    print(out)
