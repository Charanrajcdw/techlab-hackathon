import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import seaborn as sns

def label_weng_correlation(df):
    # Calculate label count
    df['Label Count'] = df['Labels'].apply(lambda x: len(x.split(',')))

    # Compute the correlation
    correlation = df[['Label Count', 'wENG']].corr().iloc[0, 1]

    # Print the correlation
    print(f'Correlation between label count and wENG: {correlation}')

    # Plot the correlation using seaborn
    plt.figure(figsize=(10, 6))
    sns.regplot(x='Label Count', y='wENG', data=df, scatter_kws={'s': 50}, line_kws={'color': 'red'})
    plt.title(f'Correlation between Label Count and wENG (Correlation: {correlation:.2f})')
    plt.xlabel('Label Count')
    plt.ylabel('wENG')
    plt.grid(True)

    # Save the plot to a BytesIO buffer
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Return the image buffer
    return {"title": "Correlation between Label Count and wENG", "img": buf, "chart_type": "correlation_chart"}
