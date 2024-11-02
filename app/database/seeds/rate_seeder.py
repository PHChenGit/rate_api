from argparse import ArgumentParser
from datetime import datetime, timedelta
import random

from app.consts import CURRENCY_USD, CURRENCY_JPY, CURRENCY_RMB, CURRENCY_NTD
from app.database.model import CurrencyRate
from app.database.utils import table_exists
from wsgi import app, db

# def create_all_tables():
#     with app.app_context():
#         db.create_all()

def run_seeds():
    today = datetime.today()

    def new_model(day_off):
        result = []
        buying_rate = random.uniform(28.0, 31.0)
        selling_rate = random.uniform(buying_rate+0.01, 32.0)
        usd_model = CurrencyRate(
            currency_code=CURRENCY_USD,
            buying_rate=buying_rate,
            selling_rate=selling_rate,
            precision=2,
            created_at=today-day_off,
            updated_at=today-day_off,
        )
        result.append(usd_model)

        buying_rate = random.uniform(0.1998, 0.21)
        selling_rate = random.uniform(0.2126, 0.25)
        jpy_model = CurrencyRate(
            currency_code=CURRENCY_JPY,
            buying_rate=buying_rate,
            selling_rate=selling_rate,
            precision=2,
            created_at=today-day_off,
            updated_at=today-day_off,
        )
        result.append(jpy_model)

        buying_rate = random.uniform(3.8, 4.2)
        selling_rate = random.uniform(4.3, 5.0)
        rmb_model = CurrencyRate(
            currency_code=CURRENCY_RMB,
            buying_rate=buying_rate,
            selling_rate=selling_rate,
            precision=2,
            created_at=today-day_off,
            updated_at=today-day_off,
        )
        result.append(rmb_model)
        return result

    model_list = []
    ntd_model = CurrencyRate(
        currency_code=CURRENCY_NTD,
        buying_rate=1,
        selling_rate=1,
        precision=0,
        created_at=today,
        updated_at=today,
    )
    model_list.append(ntd_model)

    for i in range(10):
        model_list.extend(new_model(timedelta(days=i)))

    with app.app_context():
        for i, model in enumerate(model_list):
            db.session.add(model)

            if i % 5 == 0:
                db.session.commit()

if __name__ == "__main__":
    run_seeds()
    # parser = ArgumentParser()
    # parser.add_argument('--all', action='store_true', help="Create all tables")
    # parser.add_argument('--seed', action='store_true', help="Insert data to tables")
    # args = parser.parse_args()

    # if args.all:
    #     print("Creating all tables")
    #     create_all_tables()

    # if args.seed:
    #     print("Inserting data")
    #     run_seeds()
