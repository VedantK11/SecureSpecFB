import re
import os
import csv

# Function to extract information from log text
def extract_info(log_text):
    result = {}

    # Extracting IPC
    ipc_match = re.search(r'CPU 0 cumulative IPC: (\d+\.\d+)', log_text)
    if ipc_match:
        result['IPC'] = ipc_match.group(1)

    # Extracting MPKI for various levels
    areas = ['L2C TOTAL', 'L1I TOTAL', 'L1D TOTAL', 'ITLB TOTAL', 'DTLB TOTAL', 'STLB TOTAL', 'LLC TOTAL']
    for area in areas:
        mpki_match = re.search(rf'{area}.*?MPKI:\s([\d.]+)', log_text, re.DOTALL)
        if mpki_match:
            result[f"{area}_MPKI"] = mpki_match.group(1)

    # Extracting accuracy values
    for level in ['L1D', 'L2C', 'LLC']:
        accuracy_match = re.search(rf'{level} USEFUL LOAD PREFETCHES:.*?ACCURACY:\s*([\d.-]+)', log_text, re.DOTALL)
        if accuracy_match:
            result[f'{level} Accuracy'] = accuracy_match.group(1)

    # Extracting L1D LOAD ACCESS MPKI
    l1d_load_mpki_match = re.search(r'L1D LOAD\s+ACCESS:.*?MPKI:\s*([\d.]+)', log_text, re.DOTALL)
    if l1d_load_mpki_match:
        result['L1D_LOAD_ACCESS_MPKI'] = l1d_load_mpki_match.group(1)

    # Extracting L1D Hit Rate
    l1d_hit_rate_match = re.search(r'Percentage of hit:\s*([\d.]+)', log_text, re.DOTALL)
    if l1d_hit_rate_match:
        result['L1D_Hit_Rate'] = l1d_hit_rate_match.group(1)

    # Extracting L1D Average Miss Latency
    l1d_avg_miss_latency_match = re.search(r'L1D AVERAGE MISS LATENCY:\s*([\d.]+)', log_text, re.DOTALL)
    if l1d_avg_miss_latency_match:
        result['L1D_Avg_Miss_Latency'] = l1d_avg_miss_latency_match.group(1)

    # Extracting L1I Average Miss Latency
    l1i_avg_miss_latency_match = re.search(r'L1I AVERAGE MISS LATENCY:\s*([\d.]+)', log_text, re.DOTALL)
    if l1i_avg_miss_latency_match:
        result['L1I_Avg_Miss_Latency'] = l1i_avg_miss_latency_match.group(1)

    # Extracting L2C Instruction Load MPKI
    l2c_instr_load_mpki_match = re.search(r'L2C INSTRUCTION LOAD.*?MPKI:\s*([\d.]+)', log_text, re.DOTALL)
    if l2c_instr_load_mpki_match:
        result['L2C_Instruction_Load_MPKI'] = l2c_instr_load_mpki_match.group(1)

    # Extracting L2C Average Miss Latency
    l2c_avg_miss_latency_match = re.search(r'L2C AVERAGE MISS LATENCY:\s*([\d.]+)', log_text, re.DOTALL)
    if l2c_avg_miss_latency_match:
        result['L2C_Avg_Miss_Latency'] = l2c_avg_miss_latency_match.group(1)

    return result

# Directory containing log files
folder_path = '.'  # Change this if logs are in a different folder

# List all files in the directory
files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

# Process each file
output_data = []
for file_name in files:
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'r', encoding='latin-1') as file:
        log_text = file.read()
        info = extract_info(log_text)
        info['File'] = file_name  # Add file name to the result
        output_data.append(info)

# Writing to CSV
output_file = 'output.csv'

# ✅ Collect all unique keys from all entries to avoid field mismatch
all_keys = set()
for row in output_data:
    all_keys.update(row.keys())
keys = sorted(all_keys)  # Optional: sort for readability

with open(output_file, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=keys)
    writer.writeheader()
    writer.writerows(output_data)

print(f"Extraction complete. Data saved to {output_file}")
