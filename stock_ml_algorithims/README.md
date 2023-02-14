Stock Price Prediction using Deep Learning
------------------------------------------

This code trains a deep learning model to predict the future stock prices of a specific stock based on historical data, and saves the trained model to disk for later use.

### Libraries Used

-   pandas
-   numpy
-   matplotlib
-   seaborn
-   datetime
-   os
-   yfinance
-   sklearn
-   keras

### Data Retrieval

The code retrieves the historical stock price data of a stock from the past five years using the yfinance library and stores it in a pandas DataFrame.

### Data Processing

The stock price data is then processed by scaling it between 0 and 1 using the MinMaxScaler from sklearn, and converting it into a 3D array for use with an LSTM network. The data is split into training and validation sets using train_test_split from sklearn.

### Model Creation

The model is either loaded from a saved file or created from scratch using the Sequential model from Keras. The model consists of two LSTM layers and one dense layer. The model is trained using the fit method and is stopped using early stopping when the validation loss stops improving after 20 epochs.

### Model Evaluation

The code plots the training history of the model to see how the training loss evolved over the epochs. The model makes predictions on the validation set, and the mean absolute error is calculated. The trained model is then saved to disk.

### Usage

1.  Make sure you have Python installed on your computer.
2.  Run `pip install -r requirements.txt` to install dependencies
4.  Open a command prompt or terminal window and navigate to the directory where you saved the code.
3.  Type the following command to run the code:

`python train_model.py -s [stock symbol] -w [training window]`

Replace `[stock symbol]` with the stock symbol that you want to train the model on (e.g. `AAPL` for Apple Inc.) and replace `[training window]` with the number of days you want to use as the training window (e.g. `30`). The `-w` option is optional, and the default value is `30` if not specified.

For example, to train the model on Apple Inc. stock data with a training window of 60 days, you would run the following command:

`python train_model.py -s AAPL -w 60`

### Flowchart

                                     `+-------------------+
                                      | Load Data         |
                                      +-------------------+
                                          |     |
                                          v     v
                      +--------------------------------+
                      |  Data Processing and Preparation |
                      +--------------------------------+
                                          |
                                          v
                +-----------------------------------+
                |  Load or Create Model              |
                +-----------------------------------+
                                          |
                                          v
                  +------------------------------+
                  |  Train Model                  |
                  +------------------------------+
                                          |
                                          v
                +--------------------------------+
                |  Model Evaluation and Saving    |
                +--------------------------------+`