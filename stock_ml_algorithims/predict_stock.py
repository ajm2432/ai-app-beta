import argparse
import matplotlib.pyplot as plt
from model import actions

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict the stock price of a given ticker.")
    parser.add_argument("-t","--ticker", type=str, help="The ticker symbol of the stock you want to predict.")
    parser.add_argument("-d", "--days", type=int, help="Number of days in the future to predict the stock price for.", default=30)
    args = parser.parse_args()
    predictions, last_30_days = actions.predict_stock(actions, args.ticker, args.days)
    plt.figure()
    plt.plot((predictions), label='Predicted')
    plt.plot(())
    plt.title('Predicted Stock Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()
    print(predictions)
else:
    print("Something went wrong.")
