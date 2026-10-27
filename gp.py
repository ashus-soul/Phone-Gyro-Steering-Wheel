import vgamepad as vg
gamepad=vg.VX360Gamepad()
try:
    while True:
        a=int(input("input : "))
        x=gamepad.right_trigger(a)
        print(x)
        gamepad.update()  # Applies the joystick state to the OS
#  #takes -1 to 1 what i want
except:
    print("GP disconnected") 
# gamepad.right_trigger(1)
# gamepad.update()