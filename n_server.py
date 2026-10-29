import socket

server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #-> udp

server.bind(("0.0.0.0",9999))

smooth_driveing=0.0 #felot for smoother controlssss -> too many value jittery controls

#formula for smooth driving -> 20%new + 80%old

def run_sever_hb(message):
        x=message.decode("utf-8")
        y=x.split(',')
        z=float(y[2]) #-> z axis input for accelerate -> blue 
        try:
            hb=z
            if hb<4 and hb>=0:
                # print("hb braking")
                return 1

            elif hb<0:
                #  print("hb not braking out of range")
                 return 0

            else:
                # print("hb not braking")
                return 0
            
        except ValueError:
            print("NOT A NUMBER GNG")


def run_server_acc(message):
        x=message.decode("utf-8")
        y=x.split(',')
        x=float(y[0]) #-> z axis input for accelerate -> blue 
        try:
            acc=x
            if acc<7:
                acc=abs(1)
                # print("acc ok")
                return acc
            else:
                acc=abs(0)
                # print("acc out of range")
                return acc
        except ValueError:
            print("NOT A NUMBER GNG")

def run_server_rev(message):
        x=message.decode("utf-8")
        y=x.split(',')
        x=float(y[0]) #-> z axis input for accelerate -> blue 
        try:
            acc=x
            if acc>7:
                acc=abs(1)
                print("rev ok")
                return acc
            else:
                acc=abs(0)
                print("rev out of range")
                return acc
        except ValueError:
            print("NOT A NUMBER GNG")



def run_server_tilt(message):
        x=message.decode("utf-8")
        y=x.split(',')
        # if isinstance(y[1],int):``
        # print(f"x:{y[0]}, y:{y[1]} z:{y[2]}")

        # x=float(y[0]) #-> z axis input for accelerate -> blue 
        # z=float(y[2]) #-> hadnbrake -> red
        y=float(y[1]) #-> tilt -> green
        # print(z)


            
            

        try: #this try block for tilt fxnality -> working y axis input
            # steering_angle=int(input("Enter Steering angle : "))
            steering_angle=y
            if steering_angle<=6 and steering_angle>=-6:
                a=steering_angle/6
                if a>-0.1 and a<0.1:
                    # print(abs(0))
                    ip=abs(0)
                    return ip
                else: 
                    # print(f"{a:.2f}")
                    ip=round(a,2)
                    return ip
            elif steering_angle<-6: 
                # print (-1)
                ip=-1
                return ip
            elif steering_angle>6:
                # print(1)
                ip=1
                return ip

        except ValueError:
            print("NOT A NUMBER GNG")

# def server_value():

# while True:
#         message,address=server.recvfrom(1024) #recvfrom not recv bcz we dont know who send it 
#         # print(message.decode("utf-8"))
#         # server.sendto("NEXT VALUE??".encode("utf-8"),address) #sendto not send 

#         value=run_server()
#         print(value)
        
#####code for gp######
#tried in diffrent .py but doesnt work




import vgamepad as vg
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
        valuelr=run_server_tilt(message)
        y=gamepad.left_joystick_float(valuelr,0)
        gamepad.update()
        # print(f"{value}")
        
        #acceleration system
        acc=run_server_acc(message)
        x=gamepad.right_trigger_float(acc)
        gamepad.update()

        rev=run_server_rev(message)
        b=gamepad.left_trigger_float(rev)
        gamepad.update()
        
        #brakesystem
        hb=run_sever_hb(message)
        if int(hb) == 1:
            gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        else:
            gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        gamepad.update()
except:
    print("GP disconnected") 
# gamepad.right_trigger(1)
# gamepad.update()


