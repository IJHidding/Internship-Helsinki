import pandas as pd

inputfile = pd.read_csv('annotated_output.vcf', header=None, sep='\t', low_memory=False)
column_names_original = list(pd.read_csv("/Users/iwanhidding/Internship_Helsinki_2020_2021/Filtered_clinvar.vcf", header=0, sep='\t').columns)
column_names_database = list(pd.read_csv("/Users/iwanhidding/Internship_Helsinki_2020_2021/installed_tools/dbNSFP4.1a/dbNSFP4.1a_variant.chr20", header=0, sep='\t', low_memory=False).columns)
#print(list(column_names_database))
#rint(list(column_names_database[7:9]))
#FILTERED CLINVAR MIGHT NOT HAVE A HEADER
column_names = column_names_database[7:9] + column_names_database[2:4] + column_names_original[5:] + \
               column_names_database[:2] + column_names_database[4:7] + column_names_database[9:]
inputfile.columns = column_names
print(column_names)

inputfile.to_csv("Annotated_file_with_header.txt", sep='\t', index=False)
