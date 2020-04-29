from PIL import Image
from reportlab.pdfgen import canvas
import glob
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.lib.units import cm
import math 


def makebook(path, filename="unknown", title="untitled"): 
    pdf_canvas = set_info(filename, title)
    print_string(pdf_canvas,path,filename,title)
    pdf_canvas.save() 
    
def set_info(filename, title, author="unknown"):
    pdf_canvas = canvas.Canvas("./{0}.pdf".format(filename),pagesize=landscape(A4)) # A4 landscape A4横書き
    pdf_canvas.setAuthor(author) # 作者
    pdf_canvas.setTitle(title) # 本のタイトル表題
    return pdf_canvas


def print_string(pdf_canvas,path,filename,title):
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
    
    #表紙のフォントサイズ
    title_font_size = 24
    pdf_canvas.setFont('HeiseiKakuGo-W5', title_font_size)   
    
    # 画像と本文の取り込み
    imagefiles = glob.glob(path+filename+'/*.png')
    textfile   = glob.glob(path+filename+'/*.txt')
    
    imagefiles.sort()
    npages = len(imagefiles)
    
    #使う紙の枚数
    npaper = math.ceil((npages+2)/4)
    
    #PDFの枚数
    npdf = npaper/4
            
    with open(textfile[0],"r") as f:
        line = f.read()
    
    contents = line.split("p.")
    
    # 本文をプリント　左開き
    if title == "untitled":
        title = contents[0].replace('title','').lstrip().rstrip()

    # .drawString(x,y, string)
    # x___ go right from bottom-left
    # y___ go up from bottom-left

    pdf_canvas.drawString(15.*cm, 10*cm, title)
    pdf_canvas.showPage()
      
    contents = contents[1:]
    
    
    # 左右のページ番号をあわせてプリントしていく。
    for page in range(npaper*2-1):
        page_pair = npaper*4 - 2 - page
        
        if page%2 == 0:
            leftpage = page
            rightpage = page_pair
        else:
            leftpage = page_pair
            rightpage = page
            
        content_font_size= 12
        pdf_canvas.setFont('HeiseiKakuGo-W5', content_font_size)
        
        def position(imagename,text,offset=420):
            image=Image.open(imagename)
            pdf_canvas.drawInlineImage(image,10+offset,10,width=14.0*cm, height=10.0*cm)
            
            linestep = 0
            for line in text.split('\n'):
                pdf_canvas.drawString(30+offset,500-linestep,line)
                linestep += content_font_size+2
            
        if leftpage < npages:
            position(imagefiles[leftpage],contents[leftpage],offset=0)
        if rightpage < npages:
            position(imagefiles[rightpage],contents[rightpage])
            
        pdf_canvas.showPage()
        

    
if __name__ == '__main__':
    #　画像と本文のあるディレクトリーの親Path
    path = "Books/"
    # 画像と本文のあるディレクトリー
    dirname = "ampanman1"
    makebook(path, filename=dirname,title="アンパンマンとメロンパンナちゃん")
