import serial
import time


def readserial(comport, baudrate, timestamp=False):


    ser = serial.Serial(comport, baudrate, timeout=0.1)         # 1/timeout is the frequency at which the port is read

    while True:

        data = ser.readline().decode().strip()

        if data and timestamp:
            timestamp = time.strftime('%H:%M:%S')
            print(f'{timestamp} > {data}')
            with open("data.json", "a") as f:
                f.write(data)


if __name__ == '__main__':
    readserial('/dev/tty.usbmodem101', 9600, True)  