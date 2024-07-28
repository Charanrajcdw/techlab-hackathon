import streamlit as st
from utils import *
from predictive_analysis import *
import numpy as np
 
if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False

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
    with st.form("form"):
        account=st.selectbox("Account",df['Account'].unique().tolist(),key="account")
        col1,col2=st.columns(2)
        channel=col1.selectbox("Channel",df['Channel'].unique().tolist(),key="channel")
        video=col2.selectbox("Media Type",df['Media Type'].unique().tolist(),key="type")
        title = st.text_area("Post Title",key="title")
        text = st.text_area("Post Text",key="text")
        labels = st.text_area("Labels (comma separated)",key="labels")
        form=st.form_submit_button("submit")
        if form:
            if text!="" and account!="" and channel!="" and video!="" and title!="" and labels!="":
                value = pd.DataFrame([{
                    'Account': account,
                    'Channel': channel,
                    'Media Type': video,
                    'Post Title': title,
                    'Post Text': text,
                    'Labels': labels,
                    'Post Link Shortener Clicks': np.nan,
                    'ENG': np.nan
                }])
                wENG=predictValue(value)
                st.success(f"Expected Weighted Engagement for this post is {wENG}")
            else:
                st.warning("Enter all fields to continue...")