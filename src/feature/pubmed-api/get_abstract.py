from dotenv import load_dotenv
import requests
import os
import xml.etree.ElementTree as ET
import time


class PubMedAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        self.e_utilites = {
            "einfo": "einfo.fcgi",
            "esearch": "esearch.fcgi",
            "epost": "epost.fcgi",
            "esummary": "esummary.fcgi",
            "efetch": "efetch.fcgi",
            "elink": "elink.fcgi",
            "egquery": "egquery.fcgi",
            "espell": "espell.fcgi",
            "eutils": "eutils.fcgi",
        }

    def search_ids(self, term, db="pubmed", retmax=10):
        """
        Use esearch to fetch a list of PubMed IDs based on a search term.
        """
        search_url = self.base_url + self.e_utilites["esearch"]
        params = {
            "db": db,
            "term": term.replace(" ", "%20"),
            "retmode": "json",
            "retmax": retmax,
            "api_key": self.api_key,
        }
        time.sleep(1)
        response = requests.get(search_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data["esearchresult"].get("idlist", [])
        else:
            print(f"Error fetching IDs: {response.status_code}")
            return []

    def fetch_details(self, pmid_list, db="pubmed"):
        """
        Use efetch to retrieve detailed information for a list of PMIDs.
        """
        fetch_url = self.base_url + self.e_utilites["efetch"]
        params = {
            "db": db,
            "id": ",".join(pmid_list),
            "retmode": "xml",
            "api_key": self.api_key,
        }
        time.sleep(1)
        response = requests.get(fetch_url, params=params)
        if response.status_code == 200:
            return self.parse_xml(response.content)
        else:
            print(f"Error fetching details: {response.status_code}")
            return []

    def parse_xml(self, xml_content, include_authors=False):
        """
        Parse XML response to extract required information.

        Parameters:
            xml_content (str): XML content to parse.
            include_authors (bool): Whether to include authors in the result.

        Returns:
            list: A list of dictionaries containing the parsed information.
        """
        root = ET.fromstring(xml_content)
        results = []
        for article in root.findall(".//PubmedArticle"):
            # Get PMID
            pmid = article.find(".//PMID").text
            # Get Title
            title = (
                article.find(".//ArticleTitle").text
                if article.find(".//ArticleTitle") is not None
                else "N/A"
            )
            # Get Abstract
            abstract_parts = article.findall(".//AbstractText")
            abstract = (
                " ".join([part.text for part in abstract_parts if part.text])
                if abstract_parts
                else "N/A"
            )
            # Get Accepted Date
            accepted_date = article.find(".//PubMedPubDate[@PubStatus='accepted']")
            accepted_date_str = (
                f"{accepted_date.find('Year').text}-{accepted_date.find('Month').text}-{accepted_date.find('Day').text}"
                if accepted_date is not None
                else "N/A"
            )

            # Get Authors if include_authors=True
            authors_list = None
            if include_authors:
                authors_list = [
                    f"{author.find('LastName').text}, {author.find('ForeName').text}"
                    for author in article.findall(".//Author")
                    if author.find("LastName") is not None
                    and author.find("ForeName") is not None
                ]

            # Append result
            results.append(
                {
                    "pmid": pmid,
                    "title": title,
                    "abstract": abstract,
                    "accepted_date": accepted_date_str,
                    "authors": authors_list,  # Add authors list if included
                }
            )
        return results


def main():
    load_dotenv()
    pubmed_api_key = os.getenv("PUBMED_API_KEY")
    pubmed = PubMedAPI(api_key=pubmed_api_key)

    # Step 1: Search for PMIDs
    search_term = "EGFR"
    pmids = pubmed.search_ids(term=search_term, retmax=3)
    print(f"PMIDs: {pmids}")

    # Step 2: Fetch details for the PMIDs
    details = pubmed.fetch_details(pmids)
    for detail in details:
        print(detail)


# Example usage
if __name__ == "__main__":
    main()
