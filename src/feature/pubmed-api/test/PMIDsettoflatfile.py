#! /usr/bin/python

import re
import os
import random
import string
from urllib import urlretrieve
import time
from xmltoflatfile import xml2flatfile


# -----------------------------------------------------------------------------#
# This module retrieves information from NCBI with eutils for given set of
# PMIDs and stores the information to DB.
# -----------------------------------------------------------------------------#


# -----------------------------------------------------------------------------#
# -----------------------------------------------------------------------------#
def get_temp_file_name():
    alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    file_name = ""
    for k in range(30):
        file_name = file_name + alpha[random.randrange(0, 52)]
    return file_name


# -----------------------------------------------------------------------------#
# [pmid] contains at most 50 PMID IDs.
# -----------------------------------------------------------------------------#
def get_xml_to_local_file_by_pmid(pmid, dest_file_name):
    PMIDLink = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id="
    for id in pmid:
        PMIDLink += str(id) + ","

    PMIDLink = PMIDLink.rstrip(",") + "&retmode=xml"
    urlretrieve(PMIDLink, dest_file_name)


# -----------------------------------------------------------------------------#
# [dest_file_name] contains extention.
# -----------------------------------------------------------------------------#
def PMIDset_to_flat_file(PMIDlist, dest_file_name):
    while len(PMIDlist) > 0:
        # Append file number at the end of specified dest file name.
        temp_dest_file_name = get_temp_file_name()
        # dest_file_name = '2.xml';
        # Since link made of more than 50 PMIDs can't be procesed by eutils...
        pmid_sublist = PMIDlist[0:50]
        PMIDlist[0:50] = []
        get_xml_to_local_file_by_pmid(pmid_sublist, temp_dest_file_name + ".xml")
        xml2flatfile(temp_dest_file_name + ".xml", temp_dest_file_name + ".txt")
        f = open(temp_dest_file_name + ".txt")
        content = f.readlines()
        f.close()
        w = open(dest_file_name, "a+")
        w.writelines(content)
        w.close()
        os.remove(temp_dest_file_name + ".xml")
        os.remove(temp_dest_file_name + ".txt")


def main():
    pass


if __name__ == "__main__":
    main()
