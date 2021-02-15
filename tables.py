import os
import numpy as np
# add the variant coordinate.


def get_sequence(coords, variant, ref):
    new_cords = [coords[0], str(coords[1]), str(int(coords[1]) + 1)]
    print(new_cords)
    with open('coords.bed', 'w') as file:
        file.write("\t".join(new_cords))
    genelines = os.popen("bedtools intersect -a coords.bed -wb -b Databases/hg19.ensGene.gtf").read().split('\n')
    # print(genelines.split('\n'))
    print(genelines)
    sequencelist = []
    for geneline in genelines:
        if geneline != "":
            genename = geneline[-17:-2]
            print(genename)
            sed_string = 'sed -n "/{genename}/,/>EN/p" Databases/Homo_sapiens.GRCh37.cds.all.fa'.format(genename=genename)
            bigtext = os.popen(sed_string).read().split("\n")
            if bigtext == [""]:
                pass
            else:
                size = len(bigtext)
                idx_list = [idx + 1 for idx, val in
                            enumerate(bigtext) if val.startswith(">")]
                #print(idx_list)
                res = [bigtext[i: j] for i, j in
                       zip([0] + idx_list, idx_list +
                       ([size] if idx_list[-1] != size else []))]

                for reslist in res:
                    somelist = "".join([x for x in reslist if not x.startswith(">")])
                    if somelist and "N" not in somelist:
                        sequencelist.append(somelist)
            variant_location = find_variant_location(genename, coords[1])
            #variant_sequence = ""
            variant_sequence = max(sequencelist, key=len)
            print(variant_location)
            if ref == variant_sequence[variant_location]:
                print("confirmed, continue")
                variant_sequence[variant_location] = variant
            else:
                print("ref doesnt match database")
    # turn into protein seq

    protein = {"TTT": "F", "CTT": "L", "ATT": "I", "GTT": "V",
               "TTC": "F", "CTC": "L", "ATC": "I", "GTC": "V",
               "TTA": "L", "CTA": "L", "ATA": "I", "GTA": "V",
               "TTG": "L", "CTG": "L", "ATG": "M", "GTG": "V",
               "TCT": "S", "CCT": "P", "ACT": "T", "GCT": "A",
               "TCC": "S", "CCC": "P", "ACC": "T", "GCC": "A",
               "TCA": "S", "CCA": "P", "ACA": "T", "GCA": "A",
               "TCG": "S", "CCG": "P", "ACG": "T", "GCG": "A",
               "TAT": "Y", "CAT": "H", "AAT": "N", "GAT": "D",
               "TAC": "Y", "CAC": "H", "AAC": "N", "GAC": "D",
               "TAA": "STOP", "CAA": "Q", "AAA": "K", "GAA": "E",
               "TAG": "STOP", "CAG": "Q", "AAG": "K", "GAG": "E",
               "TGT": "C", "CGT": "R", "AGT": "S", "GGT": "G",
               "TGC": "C", "CGC": "R", "AGC": "S", "GGC": "G",
               "TGA": "STOP", "CGA": "R", "AGA": "R", "GGA": "G",
               "TGG": "W", "CGG": "R", "AGG": "R", "GGG": "G"
               }

    proteinlist = []
    protein_sequence = ""

    if sequencelist == proteinlist:
        proteinlist.append("Not in coding region")
    # Generate protein sequence
    else:
        for dna_sequence in sequencelist:
        #print(dna_sequence)
            for i in range(0, len(dna_sequence) - (3 + len(dna_sequence) % 3), 3):
                if protein[dna_sequence[i:i + 3]] == "STOP":
                    break
                protein_sequence += protein[dna_sequence[i:i + 3]]
            proteinlist.append(protein_sequence)


    variantlist = []
    variant_output = ""

    #if variant_sequence == variantlist:
    #    variantlist.append("something is wrong...")
    # Generate protein sequence
    if sequencelist == variantlist:
        proteinlist.append("Not in coding region")
    else:
        for i in range(0, len(variant_sequence) - (3 + len(variant_sequence) % 3), 3):
            if protein[variant_sequence[i:i + 3]] == "STOP":
                break
            variant_output += protein[variant_sequence[i:i + 3]]

    return variant_location, proteinlist, variant_output


#get_sequence(['chr1', '874421', '874422'])
# one hot encoding of the different amino acids
def one_of_each(seq_list, size=3000):
    acid_code_dict = {"A": "1", "B": "2", "C": "3", "D": "4", "E": "5", "F": "6", "G": "7", "H": "8",
                      "I": "9", "J": "10", "K": "11", "L": "12", "M": "13", "N": "14", "O": "15", "P": "16",
                      "Q": "17", "R": "18", "S": "19", "T": "20", "U": "21", "V": "22", "W": "23", "X": "24",
                      "Y": "25", "Z": "26"}
    new_seq_list = []
    for seq in seq_list:
        new_acid_list = np.zeros(size)
        for acid in enumerate(seq):
            new_acid_list[acid[0]] = (int(acid_code_dict[acid[1]]) / 25)  # normalize the data?
        new_seq_list.append(new_acid_list)
    return np.asarray(new_seq_list)


def find_variant_location(geneid, location):
    grepstring = 'grep "{genename}" Databases/hg19.ensGene.gtf'.format(genename=geneid)
    all_lines = os.popen(grepstring).read().split("\n")[1:]
    print(all_lines)
    genelength = 0
    for line in all_lines:
        print(line)
        exon_locations = line.split("\t")[3:5]
        print(exon_locations)
        if int(exon_locations[0]) <= int(location) < int(exon_locations[1]):
            sequence_loc = int(location) - int(exon_locations[0]) + int(genelength)
            return sequence_loc
        else:
            genelength += int(exon_locations[1]) - int(exon_locations[0])
