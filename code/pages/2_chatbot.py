import streamlit as st
from utils import *
from predictive_analysis import *

if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False

if not st.session_state.file_uploaded:
    st.write("Please upload a XLSX file")
    file = st.file_uploader("Upload xlsx files", type=["xlsx"])
    if file is not None:
        dataframes = get_df_from_excel(file)
        if dataframes.get("posts-20240403T080714-0500") is not None:
            st.session_state.dataframes = dataframes
            st.session_state.file_uploaded = True  
            createModel(st.session_state.dataframes["posts-20240403T080714-0500"])  
            st.rerun()        
        else:
            st.write("Unsupported file uploaded for marketing analysis, please upload a file with mandatory fields")               

if st.session_state.file_uploaded:
    df = st.session_state.dataframes["posts-20240403T080714-0500"]
    agent = create_agent(df)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Ask questions about excel?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Process the query and get the response
        try:
            response = process_query(prompt, agent)
            if response == "[python_repl_ast] is not a valid tool, try one of [python_repl_ast].":
                raise RuntimeError() 
        except RuntimeError as e:
            response = "Oops! Unable to process that query"
        except Exception as e:
            response = "Oops! Unable to process that query"
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})