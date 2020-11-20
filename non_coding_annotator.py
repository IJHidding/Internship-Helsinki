import argparse
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('Chromosome_file', metavar='C',
                    help='The filename containing all variants from a single chromosome')
parser.add_argument('Current_Iteration', metavar='N',
                    help='The current iteration of chromosome to select the right file')
args = parser.parse_args()
database_folder = "/Users/iwanhidding/Internship_Helsinki_2020_2021/installed_tools/ncER/"
file2 = "{}ncER_perc_{}_coordSorted.txt".format(database_folder, args.Current_Iteration)
file1 = args.Chromosome_file
output = "output_annotation/chr{}_annotated.vcf".format(args.Current_Iteration)
matching_lines = []
print("checkers, starting now")
with open(file1, 'r') as f1, open(file2, 'r') as f2:
    d1 = {tuple(i.split()[:2]): i.split()[3] for i in f2.read().split('\n')}
    print('finished loading the file')
    for i in f1.read().split('\n'):

        tmp = i.split('\t')
        if tuple(tmp[:2]) in d1:
            matching_lines.append("\t".join(tmp + d1[tuple(tmp[:2])]))


print("matching lines finished, starting the writing process.")
with open(output, 'w') as out_file:
    for item in matching_lines:
        out_file.write("%s\n" % item)

