from pyfirmata import Arduino, util
import pyfirmata
from system.portscan import serial_ports

port = (serial_ports()[0])
board = Arduino(port)

#initialize value reading
it = util.Iterator(board)
it.start()

val_old = 999
trigger = 0


def serial_init(serial_port):
    board.analog[serial_port].enable_reporting()
    return board.analog[serial_port].read()


def read_digital(digital_port):
    board.digital[digital_port].mode = pyfirmata.INPUT
    return board.digital[digital_port].read()


def read_poti(serial_port, tolerance):
    global val_old
    board.analog[serial_port].enable_reporting()
    poti_changed = False
    val = int((board.analog[serial_port].read()) * 100)
    serial_adjust = abs(val - val_old)
    if (serial_adjust >= tolerance):
        poti_changed = True
    if (poti_changed):
        return val
        val_old = val


def read_shoe(serial_port, tolerance):
    board.analog[serial_port].enable_reporting()
    val = (board.analog[serial_port].read()) * 100
    if (val > tolerance):
        val = 1
        return val
    else:
        val = 0
        return val