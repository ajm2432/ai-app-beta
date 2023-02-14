import argparse
from model import actions

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train a stock prediction model')
    parser.add_argument('-s','--symbol', type=str, required=True, help='The stock symbol to train the model on')
    parser.add_argument('-w','--window', type=int, default=30, help='The number of days to use as the training window')
    args = parser.parse_args()
    actions.train_model(actions, ticker=args.symbol, window=args.window)