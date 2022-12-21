import pickle
import random

'''
cell_xor = [[[0 for k in range(3)] for j in range(10)] for i in range(10)]
for i in range(10):
    for j in range(10):
        for k in range(1,3):
            cell_xor[i][j][k] = int(random.random() * 10000000000000000)

with open("cell_xor.config", "wb") as wf:
    pickle.dump(cell_xor, wf)'''

cal_data = []
with open("cal_data.config", "wb") as wf:
    pickle.dump(cal_data, wf)
