from sklearn.linear_model import LinearRegression
import numpy as np

def train_trend_model(df):

    df = df.sort_values('date')

    df['day'] = np.arange(len(df))

    X = df[['day']]
    y = df['PM2.5']

    model = LinearRegression()
    model.fit(X, y)

    df['trend'] = model.predict(X)

    return df, model
