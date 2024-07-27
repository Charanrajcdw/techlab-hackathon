import pandas as pd
import matplotlib.pyplot as plt

def twitter_analysis(df):
    # Filter data for Twitter
    twitter_df = df[df['Channel'] == 'Twitter'].copy()  # Make a copy to avoid SettingWithCopyWarning
    
    # Convert relevant columns to numeric types using .loc to avoid warnings
    twitter_df.loc[:, 'Twitter - Post Impressions - Advanced'] = pd.to_numeric(twitter_df['Twitter - Post Impressions - Advanced'], errors='coerce')
    twitter_df.loc[:, 'Twitter - Post Likes - Advanced'] = pd.to_numeric(twitter_df['Twitter - Post Likes - Advanced'], errors='coerce')
    twitter_df.loc[:, 'Twitter - Post Replies - Advanced'] = pd.to_numeric(twitter_df['Twitter - Post Replies - Advanced'], errors='coerce')
    twitter_df.loc[:, 'Twitter - Post Retweets - Advanced'] = pd.to_numeric(twitter_df['Twitter - Post Retweets - Advanced'], errors='coerce')
    twitter_df.loc[:, 'Twitter - Post Retweets - Quoted - Advanced'] = pd.to_numeric(twitter_df['Twitter - Post Retweets - Quoted - Advanced'], errors='coerce')
    twitter_df.loc[:, 'Twitter - Post Video Views - Advanced'] = pd.to_numeric(twitter_df['Twitter - Post Video Views - Advanced'], errors='coerce')
    twitter_df.loc[:, 'Post Link Shortener Clicks'] = pd.to_numeric(twitter_df['Post Link Shortener Clicks'], errors='coerce')
    twitter_df.loc[:, 'ENG'] = pd.to_numeric(twitter_df['ENG'], errors='coerce')
    twitter_df.loc[:, 'wENG'] = pd.to_numeric(twitter_df['wENG'], errors='coerce')

    # Aggregate data by Media Type
    agg_df = twitter_df.groupby('Media Type').agg({
        'wENG': 'sum',
        'Post Link Shortener Clicks': 'sum',
        'ENG': 'sum',
        'Twitter - Post Impressions - Advanced': 'sum'
    }).reset_index()

    # Calculate additional metrics specific to Twitter
    agg_df['wENG Rate'] = (agg_df['wENG'] / agg_df['Twitter - Post Impressions - Advanced']) * 100
    agg_df['wENG/post'] = agg_df['wENG'] / agg_df['ENG']
    agg_df['CTR'] = (agg_df['Post Link Shortener Clicks'] / agg_df['Twitter - Post Impressions - Advanced']) * 100

    # Plot bar diagrams for each metric
    metrics = ['wENG', 'wENG Rate', 'wENG/post', 'Post Link Shortener Clicks', 'CTR']
    metric_labels = ['Weighted Engagements (wENG)', 'Weighted Engagement Rate (wENG Rate %)', 'Weighted Engagements per Post (wENG/post)', 'Link Clicks', 'Click Through Rate (CTR %)']

    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(20, 20))
    axes = axes.flatten()

    for idx, metric in enumerate(metrics):
        axes[idx].bar(agg_df['Media Type'], agg_df[metric], color='skyblue')
        axes[idx].set_title(metric_labels[idx])
        axes[idx].set_xlabel('Media Type')
        axes[idx].set_ylabel(metric_labels[idx])

    # Remove the empty subplot
    fig.delaxes(axes[5])

    # Add a common heading for the entire figure
    fig.suptitle('Twitter Performance Analysis by Media Type', fontsize=20, color="red", fontweight=600)

    # Adjust layout to give ample space and margins
    plt.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.05, hspace=0.4, wspace=0.3)

    # Save the plot as a PNG image
    plt.savefig('twitter_mediaType_metrics.png')
