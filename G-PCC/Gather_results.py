'''
Author: Anique Akhtar
Contact: https://aniqueakhtar.github.io/
'''
import argparse
import logging
import multiprocessing
import os, glob

from utils.parallel_process import parallel_process, Popen
from utils.avg_csv import average_csv, plot_panda_csv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

def run_gen_report(folder_path, fig_folder, res_folder):
    return Popen(['python', 'mp_report.py', folder_path, fig_folder, res_folder])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Gather_results.py', description='Run MPEG experiments.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('--results_dir', default='/home/anique/Anique/Coding/MPEG/My_Code/G-PCC/Results/')
    parser.add_argument("--calculate_average", default=True, action='store_true', help='Create csv and plot with aberage results')
    
    parser.add_argument('--num_parallel', help='Number of parallel jobs.', default=multiprocessing.cpu_count(), type=int)
    args = parser.parse_args()
    
    Encoding_results = os.path.join(args.results_dir, 'encoding_results')
    files = sorted(os.listdir(Encoding_results))
    rates = sorted(os.listdir(os.path.join(Encoding_results, files[0])))
    
    fig_folder = os.path.join(args.results_dir, 'fig')
    result_folder = os.path.join(args.results_dir, 'csvs')
    os.makedirs(fig_folder, exist_ok=True)
    os.makedirs(result_folder, exist_ok=True)
    
    
    ## Collecting parameters    
    params = []    
    for f in files:
        file = os.path.join(Encoding_results, f)
        params.append((file, fig_folder, result_folder))
    
    ## Running parameters in parallel
    logger.info('Generating GPCC experimental reports')
    parallel_process(run_gen_report, params, args.num_parallel)
    logger.info('Done')
    
    # Calculating average from csv files
    if args.calculate_average:
        csv_files = sorted(glob.glob(result_folder+'/**.csv'))
        avg_csv = average_csv(csv_files)
        
        name = os.path.dirname(args.results_dir).split('/')[-1]
        dest_csv = os.path.join(args.results_dir, name+'_avg.csv')
        dest_fig = os.path.join(args.results_dir, name+'_avg.jpg')
        
        avg_csv.to_csv(dest_csv, index=False)
        plot_panda_csv(avg_csv, 'bpp', 'd1_psnr', 'D1', 'bpp', 'PSNR', dest_fig)
        
        