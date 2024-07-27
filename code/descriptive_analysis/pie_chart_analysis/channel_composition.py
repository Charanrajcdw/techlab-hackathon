import pandas as pd
import matplotlib.pyplot as plt
import io

# Define the thresholds for each channel
thresholds = {
    'Facebook': 3.0,
    'Linkedin': 9.2,
    'Twitter': 2.8
}

# Function to create pie chart based on Media Type for each channel
def create_pie_chart(ax, df, channel):
    media_counts = df['Media Type'].value_counts()
    wedges, texts, autotexts = ax.pie(media_counts, labels=media_counts.index, autopct='%1.1f%%', startangle=140, pctdistance=0.85)
    ax.set_title(f'{channel} - Media Type Distribution of Posts Surpassing wENG Threshold')
    ax.axis('equal')
    
    # Adjust pie chart size
    for wedge in wedges:
        wedge.set_edgecolor('white')

def create_channel_pie(df):
    results = []

    # Initialize an empty DataFrame to store filtered data
    filtered_dfs = []

    # Apply the thresholds for each channel and store the filtered data
    for channel, threshold in thresholds.items():
        filtered_df = df[(df['Channel'] == channel) & (df['wENG'] > threshold)]
        filtered_dfs.append(filtered_df)

    # Concatenate all filtered DataFrames
    filtered_df = pd.concat(filtered_dfs)

    # Count the occurrences of each channel in the filtered data
    channel_counts = filtered_df['Channel'].value_counts()

    # Create a bar chart
    fig, axs = plt.subplots(2, 2, figsize=(15, 12))

    # Bar chart
    axs[0, 0].bar(channel_counts.index, channel_counts.values, color=['blue', 'green', 'red'])
    axs[0, 0].set_title('Number of Posts Surpassing wENG Thresholds by Channel')
    axs[0, 0].set_xlabel('Channel')
    axs[0, 0].set_ylabel('Number of Posts')
    axs[0, 0].tick_params(axis='x', rotation=45)
    axs[0, 0].grid(axis='y')

    # Create pie charts for each channel
    channels = ['Facebook', 'Linkedin', 'Twitter']
    for i, channel in enumerate(channels):
        ax = axs[(i + 1) // 2, (i + 1) % 2]  # Position of the pie charts
        channel_df = filtered_df[filtered_df['Channel'] == channel]
        if not channel_df.empty:
            create_pie_chart(ax, channel_df, channel)
        else:
            ax.set_visible(False)

    # Hide the empty subplot (bottom-right corner)
    axs[1, 1].set_visible(False)

    # Adjust layout to avoid overlapping
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.4, hspace=0.4)

    # Create a buffer to return the chart
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight')
    img_buffer.seek(0)

    return {
        "title": "Channel wise media type analysis",
        "img": img_buffer,
        "chart_type" : "collective_pie_chart"
    }