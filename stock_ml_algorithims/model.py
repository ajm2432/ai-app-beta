import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import os
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense, LSTM
from keras.callbacks import EarlyStopping

file_path = 'stock_ml_algorithims/stock_price_prediction.h5'
directory = 'stock_symbol_data'

class actions:
    def five_years_ago():
        now = datetime.datetime.now()
        five_years_ago = now - datetime.timedelta(days=1825)
        return five_years_ago

    def one_year_ago():
        now = datetime.datetime.now()
        one_year_ago = now - datetime.timedelta(days=365)
        return one_year_ago

    def train_model(self,ticker, window):

        ytd = self.five_years_ago()

        # Download the last year of data
        data = yf.download(ticker, start=ytd)

        # Load the stock price data into a pandas DataFrame
        df = pd.DataFrame(data)
        # Store the data as a CSV file
        df.to_csv(f"{directory}/{ticker}_last_year.csv")
        # Read CSV
        df = pd.read_csv(f"{directory}/{ticker}_last_year.csv", index_col='Date', parse_dates=True)

        # Plot the stock price data
        plt.figure(1)
        sns.lineplot(data=df['Close'])
        plt.title('Stock Price over Time')
        plt.xlabel('Date')
        plt.ylabel('Price')

        # Scale the stock price data to be between 0 and 1
        scaler = MinMaxScaler(feature_range=(0, 1))
        print(df)
        print(df[['Open','High']])
        df['Close'] = scaler.fit_transform(df['Close'].values.reshape(-1, 1))
    

        # Convert the stock price data into a 3D array for use with an LSTM network
        def create_inputs(df, look_back=1):
            inputs = []
            for i in range(len(df) - look_back):
                inputs.append(df[i:i + look_back].values)
            return np.array(inputs)

        look_back = window # Use the last 30 days of stock prices as input features
        X = create_inputs(df['Close'], look_back=look_back)
        y = df['Close'][look_back:].values

        # Split the data into training and validation sets
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, random_state=69)

        # Reshape the data for use with an LSTM network
        X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
        X_val = X_val.reshape(X_val.shape[0], X_val.shape[1], 1)

        if os.path.exists(file_path):
            model = load_model('stock_price_prediction.h5')
            # Train the LSTM network, using early stopping to avoid overfitting
            early_stopping = EarlyStopping(monitor='val_loss', patience=20)
            history = model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_val, y_val), callbacks=[early_stopping], verbose=1)
        else:
            model = Sequential()
            model.add(LSTM(units=100, return_sequences=True, input_shape=(X_train.shape[1], 1)))
            model.add(LSTM(units=100, return_sequences=False))
            model.add(Dense(units=1))
            model.compile(optimizer='adam', loss='mean_squared_error')
            early_stopping = EarlyStopping(monitor='val_loss', patience=20)
            history = model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_val, y_val), callbacks=[early_stopping], verbose=1)
            # Define the LSTM network
            


        # Plot the training history to see how the network training loss evolved
        plt.figure(2)
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('Model Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend(['Train', 'Validation'], loc='upper right')

        # Make predictions on the validation set
        val_predictions = model.predict(X_val)

        #Plot the actual vs predicted stock prices on the validation set
        plt.figure(3)
        plt.plot(scaler.inverse_transform(y_val.reshape(-1, 1)), label='Actual')
        plt.plot(scaler.inverse_transform(val_predictions.reshape(-1, 1)), label='Predicted')
        plt.title('Actual vs Predicted Stock Prices')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        val_actual = scaler.inverse_transform(y_val.reshape(-1, 1))
        val_predicted = scaler.inverse_transform(val_predictions)
        mae = mean_absolute_error(val_actual, val_predicted)
        accuracy = (1 - (mae / np.mean(val_actual))) * 100

        print(accuracy)
        plt.suptitle("Model Accuracy: {:.2f}%".format(accuracy))
        plt.show()
        if accuracy >= 60: 
            model.save('stock_price_prediction.h5')  
            print("Accuracy is above 60%, model saved 👍")
        else: 
            print("Accuracy is below 60%, model not saved 🤔")
    
    def predict_stock(self, ticker, days):
               
        ytd = self.one_year_ago()

        # Download the last year of data
        data = yf.download(ticker, start=ytd)

        # Load the stock price data into a pandas DataFrame
        df = pd.DataFrame(data)
        # Store the data as a CSV file
        df.to_csv(f"{ticker}_last_year.csv")
        # Read CSV
        df = pd.read_csv(f"{ticker}_last_year.csv", index_col='Date', parse_dates=True)
        # Load the trained model
        model = load_model(file_path)

        # Scale the stock price data
        scaler = MinMaxScaler(feature_range=(0, 1))

        # Print last 30 day csv info
        df['Close'] = scaler.fit_transform(df['Close'].values.reshape(-1, 1))

        # Get the latest 30 days of data for use as input features
        last_30_days = df['Close'][-30:].values.reshape(1, 30, 1)
        latest_data = df['Close'][-days:].values.reshape(1, days, 1)
        # Use the model to make predictions for the next 5 days
        predictions = []
        for i in range(days):
            prediction = model.predict(last_30_days)
            predictions.append(prediction[0][0])
            last_30_days = np.append(last_30_days[0][1:], prediction).reshape(1, 30, 1)
        # Invert the scaled predictions to get the actual stock prices
        predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
        last_30_days = scaler.inverse_transform(np.array(latest_data).reshape(-1, 1))
        return predictions[:,0]