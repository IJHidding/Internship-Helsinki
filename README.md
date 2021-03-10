# Variant Prioritisation Tool Setup
The variant prioritisation tool setup (VPTS) is a tool designed for in-house use for the University of Helsinki. The tool has been made available and can be used by anyone, but the setup might be a difficult process. 
The tool consists of 2 parts. The first part, callable from the GUI or by running the script directly consists of the runningscript.sh script. This script takes a single vcf file and predicts a pathogenicity score for each variant. This is done by using multiple random forest models to cover most possible variants.


## Installation
To install the pipeline, install all of the dependencies listed below, and add where possible these programs to path. Follow the VICTOR installation path from their website and then
patch the slurm.annotate script using the one in this directory.

Add all files in a directory and create a subdirectory in that folder called: output_annotation


## Dependencies
- Tabix
- Bgzip
- Bash
- Python3
    - Keras
    - Tensorflow
    - Numpy
    - Pandas
    - Bokeh
    - SKlearn
- Bedtools
- VICTOR
- ncER database


## Running the tool
If on mac OS or linux the tool can be run completely from the GUI.py script. On windows only the visualisation of the results is possible.
It is recommended to run the command line options of this tool on a calculation cluster as they can be computationally intense. 

The most simple option to run the tool is running
- sh runningscript your_vcf.vcf

This will output a file in the output annotation folder. The vcf file run is required to be in the same directory.

Loading this output file into the GUI allows running the protein analysis using the button in the GUI. 
This is a very slow annotation. Recommended to keep the number of variants very low. 