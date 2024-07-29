import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import seaborn as sns

def length_weng_correlation(df):
    # Calculate post length
    df['Post Length'] = df['Post Text'].apply(len)

    # Compute the correlation
    correlation = df[['Post Length', 'wENG']].corr().iloc[0, 1]

    # Print the correlation
    print(f'Correlation between post length and wENG: {correlation}')

    # Plot the correlation
    plt.figure(figsize=(10, 6))
    sns.regplot(x='Post Length', y='wENG', data=df, scatter_kws={'s': 50}, line_kws={'color': 'red'})
    plt.title(f'Correlation between Post Length and wENG (Correlation: {correlation:.2f})')
    plt.xlabel('Post Length')
    plt.ylabel('wENG')
    plt.grid(True)

    # Save the plot to a BytesIO buffer
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Return the image buffer
    return {"title": "Correlation between Post Length and wENG", "img": buf, "chart_type": "correlation_chart"}
