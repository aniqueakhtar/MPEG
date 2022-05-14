'''
Author: Anique Akhtar
Contact: https://aniqueakhtar.github.io/
'''
import argparse
import glob
import os
import sklearn
import point_cloud_utils as pcu
import numpy as np
import matplotlib.pyplot as plt



if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='runme.py', description='Run normal approximation experiment.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--outdir", default='./Results')
    parser.add_argument("--data_path", default='/media/anique/DATA/Dataset/LiDAR/FORD/Ford_02_q_1mm/')
    # parser.add_argument('--num_parallel', help='Number of parallel jobs.', default=mp.cpu_count(), type=int)
    args = parser.parse_args()
    
    os.makedirs(args.outdir, exist_ok=True)
       
    files = sorted(glob.glob(args.data_path + '**.ply'))
    ## Choosing 20 files for testing. Each file is 75 frames apart
    test_files = [files[i] for i in list(range(0,1500,75))]
    # Number of neighbors
    num_neigh = list(range(12,54,4))    
    # Radius size
    ball_radius = list(range(10,100,10))
    
    '''
    ## CALCULATING MSE AND ANGLE BASED ON KNN
    '''
    mse_list = []
    angle_list = []
    for frame in test_files:
        print(frame)
        (xyz, n) = pcu.load_mesh_vn(frame)
        mse = []
        angle = []
        for neighbors in num_neigh:
            _, n1 = pcu.estimate_point_cloud_normals_knn(xyz, neighbors)
            
            # Calculating mse
            # mse1 = sklearn.metrics.mean_squared_error(n, n1)
            
            # Calculating mse with normal sign changed
            # mse2 = sklearn.metrics.mean_squared_error(n, -n1)
            
            # Calculating per point mean for both positive and negative signed normals
            # Then choosing the minimum of them both by calculating row wise minimum mean.
            mean1 = ((n-n1)**2).mean(1)
            mean2 = ((n+n1)**2).mean(1)
            row_wise_mean = np.array(list(map(min, zip(mean1, mean2))))
            mse3 = row_wise_mean.mean()
            
            # print("mse for",neighbors,"neighbors :", mse3)
            mse.append(mse3)
            
            # Calculating angle            
            angle1 = np.arccos(np.clip(np.sum(n*n1, axis=1), -1.0, 1.0))
            angle2 = np.arccos(np.clip(np.sum(n*-n1, axis=1), -1.0, 1.0))
            row_wise_angle = np.array(list(map(min, zip(angle1, angle2))))
            angle3 = row_wise_angle.mean()
            
            # print("angle for",neighbors,"neighbors :", angle3)
            angle.append(angle3)
            
        mse_list.append(mse)
        angle_list.append(angle)
    
    mse_list = np.array(mse_list)
    mse_mean = mse_list.mean(0)
    angle_list = np.array(angle_list)
    angle_mean = angle_list.mean(0)
    
    # Plot MSE
    name = os.path.dirname(args.data_path).split('/')[-1]
    fig, ax = plt.subplots(figsize=(7, 4))
    plt.plot(num_neigh, mse_mean)
    plt.title(name)
    plt.xlabel('number of neighbors')
    plt.ylabel('MSE')
    plt.grid(ls='-.')
    # plt.legend(loc='lower right')
    fig.savefig(os.path.join(args.outdir, name +'_knn_MSE.jpg'), dpi=300)
    
    # Plot ANGLE
    name = os.path.dirname(args.data_path).split('/')[-1]
    fig, ax = plt.subplots(figsize=(7, 4))
    plt.plot(num_neigh, angle_mean)
    plt.title(name)
    plt.xlabel('number of neighbors')
    plt.ylabel('Angle')
    plt.grid(ls='-.')
    # plt.legend(loc='lower right')
    fig.savefig(os.path.join(args.outdir, name +'_knn_Angle.jpg'), dpi=300)
    
    
    
    # '''
    # ## CALCULATING MSE AND ANGLE BASED ON RADIUS
    # '''
    # mse_list = []
    # angle_list = []
    # for frame in test_files:
    #     print(frame)
    #     (xyz, n) = pcu.load_mesh_vn(frame)
    #     mse = []
    #     angle = []
    #     for radius in ball_radius:
    #         _, n2 = pcu.estimate_point_cloud_normals_ball(xyz, radius)
            
    #         # Calculating per point mean for both positive and negative signed normals
    #         # Then choosing the minimum of them both by calculating row wise minimum mean.
    #         mean1 = ((n-n2)**2).mean(1)
    #         mean2 = ((n+n2)**2).mean(1)
    #         row_wise_mean = np.array(list(map(min, zip(mean1, mean2))))
    #         mse3 = row_wise_mean.mean()
            
    #         # print("mse for",neighbors,"neighbors :", mse3)
    #         mse.append(mse3)
            
    #         # Calculating angle            
    #         angle1 = np.arccos(np.clip(np.sum(n*n2, axis=1), -1.0, 1.0))
    #         angle2 = np.arccos(np.clip(np.sum(n*-n2, axis=1), -1.0, 1.0))
    #         row_wise_angle = np.array(list(map(min, zip(angle1, angle2))))
    #         angle3 = row_wise_angle.mean()
            
    #         # print("angle for",neighbors,"neighbors :", angle3)
    #         angle.append(angle3)
            
    #     mse_list.append(mse)
    #     angle_list.append(angle)
    
    # mse_list = np.array(mse_list)
    # mse_mean = mse_list.mean(0)
    # angle_list = np.array(angle_list)
    # angle_mean = angle_list.mean(0)
    
    # # Plot MSE
    # name = os.path.dirname(args.data_path).split('/')[-1]
    # fig, ax = plt.subplots(figsize=(7, 4))
    # plt.plot(ball_radius, mse_mean)
    # plt.title(name)
    # plt.xlabel('number of neighbors')
    # plt.ylabel('MSE')
    # plt.grid(ls='-.')
    # # plt.legend(loc='lower right')
    # fig.savefig(os.path.join(args.outdir, name +'_radius_MSE.jpg'), dpi=300)
    
    # # Plot ANGLE
    # name = os.path.dirname(args.data_path).split('/')[-1]
    # fig, ax = plt.subplots(figsize=(7, 4))
    # plt.plot(ball_radius, angle_mean)
    # plt.title(name)
    # plt.xlabel('number of neighbors')
    # plt.ylabel('Angle')
    # plt.grid(ls='-.')
    # # plt.legend(loc='lower right')
    # fig.savefig(os.path.join(args.outdir, name +'_radius_Angle.jpg'), dpi=300)
    
    
    
    