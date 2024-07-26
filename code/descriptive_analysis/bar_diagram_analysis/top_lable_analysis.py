import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO


def analyze_top_10_labels(data):
    df = data['Corp Facebook']
    print(df.head())

    # Initialize a dictionary to aggregate wENG Rate for each label
    label_weng_rate = {}

    # Iterate over each row in the data
    for _, row in df.iterrows():
        labels = row['Labels'].split(',')
        weng_rate = row['wENG']
        for label in labels:
            if weng_rate > 3.0:
                if label in label_weng_rate:
                    label_weng_rate[label] += 1
                else:
                    label_weng_rate[label] = 1
    
    # Convert the dictionary to a DataFrame for easy manipulation
    label_weng_rate_df = pd.DataFrame(list(label_weng_rate.items()), columns=['Labels', 'Count'])
    print(label_weng_rate_df.head())

    # Find the top 10 labels based on wENG Rate
    top_labels = label_weng_rate_df.nlargest(10, 'Count')


    # Plot the bar diagram
    plt.figure(figsize=(10, 6))
    plt.bar(top_labels['Labels'], top_labels['Count'], color='skyblue')
    plt.xlabel('Labels')
    plt.ylabel('Labels count surpassed wENG rate')
    plt.title('Top 10 Performing Labels by wENG Rate')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Save the plot to a BytesIO object
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)  # Rewind the buffer

    # Optional: Display the plot
    #plt.savefig("image.png")

    # img_buffer now contains the PNG image
    return img_buffer

    




