import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

def label_wise_analysis(df, specified_labels=None):
    # If no labels are specified, get all unique labels from the dataframe
    if specified_labels is None:
        all_labels = df['Labels'].dropna().unique()
        specified_labels = [label.strip() for sublist in df['Labels'].dropna().apply(lambda x: x.split(',')) for label in sublist]
        specified_labels = list(set(specified_labels))  # Remove duplicates

    # Filter the dataframe to only include rows with the specified labels
    df_filtered = df[df['Labels'].apply(lambda labels: any(label in labels.split(',') for label in specified_labels))]

    # Extract relevant columns and calculate metrics
    df_filtered['Labels'] = df_filtered['Labels'].apply(lambda x: x.split(','))
    labels_stats = pd.DataFrame(columns=['label', 'no.of posts', '% of total posts', 'wEng rate in %', 'wEng/Post', 'Total wEng'])

    stats_list = []

    for label in specified_labels:
        label_df = df_filtered[df_filtered['Labels'].apply(lambda x: label in x)]
        num_posts = len(label_df)
        total_posts = len(df_filtered)
        wEng_rate = (label_df['wENG'].sum() / label_df['Linkedin - Post Impressions'].sum()) * 100 if label_df['Linkedin - Post Impressions'].sum() > 0 else 0
        wEng_post = label_df['wENG'].sum() / num_posts if num_posts > 0 else 0
        total_wEng = label_df['wENG'].sum()
        percent_posts = (num_posts / total_posts) * 100 if total_posts > 0 else 0
        stats_list.append({
            'Label': label,
            'No.of posts': num_posts,
            '% of total posts': f"{percent_posts:.2f}%",
            'wEng rate in %': f"{wEng_rate:.1f}%",
            'wEng/Post': f"{wEng_post:.1f}",
            'Total wEng': total_wEng
        })

    labels_stats = pd.DataFrame(stats_list)

    # Sort the labels_stats by 'Total wEng' in descending order and select the top 5
    labels_stats = labels_stats.sort_values(by='Total wEng', ascending=False).head(5)

    # Plotting
    fig, ax = plt.subplots(figsize=(16, 12))

    # Creating table
    table = ax.table(cellText=labels_stats.values, colLabels=labels_stats.columns, cellLoc='center', loc='center')

    # Formatting table
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width([0, 1, 2, 3, 4, 5])
    table.scale(1, 2)  # Increase row height

    for (i, j), cell in table._cells.items():
        if i == 0:
            cell.set_fontsize(15)
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor('black')
        else:
            if i % 2 == 0:
                cell.set_facecolor((204/255, 0, 0, 0.3))  # red RGB with alpha
            else:
                cell.set_facecolor('white')
        cell.set_edgecolor('black')

    ax.axis('off')

    # Adjust layout
    plt.subplots_adjust(left=0.05, right=0.95, top=0.85, bottom=0.1)

    # Save the plot to a BytesIO buffer
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.5)
    buf.seek(0)
    plt.close(fig)  # Close the figure to free up memory

    # Return the image buffer
    return {"title": "Top performing Labels - Statistics", "img": buf, "chart_type": "table"}
