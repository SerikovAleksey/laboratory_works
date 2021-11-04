import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
value_list = []

def dec2bin(dec):
    return [int(bit) for bit in bin(dec)[2:].zfill(8)]

def dec2dac(dec):
    GPIO.output(dac, dec2bin(dec))
    return dec2bin(dec)

def adc():
    ans = 0
    for i in range(8):
        ans = ans + 2 ** (7 - i)
        dec2dac(ans)
        time.sleep(0.0005)
        if GPIO.input(4) == 0:
            ans = ans - 2 ** (7 - i)
    return ans

def calibration(mm):
    print("Калибровка " + str(mm))
    begin = time.time()
    value_calibration = []
    while time.time() - begin < 10:
        value_calibration.append(adc())
    duration_calibration = time.time() - begin
    value_calibration_str = [str(item) for item in value_calibration]
    with open(str(mm) + " mmHg.txt", "w") as mmHg:
        mmHg.write('- Blood Lab\n\n')
        mmHg.write('- Experiment date = {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        mmHg.write('- Experiment duration = {:.2f} s\n'.format(duration_calibration))
        mmHg.write('- Sampling period = {:.2f} us\n'.format(duration_calibration/len(value_calibration) * 1000000))
        mmHg.write('- Sampling frequency = {} Hz\n'.format(int(len(value_calibration) / duration_calibration)))
        mmHg.write('- Samples count = {}\n'.format(len(value_calibration)))
        mmHg.write("\n".join(value_calibration_str))
    print("Калибровка завершена\n")

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(4, GPIO.IN)

try:
    print("Проводится калибровка! \n")
    input("Выставьте давление 160\n")
    calibration(160)
    input("Выставьте давление 120\n")
    calibration(120)
    input("Выставьте давление 80\n")
    calibration(80)
    input("Выставьте давление 40\n")
    calibration(40)

    input("\nГотово для начала эксперимента")
    begin = time.time()
    print("Начало измерений")
    while True: #adc() > 1
        value_list.append(adc())
        print(value_list[-1])

finally:
    print("Конец измерений")

    duration = time.time() - begin
    print("Duration = {:.2f} sec".format(duration))
    print("Counts = {}".format(len(value_list)))

    value_list_str = [str(item) for item in value_list]

    with open("data.txt", "w") as data:
        data.write('- Blood Lab\n\n')
        data.write('- Experiment date = {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        data.write('- Experiment duration = {:.2f} s\n'.format(duration))
        data.write('- Sampling period = {:.2f} us\n'.format(duration / len(value_list) / 1000000))
        data.write('- Sampling frequency = {} Hz\n'.format(int(len(value_list) / duration)))
        data.write('- Samples count = {}\n'.format(len(value_list)))
        data.write("\n".join(value_list_str))

    plt.plot(value_list)
    plt.show()

    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup()