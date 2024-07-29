from reportlab.pdfgen import canvas
from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak, Image, ListFlowable, ListItem, Spacer)
from reportlab.lib.styles import getSampleStyleSheet,  ParagraphStyle
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.utils import ImageReader
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import black, HexColor
import io

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
        image_path = 'code/logo.png'
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
        self.setFillColorRGB(204/255, 0, 0)  # Set color to red
        self.circle(x_circle, y_circle, circle_radius, stroke=0, fill=1)
 
        # Draw the image
        self.drawImage(image, x_image, y_image, width=image_width, height=image_height, mask='auto')

        self.restoreState()

def generatePDf(imagebuffersdict, keypoints):
    blended_red = HexColor("#cc0000")
    imagesizedict = { "single_bar_chart" : { "height" : 400 , "width": 400 }, "table" : { "height" : 400 , "width": 500 }, "collective_bar_chart" : { "height" : 500 , "width": 500 },  "collective_pie_chart" : { "height" : 500 , "width": 300 } }
    # Content
    styles = getSampleStyleSheet()
    elements = []
    
     # Create a title style with color
    title_style_red = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        spaceAfter=20,
        textColor=blended_red  # Set title color
    )

     # Create a title style with color
    title_style_black = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        spaceAfter=20,
        textColor=black  # Set title color
    )

    sub_title_black =  ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=10,
        leading=22,
        alignment=TA_LEFT,
        spaceAfter=20,
        textColor=black  # Set title color
    )

    sub_title_red =  ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=10,
        leading=22,
        alignment=TA_LEFT,
        spaceAfter=20,
        textColor=blended_red  # Set title color
    )

    bullet_style_red = ParagraphStyle(
    'BulletRed',
            parent=styles['BodyText'],
            fontSize=12,
            textColor=blended_red,
            bulletFontSize=12
        )
    
    bullet_style_black = ParagraphStyle(
    'BulletBlack',
            parent=styles['BodyText'],
            fontSize=12,
            textColor=black,
            bulletFontSize=12
        )

    
    # Create alternating color words
    title_text = "SOCIAL Media BENCHMARK Analysis"
    words = title_text.split()
    formatted_words = []

    for i, word in enumerate(words):
        if i % 2 == 0:
            formatted_words.append(f'<font color="black">{word}</font>')
        else:
            formatted_words.append(f'<font color="#cc0000">{word}</font>')

    formatted_title = ' '.join(formatted_words)

    # Add title to the elements list
    title = Paragraph(formatted_title, styles['Heading1'])
    elements.append(title)

    # PAGE - 1 :: Key points
    sub_title = Paragraph("Excel Summary", sub_title_red)
    elements.append(sub_title)
    # Adding key points as bullet points with alternating colors
    bullet_points = []
    for index, point in enumerate(keypoints):
        if index % 2 == 0:
            bullet_points.append(ListItem(Paragraph(point, bullet_style_red), bulletText='•'))
        else:
            bullet_points.append(ListItem(Paragraph(point, bullet_style_black), bulletText='•'))
    
    bullet_list = ListFlowable(bullet_points, bulletType='bullet', start='•', leftIndent=20)
    elements.append(bullet_list)
    elements.append(PageBreak())

    # Rest of PAGES with chart and its title
    title = Paragraph("Descriptive Analysis", title_style_red)
    elements.append(title)
    for index, imagebufferobj in enumerate(imagebuffersdict):
        print(f'index :: {index}')
        print(f'imagetitle :: {imagebufferobj["title"]}')
        print(f'imagedict :: {imagebufferobj} ')
        # Add title to the elements list
        title = Paragraph(imagebufferobj.get('title'), sub_title_red)
        elements.append(title)
        # Add an image in the body
        body_image = Image(imagebufferobj.get('img'))
        body_image.drawHeight = imagesizedict.get(imagebufferobj.get('chart_type')).get('height')   # Set image height
        body_image.drawWidth = imagesizedict.get(imagebufferobj.get('chart_type')).get('width')  # Set image width
        elements.append(body_image)
        elements.append(PageBreak())
   
    # Build
    pdfbuffer = io.BytesIO()
    doc = SimpleDocTemplate(pdfbuffer, pagesize=LETTER)
    doc.multiBuild(elements, canvasmaker=FooterCanvas)

    return pdfbuffer
