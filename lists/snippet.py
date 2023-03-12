import glob
from scipy.io import loadmat
import pandas as pd
import numpy as np

files = glob.glob('*.mat')

def process(v):
	v = v.squeeze()
	if type(v[0]) == np.ndarray:
		return np.vectorize(lambda x : x[0])(v)
	return v

for file in files:
	mat = loadmat(file)
	mat = {k:process(v) for k, v in mat.items() if k[0] != '_'}
	data = pd.DataFrame({k: pd.Series(v) for k, v in mat.items()})
	data.to_csv(file.replace(".mat", ".csv"))

