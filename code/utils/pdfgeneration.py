from reportlab.pdfgen import canvas
from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak, Image)
from reportlab.lib.styles import getSampleStyleSheet,  ParagraphStyle
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.utils import ImageReader
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import red


class FooterCanvas(canvas.Canvas):
 
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
 
    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()
 
    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_canvas(page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
 
    def draw_canvas(self, page_count):
        # Path to your image
        image_path = "./logo.png"
        image = ImageReader(image_path)
        
        # Position for the image
        x_image = LETTER[0] - 120
        y_image = 10  # Adjust y-coordinate for positioning the image
        image_width = 100
        image_height = 60
 
        # Position for the circle
        x_circle = 5
        y_circle = 0  # Adjust y-coordinate for positioning the circle
        circle_radius = 100
 
        self.saveState()

        # Draw the red circle
        self.setFillColorRGB(204, 0, 0)  # Set color to red
        self.circle(x_circle, y_circle, circle_radius, stroke=0, fill=1)
 
        # Draw the image
        self.drawImage(image, x_image, y_image, width=image_width, height=image_height, mask='auto')

        self.restoreState()

def generatePDf(imagebuffers, text):
     # Content
    styles = getSampleStyleSheet()
    elements = []

    # Create a title style with color
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        spaceAfter=20,
        textColor=red  # Set title color
    )
    
    elements = []
    
    # Add title to the elements list
    title = Paragraph("My Document Title 878", title_style)
    elements.append(title)

    paragraph = Paragraph(text[0], styles["Normal"])

    elements.append(paragraph)
    
    # Add an image in the body
    body_image = Image(imagebuffers)
    body_image.drawHeight = 300   # Set image height
    body_image.drawWidth = 500  # Set image width
    elements.append(body_image)

    elements.append(Paragraph("Lorem Ipsum is simply dummy text of the printing and typesetting industry."  +
    "1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", styles["Normal"]))
    elements.append(Paragraph("Lorem Ipsum is simply dummy text of the printing and typesetting industry."  +
    "1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", styles["Normal"]))


    # Add an image in the body
    body_image = Image(imagebuffers)
    body_image.drawHeight = 300   # Set image height
    body_image.drawWidth = 500  # Set image width
    elements.append(body_image)
   

    # Build
    doc = SimpleDocTemplate("my_file_4.pdf", pagesize=LETTER)
    doc.multiBuild(elements, canvasmaker=FooterCanvas)
