import streamlit as st
import io
import markdown2
from dotenv import load_dotenv
from utils import *
from descriptive_analysis import *
from predictive_analysis import *

load_dotenv()
 
if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False
 
def upload_csv():
    file = st.file_uploader("Upload xlsx files", type=["xlsx"])
    if file is not None:
        st.session_state.file = file
        st.session_state.file_uploaded = True                    

# Initialize the results array
results = []

st.write("Please upload a XLSX file")
upload_csv()
if st.session_state.file_uploaded:
    st.write("XLSX file uploaded successfully.")
    dataframes = get_df_from_excel(st.session_state.file)
        
    # create_channel_pie(dataframes["posts-20240403T080714-0500"])
    # results.append( label_wise_analysis(dataframes["posts-20240403T080714-0500"]) )
    # results.append( overall_analysis(dataframes["posts-20240403T080714-0500"]) )
    # results.append( linkedin_analysis(dataframes["posts-20240403T080714-0500"]) )
    # results.append( facebook_analysis(dataframes["posts-20240403T080714-0500"]) )
    # results.append( twitter_analysis(dataframes["posts-20240403T080714-0500"]) )
    # results.append( overallStatsTable(dataframes["posts-20240403T080714-0500"]) )
    
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