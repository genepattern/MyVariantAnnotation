"""
This script contains utilities for processing data
before/after annotation
"""

import pandas as pd

"""
Variant Formatting
"""

def var2str(variant):
    """
    Takes a tuple of four strings and returns the expected format
    for a single variant for myvariant.info

        variant ((str, str, str, str)): Input variant
    """
    chrom, pos, ref, alt = variant
    if len(ref) == len(alt) == 1:
        return parse_snv(chrom, pos, ref, alt)
    elif len(ref) == 1 and len(alt) > 1:
        return parse_ins(chrom, pos, ref, alt)
    elif len(ref) > 1 and len(alt) == 1:
        return parse_del(chrom, pos, ref, alt)
    else:
        return parse_delins(chrom, pos, ref, alt)

def parse_snv(chrom, pos, ref, alt):
    return chrom+":g."+pos+ref+">"+alt

def parse_ins(chrom, pos, ref, alt):
    pos = int(pos)
    pstr = str(pos)+"_"+str(pos+len(alt)-1)
    return chrom+":g."+pstr+"ins"+alt[1:]

def parse_del(chrom, pos, ref, alt):
    pos = int(pos)
    pstr = str(pos)+"_"+str(pos+len(ref)-2)
    return chrom+":g."+pstr+"del"

def parse_delins(chrom, pos, ref, alt):
    pos = int(pos)
    pstr = str(pos)+"_"+str(pos+len(ref)-1)
    return chrom+":g."+pstr+"delins"+alt

"""
Flatten JSON
"""

def json2df(jd):
    """
    Takes a JSON object and calls json_normalize. Remaining list elements
    are converted to comma-separated strings
    """
    df = pd.io.json.json_normalize(jd)
    for col in df.columns:
        df[col] = df[col].apply(lambda x: ','.join(list(map(str, x))) if type(x) == list else x)
    return df

"""
Read Input
"""

def load_variants(path):
    """
    Loads a list of tuples of variants from a path. Variants
    should come from a tab-separated file with at minimum column
    headers "chromosome", "position", "reference", "alternate"

        path (str): The path to a variant input file

        return ([(str, str, str, st)]): The variant tuples
    """
    variants = []
    df = pd.read_csv(path, sep='\t')
    for i, row in df.iterrows():
        variants.append((row['chromosome'], str(row['position']), row['reference'], row['alternate']))
    return variants
