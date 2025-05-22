class ServiceDetails:
    def __init__(self, service):
        self.service = service
        self.logs = service.usage_logs

    def __str__(self):
        details = [f"{log}" for log in self.logs]
        return "\n".join(details)