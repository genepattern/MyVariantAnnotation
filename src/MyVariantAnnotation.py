"""
The driver file for MyVariantAnnotation
"""

import argparse
import os
import pandas as pd
import sys

import QueryMV as QueryMV
import Utils as Utils


### Build arguments parser
parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", type=str, 
                    help="variant input file")

parser.add_argument("-o", "--output", type=str,
                    help="annotation output file")

parser.add_argument("-f", "--fields", type=str, 
                    help="comma-separated list of additional query fields",
                    default="none")

parser.add_argument("-g", "--genome", type=str,
                    help="hg19 or hg38 (default is hg19)",
                    default="hg19")

parser.add_argument("-u", "--url", type=str,
                    help="URL for the MyVariant service",
                    default="http://myvariant.info/v1/variant")

args = parser.parse_args()


pwd = os.path.dirname(os.path.realpath(__file__))+"/"

### Check that user chose a valid genome build
### myvariant.info only accepts hg19 or hg38
if args.genome not in ["hg19", "hg38"]:
    sys.exit("ERROR: Invalid genome build - please choose hg19 or hg38")

### Load the variants from the input file
variants = Utils.load_variants(args.input)

### Default Fields
fields = ",".join([
    line.strip('\n') for line in open(pwd+"dbnsfp_cols.txt").readlines()
])

if args.fields != "none":
    fields += ","+args.fields

### Query variants
query_res = QueryMV.get_annotations(variants, args.genome,
                                    url=args.url, fields=fields)

### Parse to DataFrame
query_df = Utils.json2df(query_res)

### Re-arrange columns
cols_ordered = [line.strip('\n') for line in open(pwd+"dbnsfp_col_order.txt").readlines()]
query_df = query_df[cols_ordered]

### Write results to output
query_df.to_csv(args.output, index=False, sep='\t')
