import graph_common as util

output_filename='/home/zubair-lab2/data/exp1_iot-v1/1_Exp_Haptic_Data/Direct_Datasending/HD_latencyfiles/HD_10.txt'
output_filename1='/home/zubair-lab2/data/exp1_iot-v1/1_Exp_Haptic_Data/Direct_Datasending/HD_latencyfiles/HD_100.txt'
output_filename2='/home/zubair-lab2/data/exp1_iot-v1/1_Exp_Haptic_Data/Direct_Datasending/HD_latencyfiles/HD_1000.txt'
# path ='../1_Exp._Haptic_Data/Direct_Datasending/HD_latencyfiles/%s'%output_filename


##### Find Maximum latency
data=util.read_latencies_files([output_filename,output_filename1,output_filename2]) ## Get all da file for exp [return packet_ns,latencies_ms,total_n_packets]

com_data=util.merge_all_hosts(data) # IT combine all the above data return [all_filenames, all_packet_ns, all_latencies_ms,all_total_n_packets]

latency= util.calculate_max_latency(com_data) # find maxim,un latency in all data and return teh latency

print(latency)