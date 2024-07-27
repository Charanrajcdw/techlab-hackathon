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
def create_pie_chart(df, channel):
    media_counts = df['Media Type'].value_counts()
    plt.figure(figsize=(7, 7))
    plt.pie(media_counts, labels=media_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title(f'{channel} - Media Type Distribution of Posts Surpassing weng Threshold')
    plt.axis('equal')
    plt.savefig(f'{channel}_media_type_pie_chart.png')
    plt.close()

def create_channel_pie(df):
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
    plt.figure(figsize=(10, 7))
    channel_counts.plot(kind='bar', color=['blue', 'green', 'red'])
    plt.title('Number of Posts Surpassing wENG Thresholds by Channel')
    plt.xlabel('Channel')
    plt.ylabel('Number of Posts')
    plt.xticks(rotation=45)
    plt.grid(axis='y')

    # Create pie charts for each channel
    channels = ['Facebook', 'Linkedin', 'Twitter']
    for channel in channels:
        channel_df = filtered_df[filtered_df['Channel'] == channel]
        if not channel_df.empty:
            create_pie_chart(channel_df, channel)

    # create buffer to return chart
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)

    return img_buffer
