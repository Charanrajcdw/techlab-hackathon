from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from scipy.sparse import hstack
from textblob import TextBlob
from sklearn.pipeline import Pipeline
from sklearn.impute import KNNImputer
import joblib
from scipy.sparse import hstack, csr_matrix

def createModel(df):
    # One-hot encode categorical features
    categorical_features = ['Account', 'Channel', 'Media Type']
    encoder = OneHotEncoder(sparse_output=True, handle_unknown='ignore')
    encoded_features = encoder.fit_transform(df[categorical_features])

    # Calculate derived attributes
    df['Label Count'] = df['Labels'].apply(lambda x: len(x.split(",")))
    df['Post Length'] = df['Post Text'].apply(len)
    df['Title Sentiment'] = df['Post Title'].apply(lambda x: TextBlob(x).sentiment.polarity)
    df['Text Sentiment'] = df['Post Text'].apply(lambda x: TextBlob(x).sentiment.polarity)

    # Combine all features into a single feature set
    additional_features = csr_matrix(df[['Label Count', 'Post Length', 'Title Sentiment', 'Text Sentiment']].values)
    post_link_clicks_eng = csr_matrix(df[["Post Link Shortener Clicks", "ENG"]].values)
    X_sparse = hstack((encoded_features, additional_features, post_link_clicks_eng))

    # Convert sparse matrix to dense format
    X_dense = X_sparse.toarray()

    # Target variable
    y = df['wENG']
        
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_dense, y, test_size=0.2, random_state=42)

    # Train a linear regression model
    pipeline = Pipeline([
        ('imputer', KNNImputer(n_neighbors=10)),
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

    # Save the model and transformers
    joblib.dump(pipeline, 'model.pkl')
    joblib.dump(encoder, 'encoder.pkl')

def predictValue(value):
    # Load the trained model and transformers
    loaded_pipeline = joblib.load('model.pkl')
    encoder = joblib.load('encoder.pkl')
    categorical_features = ['Account', 'Channel', 'Media Type']
    
    # Apply preprocessing
    encoded_features = encoder.transform(value[categorical_features])

    value['Label Count'] = value['Labels'].apply(lambda x: len(x.split(",")))
    value['Post Length'] = value['Post Text'].apply(len)
    value['Title Sentiment'] = value['Post Title'].apply(lambda x: TextBlob(x).sentiment.polarity)
    value['Text Sentiment'] = value['Post Text'].apply(lambda x: TextBlob(x).sentiment.polarity)

    additional_features = csr_matrix(value[['Label Count', 'Post Length', 'Title Sentiment', 'Text Sentiment']].values)
    post_link_clicks_eng = csr_matrix(value[['Post Link Shortener Clicks', 'ENG']].values)
    new_value_sparse = hstack((encoded_features, additional_features, post_link_clicks_eng))

    # Convert sparse matrix to dense format
    new_value_dense = new_value_sparse.toarray()

    # Predict using the loaded model
    prediction = loaded_pipeline.predict(new_value_dense)
    return prediction[0]
