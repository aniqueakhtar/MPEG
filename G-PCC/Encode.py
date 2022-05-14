import argparse
import logging
import multiprocessing
import os, glob

from utils.parallel_process import parallel_process, Popen

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

def assert_exists(filepath):
    assert os.path.exists(filepath), f'{filepath} not found'
    

def run_mpeg_experiment(current_mpeg_output_dir, mpeg_cfg_path, input_pc):
    os.makedirs(current_mpeg_output_dir, exist_ok=True)

    assert_exists(input_pc)
    assert_exists(mpeg_cfg_path)

    return Popen(['make',
                  '-f', f'{MPEG_TMC13_DIR}/scripts/Makefile.tmc13-step',
                  '-C', current_mpeg_output_dir,
                  f'VPATH={mpeg_cfg_path}',
                  f'ENCODER={TMC13}',
                  f'DECODER={TMC13}',
                  f'PCERROR={PCERROR}',
                  f'SRCSEQ={input_pc}'])



if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Encode.py', description='Run G-PCC experiments.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    ### GIVE FULL/ABSOLUTE PATHS FOR THE CODE TO WORK!!!
    parser.add_argument('--cfg_folder', default="/home/anique/Anique/Coding/MPEG/My_Code/G-PCC/test_cfg")
    
    parser.add_argument('--results_dir', default='/home/anique/Anique/Coding/MPEG/My_Code/G-PCC/Results/')
    parser.add_argument('--test_files', default='/home/anique/Anique/Coding/Interpolation_2/Comparison_1/Results/Test_Files/dancer')
    
    parser.add_argument('--tmc13_dir', default="/home/anique/Anique/Coding/MPEG/My_Code/G-PCC/mpeg-pcc-tmc13-master")
    parser.add_argument('--pcerror', default="/home/anique/Anique/Coding/MPEG/My_Code/G-PCC/utils/pc_error_d")
    parser.add_argument('--num_parallel', help='Number of parallel jobs.', default=multiprocessing.cpu_count(), type=int)
    args = parser.parse_args()
    
    
    MPEG_TMC13_DIR = args.tmc13_dir
    PCERROR = args.pcerror
    TMC13 = f'{MPEG_TMC13_DIR}/build/tmc3/tmc3'
    assert_exists(TMC13)
    assert_exists(PCERROR)
    
    # Find the rates and the collect the files to run the experiment on
    rates = sorted(os.listdir(args.cfg_folder))
    files = sorted(glob.glob(args.test_files + '/**.ply'))
            
    # Store all the parameters
    params = []
    for input_pc in files:
        filename = os.path.split(input_pc)[-1].split('.')[0]
        
        for rate in rates:
            current_mpeg_output_dir = os.path.join(args.results_dir, 'encoding_results', filename, rate)
            mpeg_cfg_path = os.path.join(args.cfg_folder, rate)
            params.append((current_mpeg_output_dir, mpeg_cfg_path, input_pc))
    
    # Run experiment in parallel
    logger.info('Started GPCC experiments')
    # An SSD is highly recommended, extremely slow when running in parallel on an HDD due to parallel writes
    # If HDD, set parallelism to 1
    print(len(params))
    parallel_process(run_mpeg_experiment, params, args.num_parallel)
    # print(params)
    
    logger.info('Finished GPCC experiments')
