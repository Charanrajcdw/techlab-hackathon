import streamlit as st
from utils import *
from descriptive_analysis import *
from predictive_analysis import *
import pdfplumber 
from streamlit_pdf_viewer import pdf_viewer

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

if not st.session_state.file_uploaded:
    st.write("Please upload a XLSX file")
    file = st.file_uploader("Upload xlsx files", type=["xlsx"])
    if file is not None:
        st.session_state.dataframes = get_df_from_excel(file)
        st.session_state.file_uploaded = True  
        createModel(st.session_state.dataframes["posts-20240403T080714-0500"])  
        st.rerun()                

if st.session_state.file_uploaded:
    df = st.session_state.dataframes["posts-20240403T080714-0500"]
    if "doc" not in st.session_state:
        results.append(analyze_top_10_labels(df))
        results.extend(create_channel_pie(df))
        results.append(label_wise_analysis(df))
        results.append(overall_analysis(df))
        results.append(linkedin_analysis(df))
        results.append(facebook_analysis(df))
        results.append(twitter_analysis(df))
        results.append(overallStatsTable(df))

        # TODO :: need to get Summary text from LLM for first page XL Summary -> As of now Hard coding it
        xlsummary = dummysummary
        # TODO :: need to get keypoints text from LLM for second page -> As of now Hard coding it
        keypoints = ["point 1 "," point 2" ,"point 3" ,"point 4", "point 5"]

        st.session_state.doc = generatePDf(results, dummysummary, keypoints)   
    doc=st.session_state.doc
    st.download_button("Download PDF", key="button 1", data= doc, file_name="report.pdf", mime="application/pdf")
    pdf_viewer(input= doc.getvalue(), width=700)
    st.download_button("Download PDF", key="button 2", data= doc, file_name="report.pdf", mime="application/pdf")
    
    #     agent = create_agent(df)
    #     queries = ["give no of columns and rows in file"]
    #     for query in queries:
    #         response=process_query(query,agent)
    