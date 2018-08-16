import os
import sys
import warnings
import numpy as np

with warnings.catch_warnings():
	warnings.simplefilter("ignore", category = FutureWarning)
	import keras

# __version__ = "test" # remove this later
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

aa_dict = {
	'A' : 0,
	'C' : 1,
	'D' : 2,
	'E' : 3,
	'F' : 4,
	'G' : 5,
	'H' : 6,
	'I' : 7,
	'K' : 8,
	'L' : 9,
	'M' : 10,
	'N' : 11,
	'P' : 12,
	'Q' : 13,
	'R' : 14,
	'S' : 15,
	'T' : 16,
	'V' : 17,
	'W' : 18,
	'X' : 19,
	'Z' : 19,
	'B' : 19,
	'Y' : 20,
	'-' : 21,
}

def encode_file(fname):
	with open(fname) as fh: # add error handling
		matrix = [line.strip().split() for line in open(fname)][3:-6]
	pssm = np.array(matrix)[:,2:22].astype(np.int32)
	seq = "".join(np.array(matrix)[:,1])
	
	idx_list = [aa_dict[aa] if aa in aa_dict else 19 for aa in seq]
	seq_vec = np.zeros((len(seq), 22), dtype = np.int32)
	seq_vec[np.arange(len(seq)), idx_list] = 1

	return seq, np.concatenate([seq_vec, pssm], axis = 1).reshape(1,-1,42)

class MP3Model(object):

	def __init__(self, model_file = None):

		if model_file is None:
			model_file = os.path.join(os.path.dirname(__file__), 'mp3_model.h5')
			if not os.path.exists(model_file):
				print("Whoops, it looks like the default file wasn't properly installed\n\
					You can get it from https://github.com/sanketx/MP3vec")
				sys.exit(0)
		else:
			if not os.path.exists(model_file):
				print("The specified model file does not exist\n\
					Please specify a valid model file")
				sys.exit(0)

		with warnings.catch_warnings():
			warnings.simplefilter("ignore", category = UserWarning)
			self.model = keras.models.load_model(model_file)

	def vectorize(self, protein_matrix):
		return self.model.predict(protein_matrix).reshape(-1,640)
	