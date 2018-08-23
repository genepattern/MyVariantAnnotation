"""
This module implements the API interface to MyVariant.info
"""

import json
import requests
import sys

from src.Utils import var2str

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
    params = ""
    params += "ids="+",".join(list(map(var2str, variants)))
    params += "&fields="+fields
    if genome == "hg38":
        params += "&hg38=true"
    resp = requests.post(url, params, headers=headers)
    return json.loads(resp.text)
