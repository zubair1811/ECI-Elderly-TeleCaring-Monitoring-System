import numpy as np
import graph_common

data_all_files = graph_common.read_latencies_files()
print(data_all_files)
max_latency_ms = graph_common.calculate_max_latency(data_all_files)