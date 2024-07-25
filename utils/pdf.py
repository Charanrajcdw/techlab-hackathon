import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import pdfplumber

styles = getSampleStyleSheet()
elements = []

def build_pdf(pdf_buffer): 
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    doc.build(elements)
    
def add_lines_to_elements(text,style='Normal'):
    elements.append(Paragraph(text, styles[style]))
    elements.append(Spacer(1, 12))

def add_images_to_elements(filename):
    img = Image(filename)
    img.width = 300  
    img.height = 200
    elements.append(img)
    elements.append(Spacer(1, 12))


def get_pdf_preview(pdf_buffer):
    pdf_buffer.seek(0)
    images = []
    with pdfplumber.open(pdf_buffer) as pdf:
        for page in pdf.pages:
            pil_image = page.to_image().original
            images.append(pil_image)
    return images
