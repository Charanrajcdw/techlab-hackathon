import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

def overall_analysis(df):
    # Convert columns to numeric types
    df['Linkedin - Post Impressions'] = pd.to_numeric(df['Linkedin - Post Impressions'], errors='coerce')
    df['Twitter - Post Impressions - Advanced'] = pd.to_numeric(df['Twitter - Post Impressions - Advanced'], errors='coerce')
    df['Post Link Shortener Clicks'] = pd.to_numeric(df['Post Link Shortener Clicks'], errors='coerce')
    df['ENG'] = pd.to_numeric(df['ENG'], errors='coerce')
    df['wENG'] = pd.to_numeric(df['wENG'], errors='coerce')

    # Aggregate data by Media Type
    agg_df = df.groupby('Media Type').agg({
        'wENG': 'sum',
        'Post Link Shortener Clicks': 'sum',
        'ENG': 'sum',
        'Linkedin - Post Impressions': 'sum',
        'Twitter - Post Impressions - Advanced': 'sum'
    }).reset_index()

    # Calculate additional metrics
    agg_df['Total Impressions'] = agg_df['Linkedin - Post Impressions'] + agg_df['Twitter - Post Impressions - Advanced']
    agg_df['wENG Rate'] = (agg_df['wENG'] / agg_df['Total Impressions']) * 100
    agg_df['wENG/post'] = agg_df['wENG'] / agg_df['ENG']
    agg_df['CTR'] = (agg_df['Post Link Shortener Clicks'] / agg_df['Total Impressions']) * 100

    # Plot bar diagrams for each metric
    metrics = ['wENG', 'wENG Rate', 'wENG/post', 'Post Link Shortener Clicks', 'CTR']
    metric_labels = ['Weighted Engagements (wENG)', 'Weighted Engagement Rate (wENG Rate)', 'Weighted Engagements per Post (wENG/post)', 'Link Clicks', 'Click Through Rate (CTR)']

    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(20, 20))
    axes = axes.flatten()

    for idx, metric in enumerate(metrics):
        axes[idx].bar(agg_df['Media Type'], agg_df[metric], color='skyblue')
        axes[idx].set_title(metric_labels[idx], fontsize=18, pad=20.0)
        axes[idx].set_xlabel('Media Type')
        axes[idx].set_ylabel(metric_labels[idx])

    # Remove the empty subplot
    fig.delaxes(axes[5])

    # Add a common heading for the entire figure
    # fig.suptitle('Overall Performance Analysis by Media Type', fontsize=20, color="red", fontweight=600)

    # Adjust layout to give ample space and margins
    plt.subplots_adjust(left=0.09, right=0.95, top=0.9, bottom=0.05, hspace=0.4, wspace=0.2)

    # Save the plot to a BytesIO buffer
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)  # Close the figure to free up memory

    # Return the image title and buffer
    return {"title": "Overall Performance Analysis by Media Type", "img": buf, "chart_type": "collective_bar_chart"}
