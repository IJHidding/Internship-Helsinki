#import pandas as pd
import argparse
parser = argparse.ArgumentParser(description='Loading files')
parser.add_argument('tupleoffiles',
                    help='The tuple of files for haplotype analysis')
parser.add_argument('haplonumber',
                    help='The number of matching variants to count for the analysis')
args = parser.parse_args()
saved_lines = {}

for file in str(args.tupleoffiles).replace('(', '').replace(')', '').replace(' ', '').split(','):
    print(file)
    with open(file) as f:
        for line in f:
            #print(line)
            #line = line.split("\t")[:5]
            if tuple(line) in saved_lines:
                #print(" doubles")
                saved_lines[tuple(line)] += 1
            else:
                saved_lines.update({tuple(line): 1})


haplolines = []
for line, count in saved_lines.items():
    #print(count)
    if int(count) >= int(args.haplonumber):
        haplolines.append(line)

print("finished, writing ", len(haplolines))
with open('haplofile.vcf', 'w') as out_file:
    for item in haplolines:
        out_file.write("{}\n".format(item))
