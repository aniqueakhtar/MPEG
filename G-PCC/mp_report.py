import argparse
import os
from pyntcloud import PyntCloud
import mpeg_parsing
from glob import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def find(folder, pattern):
    files = glob(os.path.join(folder, pattern))
    assert len(files) == 1
    return files[0]


def run(folder_path, fig_folder, res_folder):
    assert os.path.exists(folder_path), f'{folder_path} does not exist'
    
    rates = sorted(os.listdir(folder_path))
    name = folder_path.split('/')[-1]
    
    for idx ,r in enumerate(rates):
        path = os.path.join(folder_path, r)
        
        pc_log = find(path, '*.bin.log')
        pcerror_result = find(path, '*.pc_error')
        
        log_data = mpeg_parsing.parse_bin_log(pc_log)
        pcerror_data = mpeg_parsing.parse_pcerror(pcerror_result)
        
        pos_total_size_in_bytes = log_data['pos_bitstream_size_in_bytes']
        input_point_count = len(PyntCloud.from_file(log_data['uncompressed_data_path']).points)
        # print("\n\n", input_point_count, "\n\n")
        pos_bits_per_input_point = pos_total_size_in_bytes * 8 / input_point_count
        data = {
            'pos_total_size_in_bytes': pos_total_size_in_bytes,
            'pos_bits_per_input_point': pos_bits_per_input_point,
            'input_point_count': input_point_count
        }
        data = {**data, **log_data, **pcerror_data}
        
        pd1 = pd.DataFrame(data, index=['i',])
        results = pd1[['pos_total_size_in_bytes', 'pos_bits_per_input_point', 'd1_mse', 'd1_psnr']]
        results = results.rename({'pos_bits_per_input_point': 'bpp'}, axis=1)
        
        if idx == 0:
            all_results = results.copy(deep=True)
        else: 
            all_results = pd.concat((all_results, results), ignore_index=True)
    
    csv_name = os.path.join(res_folder, name + '.csv')
    all_results.to_csv(csv_name, index=False)
    print('Wrile results to: \t', csv_name)
    
    fig, ax = plt.subplots(figsize=(7, 4))
    plt.plot(np.array(all_results["bpp"][:]), np.array(all_results["d1_psnr"][:]), 
            label="D1", marker='x', color='red')
    plt.title(name)
    plt.xlabel('bpp')
    plt.ylabel('PSNR')
    plt.grid(ls='-.')
    plt.legend(loc='lower right')
    fig.savefig(os.path.join(fig_folder, name+'.jpg'), dpi=300)
        



if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='mp_report.py', description='Gather results for G-PCC',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('folder_path', help='MPEG test folder.')
    parser.add_argument('fig_folder', help='Plot Figure in this path.')
    parser.add_argument('res_folder', help='Output results in this path.')
    args = parser.parse_args()
    
    run(args.folder_path, args.fig_folder, args.res_folder)



