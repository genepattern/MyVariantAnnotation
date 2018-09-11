#!/bin/sh
cd /home/alexw/ucsd/research/mesirov/projects/module_dev/modules/MyVariantAnnotation/src/
python MyVariantAnnotation.py -i ../data/DLBCL-mareschal.vcf -o ../data/mareschal_vcf_results.tsv -g hg19
