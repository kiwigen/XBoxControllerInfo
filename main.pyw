from os import times
from win10toast import ToastNotifier 
from XInput import *
import SysTray
import threading
from threading import Event
from datetime import datetime

_battery_level_dict = {BATTERY_LEVEL_EMPTY : "EMPTY",
                       BATTERY_LEVEL_LOW : "LOW",
                       BATTERY_LEVEL_MEDIUM : "MEDIUM",
                       BATTERY_LEVEL_FULL : "FULL"}

_battery_type_dict = {BATTERY_TYPE_DISCONNECTED : "DISCONNECTED",
                      BATTERY_TYPE_WIRED : "WIRED",
                      BATTERY_TYPE_ALKALINE : "ALKALINE",
                      BATTERY_TYPE_NIMH : "NIMH",
                      BATTERY_TYPE_UNKNOWN : "UNKNOWN"}


BATTERY_TYPE = 0
BATTERY_LEVEL = 1          

exit = Event()
timestamp = 0

def MakeToast(message:str):
    n = ToastNotifier()    
    n.show_toast("XBox Controller", message, duration = 3)

def GetControllers():
    return get_connected()

def CheckBatteryStatus(event):   
    user = event.user_index
    batInfo = get_battery_information(user)
    print(batInfo)
    global timestamp    
    if not batInfo[BATTERY_TYPE] == _battery_type_dict[BATTERY_TYPE_WIRED] and batInfo[BATTERY_LEVEL] == _battery_level_dict[BATTERY_LEVEL_LOW] or batInfo[BATTERY_LEVEL] == _battery_level_dict[BATTERY_LEVEL_EMPTY]:        
        current = datetime.now()
        diff = current - timestamp
        duration_in_s = diff.total_seconds()      
        #Make Toast Noatification only every ~2 minutes 
        if duration_in_s > 120:            
            MakeToast("Batterie ist fast leer.")
    timestamp = datetime.now()

class MyHandler(EventHandler):
    def process_button_event(self, event):      
        if event.type == EVENT_BUTTON_PRESSED:   
            CheckBatteryStatus(event)
    
    def process_trigger_event(self, event):    
        pass
    
    def process_stick_event(self, event):
        pass
    
    def process_connection_event(self, event):
        print(event)


def InitControllerHandler():
    global timestamp
    timestamp = datetime.now()
    handler = MyHandler(0, 1, 2, 3)        # initialize handler object
    my_gamepad_thread = GamepadThread(handler)


def BatteryInfo():
    InitControllerHandler()
    while not exit.is_set():
        pass

def quitThread():
    exit.set()

if __name__ == '__main__':
    import itertools, glob
    icons = itertools.cycle(glob.glob('*.ico'))
    hover_text = "XBox Controller Info"
    menu_options = ()
    x  = threading.Thread(target = BatteryInfo)
    x.start()
    SysTray.SysTrayIcon(next(icons), hover_text, menu_options, on_quit=quitThread(), default_menu_index=1)
    print("Ende")


