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
    fig, ax = plt.subplots(figsize=(5.25, 5.25))  # 3/4th size of the original
    ax.pie(media_counts, labels=media_counts.index, autopct='%1.1f%%', startangle=140)
    ax.set_title(f'{channel} - Media Type Distribution of Posts Surpassing wENG Threshold')
    ax.axis('equal')
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight', pad_inches=0.2)
    img_buffer.seek(0)
    plt.close()
    return img_buffer

# Function to create bar chart and combine pie charts into a single image
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
    plt.figure(figsize=(10, 7))
    channel_counts.plot(kind='bar', color=['#cc0000', '#7f7f7f', '#cc0000'])
    plt.title('Number of Posts Surpassing wENG Thresholds by Channel')
    plt.xlabel('Channel')
    plt.ylabel('Number of Posts')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    
    # Create buffer to return chart
    img_buffer_bar = io.BytesIO()
    plt.savefig(img_buffer_bar, format='png', bbox_inches='tight', pad_inches=0.2)
    img_buffer_bar.seek(0)
    plt.close()

    results.append({"title": "Number of Posts Surpassing wENG Thresholds by Channel", "img": img_buffer_bar, "chart_type": "single_bar_chart"})

    # Create pie charts for each channel
    channels = ['Facebook', 'Linkedin', 'Twitter']
    pie_buffers = []
    for channel in channels:
        channel_df = filtered_df[filtered_df['Channel'] == channel]
        if not channel_df.empty:
            pie_buffers.append(create_pie_chart(channel_df, channel))

    # Combine pie charts into a single image
    fig, axs = plt.subplots(2, 2, figsize=(15, 15), constrained_layout=True)
    axs = axs.flatten()

    for i, buffer in enumerate(pie_buffers):
        img = plt.imread(buffer)
        axs[i].imshow(img)
        axs[i].axis('off')

    # Hide any unused subplot
    for j in range(len(pie_buffers), len(axs)):
        axs[j].axis('off')

    combined_img_buffer = io.BytesIO()
    plt.savefig(combined_img_buffer, format='png', bbox_inches='tight', pad_inches=0.2)
    combined_img_buffer.seek(0)
    plt.close()

    # Add the combined pie charts to the results
    results.append({"title": "Channel wise media type analysis", "img": combined_img_buffer, "chart_type": "collective_bar_chart"})

    return results