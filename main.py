from abc import ABC, abstractmethod


class BaseVehicle(ABC):
    def __init__(self):
        self.__odometer = 0

    @property
    def odometer(self):
        return self.__odometer

    @abstractmethod
    def calculate_efficiency(self):
        pass

    def drive(self, distance):
        if distance > 0:
            self.__odometer += distance
        else:
            raise ValueError("Khoảng cách đi phải lớn hơn 0!")

    def __lt__(self, other):
        return self.odometer < other.odometer

    @staticmethod
    def validate_license_plate(plate):
        return len(plate) == 9 and plate.startswith("29")


class AutonomousFeature:
    def calculate_efficiency(self):
        return 95.0


class ElectricBus(BaseVehicle):
    def calculate_efficiency(self):
        efficiency = 100 - (self.odometer * 0.005)

        if efficiency < 50:
            return 50.0

        return efficiency


class RoboBus(ElectricBus, AutonomousFeature):
    def __init__(self, license_plate):
        super().__init__()
        self.license_plate = license_plate

    def calculate_efficiency(self):
        electric_eff = ElectricBus.calculate_efficiency(self)
        auto_eff = AutonomousFeature.calculate_efficiency(self)

        return (electric_eff + auto_eff) / 2


def display_mro(vehicle):
    print("\nMRO của RoboBus:")
    for cls in vehicle.__class__.__mro__:
        print(cls.__name__)


def create_vehicle():
    while True:
        plate = input("Nhập biển số xe: ").strip()

        if BaseVehicle.validate_license_plate(plate):
            vehicle = RoboBus(plate)

            print("\nĐăng ký xe thành công!")
            display_mro(vehicle)

            return vehicle

        print("Biển số không hợp lệ! Vui lòng nhập lại.")


def simulate_drive(vehicle):
    if vehicle is None:
        print("Chưa có xe nào được khởi tạo!")
        return

    try:
        distance = float(input("Nhập số km vừa di chuyển: "))

        vehicle.drive(distance)

        print(f"\nTổng quãng đường: {vehicle.odometer:.2f} km")

        efficiency = vehicle.calculate_efficiency()

        print(f"Hiệu suất hiện tại: {efficiency:.2f}%")

    except ValueError as e:
        print(f"Lỗi: {e}")


def main():
    current_vehicle = None

    while True:
        title = " SMART TRANSIT MENU ".center(50, "=")

        choice = input(f"""
{title}
1. Khởi tạo và đăng ký RoboBus
2. Giả lập vận hành và kiểm tra hiệu suất
3. Thoát

Chọn chức năng (1-3): """)

        match choice:
            case "1":
                current_vehicle = create_vehicle()

            case "2":
                simulate_drive(current_vehicle)

            case "3":
                print("Thoát chương trình!")
                break

            case _:
                print("Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    main()