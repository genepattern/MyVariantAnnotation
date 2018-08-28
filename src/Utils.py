"""
This script contains utilities for processing data
before/after annotation
"""

import numpy as np
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

def parse_dict(d):
    """
    Given a single layer dictionary d, return a string representation
    of the form "key1=val1,key2=val2,..."

        d (dict): Any dictionary, preferrably with no nesting

        returns (str): String represenation of d described above
    """
    return ",".join([str(key)+"="+str(value) for key, value in d.iteritems()])

def parse_dict_list(dl):
    """
    Returns the string representation of a list of dictionaries in
    the form "key1=val1,key2=val2|key1=val2,..."

        dl ([dict]): List of dictionaries

        returns (str): String representation of dl described above
    """
    return "|".join([parse_dict(d) for d in dl])

def is_list_of_dict(l):
    """
    Checks if a list is entirely composed of dictionaries

        l ([]): List of any type

        returns (bool): True if l is entirely composed of dicts
    """
    return all(type(x) == dict for x in l)

def parse_lists(elem):
    """
    Takes a single element from a column in a json_normalize()
    result and parse the element if it is a list of values or
    a list of dictionaries. List of dictionaries are converted
    to strings of the form "key1=val1,key2=val2|..." and all other
    lists are converted to "val1|val2|...". Non-list elements are
    left unchanged.

        elem (any): Column value from a json_normalize() call

        returns (str): Parsed version of the element
    """
    if type(elem) == list:
        if is_list_of_dict(elem):
            return parse_dict_list(elem)
        else:
            return "|".join(list(map(str, elem)))
    elif pd.isnull(elem):
        return elem
    else:
        return str(elem)

def json2df(jd):
    """
    Takes a JSON object and calls json_normalize. Remaining list elements
    are converted to comma-separated strings
    """
    df = pd.io.json.json_normalize(jd)
    for col in df.columns:
        df[col] = df[col].apply(parse_lists)
    ## dbnsfp parsing steps
    for i, row in df.iterrows():
        if not pd.isnull(row['dbnsfp.aa']):
            row['dbnsfp.aa.refcodon'] = '|'.join([rc.split('=')[-1] 
                                                    for rc in row['dbnsfp.aa'].split('|')])
    return df[df.columns[::-1]]

"""
Read Input
"""

def load_variants(path):
    """
    Loads a list of tuples of variants from a path. Variants
    should come from a tab-separated file with at minimum column
    headers "chromosome", "position", "reference", "alternate"

        path (str): The path to a variant input file

        return ([(str, str, str, str)]): The variant tuples
    """
    variants = []
    df = pd.read_csv(path, sep='\t')
    for i, row in df.iterrows():
        variants.append((row['chromosome'], str(row['position']), row['reference'], row['alternate']))
    return variants
