class Report:
    def __init__(self, room_id: str):
        self.room_id = room_id

class DailyReport(Report):
    def __init__(self, room_id: str, date):
        super().__init__(room_id)
        self.date = date

class WeeklyReport(Report):
    def __init__(self, room_id: str, week_start_date):
        super().__init__(room_id)
        self.week_start_date = week_start_date