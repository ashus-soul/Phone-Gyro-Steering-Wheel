import socket

server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #-> udp

server.bind(("0.0.0.0",9999))

smooth_driveing=0.0 #felot for smoother controlssss -> too many value jittery controls

#formula for smooth driving -> 20%new + 80%old
#
while True:
    message,address=server.recvfrom(1024) #recvfrom not recv bcz we dont know who send it 
    # print(message.decode("utf-8"))
    # server.sendto("NEXT VALUE??".encode("utf-8"),address) #sendto not send 
    x=message.decode("utf-8")
    y=x.split(',')
    # if isinstance(y[1],int):
    # print(f"x:{y[0]}, y:{y[1]} z:{y[2]}")
    z=float(y[1])
    # print(z)

    try:
        # steering_angle=int(input("Enter Steering angle : "))
        steering_angle=z
        if steering_angle<=4 and steering_angle>=-4:
            a=steering_angle/4
            if a>-0.3 and a<0.3:
                print(abs(0))
            else: 
                print(f"Steering : {a:.2f}")
        elif steering_angle>-4 : 
            print (1)
        elif steering_angle<4 : 
            print (1)
                
    except ValueError:
        print("NOT A NUMBER GNG")
