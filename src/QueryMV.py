"""
This module implements the API interface to MyVariant.info
"""

import json
import math
import requests
import sys

from Utils import var2str

def get_annotations(variants, genome, fields='all', 
                    url="http://myvariant.info/v1/variant"):
    """
    Returns the JSON result ofa myvariant.info query

        variants ([(str, int, str, str)]): List of variant tuples
        genome (str): Either 'hg19' or 'hg38'
        fields (str): Optional - comma-separated string of specific fields
                        to query
        url (str): API endpoint URL running the myvariant server

        returns (dict): The JSON response from myvariant.info
    """
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    params = "fields="+fields
    if genome == "hg38":
        params += "&hg38=true"
    query_res = []
    n_chunks = int(math.ceil(len(variants)/1000.0))  #myvariant limits to 1000
    for i in range(n_chunks):
        lower_bound = 1000*i
        upper_bound = min(lower_bound+1000, len(variants))
        chunk = variants[lower_bound:upper_bound]
        params += "&ids="+",".join(list(map(var2str, chunk)))
        resp = requests.post(url, params, headers=headers)
        query_res += json.loads(resp.text)
    return query_res
