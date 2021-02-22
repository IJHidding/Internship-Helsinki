import os
import numpy as np
# add the variant coordinate.


def get_sequence(coords, variant, ref):
    new_cords = [coords[0], str(coords[1]), str(int(coords[1]) + 1)]
    # print(new_cords)
    with open('coords.bed', 'w') as file:
        file.write("\t".join(new_cords))
    genelines = os.popen("bedtools intersect -a coords.bed -wb -b Databases/hg19.ensGene.gtf").read().split('\n')
    # print(genelines.split('\n'))
    # print(genelines)
    sequencelist = []
    for geneline in genelines:
        # print(geneline)
        if geneline != "":
            genename = geneline[-17:-2]
            # print(genename)
            # ##### // turn this into a grep just to get coords, or leave ike this as its already working
            sed_string = 'sed -n "/{genename}/,/>EN/p" Databases/Homo_sapiens.GRCh37.cds.all.fa'.format(genename=genename)
            bigtext = os.popen(sed_string).read().split("\n")
            # print(bigtext)
            if bigtext == [""]:
                pass
            else:
                # print(bigtext)
                size = len(bigtext)
                idx_list = [idx + 1 for idx, val in
                            enumerate(bigtext) if val.startswith(">")]
                # print(idx_list)
                res = [bigtext[i: j] for i, j in
                       zip([0] + idx_list, idx_list +
                       ([size] if idx_list[-1] != size else []))]
                genomic_coords_list = []
                for reslist in res:
                    # print(reslist)
                    genomic_coords = [x.split(" ")[2].split(":")[2:5] for x in reslist if x.startswith(">")]
                    # print("gnemomic coords are :", genomic_coords)
                    if genomic_coords:
                        genomic_coords_list.append(genomic_coords[0])
                    # somelist = "".join([x for x in reslist if not x.startswith(">")])
                    # print(somelist)
                    # if somelist:
                    #     sequencelist.append(somelist)
            #print(genomic_coords_list[:-1])
            variant_location_list, genelength = find_variant_location(genename, coords[1])
            # print()
            # variant_sequence = max(sequencelist, key=len)
            # print(variant_location)
            # print(ref, variant_sequence[variant_location])
            ### print([len(i) for i in sequencelist], genelength)
            sequence_database = []
            variant_sequence_database = []
            for location, genomic_coordinates in zip(variant_location_list, genomic_coords_list[:-1]):
                if location is not None:
                    location_sed_string = 'sed -n "/{genomic_location}/,/>/p" Databases/Homo_sapiens.GRCh37.cds.all.fa'.format(genomic_location=":".join(genomic_coordinates))
                    location_list_from_data = os.popen(location_sed_string).read().split("\n")
                    # the -2 at the end removes both the empty string: "" at the end
                    # and it removes the first line of the next gene in the database
                    sequence_string = "".join(location_list_from_data[1:-2])
                    sequence_database.append(sequence_string)
                    # print(sequence_string)
                    # Need to confirm this location fix.
                    variant_sequence = sequence_string[:location] + variant + sequence_string[location + 1:]
                    # print(variant_sequence)
                    variant_sequence_database.append(variant_sequence)
        break
    sequence_output = [convert_to_protein(x) for x in sequence_database]
    variant_sequence_output = [convert_to_protein(x) for x in variant_sequence_database]
    variant_location_output = [x for x in variant_location_list if x]
    return variant_location_output, sequence_output, variant_sequence_output


def convert_to_protein(sequence):
    """
    This function turns a DNA sequence into a protein sequence.
    :param sequence: A DNA sequence.
    :return: A protein sequence
    """
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

    protein_sequence = ""

        # print(dna_sequence)
    for i in range(0, len(sequence) - (3 + len(sequence) % 3), 3):
        if "N" in sequence[i:i + 3]:
            protein_sequence += "X"
        elif protein[sequence[i:i + 3]] == "STOP":
            break
        else:
            protein_sequence += protein[sequence[i:i + 3]]

    return protein_sequence


# one hot encoding of the different amino acids
def one_of_each(seq_list, size=3000):
    """
    This function encodes the protein sequences into numerical format. It then divides by 25 to transform the values to fit
    within the 0-1 range.
    :param seq_list: A list containing protein sequences in amino acid format.
    :param size: The maximum size of the protein
    :return: returns a numpy array containing all the proteins in numerical format.
    """
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
    """
    This function uses the gene id supplied to it from a bedtools command to find the genomic details of all the exons.
    It then uses this information to identify where in the coding region of the gene, the genetic variant is introduced.
    The function returns the location as a list containing the location of the variant per isoform of the protein. It
    additionally returns a list of the length of each isoform for control. This function will/should likely be expanded
    to check the start and end locations to compare with sequences gotten from another function.
    :param geneid: The ens gene gene ID
    :param location: the variant location
    :return: A list containing the location of the variant in the protein sequence, and a list of the length of the
    different isoforms.
    """
    grepstring = 'grep "{genename}" Databases/hg19.ensGene.gtf'.format(genename=geneid)
    all_lines = os.popen(grepstring).read().split("\n")[1:]
    # print(all_lines)
    genelengthlist = [None] * 20
    sequence_loc_list = [None] * 20
    # print(sequence_loc_list)
    genelength = 0
    geneversioncount = 0
    for line in all_lines:
        # check if the line isnt empty, to prevent errors.
        if line == "":
            break
        transcript_id = line.split("\t")[8].split(" ")[3][1:16]
        # print(transcript_id)
        if genelength == 0:
            pass
        else:
            if transcript_id != saved_transcript_id:
                genelengthlist[geneversioncount] = genelength
                geneversioncount += 1
                genelength = 0
                # print("next")
                # break

        exon_locations = line.split("\t")[3:5]
        if line.split("\t")[2] != "exon":
            continue
        #print(exon_locations)
        # print(exon_locations)
        if int(exon_locations[0]) <= int(location) < int(exon_locations[1]):
            sequence_loc = int(location) - int(exon_locations[0]) + int(genelength)
            # print("sequence location is :", sequence_loc)
            sequence_loc_list[geneversioncount] = sequence_loc
        else:
            genelength += int(exon_locations[1]) - int(exon_locations[0])
        saved_transcript_id = transcript_id

        # print(geneversioncount)
    #print("checkers", sequence_loc_list, genelengthlist)
    return sequence_loc_list, genelengthlist


print(get_sequence(['chr1', '874421', '874422'], 'A', 'G'))
