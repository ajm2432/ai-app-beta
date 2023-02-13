from flask import Blueprint

blueprint = Blueprint(
    'stock_predict_blueprint',
    __name__,
    url_prefix=''
)