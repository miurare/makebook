from pdf2image import convert_from_path
import PyPDF2
import os

pdfname = input("pdfName:")

print("before:{:.2f}MB".format(os.path.getsize(pdfname)/1e6))

image = convert_from_path(pdfname)

merger = PyPDF2.PdfFileMerger()

page = 0
for i in image:
    if page < 10:
        pdf_filename = "_tmp0{}.pdf".format(page)
    else:
        pdf_filename = "_tmp{}.pdf".format(page)

    i.save(pdf_filename, resolution=72)
    merger.append(pdf_filename)
    page += 1

newpdfname = pdfname.replace('.pdf', '_reduce.pdf')
merger.write(newpdfname)
os.system('rm -rf _tmp*pdf')

print("after:{:.2f}MB".format(os.path.getsize(newpdfname)/1e6))
