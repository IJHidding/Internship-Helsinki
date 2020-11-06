import sklearn
import pandas as pd

import pymysql
pymysql.install_as_MySQLdb()
#import gobbledigook

# read in vcf format, kick out header
#inputfile = pd.read_csv("annotated_output.vcf", header=None, sep="\t", skiprows=6)

#print(inputfile.head())
# Checking the different columns used.
# add a way to add column names to the dataframe, by reading in the original files?

#columnnames = pd.read_csv("original file", header=0, sep='\t').columns
#columnnames_part2 = pd.read_csv("databasefile", header=0, sep='\t').columns
#tmp[7:9] + tmp[2:4] + d1[tuple(tmp[7:9] + tmp[2:4])] + tmp[:2] + tmp[4:7] + tmp[9:]
#inputfile.columns =columnnames

# set target variable as # info
# target = ["INFO"]

# one hot encoding

# build random forest ?

# Test/train split

# train classifier

# test classifier


