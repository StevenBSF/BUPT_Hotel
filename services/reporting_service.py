from repositories.usage_log_repository import UsageLogRepository
class ReportingService:
    def __init__(self, log_repo: UsageLogRepository):
        self.log_repo = log_repo

    def generate_daily_report(self, room_id: str, date):
        return DailyReport(room_id, date)

    def generate_weekly_report(self, room_id: str, week_start_date):
        return WeeklyReport(room_id, week_start_date)
