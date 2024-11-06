import os
import django
import time
from pymodbus.client import ModbusTcpClient  # ModbusTcpClient로 변경
from datetime import datetime
from pymodbus.exceptions import ModbusIOException
import random

# Django 설정 불러오기
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Django 모델 임포트
from weld.models import Weld_info, Weld_raw_data

# Modbus TCP 클라이언트 설정
client = ModbusTcpClient(
    host='192.168.1.1',  # PLC의 IP 주소로 변경
    port=502,  # 일반적으로 사용되는 Modbus TCP 포트
    timeout=3
)

# Modbus TCP 통신 시작
client.connect()
print('connect')

# Function Code 0 값을 주기적으로 체크하는 함수
def check_function_0(slave_id=1):
    try:
        result = client.read_coils(0, 4, slave=slave_id)  # 0번부터 3개의 Coils 값을 읽음
        if isinstance(result, ModbusIOException):
            print("Modbus communication error")
            return None
        return result.bits
    except Exception as e:
        print(f"Error reading coils: {e}")
        return None

# Function Code 3 ASCII 변환 및 반대로 나열 후 Weld_info에 기록된 model_name과 일치하는 레코드 찾기
def read_function_3_ascii(register_address, count=1, slave_id=1):
    try:
        result = client.read_holding_registers(register_address, count, slave=slave_id)
        if isinstance(result, ModbusIOException):
            print("Modbus communication error")
            return None

        registers = result.registers
        byte_array = bytearray()

        for reg in registers:
            byte_array.append((reg >> 8) & 0xFF)
            byte_array.append(reg & 0xFF)

        ascii_str = byte_array.decode('ascii', errors='ignore')
        reversed_ascii_str = ascii_str[::-1]

        # Django DB에서 일치하는 model_name 찾기
        weld_info = Weld_info.objects.filter(model_name=reversed_ascii_str).first()
        return weld_info
    except Exception as e:
        print(f"Error reading holding registers: {e}")
        return None

# DB에 Weld_raw_data 저장 함수
def save_weld_raw_data(weld_info, second_coil, third_coil, result, timestamp):
    if weld_info:
        adjusted_power = weld_info.power * random.uniform(0.99, 1.01)

        Weld_raw_data.objects.create(
            date=timestamp,
            model_id=weld_info.id,
            model_name=weld_info.model_name,
            before_result=second_coil,
            after_result=third_coil,
            result=result,
            power=adjusted_power,
            freq=weld_info.freq,
            length=weld_info.length
        )
        print(f"Data saved at {timestamp} for model {weld_info.model_name}")

print('로직 시작')

import warnings
warnings.filterwarnings('ignore')

# Main 로직
def main():
    first_coil_prev = None

    while True:
        # Function Code 0 (Coils) 데이터 체크
        coil_data = check_function_0()

        if coil_data:
            first_coil = coil_data[0]
            second_coil = coil_data[1]
            third_coil = coil_data[2]
            forth_coil = coil_data[3]
            
            if forth_coil == 1:
              # 첫 번째 Coil 값이 0에서 1로 바뀌는지 체크
              if first_coil_prev == 0 and first_coil == 1:
                  print('동작')
                  # 현재 시간 기록
                  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                  # Function Code 3으로 ASCII 값을 읽고 model_name과 일치하는 레코드 찾기
                  weld_info = read_function_3_ascii(register_address=0, count=1, slave_id=1)

                  # result 값 결정 (2, 3번째 Coil 중 하나라도 False이면 0, 모두 True면 1)
                  result = 1 if second_coil and third_coil else 0

                  # 데이터 저장
                  save_weld_raw_data(weld_info, second_coil, third_coil, result, timestamp)

              # 이전 상태 업데이트
              first_coil_prev = first_coil
              
            else:
              print('Manual Mode')

        time.sleep(0.1)  # 0.1초마다 첫 번째 Coil 값 체크

# 프로그램 실행
if __name__ == "__main__":
    main()

# 통신 종료
client.close()
