"""Render the three required Project 1 PDFs from the Markdown records."""
from pathlib import Path
import re,json
from html import escape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,LongTable,TableStyle,PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parent;DOCS=ROOT/'docs'
fontdir=Path('C:/Windows/Fonts')
if (fontdir/'arial.ttf').exists():
 pdfmetrics.registerFont(TTFont('ProjectFont',str(fontdir/'arial.ttf')))
 pdfmetrics.registerFont(TTFont('ProjectBold',str(fontdir/'arialbd.ttf')))
 pdfmetrics.registerFontFamily('ProjectFont',normal='ProjectFont',bold='ProjectBold',italic='ProjectFont',boldItalic='ProjectBold')
 normal,bold='ProjectFont','ProjectBold'
else:normal,bold='Helvetica','Helvetica-Bold'
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyProject',fontName=normal,fontSize=9.1,leading=12,spaceAfter=6))
styles.add(ParagraphStyle(name='SmallProject',fontName=normal,fontSize=7.4,leading=9.5,spaceAfter=2,wordWrap='CJK'))
for key,size in [('Title',18),('Heading1',14),('Heading2',11),('Heading3',10)]:styles[key].fontName=bold;styles[key].fontSize=size;styles[key].leading=size+3;styles[key].keepWithNext=True

def inline(text):
 text=escape(text)
 text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:f'<link href="{m.group(2)}" color="#15536b">{m.group(1)}</link>',text)
 text=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',text)
 return re.sub(r'`([^`]+)`',r'\1',text)

def render(markdown,target):
 lines=markdown.splitlines();story=[];i=0
 while i<len(lines):
  line=lines[i].strip()
  if not line:i+=1;continue
  if line=='<!-- PAGEBREAK -->':story.append(PageBreak());i+=1;continue
  if line.startswith('|'):
   data=[]
   while i<len(lines) and lines[i].strip().startswith('|'):
    cells=[x.strip() for x in lines[i].strip().strip('|').split('|')]
    if not all(re.fullmatch(r'[-: ]+',x) for x in cells):data.append([Paragraph(inline(x),styles['SmallProject']) for x in cells])
    i+=1
   if data:
    t=LongTable(data,colWidths=[504/len(data[0])]*len(data[0]),repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8f0f3')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.6,colors.HexColor('#78909c')),('LINEBELOW',(0,1),(-1,-1),.25,colors.HexColor('#d9e1e5')),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    story.extend([t,Spacer(1,8)])
   continue
  if line.startswith('#'):
   level=len(line)-len(line.lstrip('#'));style=styles['Title'] if level==1 else styles['Heading2' if level==2 else 'Heading3']
   story.append(Paragraph(inline(line.lstrip('#').strip()),style));i+=1;continue
  if line.startswith('- '):story.append(Paragraph('- '+inline(line[2:]),styles['BodyProject']));i+=1;continue
  if re.match(r'^\d+\.\s+',line):
   story.append(Paragraph(inline(line),styles['BodyProject']));i+=1;continue
  paragraph=[line];i+=1
  while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','- ','<!--')) and not re.match(r'^\d+\.\s+',lines[i].strip()):paragraph.append(lines[i].strip());i+=1
  story.append(Paragraph(inline(' '.join(paragraph)),styles['BodyProject']))
 def footer(canvas,doc):
  canvas.setFont(normal,8);canvas.setFillColor(colors.HexColor('#526771'));canvas.drawString(54,27,'DUOL Valuation | Valuation date: September 21, 2026');canvas.drawRightString(558,27,str(doc.page))
 doc=SimpleDocTemplate(str(target),pagesize=letter,rightMargin=54,leftMargin=54,topMargin=40,bottomMargin=43,title=target.stem,author='DUOL Research; AI assistance disclosed')
 doc.build(story,onFirstPage=footer,onLaterPages=footer)
 return len(PdfReader(target).pages)

if __name__=='__main__':
 pages={}
 for source,dest in [('research-evolution.md','Research-Evolution.pdf'),('decision-memo.md','Decision-Memo.pdf'),('validation-and-ai-use.md','Validation-and-AI-Use.pdf')]:
  text=(DOCS/source).read_text(encoding='utf-8')
  if source=='research-evolution.md':text=text.replace('<!-- UNCHANGED EDITION A -->',(DOCS/'edition-a.md').read_text(encoding='utf-8'))
  pages[dest]=render(text,DOCS/dest)
 if pages['Decision-Memo.pdf']>2:raise ValueError('Decision memo exceeds two pages: '+str(pages))
 print(json.dumps(pages,indent=2))
