from flask import Flask
from housing.logger import logging
from housing.exception import Housing_Exception
import sys

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    # to check exception is working properly, raising a exception
    try:
        raise Exception("False Exception : Testing Custom Exception...")
    except Exception as e:
        housing = Housing_Exception(e,sys)
        logging.info("False Exception : Testing Custom Exception...")

    logging.info("Testing Logging Module...")
    return 'CI/CD Pipeline has been Estalished!!!'

if __name__ == '__main__':
    app.run(debug=True)