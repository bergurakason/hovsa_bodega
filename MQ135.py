from numpy import True_
import smbus
import time

bus = smbus.SMBus(1)
i2c_address = 0x49

med_luft = 600
Dårlig_luft = 900
max_val = 1023


def get_data():
    # Reads word (2 bytes) as int - 0 is comm byte
    rd = bus.read_word_data(i2c_address, 0)
    # Exchanges high and low bytes
    data = ((rd & 0xFF) << 8) | ((rd & 0xFF00) >> 8)
    # Ignores two least significiant bits
    adc_val = data >> 2
    air_quality = 100- ((adc_val/max_val) * 100.0)
    air_quality = format(air_quality, '.2f')
    print("luftkvalitet procent: ", air_quality)
    print(adc_val)
    return adc_val

def air_quality():
    current_qual = get_data()
    if current_qual < med_luft:
        print("Luften er god")
    elif Dårlig_luft > current_qual >= med_luft:
        print("Luften er ikke super")
    elif current_qual >= Dårlig_luft:
        print("Luften er meget dårlig")


while True:
    air_quality()
    time.sleep(5.0)