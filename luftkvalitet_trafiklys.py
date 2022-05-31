from numpy import True_
import smbus
import time
import led

bus = smbus.SMBus(1)
i2c_address = 0x49

# % værdi for hvornår luft kvaliteten begynder ikke at være god
god_luft = 50
# % værdi for hvornår luft kvaliteten er dårlig
Dårlig_luft = 25
# max værdi for adc værdi
max_val = 1023


def get_data():
    # Reads word (2 bytes) as int - 0 is comm byte
    rd = bus.read_word_data(i2c_address, 0)
    # Exchanges high and low bytes
    data = ((rd & 0xFF) << 8) | ((rd & 0xFF00) >> 8)
    # Ignores two least significiant bits
    adc_val = data >> 2
    # Regner adc om til en % værdi
    air_quality = 100- ((adc_val/max_val) * 100.0)
    # Formaterer luft kvaliteten til print format
    percentage = format(air_quality, '.2f')
    print("luftkvalitet procent: ", percentage) # Luft kvalitet printes
    print(adc_val) # Rå adc værdi
    # % luft kvalitet returneres
    return air_quality

def air_quality():
    current_qual = get_data()
    # Kører hvis luft kvaliteten er over grænsen for god luft 
    if current_qual > god_luft:
        print("Luften er god")
        # Tænder den grønne led og slukker hhv rød og gul
        led.green_on()
    # Kører hvis luft kvaliteten er over grænsen for Dårlig luft, men under grænsen for god luft
    elif Dårlig_luft < current_qual >= god_luft:
        print("Luften er ikke super")
        # Tænder den gule led og slukker hhv grøn og rød
        led.yellow_on()
    # Kører hvis luft kvaliteten er under grænsen for Dårligluft
    elif current_qual <= Dårlig_luft:
        print("Luften er meget dårlig")
        # Tænder den røde led og slukker hhv grøn og gul
        led.red_on()


while True:
    air_quality()
    time.sleep(5.0)