#!/bin/bash

# Script to concatenate all the esp txt files, previously separated by
# chromosome, into one file, with just one header line, arbitrarily taken
# the chr 1 file. This header line just names the columns.
# Assumes the file names will match those of the initial download from
# Feb 25, 2015 (ex ESP6500SI-V2-SSA137.GRCh38-liftover.chrY.snps_indels.txt)
# To merge vcf format, probably use vcftools merge TODO

# Arg 1: directory of esp files
# Arg 2: destination file (ex all_chr_snps_indels.txt)
# Arg 3: specify which mutations to keep. Options are "p" (for protein
#        changes). OPTIONAL. (more options TODO)

# sample usage:
#   ./concatESPtxt.sh ./esp_dl ./esp_dl/all_chr_snps_indels.txt p

###################################################################
## Change this to modify expected file name
# ex ESP6500SI-V2-SSA137.GRCh38-liftover.chrY.snps_indels.txt
filePrefix="$1""/ESP6500SI-V2-SSA137.GRCh38-liftover.chr"
fileSuffix=".snps_indels.txt"
###################################################################

all_chr="$2" # merged ESP files
chr_list=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10" "11" "12" "13" "14" "15" "16" "17" "18" "19" "20" "21" "22" "X" "Y")

# get one header line from first file (assumes it's line 8)
head -n 8 "$filePrefix""1""$fileSuffix" | tail -n 1 > $all_chr

for chr in ${chr_list[@]} ; do
  currFile="$filePrefix""$chr""$fileSuffix" 

  # chr X and Y have a different number of lines in the headers
  if [[ $chr == "X" || $chr == "Y" ]] ; then
    tail -n +7 $currFile >> $all_chr
  else
    tail -n +9 $currFile >> $all_chr
  fi
done

# if keeping only protein changes
if [[ "$3" == "p" ]] ; then
  # keep header line
  head -n 1 $all_chr > tmp

  # grep for protein AA changes. format is "p.(<ref><pos><alt>)
  grep -E "p\.\(" $all_chr >> tmp 
  mv tmp $all_chr
fi
