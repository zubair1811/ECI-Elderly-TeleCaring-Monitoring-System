import socket, sys
import multiprocessing

import numpy as np
import torch
from torch import nn
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

            #####TODO Please write you ML code here - Recievce data decode get ML outrput encode forward

            decoded_data = data.decode()

            # Extract data between 'B' and 'E'
            start = decoded_data.find('B') + 1
            end = decoded_data.find('E', start)
            substring = decoded_data[start:end].strip()

            # rssi_value = substring.split()[0]  # Assuming space as delimiter
            # rssi_value = float(rssi_value)  # Convert to float
            # predicted_room = predict_location([rssi_value])
            # print(f"Predicted Room: Room {predicted_room + 1}")
            # Split substring into RSSI and the rest for HAR
            all_values = substring.split()
            rssi_value = float(all_values[0])  # First value for RSSI
            har_values = [float(x) for x in
                          all_values[1:]]  # Convert remaining data to float and scale down by dividing by 10

            # Create HAR data array
            har_data = np.array(har_values).reshape(1, -1)  # Reshape according to your HAR model's needs
            model1 = load_model1('/home/mines/PycharmProjects/pythonProject1/exp1_iot/1_Exp_Haptic_Data/lstm_rssi_model.pth')

            # # RSSI Prediction
            predicted_room = predict1(model1, [rssi_value])
            print(f"Predicted Room: Room {predicted_room + 1}")
            #
            # HAR Prediction (ensure your predict function and har_data shape align with your model's expectations)
            # har_prediction = predict(har_data)  # Function predict() should be defined to handle HAR data
            # print(f'Predicted HAR Class: {har_prediction}')

            model2 = load_model2('/home/mines/PycharmProjects/pythonProject1/exp1_iot/1_Exp_Haptic_Data/best_model.pth')

            # When you need to make a prediction
            predicted_class = predict2(model2, har_data)
            print(predicted_class)

            message = f"Predicted Room: Room {predicted_room + 1}, Predicted HAR Class: {predicted_class}"
            print(message)

            # Encoding and sending the message
            sock_out.sendall(message.encode())
            print(f"F-Server <--- {message}")

            # sock_out.sendall(data)  # TODO for sent all
            # print(f"F-Server <--- {data}, {len(data)}")  # TODO
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
    # sender = multiprocessing.Process(target=packet_backwarding)
    #
    receiver.start()
    # sender.start()
    #
    #     receiver.terminate()
    #     sender.terminate()
    #
    receiver.join()
    # sender.join()
