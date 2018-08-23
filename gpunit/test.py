"""
This isn't a gpunit

TODO: Replace this script with real gpunits when I figure out how they work
"""


"""
Utils
"""

import src.Utils as Utils

assert(Utils.var2str(("chr1", "35366", "C", "T")) == "chr1:g.35366C>T")
assert(Utils.var2str(("chr2", "17142", "C", "CA")) == "chr2:g.17142_17143insA")
assert(Utils.var2str(("chrMT", "8271", "CACTGTGTAT", "C")) == "chrMT:g.8271_8279del")
assert(Utils.var2str(("chrX", "14112", "CAGTGC", "TG")) == "chrX:g.14112_14117delinsTG")

"""
Query
"""

#import src.QueryMV as QueryMV

#variants = [("chr16", "28883241", "A", "G")]
#genome = "hg19"
#fields = "all"
#url = "http://myvariant.info/v1/variant"

#QueryMV.get_annotations(variants, genome, fields=fields, url=url) 
