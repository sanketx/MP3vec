import os
import sys
import argparse
import subprocess

from Bio import SeqIO


def make_pssm():

    description = """Wrapper utility for generating PSSM files using PSI-BLAST.
    This program generates PSSM profiles for FASTA sequences. You need to provide
    the path to an input FASTA file (multiple sequences are allowed) along with
    the destination directory where the PSSM files will be stored. The files will
    be named using the sequence ID in the FASTA file and will be saved with a
    '.pssm' extension. You also need to specify the path to the Uniref90 BLAST
    database and the number of threads you wish to use for the PSSM computation.
    By default, only 1 thread will be used."""

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "-i", "--in_file",
        help="Path to Input FASTA file containing protein sequences",
        action="store",
        required=True
    )

    parser.add_argument(
        "-o", "--out_directory",
        help="Path to Output Directory to write PSSM files",
        action="store",
        required=True
    )

    parser.add_argument(
        "-d", "--blast_db",
        help="Path to Uniref90 BLAST database",
        action="store",
        required=True
    )

    parser.add_argument(
        "-n", "--num_threads",
        help="Number of threads (CPUs) to use in the BLAST search",
        action="store",
        type=int,
        required=False
    )

    args = parser.parse_args()

    in_file = args.in_file
    out_directory = args.out_directory
    blast_db = args.blast_db
    num_threads = args.num_threads

    ########################### Validate everything ###########################

    if not os.path.exists(in_file):
        print("The specified FASTA file does not exist")
        sys.exit(0)

    if not os.path.isdir(out_directory):
        print("Output Directory does not exist")
        sys.exit(0)

    if not os.path.exists(blast_db + ".00.psq"):
        print("The specified BLAST DB file does not exist")
        sys.exit(0)

    if num_threads is None:
        num_threads = "1"

    elif num_threads < 1:
        num_threads = "1"

    else:
        num_threads = str(num_threads)

    ###########################################################################

    count = 0

    for record in SeqIO.parse(in_file, "fasta"):
        fasta_file = os.path.join(out_directory, record.id + '.fa')
        pssm_file = os.path.join(out_directory, record.id + '.pssm')
        SeqIO.write(record, fasta_file, "fasta")

        with open(os.devnull, 'w') as null:
            subprocess.call(
                [
                    "psiblast",
                    "-db",
                    blast_db,
                    "-query",
                    fasta_file,
                    "-inclusion_ethresh",
                    "0.001",
                    "-num_iterations",
                    "3",
                    "-num_threads",
                    num_threads,
                    "-out_ascii_pssm",
                    pssm_file
                ],
                stdout=null,
                stderr=null,
            )

        os.remove(fasta_file)
        print(f"Generated PSSM for protein {record.id}")
        count += 1

    print(f"Generated PSSMs for {count} proteins")
