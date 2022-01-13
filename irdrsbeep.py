#!python3

import argparse
import configparser
import irsdk
import time
import functools

try:
    import winsound
except ImportError:
    import os
    def beep(frequency,duration):
        os.system('beep -f %s -l %s' % (frequency,duration))
else:
    def beep(frequency,duration):
        winsound.Beep(frequency,duration)

VERSION = '0.1.0'

# no auto-flushing in windows
print = functools.partial(print, flush=True)

class State:
    connected = False
    drs = -1

def check_iracing():
    if state.connected and not (ir.is_initialized and ir.is_connected):
        state.connected = False
        state.drs = -1
        ir.shutdown()
        print('irsdk disconnected')
    elif not state.connected:
        if not ir.startup():
            pass
        elif ir.is_connected:
            state.connected = True
            print('irsdk connected')
        else:
            print('not connected')


def beep_upcoming():
    frequency = config.getint('drs', 'upcoming_frequency', fallback=500)
    duration = config.getint('drs', 'upcoming_duration', fallback=100)
    if frequency == 0:
        return
    beep(frequency, duration)

def beep_available():
    frequency = config.getint('drs', 'available_frequency', fallback=1500)
    duration = config.getint('drs', 'available_duration', fallback=200)
    if frequency == 0:
        return
    beep(frequency, duration)

def loop():
    # freeze for consisten per-frame data
    ir.freeze_var_buffer_latest()

    drs = ir['DRS_Status']
    if drs is None:
        return

    # DrsStatus: 0 = inactive, 1 = can be activated in next DRS zone, 2 = can be activated now, 3 = active.
    if state.drs == 0 and drs == 1:
        beep_upcoming()
    if state.drs == 1 and (drs == 2 or drs == 3):
        beep_available()

    if drs != state.drs:
        state.drs = drs
        if args.verbose:
            print('drs update = ', drs)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='drs beep for iRacing %s' % VERSION)
    parser.add_argument('-v', '--version', action='version', version=VERSION, help='show version and exit')
    parser.add_argument('--beep', action='store_true', help='play "upcoming" and "available" drs beep sounds, then exit')
    parser.add_argument('--verbose', action='store_true', help='verbose output for debugging')
    parser.add_argument('--tick', type=float, default=0.05, help=argparse.SUPPRESS)

    args = parser.parse_args()
    config = configparser.ConfigParser()
    config.read('irdrsbeep.ini')

    if args.beep:
        print('"drs upcoming" beep')
        beep_upcoming()
        time.sleep(1)
        print('"drs available" beep')
        beep_available()
        quit()

    ir = irsdk.IRSDK()
    state = State()
    print("waiting for iracing...")
    try:
        while True:
            check_iracing()
            if state.connected:
                loop()
                time.sleep(0.05)
            else:
                time.sleep(1)
    except KeyboardInterrupt:
        # press ctrl+c to exit
        pass
