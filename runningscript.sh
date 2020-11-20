#input_file=$1
#database_folder="/Users/iwanhidding/Internship_Helsinki_2020_2021/installed_tools/dbNSFP4.1a/"
################### Splitting input in different chromosomes and annotate using python
#grep '^#' $input_file > output_annotation/header.vcf
chromosome_list=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 "M" "X" "Y")
# chromosome_list=(17 18 19 20 21 22 "M" "X" "Y")
#for current_iteration in "${chromosome_list[@]}"
#do
#  grep -E "^(${current_iteration}[[:space:]])" "$input_file" > chromsomefile
#  python3 VcfAnnotater.py chromsomefile $database_folder "$current_iteration"
#done

#cat header.vcf chr*_annotated.vcf > annotated_output.vcf



#grep '^#' $input_file > header.vcf
chromosome_list=("chr1" "chr2" "chr3" "chr4" "chr5" "chr6" "chr7" "chr8" "chr9" "chr10" "chr11" "chr12" "chr13" "chr14" "chr15" "chr16" "chr17" "chr18" "chr19" "chr20" "chr21" "chr22" "chrX")
#for current_iteration in "${chromosome_list[@]}"
#do
#  grep -E "^(${current_iteration}[[:space:]])" "$input_file" > output_annotation/chromsomefile
#  python3 non_coding_annotator.py output_annotation/chromsomefile "$current_iteration"
#done

#cat output_annotation/header.vcf output_annotation/chr*_annotated.vcf > annotated_output.vcf

## VICTOR Annotation, change file location in text (change this to argument), also bgzip the file and tabix index.
# bash VICTOR/slurm.annotate 1>slurm.annotate.run_1.stdout 2>slurm.annotate.run_1.stderr

for current_iteration in "${chromosome_list[@]}"
do
  bedtools intersect -a ../../Internship_Helsinki_2020_2021/chr_Filtered_clinvar.vcf -b ../../Internship_Helsinki_2020_2021/installed_tools/ncER/ncER_perc_${current_iteration}_coordSorted.txt -wb >> output_annotation/non_coding_chr_out.vcf
done
### VEST


# python /Users/iwanhidding/Internship_Helsinki_2020_2021/installed_tools/VEST/VEST/RunVest VEST_input.txt -g # (for genomic coordinates)-c #classifier_name
# formatting vest

# export VESTDIR=/Users/iwanhidding/Internship_Helsinki_2020_2021/installed_tools/VEST/VEST
# export SNVBOXDIR=/Users/iwanhidding/Internship_Helsinki_2020_2021/installed_tools/VEST/SNVbox
# awk '{print $1,$2,"+", $4, $5}' out.vcf | sed 's/ /     /g' > VEST_input.txt
# awk the first 2 columns, then insert a column of + then add column 4 and 5
# could do python as well, for line in ... string split (\t) ... append(1 , 2, "+", 4, 5) but likely slow.
# chr22 25115449 + A G
# chr22 25119120 + A C
# chr22 25124311 --- C G

"""
To facilitate comparison between scores, we added rank scores for most functional prediction scores and conservation
scores, and replacing the  converted scores in the previous versions. In short, for a given type of
prediction/conservation scores, all its scores in dbNSFP were first ranked and the rankscore is the rank divided
by the total number of all its scores. Roughly speaking, the rankscore will range from 0 to 1, and the larger the score,
the higher rank the score in dbNSFP, therefore the SNP is more likely to have damaging effect.
"""


################MCAP
# zgrep chr + loc + alt / ref from the mcapv1_4 file
# M-CAP	> 0.025 pathogenic # doesnt really matter for the program. 
############# CADD
# run cadd api check

#Specify score file link
# check if this file is saved already
# SCORE_FILE=http://krishna.gs.washington.edu/download/CADD/v1.4/GRCh37/whole_genome_SNVs_inclAnno.tsv.gz
#Download Tabix Index
# INDEX=IndexFile
# wget -c $SCORE_FILE.tbi -O $INDEX
#Retrieve variant scores

# get the chr + coordinates from the input
#tabix $SCORE_FILE $INDEX 22:43451446-43451447

# then filter the right ref/alt from the output.

############### Funseq2
# another zgrep



################ other tools?




################# Combine outputs and prep for machine learning





################# Perform machine learning # although this step only once after this just analyze the variants.






################## Variant prio # this is where we can combine multiple samples, maybe positive and negative