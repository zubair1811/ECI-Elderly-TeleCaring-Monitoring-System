import socket, sys
import multiprocessing

import numpy as np
import torch
from torch import nn
import libfunctions as code
from rssi_predict import load_model1, predict1
from har_predict import load_model2, predict2


# import torch.nn as nn

exec(open("../1_Exp_Haptic_Data/settings.txt").read())  # TODO use to run with CMD in mininet command using maketerm
# exec(open("./settings.txt").read()) # Uncooment and use for directly used with xterm

listen_port = kin_link_0
target_ip = PC_3
b_target_ip = PC_1


def packet_forwarding():
    sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock_in.bind(("0.0.0.0", listen_port))
    sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    send_addr = (target_ip, listen_port + 1)  # TODO for sent all
    sock_out.connect(send_addr)  # TODO for sent all
    print("Server running...")
    while True:
        try:
            data, recv_addr = sock_in.recvfrom(1024)
            # print(f"F_Server ---> {data}, {len(data)}") # TODO
            if not data:
                break
            # Uncomment this to run ML code 
            """ 
            #####TODO -------------------> Start ML CODE

            #####TODO Please write you ML code here - Recievce data decode get ML outrput encode forward
            data_tmstmp = code.coding(data.decode())
            data_payload = code.decoding(data.decode())

            rssi_value = float(data_payload[0])  # First value for RSSI
            har_values = [float(x) for x in
                          data_payload[1:]]  # Convert remaining data to float and scale down by dividing by 10

            # Create HAR data array
            har_data = np.array(har_values).reshape(1, -1)  # Reshape according to your HAR model's needs
            model1 = load_model1('../1_Exp_Haptic_Data/lstm_rssi_model.pth')

            # # RSSI Prediction
            predicted_room = predict1(model1, [rssi_value])
            print(f"Predicted Room: Room {predicted_room + 1}")

            model2 = load_model2('../1_Exp_Haptic_Data/best_model.pth')

            # When you need to make a prediction
            predicted_class = predict2(model2, har_data)
            print(predicted_class)

            message = f"Predicted Room: Room {predicted_room + 1}, Predicted HAR Class: {predicted_class}"
            feedback_data=code.message_format2(message)
            feedback_msg=data_tmstmp+feedback_data

            # Encoding and sending the message
            print(f"F-Server <--- {feedback_msg}")
            
            sock_out.sendall(feedback_msg.encode())
            ####--------------------> TODO END ML CODE
            """


            print(f"F-Server <--- {data}") ######### These two lines are used to send ditrect data and  by commint the aove block
            sock_out.sendall(data)

        except KeyboardInterrupt:
            print("Server in Exception mode")  # TODO
            break
    print("Closing...")
    sock_out.close()
    sys.exit(0)


def packet_backwarding():
    sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock_in.bind(("0.0.0.0", listen_port + 2))
    print("B_Server running...")
    while True:
        try:
            data, recv_addr = sock_in.recvfrom(1024)
            if not data:
                break
            send_addr = (b_target_ip, listen_port + 3)
            sock_in.sendto(data, send_addr)
            print(f"B-Server <--- {data}, {len(data)}")  # TODO
            # sock_in.sendall(data) # TODO for sent all
        except KeyboardInterrupt:
            print("Server in Exception mode")  # TODO
            break
    print("Closing...")
    sock_in.close()


if __name__ == '__main__':
    receiver = multiprocessing.Process(target=packet_forwarding)
    sender = multiprocessing.Process(target=packet_backwarding)
    #
    receiver.start()
    sender.start()
    #
    #     receiver.terminate()
    #     sender.terminate()
    #
    receiver.join()
    sender.join()
