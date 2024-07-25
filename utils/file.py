import pandas as pd

def get_df_from_excel(excel_file_path):
    excel_data = pd.ExcelFile(excel_file_path)
    dataframes = {}
    for sheet_name in excel_data.sheet_names:
        df = excel_data.parse(sheet_name)
        dataframes[sheet_name] = df
        print(f"Loaded sheet: {sheet_name}")
    return dataframes


