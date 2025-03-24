from datetime import datetime

from os import walk
from flask import Blueprint, jsonify, request
from app.database.model import CurrencyRate
from app.consts import CURRENCY_USD, CURRENCY_RMB, CURRENCY_JPY, CURRENCY_NTD
from db import db

routes_bp = Blueprint("routes", __name__)


@routes_bp.route("/api/hello", methods=["GET"])
def hello_world():
    return jsonify({"message": "Hello, World!"})


@routes_bp.route("/api/rate_list", methods=["GET"])
def get_currency_rate_list():
    currency_code = request.args.get("currency_code")
    if currency_code is None:
        error_msg = "currency_code is required"
        return jsonify({"error": error_msg})

    rate_list = db.session.execute(
        db.select(CurrencyRate).filter(
            CurrencyRate.currency_code == currency_code,
            CurrencyRate.updated_at <= datetime(2024, 11, 2, 23, 59, 59),
            # CurrencyRate.updated_at >= datetime(2024, 11, 2, 0, 0, 0),
        )
    ).scalars()
    rates_data = [
        {
            "id": rate.id,
            "currency_code": rate.currency_code,
            "buying_rate": rate.buying_rate,
            "selling_rate": rate.selling_rate,
            "created_at": rate.formatted_created_at,
            "updated_at": rate.formatted_updated_at,
        }
        for rate in rate_list
    ]
    return jsonify({"rate_list": rates_data})


@routes_bp.route("/api/rate/convert", methods=["POST"])
def convert_exchange_rate():
    supported_currency_list = [CURRENCY_NTD, CURRENCY_JPY, CURRENCY_RMB, CURRENCY_USD]
    ori_currency_code = request.values["ori_currency_code"]

    if ori_currency_code is None:
        error_msg = "ori_currency_code is required"
        return jsonify({"error": error_msg})

    if ori_currency_code not in supported_currency_list:
        error_msg = "ori_currency_code is not supported"
        return jsonify({"error": error_msg})

    target_currency_code = request.values["target_currency_code"]
    if target_currency_code is None:
        error_msg = "target_currency_code is required"
        return jsonify({"error": error_msg})

    ori_currency_price = float(request.values["ori_currency_price"])
    if not ori_currency_price:
        error_msg = "ori_currency_price is required"
        return jsonify({"error": error_msg})

    result = None
    if ori_currency_code == "ntd" or target_currency_code == "ntd":
        currency = (
            target_currency_code if ori_currency_code == "ntd" else ori_currency_code
        )
        rate = (
            CurrencyRate.query.filter_by(currency_code=currency)
            .order_by(CurrencyRate.updated_at.desc())
            .first()
        )

        if rate is None:
            print("not found rate")
            return jsonify({"error": "not found rate"})

        if ori_currency_code == "ntd":
            result = ori_currency_price / rate.selling_rate
        elif target_currency_code == "ntd":
            print("buying rate")
            print(rate.buying_rate)
            print(f"ori_currency_price: {ori_currency_price}")
            result = ori_currency_price * rate.buying_rate
    else:
        rate = (
            CurrencyRate.query.filter_by(currency_code=ori_currency_code)
            .order_by(CurrencyRate.update_at.desc())
            .first()
        )
        ori_to_ntd = ori_currency_price * rate.buying_rate
        rate = (
            CurrencyRate.query.filter_by(currency_code=target_currency_code)
            .order_by(CurrencyRate.update_at.desc())
            .first()
        )
        result = ori_to_ntd / rate.selling_rate
    return jsonify({"result": result})
