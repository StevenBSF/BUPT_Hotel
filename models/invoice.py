class Invoice:
    def __init__(self, service):
        self.service = service
        self.amount = service.calculate_fee()
        # add timestamp, customer, etc.

    def __str__(self):
        return f"Invoice for service {self.service.service_id}: {self.amount} 元"
