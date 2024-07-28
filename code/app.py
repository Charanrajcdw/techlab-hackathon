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

        # create agent
        agent = create_agent(df)
        #generate summary of excel
        xlsummary = process_query("give detailed summary of dataframe in marketing analysis format??", agent)
        
        keypoints = ["For dataframe, list the column names along with their data types and the count of missing values",
        "Generate a statistical summary for each numerical column in the Excel file, including metrics such as mean, median, standard deviation, minimum, and maximum values.",
        "For each categorical column in the Excel file, list the unique values and their respective counts."
        "Perform a data quality check on the Excel file to identify any inconsistencies, duplicate rows, or outliers in the data.",
        "List the top 5 and bottom 5 records for each numerical column based on their values."]

        # keypoints = []
        # #generate keypoints
        # for keypointquery in keypointsqueries:
        #     keypoints.append(process_query(keypointquery, agent))

        st.session_state.doc = generatePDf(results, xlsummary, keypoints)   
    doc=st.session_state.doc
    st.download_button("Download PDF", key="button 1", data= doc, file_name="report.pdf", mime="application/pdf")
    pdf_viewer(input= doc.getvalue(), width=700)
    st.download_button("Download PDF", key="button 2", data= doc, file_name="report.pdf", mime="application/pdf")
    
    