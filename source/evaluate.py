import sys

import numpy as np
import pandas as pd

# Argument from main.py
TRIAL_NUM = int(sys.argv[1])
PATH_SCRIPT = sys.argv[2]
PATH_OUT = sys.argv[3]

# well_reference = {'body': [[0, 6], [0, 7], [1, 5], [1, 6], [1, 7], [1, 8], [2, 4], [2, 6], [2, 7], [2, 9], [3, 3], [3, 1], [4, 2], [4, 3], [4, 4], [4, 6], [4, 7], [4, 9], [4, 1], [4, 1], [5, 2], [5, 3], [5, 5], [5, 6], [5, 7], [5, 8], [5, 1], [5, 1], [6, 3], [6, 4], [6, 9], [6, 1], [7, 4], [7, 5], [7, 6], [7, 7], [7, 8], [7, 9]], 'mouth': [[5, 4], [5, 9], [6, 5], [6, 6], [6, 7], [6, 8]], 'eyes': [[3, 5], [3, 8]]}
well_reference = {'body': [[0, 6], [0, 7], [1, 5], [1, 6], [1, 7], [1, 8], [2, 4], [2, 6], [2, 7], [2, 9], [3, 3], [3, 1], [4, 2], [4, 3], [4, 4], [4, 6], [4, 7], [4, 9], [4, 1], [4, 1], [5, 2], [5, 3], [5, 5], [5, 6], [5, 7], [5, 8], [5, 1], [5, 1], [6, 3], [6, 4], [6, 9], [6, 1], [7, 4], [7, 5], [7, 6], [7, 7], [7, 8], [7, 9]], }

# load absorbance data
absorbance_data = pd.DataFrame()
for abs in [405, 450, 620]: 
    df = pd.read_csv(f'{PATH_OUT}/result_{abs}.csv')    
    
    absorbance = {}
    for key in well_reference.keys():
        part_ls = []
        for well in well_reference[key]:
            value = df.iloc[well[0], well[1]]

            part_ls.append(float(value))
            absorbance[key] = np.mean(part_ls)

    absorbance_data[abs] = absorbance.values()

result = np.array(absorbance_data.T[0])

# load target data
df_target = pd.read_csv(f'{PATH_SCRIPT}/target_slime.csv')
target = np.array(df_target['body'])

# calculate score
score = np.sqrt(((target - result)**2).sum()) 

# output score
print(score)