from services import fill__dropshipping_data_service
from threading import Thread


class OrderProcessorService:
    def __init__(self):
        self.service = fill__dropshipping_data_service.FillDropshippingDataService()

    def load_order(self, order):
        print('loading order')
        if order['status'] == 'processing':
            thread = Thread(target=self.service.fill_dropshipping, args=(order,))
            thread.daemon = True
            thread.start()
        elif order.status == 'completed':
            pass  # TODO
