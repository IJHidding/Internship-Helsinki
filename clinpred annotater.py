import argparse
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('inputfile', metavar='i',
                    help='The input file for annotation')
args = parser.parse_args()
file1 = args.inputfile
output = "full_file_annotated.vcf"
matching_lines = []

clinpred_file = "/Users/iwanhidding/Internship_Helsinki_2020_2021/installed_tools/chr_clinpred.txt"
vest_file = "/Users/iwanhidding/Documents/i_j_hidding_20201104_025318/Variant.Result.tsv"

# samesees with the non coding variants, unsure what to do with the p-value and FDR.
with open(file1, 'r') as bayes, open(clinpred_file, 'r') as clin, open(vest_file, 'r') as vest:
    clin_d = {}
    for i in clin.read().split('\n'):
        if len(i.split('\t')) == 4:
            clin_d.update({tuple(i.split()[:4]): i.split()[4]})
        #print(i)
    #print([i for i in clin.read().split('\n')])
    #clin_d = {tuple(i.split()[:4]): i.split()[4] for i in clin.read().split('\n')}
    print('clincheck')
    vest_d = {}
    for i in vest.read().split('\n'):
        #print(len(i.split('\t')))
        if len(i.split('\t')) > 43:
            # print(len(i.split('\t')))
            if i.split('\t')[43] != "":
            #print(i.split('\t')[43])
                vest_d.update({tuple(i.split('\t')[:2] + i.split('\t')[3:5]): i.split('\t')[43]})
    #vest_d = {tuple(i.split()[:2] + i.split()[3:5]): i.split()[43] for i in vest.read().split('\n')}
    print('vestcheck')
    for i in bayes.read().split('\n'):

        bayes_line = i.split('\t')
        if tuple(bayes_line[:2] + bayes_line[3:5]) in clin_d:
            matching_lines.append("\t".join([bayes_line] + clin_d[tuple(bayes_line[:4])]))
        elif tuple(bayes_line[:4]) in vest_d:
            matching_lines.append("\t".join([bayes_line] + vest_d[tuple(bayes_line[:4])]))
        else:
            matching_lines.append("\t".join(bayes_line))
## add a if clin and vest.

print("matching lines finished, starting the writing process.")
with open(output, 'w') as out_file:
    for item in matching_lines:
        out_file.write("%s\n" % item)
