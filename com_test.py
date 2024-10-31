from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusIOException
import time

# Modbus RTU 클라이언트 설정
client = ModbusSerialClient(
    port='COM7',     # 통신할 포트 설정 (예: COM5)
    baudrate=9600,   
    timeout=3,       
    parity='N',      
    stopbits=1,      
    bytesize=8       
)

# Modbus RTU 통신 시작
client.connect()

# Coils (Function Code 0) 값을 읽는 함수
def read_coils(register_address, count=1, slave_id=1):
    try:
        # read_coils: PLC에서 Coils(디지털 값) 읽기
        result = client.read_coils(register_address, count, slave=slave_id)
        if isinstance(result, ModbusIOException):
            print("Modbus communication error")
            return None
        
        # Coils 값 출력 (True: ON, False: OFF)
        return result.bits
    except Exception as e:
        print(f"Error reading coils: {e}")
        return None

# Holding Registers (Function Code 3) 값을 읽고 ASCII로 변환하는 함수
def read_holding_registers_ascii(register_address, count=1, slave_id=1):
    try:
        # read_holding_registers: PLC에서 보유 레지스터 읽기
        result = client.read_holding_registers(register_address, count, slave=slave_id)
        if isinstance(result, ModbusIOException):
            print("Modbus communication error")
            return None
        
        # 레지스터 값을 바이트로 변환
        registers = result.registers
        byte_array = bytearray()
        
        for reg in registers:
            # 레지스터를 2바이트로 분할하여 바이트 배열에 추가
            byte_array.append((reg >> 8) & 0xFF)  # 상위 바이트
            byte_array.append(reg & 0xFF)         # 하위 바이트

        # 바이트 배열을 ASCII 문자열로 변환
        ascii_str = byte_array.decode('ascii', errors='ignore')
      
      
        # ASCII 문자열을 반대로 나열
        reversed_ascii_str = ascii_str[::-1]
        
        return reversed_ascii_str
      
    except Exception as e:
        print(f"Error reading holding registers: {e}")
        return None
import datetime
# Main: Coils 및 Holding Registers 데이터 읽기
def main():
    # Coils 데이터 수집 (예: 주소 0번 Coil에서 10개 값을 읽음)
    coil_address = 0  # Coil 시작 주소
    coil_count = 4  # 읽을 Coils 수
    slave_id = 1      # PLC Slave ID
    
    # Holding Registers 데이터 수집 (예: 주소 100번 레지스터에서 2개 값을 읽음)
    register_address = 0  # 레지스터 주소
    register_count = 1     # 읽을 레지스터 수
    
    print('수집시간 : ', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # Holding Registers 값 읽고 ASCII로 변환
    register_data_ascii = read_holding_registers_ascii(register_address, register_count, slave_id)
    if register_data_ascii is not None:
      print(f"모델명: {register_data_ascii}")
    
    # Coils 값 읽기
    coil_data = read_coils(coil_address, coil_count, slave_id)
    if coil_data is not None:
      print(f"[동작상태, 조립비전, 용접비전]: {coil_data[:3]}")



# 프로그램 실행
if __name__ == "__main__":
    main()

# 통신 종료
client.close()
