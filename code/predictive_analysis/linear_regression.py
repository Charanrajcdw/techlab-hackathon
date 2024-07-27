import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.preprocessing import OneHotEncoder
from scipy.sparse import hstack
from textblob import TextBlob
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer


def predictEng(df):

    # One-hot encode categorical features
    categorical_features = ['Account', 'Channel', 'Media Type']
    encoder = OneHotEncoder(sparse_output=False)
    encoded_features = encoder.fit_transform(df[categorical_features])

    # Vectorize text features
    vectorizer = CountVectorizer(max_features=1000)
    title_vectorized = vectorizer.fit_transform(df['Post Title'])
    text_vectorized = vectorizer.fit_transform(df['Post Text'])
    labels_vectorized = vectorizer.fit_transform(df['Labels'])

    # Vectorize text features using TF-IDF
    tfidf_vectorizer = TfidfVectorizer(max_features=1000)
    title_tfidf = tfidf_vectorizer.fit_transform(df['Post Title'])
    text_tfidf = tfidf_vectorizer.fit_transform(df['Post Text'])
    labels_tfidf = tfidf_vectorizer.fit_transform(df['Labels'])

    # Calculate derived attributes
    df['Label Count'] = df['Labels'].apply(lambda x: len(x.split(",")))
    df['Post Length'] = df['Post Text'].apply(len)

    # getting sentimental scores
    df['Title Sentiment'] = df['Post Title'].apply(lambda x: TextBlob(x).sentiment.polarity)
    df['Text Sentiment'] = df['Post Text'].apply(lambda x: TextBlob(x).sentiment.polarity)

    # Combine all features into a single feature set
    additional_features = df[['Label Count', 'Post Length','Title Sentiment','Text Sentiment']].values
    X = hstack((encoded_features, title_tfidf, text_tfidf, labels_tfidf,title_vectorized, text_vectorized, labels_vectorized, additional_features,df[["Post Link Shortener Clicks","ENG"]]))

    # Target variable
    y = df['wENG']
        
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a linear regression model
    pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),
        ('model', LinearRegression())
    ])

    # Train the model using the pipeline
    pipeline.fit(X_train, y_train)

    # Evaluate the model
    y_pred = pipeline.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("Mean Absolute Error:", mae)
    print("Mean Squared Error:", mse)
    print("R-squared:", r2)