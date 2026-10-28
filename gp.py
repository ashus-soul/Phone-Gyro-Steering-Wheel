import vgamepad as vg
from server import value
gamepad=vg.VX360Gamepad() #error -> befoere no () so no class
try:
    while True:
        # a=int(input("input : "))
        # x=gamepad.right_trigger(a)
        # print(x)
        # gamepad.update()  # Applies the joystick state to the OS
#  #takes -1 to 1 what i want
        # run_server(message,address)
        y=gamepad.left_joystick_float(a=value,b=0)
        gamepad.update()
except:
    print("GP disconnected") 
# gamepad.right_trigger(1)
# gamepad.update()
