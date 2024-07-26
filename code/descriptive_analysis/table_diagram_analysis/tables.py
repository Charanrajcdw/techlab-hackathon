import pandas as pd

# For stats calculation
def calculate_stats(df):
    total_posts = df.shape[0]
    total_impressions = df['Facebook - Post Impressions - Organic'].sum() + df['Linkedin - Post Impressions'].sum() + df['Twitter - Post Impressions - Advanced'].sum()
    total_engagements = df['ENG'].sum()
    total_wengagements = df['wENG'].sum()
    total_link_clicks = df['Post Link Shortener Clicks'].sum()
    avg_ctr = total_link_clicks / total_impressions if total_impressions > 0 else 0
    avg_weng_rate = total_wengagements / total_impressions if total_impressions > 0 else 0
    
    return {
        'Total Posts': total_posts,
        'Total Impressions': total_impressions,
        'Total Engagements': total_engagements,
        'Total Weighted Engagements': total_wengagements,
        'Total Link Clicks': total_link_clicks,
        'Avg CTR': f"{round(avg_ctr * 100, 2)}%",
        'Avg wEng Rate': f"{round(avg_weng_rate * 100, 2)}%"
    }


# Function to calculate statistics and format them into a table
def overallStatsTable(df):
    # From the first spreadsheet
    # df = list(dataframes.values())[0]
    
    # Convert columns to numeric types
    df['Facebook - Post Impressions - Organic'] = pd.to_numeric(df['Facebook - Post Impressions - Organic'], errors='coerce')
    df['Linkedin - Post Impressions'] = pd.to_numeric(df['Linkedin - Post Impressions'], errors='coerce')
    df['Twitter - Post Impressions - Advanced'] = pd.to_numeric(df['Twitter - Post Impressions - Advanced'], errors='coerce')
    df['Post Link Shortener Clicks'] = pd.to_numeric(df['Post Link Shortener Clicks'], errors='coerce')
    df['ENG'] = pd.to_numeric(df['ENG'], errors='coerce')
    df['wENG'] = pd.to_numeric(df['wENG'], errors='coerce')

    # Calculate stats for each channel and overall
    facebook_stats = calculate_stats(df[df['Channel'] == 'Facebook'])
    twitter_stats = calculate_stats(df[df['Channel'] == 'Twitter'])
    linkedin_stats = calculate_stats(df[df['Channel'] == 'Linkedin'])
    total_stats = calculate_stats(df)

    # Format and print the results in a table format
    stats_df = pd.DataFrame({
        'Platform/Metric': ['Total Posts', 'Total Impressions', 'Total Engagements', 'Total Weighted Engagements', 'Total Link Clicks', 'Avg CTR', 'Avg wEng Rate'],
        'Facebook': [facebook_stats['Total Posts'], facebook_stats['Total Impressions'], facebook_stats['Total Engagements'], facebook_stats['Total Weighted Engagements'], facebook_stats['Total Link Clicks'], facebook_stats['Avg CTR'], facebook_stats['Avg wEng Rate']],
        'Twitter': [twitter_stats['Total Posts'], twitter_stats['Total Impressions'], twitter_stats['Total Engagements'], twitter_stats['Total Weighted Engagements'], twitter_stats['Total Link Clicks'], twitter_stats['Avg CTR'], twitter_stats['Avg wEng Rate']],
        'Linkedin': [linkedin_stats['Total Posts'], linkedin_stats['Total Impressions'], linkedin_stats['Total Engagements'], linkedin_stats['Total Weighted Engagements'], linkedin_stats['Total Link Clicks'], linkedin_stats['Avg CTR'], linkedin_stats['Avg wEng Rate']],
        'Overall': [total_stats['Total Posts'], total_stats['Total Impressions'], total_stats['Total Engagements'], total_stats['Total Weighted Engagements'], total_stats['Total Link Clicks'], total_stats['Avg CTR'], total_stats['Avg wEng Rate']]
    }).T

    ############### BEGIN : To transpose the arrangement ###############
    # numeric_cols = ['Facebook', 'Twitter', 'Linkedin', 'Overall']
    # stats_df[numeric_cols] = stats_df[numeric_cols].astype(int, errors='ignore')
    ############### END : To transpose the arrangement ###############

    ############### BEGIN : To transpose the arrangement ###############
    # Set the first row as the header
    stats_df.columns = stats_df.iloc[0]
    stats_df = stats_df[1:]

    numeric_cols = ['Total Posts', 'Total Impressions', 'Total Engagements', 'Total Weighted Engagements', 'Total Link Clicks']
    stats_df[numeric_cols] = stats_df[numeric_cols].astype(int, errors='ignore')
    ############### END : To transpose the arrangement ###############

    print(stats_df)