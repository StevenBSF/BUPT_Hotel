class Customer:
    def __init__(self, customer_id: str, name: str):
        self.customer_id = customer_id
        self.name = name
        self.room = None
        self.active_service = None

    def assign_room(self, room):
        self.room = room

    def start_service(self, service):
        self.active_service = service

    def stop_service(self):
        self.active_service = None