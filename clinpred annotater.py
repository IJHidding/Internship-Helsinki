import argparse
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('inputfile', type=str,
                    help='The input file for annotation')
parser.add_argument('vestfile', type=str,
                    help='The vest file for annotation')
args = parser.parse_args()
file1 = args.inputfile
output = "full_file_annotated.vcf"
matching_lines = []
clin_list = []
vest_list = []
non_coding = []
clinpred_file = "/Users/iwanhidding/Internship_Helsinki_2020_2021/installed_tools/chr_clinpred.txt"
# vest_file = "/Users/iwanhidding/Documents/i_j_hidding_20201104_025318/Variant_Additional_Details.Result.tsv"
vest_file = args.vestfile

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
        #print(len(i.split('\t')))
        if len(i.split('\t')) >= 40:
            #print()
            #print('check')
            #print(tuple(i.split('\t')[2:4] + i.split('\t')[5:7]))
            if i.split('\t')[-2] != "":
                #print(tuple(i.split('\t')[2:4] + i.split('\t')[5:7]): i.split('\t')[33])
                vest_d.update({tuple(i.split('\t')[2:4] + i.split('\t')[5:7]): i.split('\t')[-2]})
            elif i.split('\t')[-3] != "":
                vest_d.update({tuple(i.split('\t')[2:4] + i.split('\t')[5:7]): i.split('\t')[-3]})
            elif i.split('\t')[-4] != "":
                vest_d.update({tuple(i.split('\t')[2:4] + i.split('\t')[5:7]): i.split('\t')[-4]})
            elif i.split('\t')[-5] != "":
                vest_d.update({tuple(i.split('\t')[2:4] + i.split('\t')[5:7]): i.split('\t')[-5]})
            elif i.split('\t')[-6] != "":
                vest_d.update({tuple(i.split('\t')[2:4] + i.split('\t')[5:7]): i.split('\t')[-6]})
            elif i.split('\t')[-7] != "":
                vest_d.update({tuple(i.split('\t')[2:4] + i.split('\t')[5:7]): i.split('\t')[-7]})
            #else:
            #    vest_d.update({tuple(i.split('\t')[2:4] + i.split('\t')[5:7]): "."})
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
        else:
            non_coding.append("\t".join(bayes_line))
print('singlecount clin: ', singlecount_clin)
print('singlecount vest: ', singlecount_vest)
print('doublecount: ', doublecount)

print("matching lines finished, starting the writing process.")
with open('output_annotation/full.prediction', 'w') as out_file:
    for item in matching_lines:
        out_file.write("%s\n" % item)

with open('output_annotation/vest.prediction', 'w') as out_file:
    for item in vest_list:
        out_file.write("%s\n" % item)

with open('output_annotation/clinpred.prediction', 'w') as out_file:
    for item in clin_list:
        out_file.write("%s\n" % item)

with open('output_annotation/non_coding.txt', 'w') as out_file:
    for item in non_coding:
        out_file.write("%s\n" % item)
