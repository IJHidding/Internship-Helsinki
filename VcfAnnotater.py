import argparse
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('Chromosome_file', metavar='C',
                    help='The filename containing all variants from a single chromosome')
parser.add_argument('Database_folder', metavar='D',
                    help='The folder containing the reference database used for annotation')
parser.add_argument('Current_Iteration', metavar='N',
                    help='The current iteration of chromosome to select the right file')
args = parser.parse_args()
# databasedirectory = "/Users/iwanhidding/Internship_Helsinki_2020_2021/installed_tools/dbNSFP4.1a/"
file2 = "{}dbNSFP4.1a_variant.chr{}".format(args.Database_folder, args.Current_Iteration)
file1 = args.Chromosome_file
output = "chr{}_annotated.vcf".format(args.Current_Iteration)
matching_lines = []

with open(file1, 'r') as f1, open(file2, 'r') as f2:
    d1 = {tuple(i.split()[:2] + i.split()[3:5]): i.split()[5:] for i in f1.read().split('\n')}
    #print(f2.read().split('\n'))
    #print(tuple(i.split()[:2] + i.split()[3:5]))
    for i in f2.read().split('\n'):

        tmp = i.split('\t')
        #print(d1.values()[0])
        # print(tuple(tmp[7:9] + tmp[2:4]))
        if tuple(tmp[7:9] + tmp[2:4]) in d1:
#            print(tmp[7:9] + tmp[2:4])
#            print(d1[tuple(tmp[7:9] + tmp[2:4])][:])
#            print(tmp[:2] + tmp[4:7] + tmp[9:])
            matching_lines.append("\t".join(tmp[7:9] + tmp[2:4] + d1[tuple(tmp[7:9] + tmp[2:4])]
                                  + tmp[:2] + tmp[4:7] + tmp[9:]))


print("matching lines finished, starting the writing process.")
with open(output, 'w') as out_file:
    for item in matching_lines:
        out_file.write("%s\n" % item)

