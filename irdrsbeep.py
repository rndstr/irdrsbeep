#!python3

import configparser
import irsdk
import time
import winsound

class State:
    connected = False
    drs = 0

def check_iracing():
    if state.connected and not (ir.is_initialized and ir.is_connected):
        state.connected = False
        state.drs = -1
        ir.shutdown()
        print('irsdk disconnected')
    elif not state.connected:
        if not ir.startup():
            print('irsdk start failed')
        elif ir.is_connected:
            state.connected = True
            print('irsdk connected')
        else:
            print('not connected')

def loop():
    # freeze for consisten per-frame data
    ir.freeze_var_buffer_latest()

    t = ir['SessionTime']
    print('session time:', t)

    drs = ir.get_session_info_update_by_key('DrsStatus')
    if drs is None:
        return

    # DrsStatus: 0 = inactive, 1 = can be activated in next DRS zone, 2 = can be activated now, 3 = active.

    if state.drs == 0 and drs == 1:
        winsound.Beep(config.getint('drs', 'upcoming_frequency', fallback=1500), config.getint('drs', 'upcoming_duration', fallback=300)
    if state.drs == 1 and drs == 2:
        winsound.Beep(config.getint('drs', 'available_frequency', fallback=5000), config.getint('drs', 'available_duration', fallback=1000)

    if drs != state.drs:
        state.drs = drs
        print('tick change: ', drs)

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('irdrsbeep.ini')
    ir = irsdk.IRSDK()
    state = State()
    try:
        while True:
            check_iracing()
            if state.ir_connected:
                loop()
            time.sleep(1)
    except KeyboardInterrupt:
        # press ctrl+c to exit
        pass
