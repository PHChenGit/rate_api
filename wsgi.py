from argparse import ArgumentParser
from pathlib import Path

from flask import Flask
from app.route import routes_bp 
from db import db, init_app as init_db
from dotenv import load_dotenv
# from app.database.seeds import run_seeds

dotenv_file = Path('.') / '.env'
load_dotenv(dotenv_path=dotenv_file) 

app = Flask(__name__)
app.register_blueprint(routes_bp)
init_db(app)

 

if __name__ == "__main__":
    # parser = ArgumentParser()
    # parser.add_argument('--seed', action=True, "Run seeders")
    # args = parser.parse_args() 
    #
    # if args.seed:
    #     run_seeds(app, db)


    app.run(debug=True, port=5000)

