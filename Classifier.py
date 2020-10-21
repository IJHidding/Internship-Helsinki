import sklearn
import pandas as pd


# read in vcf format, kick out header
inputfile = pd.read_csv("annotated_output.vcf", header=None, sep="\t", skiprows=6)

#print(inputfile.head())
# Checking the different columns used.
# add a way to add column names to the dataframe, by reading in the original files?



# set target variable as # info
target = ["INFO"]

# one hot encoding

# build random forest ?

# Test/train split

# train classifier

# test classifier


