from abc import ABC, abstractmethod


class BaseDevice(ABC):
    factory_name = "Rikkei Smart Factory"
    base_maintenance_cost = 1000000

    def __init__(self, device_code, device_name):
        self.device_code = device_code
        self.device_name = device_name
        self.__operating_hours = 0

    @property
    def operating_hours(self):
        return self.__operating_hours

    def add_operating_hours(self, hours):
        self.__operating_hours += hours

    @property
    def device_name(self):
        return self.__device_name

    @device_name.setter
    def device_name(self, value):
        self.__device_name = " ".join(value.strip().upper().split())

    @staticmethod
    def validate_device_code(device_code):
        return (
            len(device_code) == 10
            and device_code[0].isalpha()
            and device_code.isalnum()
        )

    @classmethod
    def update_maintenance_cost(cls, new_cost):
        cls.base_maintenance_cost = new_cost

    @abstractmethod
    def track_performance(self):
        pass

    @abstractmethod
    def run_diagnostic(self):
        pass

    def __add__(self, other):
        if not isinstance(other, BaseDevice):
            raise TypeError
        return self.operating_hours + other.operating_hours

    def __lt__(self, other):
        if not isinstance(other, BaseDevice):
            raise TypeError
        return self.operating_hours < other.operating_hours


class ThermalSensor(BaseDevice):
    def __init__(
        self,
        device_code,
        device_name,
        current_temperature=25.0,
        safety_threshold=80.0
    ):
        super().__init__(device_code, device_name)
        self.current_temperature = current_temperature
        self.safety_threshold = safety_threshold

    def track_performance(self):
        return abs(
            self.safety_threshold - self.current_temperature
        )

    def run_diagnostic(self):
        if self.current_temperature > self.safety_threshold:
            return (
                f"Nguy hiểm: Vượt ngưỡng nhiệt! "
                f"(Nhiệt độ hiện tại: {self.current_temperature} độ C / "
                f"Ngưỡng an toàn: {self.safety_threshold} độ C)"
            )
        return "Hệ thống nhiệt hoạt động bình thường."


class ProductionRobot(BaseDevice):
    def __init__(
        self,
        device_code,
        device_name,
        completed_products=0
    ):
        super().__init__(device_code, device_name)
        self.completed_products = completed_products

    def track_performance(self):
        if self.operating_hours == 0:
            return 0
        return round(
            self.completed_products
            / (self.operating_hours * 500)
            * 100,
            2
        )

    def run_diagnostic(self):
        if self.completed_products > 10000:
            return (
                "Cảnh báo bảo dưỡng: "
                "Sản lượng vượt 10,000 sản phẩm."
            )
        return "Robot hoạt động bình thường."


class HybridSmartActuator(
    ProductionRobot,
    ThermalSensor
):
    def __init__(
        self,
        device_code,
        device_name,
        completed_products=0,
        current_temperature=25.0,
        safety_threshold=80.0
    ):
        super().__init__(
            device_code,
            device_name,
            completed_products
        )
        self.current_temperature = current_temperature
        self.safety_threshold = safety_threshold

    def run_diagnostic(self):
        if self.current_temperature > self.safety_threshold:
            return (
                f"Nguy hiểm: Vượt ngưỡng nhiệt! "
                f"(Nhiệt độ hiện tại: {self.current_temperature} độ C / "
                f"Ngưỡng an toàn: {self.safety_threshold} độ C)"
            )

        if self.completed_products > 10000:
            return (
                "Cảnh báo bảo dưỡng: "
                "Sản lượng vượt 10,000 sản phẩm."
            )

        return "Hybrid hoạt động bình thường."


class MQTTEngineGateway:
    def process_stream(self, device):
        print(
            "[Hệ thống MQTT Engine]: Đang khởi tạo "
            "băng thông kết nối dữ liệu IoT..."
        )
        print(
            "Xác thực cổng ngoại vi bằng Duck Typing thành công!"
        )
        print(
            f"Dữ liệu của thiết bị "
            f"{device.device_code} đã được đóng gói "
            f"và xuất chuỗi luồng thành công."
        )


class ERPReportGateway:
    def process_stream(self, device):
        print(
            "[ERP Gateway]: Đang đồng bộ dữ liệu..."
        )
        print(
            "Xác thực cổng ngoại vi bằng Duck Typing thành công!"
        )
        print(
            f"Dữ liệu của thiết bị "
            f"{device.device_code} đã được đồng bộ ERP."
        )


def export_telemetry_data(
    data_gateway,
    device_object
):
    try:
        data_gateway.process_stream(device_object)
    except AttributeError:
        print(
            "[Lỗi] (ERR-IOT-05): Xung đột kiến trúc! "
            "Không thể xuất dữ liệu do cấu hình "
            "cổng ngoại vi không tương thích."
        )


def check_current_device(current_device):
    if current_device is None:
        print(
            "[Lỗi] (ERR-IOT-02): Thao tác bị từ chối! "
            "Hệ thống chưa có thông tin thiết bị hoạt động."
        )
        return False
    return True


def input_positive_number(message):
    try:
        value = float(input(message))
        if value <= 0:
            raise ValueError
        return value
    except ValueError:
        print(
            "[Lỗi] (ERR-IOT-03): Định dạng dữ liệu sai! "
            "Giá trị nhập vào phải là số lớn hơn 0."
        )
        return None


devices_list = []
current_device = None

while True:
    print("\n===== RIKKEI SMART FACTORY IOT PRO =====")
    print("1. Đăng ký thiết bị")
    print("2. Xem thông tin thiết bị")
    print("3. Check-in giờ vận hành")
    print("4. Tự chẩn đoán")
    print("5. So sánh & cộng giờ chạy")
    print("6. Xuất dữ liệu")
    print("7. Thoát")

    choice = input("Chọn chức năng (1-7): ")

    if choice == "1":
        print("\n--- ĐĂNG KÝ THIẾT BỊ IOT MỚI ---")
        print("1. Production Robot")
        print("2. Thermal Sensor")
        print("3. Hybrid Smart Actuator")

        device_type = input(
            "Chọn phân loại thiết bị (1-3): "
        )

        code = input(
            "Nhập mã thiết bị 10 ký tự: "
        )

        if not BaseDevice.validate_device_code(code):
            print(
                "[Lỗi] (ERR-IOT-01): "
                "Mã thiết bị không hợp lệ! "
                "Phải gồm đúng 10 ký tự "
                "và bắt đầu bằng tiền tố quy định."
            )
            continue

        name = input(
            "Nhập tên thiết bị: "
        )

        if device_type == "1":
            current_device = ProductionRobot(
                code,
                name
            )

        elif device_type == "2":
            current_device = ThermalSensor(
                code,
                name
            )

        elif device_type == "3":
            current_device = HybridSmartActuator(
                code,
                name
            )

        else:
            print(
                "[Lỗi] (ERR-IOT-06): "
                "Lựa chọn không hợp lệ!"
            )
            continue

        devices_list.append(current_device)

        print(
            "[Thành công]: Đăng ký thiết bị thành công!"
        )
        print(
            f"Tên thiết bị: "
            f"{current_device.device_name}"
        )

    elif choice == "2":
        if not check_current_device(
            current_device
        ):
            continue

        print(
            "\n--- THÔNG TIN THIẾT BỊ HIỆN TẠI ---"
        )
        print(
            f"Loại thiết bị: "
            f"{type(current_device).__name__}"
        )
        print(
            f"Nhà máy: "
            f"{current_device.factory_name}"
        )
        print(
            f"Mã thiết bị: "
            f"{current_device.device_code}"
        )
        print(
            f"Tên thiết bị: "
            f"{current_device.device_name}"
        )
        print(
            f"Số giờ vận hành: "
            f"{current_device.operating_hours} giờ"
        )

        if hasattr(
            current_device,
            "completed_products"
        ):
            print(
                f"Sản phẩm hoàn thành: "
                f"{current_device.completed_products}"
            )

        if hasattr(
            current_device,
            "current_temperature"
        ):
            print(
                f"Nhiệt độ hiện tại: "
                f"{current_device.current_temperature}"
            )

        print(
            "[Hệ thống MRO]:",
            " -> ".join(
                cls.__name__
                for cls in type(current_device).__mro__
            )
        )

    elif choice == "3":
        if not check_current_device(
            current_device
        ):
            continue

        print(
            "\n--- GHI NHẬN SỐ LIỆU VẬN HÀNH ---"
        )

        hours = input_positive_number(
            "Nhập số giờ chạy mới phát sinh: "
        )

        if hours is None:
            continue

        current_device.add_operating_hours(
            hours
        )

        if hasattr(
            current_device,
            "completed_products"
        ):
            products = input_positive_number(
                "Nhập số lượng sản phẩm hoàn thành mới bổ sung: "
            )

            if products is None:
                continue

            current_device.completed_products += int(
                products
            )

        print(
            "[Thành công]: Đã cập nhật số liệu vận hành."
        )
        print(
            f"Tổng số giờ chạy tích lũy: "
            f"{current_device.operating_hours} giờ"
        )

        result = (
            current_device.track_performance()
        )

        if isinstance(
            current_device,
            ProductionRobot
        ):
            print(
                f"Chỉ số hiệu suất thiết bị "
                f"tổng thể (OEE): {result}%"
            )
        else:
            print(
                f"Biên độ nhiệt: {result}"
            )

    elif choice == "4":
        if not check_current_device(
            current_device
        ):
            continue

        print(
            "\n--- QUY TRÌNH TỰ CHẨN ĐOÁN "
            "LỖI KỸ THUẬT ---"
        )

        result = (
            current_device.run_diagnostic()
        )

        if (
            "Nguy hiểm" in result
            or "Cảnh báo" in result
        ):
            print(
                "[Cảnh báo hệ thống]: "
                "Thiết bị phát hiện trạng thái "
                "bất thường!"
            )

        print(
            f"Kết quả chẩn đoán: {result}"
        )

        print(
            f"Định mức chi phí bảo trì "
            f"hệ thống dự kiến: "
            f"{BaseDevice.base_maintenance_cost:,} VND"
        )

    elif choice == "5":
        if not check_current_device(
            current_device
        ):
            continue

        print(
            "\n--- KIỂM KÊ & SO SÁNH TẢI ---"
        )

        for device in devices_list:
            if device != current_device:
                print(
                    f"{device.device_code} - "
                    f"{device.device_name}"
                )

        code = input(
            "Chọn mã thiết bị đối ứng: "
        )

        target = None

        for device in devices_list:
            if device.device_code == code:
                target = device
                break

        if target is None:
            continue

        try:
            print(
                "[Kết quả So sánh (__lt__)]:",
                current_device < target
            )

            print(
                "[Kết quả Tổng hợp (__add__)]:",
                current_device + target,
                "giờ"
            )

        except TypeError:
            print(
                "[Lỗi] (ERR-IOT-04): "
                "Lỗi kiểu dữ liệu! "
                "Không thể thực hiện toán tử "
                "với đối tượng ngoài hệ thống."
            )

    elif choice == "6":
        if not check_current_device(
            current_device
        ):
            continue

        print(
            "\n--- XUẤT DỮ LIỆU VẬN HÀNH "
            "RA CỔNG NGOẠI VI ---"
        )

        print("1. MQTT")
        print("2. ERP")

        gateway_choice = input(
            "Chọn cổng kết nối ngoại vi (1-2): "
        )

        if gateway_choice == "1":
            gateway = MQTTEngineGateway()

        elif gateway_choice == "2":
            gateway = ERPReportGateway()

        else:
            print(
                "[Lỗi] (ERR-IOT-06): "
                "Lựa chọn không hợp lệ!"
            )
            continue

        export_telemetry_data(
            gateway,
            current_device
        )

    elif choice == "7":
        print(
            "\nCảm ơn bạn đã sử dụng hệ thống "
            "Quản lý Thiết bị Rikkei Smart Factory IoT Pro!"
        )
        break

    else:
        print(
            "[Lỗi] (ERR-IOT-06): "
            "Lựa chọn không hợp lệ! "
            "Vui lòng nhập đúng số thứ tự "
            "chức năng từ 1 đến 7."
        )