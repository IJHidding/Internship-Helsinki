input_file=$1
database_folder="/Users/iwanhidding/Internship_Helsinki_2020_2021/installed_tools/dbNSFP4.1a/"
################### Splitting input in different chromosomes and annotate using python
grep '^#' $input_file > header.vcf
#chromosome_list=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 "M" "X" "Y")
chromosome_list=(17 18 19 20 21 22 "M" "X" "Y")
for current_iteration in "${chromosome_list[@]}"
do
  grep -E "^(${current_iteration}[[:space:]])" "$input_file" > chromsomefile
  python3 VcfAnnotater.py chromsomefile $database_folder "$current_iteration"
done

cat header.vcf chr*_annotated.vcf > annotated_output.vcf





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