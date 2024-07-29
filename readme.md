# Like Minded Aces -  CDW AI Automated Marketing Analysis Application

## Overview

The **CDW AI Automated Marketing Analysis Application** is a Streamlit-based web application designed to provide comprehensive marketing analysis through automated processes. It reads marketing data from an uploaded XLSX file, performs various analyses, and generates a detailed PDF report.

## Hosted Link

You can access the application online at [https://like-minded-aces.streamlit.app/](https://like-minded-aces.streamlit.app/).

## Features

- Automated extraction and display of PDF with descriptive analysis data and ability to download the pdf.
- Comprehensive analysis of marketing data across different channels (LinkedIn, Facebook, Twitter).
- Chatbot that can be used to ask multilingual questions related to the excel file.
- Predictive analysis form that can be used to find the weighted engineering for a new post

## Requirements

- numpy
- pandas
- reportlab
- pdfplumber
- markdown2
- langchain
- langchain_experimental
- langchain_openai
- statsmodels
- streamlit
- matplotlib
- scikit-learn
- textblob
- streamlit_pdf_viewer
- openpyxl
- tabulate
- seaborn

## Usage

1. Run the Streamlit app:
    ```bash
    cd code
    streamlit run app.py
    ```
    (While running in localhost change the logo path from "code/logo.png" to "./logo.png" in the file /code/utils/pdfgeneration.py)

2. Open your web browser and go to `http://localhost:8501`.

3. Upload an XLSX file containing your marketing data.

4. The application will process the data and display the results. You can preview and download the generated PDF report.

5. Visit the page wENG predictor to predict the weighted engineering for the new post.

6. Visit the page Chatbot to ask questions related to the excel file uploaded.
