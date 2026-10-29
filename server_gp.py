import socket
import vgamepad as vg

server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #-> udp

server.bind(("0.0.0.0",9999))

smooth_driveing=0.0 #felot for smoother controlssss -> too many value jittery controls

#formula for smooth driving -> 20%new + 80%old

#zones -> tune these to your phone
ACC_MAX=6   #x below this -> acc
REV_MIN=8   #x above this -> rev   (between ACC_MAX and REV_MIN = dead zone, no acc no rev)
HB_MIN=0    #z from HB_MIN to HB_MAX -> handbrake
HB_MAX=4


def parse_message(message):
        x=message.decode("utf-8")
        y=x.split(',')
        return float(y[0]), float(y[1]), float(y[2])


def run_sever_hb(z):
        #-> z axis input for accelerate -> blue
        hb=z
        if hb<HB_MAX and hb>=HB_MIN:
            # print("hb braking")
            return 1

        elif hb<0:
            # print("hb not braking out of range")
            return 0

        else:
            # print("hb not braking")
            return 0


def run_server_acc(x):
        #-> z axis input for accelerate -> blue
        acc=x
        if acc<ACC_MAX:
            # print("acc ok")
            return 1
        else:
            # print("acc out of range")
            return 0


def run_server_rev(x):
        #-> z axis input for accelerate -> blue
        acc=x
        if acc>REV_MIN:
            # print("rev ok")
            return 1
        else:
            # print("rev out of range")
            return 0


def run_server_tilt(y):
        # if isinstance(y[1],int):``
        # print(f"x:{y[0]}, y:{y[1]} z:{y[2]}")

        # x=float(y[0]) #-> z axis input for accelerate -> blue
        # z=float(y[2]) #-> hadnbrake -> red
        #y=float(y[1]) #-> tilt -> green
        # print(z)

        #this fxn for tilt fxnality -> working y axis input
        # steering_angle=int(input("Enter Steering angle : "))
        steering_angle=y
        if steering_angle<=6 and steering_angle>=-6:
            a=steering_angle/6
            if a>-0.1 and a<0.1:
                # print(abs(0))
                return 0
            else:
                # print(f"{a:.2f}")
                return round(a,2)
        elif steering_angle<-6:
            # print (-1)
            return -1
        else:
            # print(1)
            return 1

# def server_value():

# while True:
#         message,address=server.recvfrom(1024) #recvfrom not recv bcz we dont know who send it
#         # print(message.decode("utf-8"))
#         # server.sendto("NEXT VALUE??".encode("utf-8"),address) #sendto not send

#         value=run_server()
#         print(value)

#####code for gp######
#tried in diffrent .py but doesnt work


gamepad=vg.VX360Gamepad() #error -> befoere no () so no class
try:
    while True:
        # a=int(input("input : "))
        # x=gamepad.right_trigger(a)
        # print(x)
        # gamepad.update()  # Applies the joystick state to the OS
#  #takes -1 to 1 what i want
        # run_server(message,address)
        message,address=server.recvfrom(1024) #recvfrom not recv bcz we dont know who send it

        try:
            x,y,z=parse_message(message)
        except (ValueError,IndexError):
            print("NOT A NUMBER GNG")
            continue

        valuelr=run_server_tilt(y)
        gamepad.left_joystick_float(valuelr,0)
        # print(f"{value}")

        #acceleration system
        acc=run_server_acc(x)
        gamepad.right_trigger_float(acc)

        rev=run_server_rev(x)
        gamepad.left_trigger_float(rev)

        #brakesystem
        hb=run_sever_hb(z)
        if int(hb) == 1:
            gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        else:
            gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        gamepad.update()
except KeyboardInterrupt:
    print("stopped")
except Exception as e:
    print("GP disconnected",e)
finally:
    gamepad.reset()
    gamepad.update()
# gamepad.right_trigger(1)
# gamepad.update()