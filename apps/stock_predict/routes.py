
from apps.home import blueprint
from flask import render_template, request, Response, jsonify,session
from flask_login import login_required
from stock_ml_algorithims import model
from apps.stock_predict import blueprint

@blueprint.route('/predict-stock', methods=['GET','POST'])
@login_required
def predict_stock():
        predictions = model.actions.predict_stock(model.actions, "AAPL", 5)
        predictions = predictions.tolist()
        print(jsonify(response=predictions))
        return jsonify(response=predictions)

@blueprint.route('/stock-predictor', methods=['GET','POST'])
@login_required
def stock_predictor():
        return  render_template('stock_predictor/stocks_predictor.html')     