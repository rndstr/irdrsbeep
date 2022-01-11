#!python3

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
    if drs == 2 and state.drs == 1:
        winsound.Beep(2500, 1000)

    if drs != state.drs:
        state.drs = drs
        print('tick change: ', drs)

if __name__ == '__main__':
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
