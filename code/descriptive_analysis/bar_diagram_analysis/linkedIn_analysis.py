import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

def linkedin_analysis(df):
    # Filter data for LinkedIn
    linkedin_df = df[df['Channel'] == 'Linkedin'].copy()  # Make a copy to avoid SettingWithCopyWarning
    
    # Convert relevant columns to numeric types using .loc to avoid warnings
    linkedin_df.loc[:, 'Linkedin - Post Impressions'] = pd.to_numeric(linkedin_df['Linkedin - Post Impressions'], errors='coerce')
    linkedin_df.loc[:, 'Linkedin - Post Likes'] = pd.to_numeric(linkedin_df['Linkedin - Post Likes'], errors='coerce')
    linkedin_df.loc[:, 'Linkedin - Post Shares'] = pd.to_numeric(linkedin_df['Linkedin - Post Shares'], errors='coerce')
    linkedin_df.loc[:, 'Linkedin - Post Video Views 3s'] = pd.to_numeric(linkedin_df['Linkedin - Post Video Views 3s'], errors='coerce')
    linkedin_df.loc[:, 'Post Link Shortener Clicks'] = pd.to_numeric(linkedin_df['Post Link Shortener Clicks'], errors='coerce')
    linkedin_df.loc[:, 'ENG'] = pd.to_numeric(linkedin_df['ENG'], errors='coerce')
    linkedin_df.loc[:, 'wENG'] = pd.to_numeric(linkedin_df['wENG'], errors='coerce')

    # Aggregate data by Media Type
    agg_df = linkedin_df.groupby('Media Type').agg({
        'wENG': 'sum',
        'Post Link Shortener Clicks': 'sum',
        'ENG': 'sum',
        'Linkedin - Post Impressions': 'sum'
    }).reset_index()

    # Calculate additional metrics specific to LinkedIn
    agg_df['wENG Rate'] = (agg_df['wENG'] / agg_df['Linkedin - Post Impressions']) * 100
    agg_df['wENG/post'] = agg_df['wENG'] / agg_df['ENG']
    agg_df['CTR'] = (agg_df['Post Link Shortener Clicks'] / agg_df['Linkedin - Post Impressions']) * 100

    # Plot bar diagrams for each metric
    metrics = ['wENG', 'wENG Rate', 'wENG/post', 'Post Link Shortener Clicks', 'CTR']
    metric_labels = ['Weighted Engagements (wENG)', 'Weighted Engagement Rate (wENG Rate %)', 'Weighted Engagements per Post (wENG/post)', 'Link Clicks', 'Click Through Rate (CTR %)']

    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(20, 20))
    axes = axes.flatten()

    for idx, metric in enumerate(metrics):
        axes[idx].bar(agg_df['Media Type'], agg_df[metric], color='skyblue')
        axes[idx].set_title(metric_labels[idx], fontsize=18, pad=20.0)
        axes[idx].set_xlabel('Media Type')
        axes[idx].set_ylabel(metric_labels[idx])

    # Remove the empty subplot
    fig.delaxes(axes[5])

    # Adjust layout to give ample space and margins
    plt.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.05, hspace=0.4, wspace=0.3)

    # Save the plot to a BytesIO buffer
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)  # Close the figure to free up memory

    # Return the image buffer
    return {"title": "LinkedIn Performance Analysis by Media Type", "img": buf, "chart_type": "collective_bar_chart"}
