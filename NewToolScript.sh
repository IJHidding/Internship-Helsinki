#!/usr/bin/env bash
victor_path="path/to/victor"
input_file=$1


#python VICTOR input_file
bash ${victor_path}VICTOR/slurm.annotate 1>slurm.annotate.run_1.stdout 2>slurm.annotate.run_1.stderr

python vestannotation input_file
python clinpredannotater.py victor_file
python predictorscript.py

