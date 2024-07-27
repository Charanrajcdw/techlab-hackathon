import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import OneHotEncoder
from scipy.sparse import hstack


def predictEng(data):
    df = data['Corp Facebook']
    print(df.head())

    # One-hot encode categorical features
    categorical_features = ['Account', 'Channel', 'Media Type']
    encoder = OneHotEncoder(sparse_output=False)
    encoded_features = encoder.fit_transform(df[categorical_features])

    # Vectorize text features
    vectorizer = CountVectorizer(max_features=1000)
    title_vectorized = vectorizer.fit_transform(df['Post Title'])
    text_vectorized = vectorizer.fit_transform(df['Post Text'])
    labels_vectorized = vectorizer.fit_transform(df['Labels'])

    # Combine all features into a single feature set
    X = hstack((encoded_features, title_vectorized, text_vectorized, labels_vectorized, df[['Facebook - Post Comments', 'Facebook - Post Impressions - Organic', 'Facebook - Post Reactions', 'Facebook - Post Shares', 'Facebook - Post Video Views 3s - Organic', 'Post Link Shortener Clicks', 'ENG']]))

    # Target variable
    y = df['wENG']
        
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)
    print("Mean Absolute Error:", mae)
    print("Mean Squared Error:", mse)
    print("R-squared:", r2)
    print("Accuracy:",accuracy)

