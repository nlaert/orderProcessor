import time

from flask import Flask, request, jsonify
from services import order_processor_service

app = Flask(__name__)


@app.route('/order-processor', methods=['POST'])
def order_processor():
    order = request.get_json()
    order_processor_service.OrderProcessorService().load_order(order)
    time.sleep(5)
    return ''


if __name__ == '__main__':
    app.run()
