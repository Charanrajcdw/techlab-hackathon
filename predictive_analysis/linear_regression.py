import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.feature_extraction.text import CountVectorizer


def predictEng(df):
    # Load data
    data = df['Corp Facebook']

    # Display the first few rows
    print(data.head())




    # Vectorize the post text
    vectorizer = CountVectorizer(max_features=1000)
    X_text = vectorizer.fit_transform(data['Post Text']).toarray()

    # Combine text features with numerical features
    X = pd.concat([pd.DataFrame(X_text), data[['Media Type', 'Facebook - Post Shares', 'Labels', 'Facebook - Post Impressions - Organic', 'Post Link Shortener Clicks']]], axis=1)
    
    # Ensure all column names are strings
    X.columns = X.columns.astype(str)       
    y = data['wENG']



    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    print(y_pred)

    # Calculate evaluation metrics
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f'Mean Squared Error: {mse}')
    print(f'R^2 Score: {r2}')

