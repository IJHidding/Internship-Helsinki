import argparse
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('inputfile', metavar='i',
                    help='The input file for annotation')
args = parser.parse_args()
file1 = args.inputfile
output = "full_file_annotated.vcf"
matching_lines = []
clin_list = []
vest_list = []
clinpred_file = "/Users/iwanhidding/Internship_Helsinki_2020_2021/installed_tools/chr_clinpred.txt"
vest_file = "/Users/iwanhidding/Documents/i_j_hidding_20201104_025318/Variant_Additional_Details.Result.tsv"


with open(file1, 'r') as bayes, open(clinpred_file, 'r') as clin, open(vest_file, 'r') as vest:
    clin_d = {}
    for i in clin.read().split('\n'):
        if len(i.split('\t')) == 5:
            clin_d.update({tuple(i.split()[:4]): i.split()[4]})
    print('clincheck')
    vest_d = {}
    #count = 0
    for i in vest.read().split('\n'):

        #print(i.split('\t'))
        #print()
        #count += 1
        #if count == 15:
        #    exit()
        if len(i.split('\t')) == 40:
            #print('check')
            #print(tuple(i.split('\t')[2:4] + i.split('\t')[5:7]))
            if i.split('\t')[33] != "":
                vest_d.update({tuple(i.split('\t')[2:4] + i.split('\t')[5:7]): i.split('\t')[33]})
            elif i.split('\t')[34] != "":
                vest_d.update({tuple(i.split('\t')[2:4] + i.split('\t')[5:7]): i.split('\t')[34]})
            elif i.split('\t')[35] != "":
                vest_d.update({tuple(i.split('\t')[2:4] + i.split('\t')[5:7]): i.split('\t')[35]})
            elif i.split('\t')[36] != "":
                vest_d.update({tuple(i.split('\t')[2:4] + i.split('\t')[5:7]): i.split('\t')[36]})
            elif i.split('\t')[37] != "":
                vest_d.update({tuple(i.split('\t')[2:4] + i.split('\t')[5:7]): i.split('\t')[37]})
            elif i.split('\t')[38] != "":
                vest_d.update({tuple(i.split('\t')[2:4] + i.split('\t')[5:7]): i.split('\t')[38]})
            else:
                vest_d.update({tuple(i.split('\t')[2:4] + i.split('\t')[5:7]): "."})
    print('vestcheck')
    #nonc_vest_d = {}
    #for i in nonc_vest.read().split('\n'):
    #    if len(i.split('\t')) > 43:
    #        if i.split('\t')[43] != "":
    #            nonc_vest_d.update({tuple(i.split('\t')[2:4] + i.split('\t')[5:7]): i.split('\t')[43]})
    print('nonc_vest check')
    doublecount = 0
    singlecount_vest = 0
    singlecount_clin = 0
    for i in bayes.read().split('\n'):
        bayes_line = i.split('\t')
        #print(tuple(bayes_line[:2] + bayes_line[3:5]))
        #print(tuple(bayes_line[:2] + bayes_line[3:5]))
        if tuple(bayes_line[:2] + bayes_line[3:5]) in clin_d and tuple(bayes_line[:2] + bayes_line[3:5]) in vest_d:

            #print('bothcheck')
            matching_lines.append("\t".join(bayes_line + [clin_d[tuple(bayes_line[:2] + bayes_line[3:5])]]
                                            + [vest_d[tuple(bayes_line[:2] + bayes_line[3:5])]]))
            doublecount += 1
        #elif tuple(bayes_line[:2] + bayes_line[3:5]) in clin_d and tuple(bayes_line[:2] + bayes_line[3:5]) in nonc_vest_d:
        #    #rint('bothcheck -2')
        #    matching_lines.append("\t".join(bayes_line + [clin_d[tuple(bayes_line[:2] + bayes_line[3:5])]]
        #                                    + [nonc_vest_d[tuple(bayes_line[:2] + bayes_line[3:5])]]))
        #    doublecount += 1
        elif tuple(bayes_line[:2] + bayes_line[3:5]) in clin_d:
            #print('singlecheck')
            clin_list.append("\t".join(bayes_line + [clin_d[tuple(bayes_line[:2] + bayes_line[3:5])]]))
            singlecount_clin += 1
        elif tuple(bayes_line[:2] + bayes_line[3:5]) in vest_d:
            #print('singlecheck')

            vest_list.append("\t".join(bayes_line + [vest_d[tuple(bayes_line[:2] + bayes_line[3:5])]]))
            singlecount_vest += 1
        #elif tuple(bayes_line[:2] + bayes_line[3:5]) in nonc_vest_d:
        #
        #    matching_lines.append("\t".join(bayes_line + ['.'] + [nonc_vest_d[tuple(bayes_line[:2] + bayes_line[3:5])]]))
        #    singlecount += 1
        #elif tuple(bayes_line[:2]) in nc_dict:
        #    nc_lines.append("\t".join(bayes_line + nc_dict[tuple(bayes_line[:2])]))
        #else:
            #matching_lines.append("\t".join(bayes_line + ['.'] + ['.']))
print('singlecount clin: ', singlecount_clin)
print('singlecount vest: ', singlecount_vest)
print('doublecount: ', doublecount)

print("matching lines finished, starting the writing process.")
with open('fullmatchingfile.txt', 'w') as out_file:
    for item in matching_lines:
        out_file.write("%s\n" % item)

with open('Vestmatchingfile.txt', 'w') as out_file:
    for item in vest_list:
        out_file.write("%s\n" % item)

with open('clinmatchingfile.txt', 'w') as out_file:
    for item in clin_list:
        out_file.write("%s\n" % item)
