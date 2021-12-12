from services.fill_dropshipping_data_service import FillDropshippingDataService
from services.fill_invoice_data_service import FillInvoiceDataService
from threading import Thread


class OrderProcessorService:
    def __init__(self):
        self.dropshipping_service = FillDropshippingDataService()
        self.invoice_service = FillInvoiceDataService()

    def load_order(self, order):
        print('loading order')
        if order['status'] == 'processing':
            thread = Thread(target=self.dropshipping_service.fill_dropshipping, args=(order,))
            thread.daemon = True
            thread.start()
        elif order['status'] == 'completed' and self.__should_create_invoice(order):
            thread = Thread(target=self.invoice_service.fill_invoice, args=(order,))
            thread.daemon = True
            thread.start()

    def __should_create_invoice(self, order):
        for meta_data in order['meta_data']:
            if meta_data['key'] == 'my_custom_val':
                return False
        return True
