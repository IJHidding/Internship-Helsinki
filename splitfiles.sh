#!/bin/zsh
# a quick script to separate the uniprot file.

input=$1


grep "ACT_SITE" "$input" > protein_act_site.tsv
grep "BINDING" "$input" > protein_binding.tsv
grep "DNA_BIND" "$input" > protein_dna_bind.tsv
grep "METAL" "$input" > protein_metal.tsv
