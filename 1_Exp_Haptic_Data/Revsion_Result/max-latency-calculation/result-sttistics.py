import graph_common as util
import numpy as np

### Direct Data without ML MOdel 
# host=15
# NoML_10=f'../NoML/Host_{host}/HD_10.txt'
# NoML_100=f'../NoML/Host_{host}/HD_100.txt'
# NoML_1000=f'../NoML/Host_{host}/HD_1000.txt'
# No_ML_data=[NoML_10,NoML_100,NoML_1000]

# # With ML Model 
host=0
WithML_10=f'../WithML/Host_{host}/HD_10.txt'
WithML_100=f'../WithML/Host_{host}/HD_100.txt'
WithML_1000=f'../WithML/Host_{host}/HD_1000.txt'
With_ML_data=[WithML_10,WithML_100,WithML_1000]




##### Find Maximum/ min latency from all
# data=util.read_latencies_files(With_ML_data) ## Get all da file for exp [return packet_ns,latencies_ms,total_n_packets]


# com_data=util.merge_all_hosts(data) # IT combine all the above data return [all_filenames, all_packet_ns, all_latencies_ms,all_total_n_packets]

# latency_max= util.calculate_max_latency(com_data) # find maxim,un latency in all data and return the latency()
# latency_min= util.calculate_mim_latency(com_data)

# print(f"MAX:{latency_max} \nMin:{latency_min}")


# ##### FOfr Single File analysis use this 
# print("Singel File Analysis")
# print("------------------------")
# packet_ns, latencies_ms, total_n_packets=util.read_latencies_file(WithML_1000)
# latency_max= np.amax(latencies_ms)
# latency_min=np.amin(latencies_ms)

# print(f"MAX:{latency_max} \nMin:{latency_min}")
# print("------------------------")

# ##### Find  Average latency for all

# data=util.read_latencies_files(With_ML_data) ## Get all da file for exp [return packet_ns,latencies_ms,total_n_packets]

# com_data=util.merge_all_hosts(data) # IT combine all the above data return [all_filenames, all_packet_ns, all_latencies_ms,all_total_n_packets]
# print(f'Avergae: {np.average(com_data[0][2])}')
# print(f'Mean: {np.mean(com_data[0][2])}')


packet_ns, latencies_ms, total_n_packets=util.read_latencies_file(WithML_100) 
cutoff_time_ms=15 # this is a cutoff va,use we used in Exp
tofo=util.calc_basic_statistics(packet_ns,latencies_ms,total_n_packets,cutoff_time_ms)
print(tofo)
ofo=util.calc_consecutive_drop_statistics(packet_ns,latencies_ms,total_n_packets,cutoff_time_ms)
print(ofo)
# drop=util.packets_received_within_cutoff(packet_ns,latencies_ms,total_n_packets,cutoff_time_ms)
# print(drop)

### This function is used to convert txt file with tap b/w two point to space
# def convert_tap2space(inputpath, outputpath):
#     fin = open(inputpath, "r") 
#     fout = open(outputpath, "w")
#     for line in fin:
#         new_line = line.replace('\t', ' ')
#         fout.write(new_line) 

#     fin.close()
#     fout.close()
