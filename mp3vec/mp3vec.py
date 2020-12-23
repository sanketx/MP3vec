import os
import sys
import numpy as np
import tensorflow as tf

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

aa_dict = {
	'A': 0,
	'C': 1,
	'D': 2,
	'E': 3,
	'F': 4,
	'G': 5,
	'H': 6,
	'I': 7,
	'K': 8,
	'L': 9,
	'M': 10,
	'N': 11,
	'P': 12,
	'Q': 13,
	'R': 14,
	'S': 15,
	'T': 16,
	'V': 17,
	'W': 18,
	'X': 19,
	'Z': 19,
	'B': 19,
	'Y': 20,
	'-': 21,
}


class MP3Model:
	"""Core MP3vec model class

	Attributes
	----------
	model : tf.keras.Model
		The trained model which generates MP3vecs

	Methods
	-------
	encode_file(pssm_file)
		Encodes a protein specified in a PSSM file

	vectorize(protein_matrix)
		Returns the MP3vec representation of an encoded protein

	"""

	def __init__(self, model_file=None):
		"""
		Parameters
		----------
		model_file : str, optional
			Path to the saved MP3vec model file
		"""

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

		self.model = tf.keras.models.load_model(model_file)

	def encode_file(self, pssm_file):
		"""Encodes a protein specified in a PSSM file

		Parameters
		----------
		pssm_file : str
			Path to the ASCII PSSM file generated by PSI BLAST / mp3pssm

		Returns
		-------
		seq : str
			The protein sequence
		np.ndarray
			The encoded protein and PSSM profile -> (1, L, 42)
		"""
		if not os.path.exists(pssm_file):
			print("The specified PSSM file does not exist\n\
				Please specify a valid PSSM file")
			sys.exit(0)

		with open(pssm_file) as fh:
			matrix = [line.strip().split() for line in fh][3:-6]

		pssm = np.array(matrix)[:, 2:22].astype(np.int32)
		seq = "".join(np.array(matrix)[:, 1])

		idx_list = [aa_dict[aa] if aa in aa_dict else 19 for aa in seq]
		seq_vec = np.zeros((len(seq), 22), dtype=np.int32)
		seq_vec[np.arange(len(seq)), idx_list] = 1

		return seq, np.concatenate([seq_vec, pssm], axis=1).reshape(1, -1, 42)

	def vectorize(self, protein_matrix):
		"""Returns the MP3vec representation of an encoded protein

		Parameters
		----------
		protein_matrix : np.ndarray
			The encoded protein and PSSM profile -> (1, L, 42)

		Returns
		-------
		np.ndarray
			The MP3vec representation -> (L, 640)
		"""
		return self.model.predict(protein_matrix).reshape(-1, 640)
