# Running G-PCC using python code
## Goal
The goal here is to run G-PCC encoding using a python script. 

Once encoding is finished, we have a separate file to go through the encoded data and save the results in a csv file while also plotting the results.

The file runs in parallel and uses the `utils.parallel_process.py` file to run everything in parallel on different CPU cores. This makes the runtime much smaller.

## How To Run
**I have noticed that if I don't use absolute paths, the scipt does not work.**
### Encoding
To encode using G-PCC:
```
python Encode.py
```
### Collecting Results
To collect the results once the encoding is performed:
```
python Gather_results.py
```


## Requirements
Install pyntcloud to calculate the number of points for bpp calculation. Maybe change that line to your own implementation if you don't want to use this library.
```
conda install pyntcloud -c conda-forge
```

keep pandas updated. Older version of pandas gives an error on this line:
```
pd1 = pd.DataFrame(data, index=['i',])
```

If you get this error, try running the file in the terminal:
```
RuntimeError: python mp_report.py /home/anique/Anique/Coding/MPEG/My_Code/G-PCC/Results/encoding_results/dancer_vox11_00000002 /home/anique/Anique/Coding/MPEG/My_Code/G-PCC/Results/fig /home/anique/Anique/Coding/MPEG/My_Code/G-PCC/Results/csvs returned with code 1
```


## Further Improvements
Please do let me know if there are any comments or suggested improvements to this work.