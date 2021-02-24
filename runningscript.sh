#!/bin/zsh
# This is the pipeline for variant analysis as part of the VPTS program.
# This program will run from the GUI on mac OSX and linux. For use of this program on windows, this script has to be
# run from the command line on a unix server. The output file can then be used on mac OSX, linux or windows from the GUI
# to analyse protein structure.

inputfile=$1
echo "${inputfile}"

# save header
grep "^#" "${inputfile}" > header.txt
#awk '{if($0 !~ /^#/) print "chr"$0; else print $0}' "${inputfile}" > with_chr.vcf
# maybe check for ^chr on the file and change if needed
# also make sure all files are created in a new directory

chr_chromosome_list=("chr1" "chr2" "chr3" "chr4" "chr5" "chr6" "chr7" "chr8" "chr9" "chr10" "chr11" "chr12" "chr13" "chr14" "chr15" "chr16" "chr17" "chr18" "chr19" "chr20" "chr21" "chr22" "chrX")

## VICTOR Annotation, change file location in text (change this to argument), also bgzip the file and tabix index.

# send the file to the cravat server for vest annotation
python3 Cravat_put.py "$inputfile" > jobid.txt

# prep the input file for victor annotation
bgzip -c "${inputfile}" > inputfile.vcf.gz
tabix -p vcf inputfile.vcf.gz

# while vest is running annotate locally using victor
# $pathtovictor
bash /Users/iwanhidding/Internship_Helsinki_2020_2021/installed_tools/VICTOR/slurm.annotate 1>slurm.annotate.run_1.stdout 2>slurm.annotate.run_1.stderr inputfile.vcf.gz
# add the unique thing to this.

job_id=$(cat jobid.txt)

# check if cravat is done yet or wait and receive the vest annotation
python3 Cravat_get.py "$job_id" output_annotation/


# Unzip the victor output.
gunzip VICTOR_annotation.ann.del.gz

# this line grabs only one variant as the VICTOR tool annotated the variant per isoform of the protein
( grep  '^#' VICTOR_annotation.ann.del ; grep -v "^#" VICTOR_annotation.ann.del | LC_ALL=C sort -t $'\t' -k1,1 -k2,2n -k4,4 | awk -F '\t' 'BEGIN{ prev="";} {key=sprintf("%s\t%s\t%s",$1,$2,$4);if(key==prev) next;print;prev=key;}' )  > tmp && mv tmp VICTOR_annotation.ann.del

awk '{if($0 !~ /^#/) print "chr"$0; else print $0}' VICTOR_annotation.ann.del > tmp && mv tmp VICTOR_annotation.ann.del

# Combine all coding annotations into different files depending on which are available # fix the other excel option
python3 clinpred\ annotater.py VICTOR_annotation.ann.del output_annotation/"${job_id}"/Variant_Additional_Details.Result.tsv

# Non coding annotation
for current_iteration in "${chr_chromosome_list[@]}"
do
  echo "${current_iteration}"
  bedtools intersect -a output_annotation/non_coding.txt -b /Users/iwanhidding/Internship_Helsinki_2020_2021/installed_tools/ncER/ncER_perc_"${current_iteration}"_coordSorted.txt -wb >> output_annotation/non_coding_chr_out.vcf
done

# add the column names from the other stuff still to this
grep "^#CHR" "${inputfile}" | sed -e 's/$/  . NC_CHR  NC_POS1 NCPOS2  NC_SCORE/' > output_annotation/headerline.txt

cat output_annotation/headerline.txt output_annotation/non_coding_chr_out.vcf > output_annotation/non_coding.prediction

grep "^#CHR" "${inputfile}" | sed -e 's/$/  . VEST4 ClinPred_score/' > output_annotation/headerline.txt

cat output_annotation/headerline.txt output_annotation/full.prediction > tmp && mv tmp output_annotation/full.prediction

grep "^#CHR" "${inputfile}" | sed -e 's/$/  . VEST4/' > output_annotation/headerline.txt

cat output_annotation/headerline.txt output_annotation/vest.prediction > tmp && mv tmp output_annotation/vest.prediction

grep "^#CHR" "${inputfile}" | sed -e 's/$/  . ClinPred_score/' > output_annotation/headerline.txt

cat output_annotation/headerline.txt output_annotation/clinpred.prediction > tmp && mv tmp output_annotation/clinpred.prediction


# Predict the effect based on the output.
# we know the output files, so no need to loop.
# just go over each one

python3 predictor.py output_annotation/non_coding.prediction non_coding output_annotation/non_coding_pred.txt
python3 predictor.py output_annotation/full.prediction full output_annotation/full_pred.txt
python3 predictor.py output_annotation/vest.prediction vest output_annotation/vest_pred.txt
python3 predictor.py output_annotation/clinpred.prediction clinpred output_annotation/clinpred_pred.txt


# combined output and header and sort
grep -v "^#" output_annotation/*_pred.txt | cut -d ':' -f 2- > all_ann_variants.txt
cat header.txt all_ann_variants.txt | sort -k1,1V -k2,2n > output_annotation/predicted_output.vcf

# cleanup
rm VICTOR_annotation*
rm slurm.annotate*
rm output_annotation/non_coding_chr_out.vcf
rm all_ann_variants.txt
rm output_annotation/*_pred.txt
rm output_annotation/*.prediction
rm output_annotation/headerline.txt
rm inputfile.vcf.gz
rm header.txt
rm job_id.txt