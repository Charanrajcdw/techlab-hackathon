import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import seaborn as sns

def label_ctr_correlation(df):
    # Calculate Click Through Rate (CTR)
    df['Total Impressions'] = df["Facebook - Post Impressions - Organic"] + df["Linkedin - Post Impressions"] + df["Twitter - Post Impressions - Advanced"]
    df['Click Through Rate'] = df['Post Link Shortener Clicks'] / df['Total Impressions']

    # Count the number of labels
    df['Label Count'] = df['Labels'].apply(lambda x: len(x.split(',')))

    # Find correlation
    correlation = df[['Click Through Rate', 'Label Count']].corr()

    # Print the correlation
    print("Correlation between Click Through Rate and Label Count:")
    print(correlation)

    # Plot the correlation
    plt.scatter(df['Label Count'], df['Click Through Rate'])
    plt.xlabel('Label Count')
    plt.ylabel('Click Through Rate')
    plt.title('Correlation between Label Count and Click Through Rate')

    # Save the plot to a BytesIO buffer
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Return the image buffer
    return {"title": "Correlation between Label Count and Click Through Rate", "img": buf, "chart_type": "correlation_chart"}
