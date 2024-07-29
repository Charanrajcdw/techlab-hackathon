import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

def length_ctr_correlation(df):
    # Calculate Click Through Rate (CTR)
    df['Total Impressions'] = df["Facebook - Post Impressions - Organic"] + df["Linkedin - Post Impressions"] + df["Twitter - Post Impressions - Advanced"]
    df['Click Through Rate'] = df['Post Link Shortener Clicks'] / df['Total Impressions']

    # Calculate Post Length
    df['Post Length'] = df['Post Text'].apply(len)

    # Find correlation
    correlation = df[['Click Through Rate', 'Post Length']].corr()

    # Print the correlation
    print("Correlation between Click Through Rate and Post Length:")
    print(correlation)

    # Plot the correlation
    plt.scatter(df['Post Length'], df['Click Through Rate'])
    plt.xlabel('Post Length')
    plt.ylabel('Click Through Rate')
    plt.title('Correlation between Post Length and Click Through Rate')
    
    # Save the plot to a BytesIO buffer
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Return the image buffer
    return {"title": "Correlation between Post Length and Click Through Rate", "img": buf, "chart_type": "correlation_chart"}