"""
This script contains utilities for processing data
before/after annotation
"""

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
