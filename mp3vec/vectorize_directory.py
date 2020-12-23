import os
import sys
import glob
import argparse

import numpy as np
from mp3vec import MP3Model


def vectorize_directory():

    description = """MP3vec command line utility. This program can be used to generate
    Multi-Purpose Protein Prediction vectors as described in the paper. It accepts PSSM
    files as input and creates a protein feature vector that can be saved as either a
    Numpy array or as a CSV file. To use this program, please provide the path to a
    directory containing PSSM files. Ensure that these files have a '.pssm' extension or
    they will be ignored. You also have to specify an output directory where the generated
    vectors will be stored. Finally, you need to specify the output file format, either
    numpy array or CSV file.
    """
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "-i", "--in_directory",
        help="Path to Input Directory containing PSSM files",
        action="store",
        required=True
    )

    parser.add_argument(
        "-o", "--out_directory",
        help="Path to Output Directory to write MP3vec files",
        action="store",
        required=True
    )

    parser.add_argument(
        "-m", "--model_file",
        help="Path to MP3 model file. Optional parameter for custom models",
        action="store",
        required=False
    )

    parser.add_argument(
        "-t", "--otype",
        help="Output file format. numpy (NPY) or comma separated values (CSV)",
        action="store",
        required=True,
        choices=["NPY", "CSV"]
    )

    args = parser.parse_args()

    in_directory = args.in_directory
    out_directory = args.out_directory
    model_file = args.model_file
    otype = args.otype.lower()

    ########################### Validate everything ###########################

    if not os.path.isdir(in_directory):
        print("Input Directory does not exist")
        sys.exit(0)

    if not os.path.isdir(out_directory):
        print("Output Directory does not exist")
        sys.exit(0)

    if model_file is not None and not os.path.exists(model_file):
        print("The specified model file does not exist")
        sys.exit(0)

    pssm_list = glob.glob(os.path.join(in_directory, "*.pssm"))

    if len(pssm_list) == 0:
        print("No files with '.pssm' extension found in the Input Directory")
        sys.exit(0)

    ###########################################################################

    model = MP3Model(model_file)

    for i, fname in enumerate(sorted(pssm_list), 1):
        _, protein_matrix = model.encode_file(fname)
        vec = model.vectorize(protein_matrix)
        ofname = os.path.split(fname)[1].split('.')[0]

        if otype == "npy":
            dest = os.path.join(out_directory, ofname)
            np.save(dest, vec)

        else:
            dest = os.path.join(out_directory, ofname + '.csv')
            np.savetxt(dest, vec, fmt="%.16f", delimiter=',')

        print(f"Vectorized {ofname}, file {i} / {len(pssm_list)}")
