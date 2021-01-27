import os


def get_sequence(coords):
    with open('coords.bed', 'w') as file:
        file.write(coords)
    genelines = os.popen("bedtools intersect -a coords.bed -wb -b Databases/hg19.ensGene.gtf").read().split('\n')
    # print(genelines.split('\n'))
    for geneline in genelines:
        if geneline != "":
            genename = geneline[-17:-2]
    sed_string = 'sed -n "/{genename}/,/>EN/p" Databases/Homo_sapiens.GRCh37.cds.all.fa'.format(genename=genename)
    bigtext = os.popen(sed_string).read().split("\n")

    size = len(bigtext)
    idx_list = [idx + 1 for idx, val in
                enumerate(bigtext) if val.startswith(">")]

    res = [bigtext[i: j] for i, j in
           zip([0] + idx_list, idx_list +
               ([size] if idx_list[-1] != size else []))]

    sequencelist = []
    for reslist in res:
        somelist = "".join([x for x in reslist if not x.startswith(">")])
        if somelist and "N" not in somelist:
            sequencelist.append(somelist)

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

    # Generate protein sequence
    for dna_sequence in sequencelist:
        #print(dna_sequence)
        for i in range(0, len(dna_sequence) - (3 + len(dna_sequence) % 3), 3):
            if protein[dna_sequence[i:i + 3]] == "STOP":
                break
            protein_sequence += protein[dna_sequence[i:i + 3]]
        proteinlist.append(protein_sequence)

    # print(proteinlist)
    return proteinlist


get_sequence("\t".join(['chr1', '874421', '874422']))
