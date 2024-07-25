import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import io
import pdfplumber
from langchain_experimental.agents import create_csv_agent
from langchain_openai import AzureOpenAI
import markdown2
from dotenv import load_dotenv

load_dotenv()
deployment_name = "gpt-35-turbo-instruct"
 
if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False
 
def upload_csv():
    file = st.file_uploader("Upload csv files", type=["csv"])
    if file is not None:
        st.session_state.file = file
        st.session_state.file_uploaded = True
 
def create_agent():
    llm = AzureOpenAI(
        deployment_name=deployment_name,
        verbose= True,
        temperature= 0
    )
    st.session_state.agent = create_csv_agent(llm, st.session_state.file,  verbose=True, allow_dangerous_code=True)
 
def add_lines_to_pdf(elements):
    max_attempts = 5
    completed_count = 0
    agent = st.session_state.agent
    queries = [
        "give detailed 50 lines summary of csv in marketing analysis?",
        # "predict which video will have highest likes in one month and how much it will be give its name"
    ]
    while max_attempts > 0 and completed_count != len(queries):
        for query in queries:
            response = agent.invoke(query)
            if 'output' in response:
                if(response['output'] == 'Agent stopped due to iteration limit or time limit.'):
                    max_attempts -= 1
                    print(f"Attempts Tried :: {max_attempts}")
                    continue
                else:
                    output = markdown2.markdown(response['output'])
                    elements.append(Paragraph(output, styles['Normal']))
                    elements.append(Spacer(1, 12))
                    completed_count += 1
            else:
                print("No output found in the response")
    if max_attempts == 0:
        print("Agent failed")
 
def add_images_to_pdf(elements):
    max_attempts = 5
    completed_count = 0
    agent = st.session_state.agent
    queries = [
        # "generate bar graph plot and save it in the same directory to the given using matplotlib for top 5 videos with highest views with title in y axis, ensure the title fits within the PNG boundaries by truncating it with only starting 5 letters and add .. to it if it is too long.  print the file name only"
    ]
    while max_attempts > 0 and completed_count != len(queries):
        for query in queries:
            response = agent.invoke(query)
            if 'output' in response:
                if(response['output'] == 'Agent stopped due to iteration limit or time limit.'):
                    max_attempts -= 1
                    print(f"Attempts Tried :: {max_attempts}")
                    continue
                else:
                    img = Image(response['output'])
                    img.width = 300  
                    img.height = 200
                    elements.append(img)
                    elements.append(Spacer(1, 12))
                    completed_count += 1
            else:
                print("No output found in the response")
    if max_attempts == 0:
        print("Agent failed")
    
def display_pdf_preview(pdf_buffer):
    pdf_buffer.seek(0)
    images = []
    with pdfplumber.open(pdf_buffer) as pdf:
        for page in pdf.pages:
            pil_image = page.to_image().original
            images.append(pil_image)
    return images
 
st.write("Please upload a CSV file")
upload_csv()
if st.session_state.file_uploaded:
    st.write("CSV file uploaded successfully.")
    create_agent()
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    elements.append(Paragraph("CSV Data Report", styles['Title']))
    elements.append(Spacer(1, 12))
    add_lines_to_pdf(elements)
    add_images_to_pdf(elements)
    doc.build(elements)
    images = display_pdf_preview(pdf_buffer)
    for img in images:
        st.image(img)
    st.download_button("Download PDF", data=pdf_buffer, file_name="report.pdf", mime="application/pdf")