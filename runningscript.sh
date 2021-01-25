#!/bin/zsh
# VATS variant analysis tool system
inputfile=$1
echo "${inputfile}"
working_loc="/Users/iwanhidding/PycharmProjects/Internship-Helsinki/"

# save header
grep "^#" "${inputfile}" > /Users/iwanhidding/PycharmProjects/Internship-Helsinki/header.txt
#awk '{if($0 !~ /^#/) print "chr"$0; else print $0}' "${inputfile}" > with_chr.vcf
# maybe check for ^chr on the file and change if needed
# also make sure all files are created in a new directory

chr_chromosome_list=("chr1" "chr2" "chr3" "chr4" "chr5" "chr6" "chr7" "chr8" "chr9" "chr10" "chr11" "chr12" "chr13" "chr14" "chr15" "chr16" "chr17" "chr18" "chr19" "chr20" "chr21" "chr22" "chrX")

## VICTOR Annotation, change file location in text (change this to argument), also bgzip the file and tabix index.

# send the file to the cravat server for vest annotation
python3 /Users/iwanhidding/PycharmProjects/Internship-Helsinki/Cravat_put.py "$inputfile" > /Users/iwanhidding/PycharmProjects/Internship-Helsinki/jobid.txt

# prep the input file for victor annotation
bgzip -c "${inputfile}" > inputfile.vcf.gz
tabix -p vcf inputfile.vcf.gz

# while vest is running annotate locally using victor
#bash /Users/iwanhidding/Internship_Helsinki_2020_2021/installed_tools/VICTOR/slurm.annotate 1>slurm.annotate.run_1.stdout 2>slurm.annotate.run_1.stderr inputfile.vcf.gz
# add the unique thing to this.

job_id=$(cat jobid.txt)

# check if cravat is done yet or wait and receive the vest annotation
python3 /Users/iwanhidding/PycharmProjects/Internship-Helsinki/Cravat_get.py "$job_id" output_annotation/


# Unzip the victor output.
gunzip /Users/iwanhidding/PycharmProjects/Internship-Helsinki/VICTOR_annotation.ann.del.gz
( grep  '^#' /Users/iwanhidding/PycharmProjects/Internship-Helsinki/VICTOR_annotation.ann.del ; grep -v "^#" /Users/iwanhidding/PycharmProjects/Internship-Helsinki/VICTOR_annotation.ann.del | LC_ALL=C sort -t $'\t' -k1,1 -k2,2n -k4,4 | awk -F '\t' 'BEGIN{ prev="";} {key=sprintf("%s\t%s\t%s",$1,$2,$4);if(key==prev) next;print;prev=key;}' )  > tmp && mv tmp /Users/iwanhidding/PycharmProjects/Internship-Helsinki/VICTOR_annotation.ann.del

awk '{if($0 !~ /^#/) print "chr"$0; else print $0}' /Users/iwanhidding/PycharmProjects/Internship-Helsinki/VICTOR_annotation.ann.del > tmp && mv tmp /Users/iwanhidding/PycharmProjects/Internship-Helsinki/VICTOR_annotation.ann.del

# Combine all coding annotations into different files depending on which are available
python3 /Users/iwanhidding/PycharmProjects/Internship-Helsinki/clinpred\ annotater.py VICTOR_annotation.ann.del /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/"${job_id}"/Variant_Additional_Details.Result.tsv

# Non coding annotation
for current_iteration in "${chr_chromosome_list[@]}"
do
  echo "${current_iteration}"
  bedtools intersect -a /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/non_coding.txt -b /Users/iwanhidding/Internship_Helsinki_2020_2021/installed_tools/ncER/ncER_perc_"${current_iteration}"_coordSorted.txt -wb >> /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/non_coding_chr_out.vcf
done

# add the column names from the other stuff still to this
grep "^#CHR" "${inputfile}" | sed -e 's/$/  . NC_CHR  NC_POS1 NCPOS2  NC_SCORE/' > /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/headerline.txt

cat /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/headerline.txt /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/non_coding_chr_out.vcf > /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/non_coding.prediction

grep "^#CHR" "${inputfile}" | sed -e 's/$/  . VEST4 ClinPred_score/' > /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/headerline.txt

cat /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/headerline.txt /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/full.prediction > tmp && mv tmp  /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/full.prediction

grep "^#CHR" "${inputfile}" | sed -e 's/$/  . VEST4/' > /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/headerline.txt

cat /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/headerline.txt /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/vest.prediction > tmp && mv tmp /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/vest.prediction

grep "^#CHR" "${inputfile}" | sed -e 's/$/  . ClinPred_score/' > /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/headerline.txt

cat /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/headerline.txt /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/clinpred.prediction > tmp && mv tmp /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/clinpred.prediction


# Predict the effect based on the output.
# we know the output files, so no need to loop.
# just go over each one
# for file in predictioninput/*.txt;
# do
#   python3 predictor.py -i inputfile -a {full, vest, clinpred, non_coding} -o whateveroutputfileiwant.vcf/txt
# done
python3 predictor.py /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/non_coding.prediction non_coding /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/non_coding_pred.txt
python3 predictor.py /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/full.prediction full /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/full_pred.txt
python3 predictor.py /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/vest.prediction vest /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/vest_pred.txt
python3 predictor.py /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/clinpred.prediction clinpred /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/clinpred_pred.txt


# combined output and header and sort
grep -v "^#" /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/*_pred.txt | cut -d ':' -f 2- > /Users/iwanhidding/PycharmProjects/Internship-Helsinki/all_ann_variants.txt
cat /Users/iwanhidding/PycharmProjects/Internship-Helsinki/header.txt /Users/iwanhidding/PycharmProjects/Internship-Helsinki/all_ann_variants.txt | sort -k1,1V -k2,2n > /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/predicted_output.vcf

# cleanup
rm /Users/iwanhidding/PycharmProjects/Internship-Helsinki/VICTOR_annotation*
rm /Users/iwanhidding/PycharmProjects/Internship-Helsinki/slurm.annotate*
rm /Users/iwanhidding/PycharmProjects/Internship-Helsinki/output_annotation/non_coding_chr_out.vcf