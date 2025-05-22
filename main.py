# main.py

from datetime import datetime, timedelta
from repositories.room_repository import RoomRepository
from repositories.usage_log_repository import UsageLogRepository
from models.room import Room
from models.air_conditioner import AirConditioner
from models.control_panel import ControlPanel
from controllers.customer_controller import CustomerController
from controllers.staff_controller import StaffController
from services.billing_service import BillingService
from services.service_details_service import ServiceDetailsService

def setup_demo_environment():
    """
    初始化演示环境：
    - 创建一个房间并注册到 RoomRepository
    - 准备一个空的 UsageLogRepository
    """
    # 创建仓库
    room_repo = RoomRepository()
    log_repo  = UsageLogRepository()

    # # 创建设备与房间，并加入仓库
    # ac = AirConditioner(ac_id="101")         # 默认初始状态
    # panel = ControlPanel(panel_id="101", ac=ac)

    room = Room(room_id="101")
    room_repo.add(room)

    return room_repo, log_repo

def demo_customer_flow(customer_ctrl: CustomerController):
    print("=== 客户使用空调用例 ===")
    # 1. 启动空调
    mode, target_temp, fee_rate, current_fee = \
        customer_ctrl.start_air_conditioning(
            customer_id="C001", room_id="101", current_temp=30.0
        )
    print(f"start →  mode={mode}, target_temp={target_temp}, fee_rate={fee_rate}, current_fee={current_fee}")

    # 2. 可选：改温度、改风速
    ok = customer_ctrl.change_temperature("101", 22.0)
    print(f"change_temp → success={ok}")
    new_rate = customer_ctrl.change_fan_speed("101", "high")
    print(f"change_fan_speed → new_rate={new_rate}")

    # 3. 循环查询：温度、风速、费用
    cur_temp, rate, fee = customer_ctrl.query_current_temperature("101")
    print(f"query_temp → cur_temp={cur_temp}, rate={rate}, fee={fee}")
    cur_fan, rate, fee = customer_ctrl.query_current_fan_speed("101")
    print(f"query_fan  → cur_fan={cur_fan},    rate={rate}, fee={fee}")
    rate, fee = customer_ctrl.query_current_fee("101")
    print(f"query_fee  → rate={rate}, fee={fee}")

    # 4. 停止服务
    total_fee, duration = customer_ctrl.stop_air_conditioning("101")
    print(f"stop  → total_fee={total_fee:.2f}, duration={duration:.1f}min")

def demo_staff_flow(room_repo, log_repo):
    print("\n=== 前台出具账单与详单 ===")
    # 初始化服务
    billing_svc = BillingService(log_repo)
    details_svc = ServiceDetailsService(log_repo)
    staff_ctrl = StaffController(billing_svc, details_svc)

    # 假设客户从 2025-05-01 14:00 到 2025-05-01 16:30 使用了服务
    check_in  = datetime.now() - timedelta(hours=5)
    check_out = datetime.now()

    # 1. 生成并打印账单
    invoice = staff_ctrl.generate_invoice("101",
                                          check_in.strftime("%Y-%m-%d %H:%M"),
                                          check_out.strftime("%Y-%m-%d %H:%M"))
    print(f"GenerateInvoice → invoice:\n{invoice}\n")
    ok1 = staff_ctrl.print_invoice("101", invoice)
    print(f"PrintInvoice → status={ok1}")

    # 2. 生成并打印详单
    details = staff_ctrl.generate_service_details("101",
                                                  check_in.strftime("%Y-%m-%d %H:%M"),
                                                  check_out.strftime("%Y-%m-%d %H:%M"))
    print("GenerateServiceDetails →")
    for d in details:
        print(d)
        print("---")
    ok2 = staff_ctrl.print_service_details("101", details)
    print(f"PrintServiceDetails → status={ok2}")

if __name__ == "__main__":
    # 1. 环境准备
    room_repo, log_repo = setup_demo_environment()

    # 2. 创建客户与前台控制器
    customer_ctrl = CustomerController(room_repo, log_repo)

    # 3. 演示客户流程
    demo_customer_flow(customer_ctrl)

    # 4. 演示前台营业员流程
    demo_staff_flow(room_repo, log_repo)
