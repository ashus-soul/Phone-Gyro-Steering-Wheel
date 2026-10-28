import socket

server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #-> udp

server.bind(("0.0.0.0",9999))

smooth_driveing=0.0 #felot for smoother controlssss -> too many value jittery controls

#formula for smooth driving -> 20%new + 80%old


def run_server(message):
        x=message.decode("utf-8")
        y=x.split(',')
        # if isinstance(y[1],int):``
        # print(f"x:{y[0]}, y:{y[1]} z:{y[2]}")
        z=float(y[1])
        # print(z)

        try:
            # steering_angle=int(input("Enter Steering angle : "))
            steering_angle=z
            if steering_angle<=6 and steering_angle>=-6:
                a=steering_angle/6
                if a>-0.1 and a<0.1:
                    print(abs(0))
                    ip=abs(0)
                    return ip
                else: 
                    print(f"{a:.2f}")
                    ip=round(a,2)
                    return ip
            elif steering_angle<-6: 
                print (-1)
                ip=-1
                return ip
            elif steering_angle>6:
                print(1)
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
        value=run_server(message)
        y=gamepad.left_joystick_float(value,0)
        gamepad.update()
        print(f"{value}")

except:
    print("GP disconnected") 
# gamepad.right_trigger(1)
# gamepad.update()


