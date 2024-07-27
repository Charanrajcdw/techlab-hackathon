import streamlit as st
import io
import markdown2
from dotenv import load_dotenv
from utils import *
from descriptive_analysis import *
from predictive_analysis import *
import pdfplumber 
from streamlit_pdf_viewer import pdf_viewer

load_dotenv()

# Define the custom HTML and CSS
custom_html = """
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
<style>
    .custom-text {
        font-size: 20px;
        text-align: center;
        font-family: 'Poppins', sans-serif;
        margin-bottom: 40px;
    }
</style>
<div class="custom-text">CDW AI AUTOMATED MARKETING ANALYSIS</div>
"""
 
# Write the custom HTML to the Streamlit app
st.markdown(custom_html, unsafe_allow_html=True)

dummysummary = "Social media marketing analysis involves the systematic study of social media platforms to understand and optimize marketing efforts. It encompasses various metrics, methodologies" 
 

if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False
 
def upload_csv():
    file = st.file_uploader("Upload xlsx files", type=["xlsx"])
    if file is not None:
        st.session_state.file = file
        st.session_state.file_uploaded = True  

def display_pdf_preview(pdf_buffer):
    pdf_buffer.seek(0)
    images = []
    with pdfplumber.open(pdf_buffer) as pdf:
        for page in pdf.pages:
            pil_image = page.to_image().original
            images.append(pil_image)
    return images                  

# Initialize the results array
results = []

st.write("Please upload a XLSX file")
upload_csv()
if st.session_state.file_uploaded:
    st.write("XLSX file uploaded successfully.")
    dataframes = get_df_from_excel(st.session_state.file)
    results.append( analyze_top_10_labels(dataframes["posts-20240403T080714-0500"]) )
    results.extend( create_channel_pie(dataframes["posts-20240403T080714-0500"]))
    results.append( label_wise_analysis(dataframes["posts-20240403T080714-0500"]) )
    results.append( overall_analysis(dataframes["posts-20240403T080714-0500"]) )
    results.append( linkedin_analysis(dataframes["posts-20240403T080714-0500"]) )
    results.append( facebook_analysis(dataframes["posts-20240403T080714-0500"]) )
    results.append( twitter_analysis(dataframes["posts-20240403T080714-0500"]) )
    results.append( overallStatsTable(dataframes["posts-20240403T080714-0500"]) )

    # TODO :: need to get Summary text from LLM for first page XL Summary -> As of now Hard coding it
    xlsummary = dummysummary
    # TODO :: need to get keypoints text from LLM for second page -> As of now Hard coding it
    keypoints = ["point 1 "," point 2" ,"point 3" ,"point 4", "point 5"]

    doc = generatePDf(results, dummysummary, keypoints)   

    st.download_button("Download PDF", key="button 1", data= doc, file_name="report.pdf", mime="application/pdf")
    pdf_viewer(input= doc.getvalue(),
                   width=700)
    st.download_button("Download PDF", key="button 2", data= doc, file_name="report.pdf", mime="application/pdf")
    
    # pdf_buffer = io.BytesIO()
    # add_lines_to_elements("Social Media Data Report","Title")
    # for sheet_name, df in dataframes.items():
    #     print(f"Processing sheet: {sheet_name}")
    #     agent = create_agent(df)
    #     queries = ["give no of columns and rows in file"]
    #     for query in queries:
    #         response=process_query(query,agent)
    #         add_lines_to_elements(markdown2.markdown(response))
    # build_pdf(pdf_buffer)
    # images = get_pdf_preview(pdf_buffer)
    # for img in images:
    #     st.image(img)
    # st.download_button("Download PDF", data=pdf_buffer, file_name="report.pdf", mime="application/pdf")