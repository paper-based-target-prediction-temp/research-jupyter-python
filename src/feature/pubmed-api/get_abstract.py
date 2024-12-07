from dotenv import load_dotenv
import requests
import os
import xml.etree.ElementTree as ET
import time
from src.core.mongodb import db as mongo_db
from src.core.config import settings


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

    def batch_fetch_and_store(
        self, term, retmax, batch_size, collection_name="pubmed_articles"
    ):
        """
        Fetch a large number of PMIDs for the given term and store details in MongoDB in batches.
        """
        print(f"Searching for PMIDs with term: {term}")
        pmids = self.search_ids(term, retmax=retmax)
        print(f"Found {len(pmids)} PMIDs")
        print(f"Fetching and storing details for {len(pmids)} PMIDs")
        # Split into chunks of batch_size
        for i in range(0, len(pmids), batch_size):
            chunk = pmids[i : i + batch_size]
            details = self.fetch_details(chunk)
            if details:
                # Insert into MongoDB
                collection = mongo_db.get_collection(collection_name)
                collection.insert_many(details)  # list로 db에 한번에 저장
                print(f"Inserted {len(details)} documents into {collection_name}")


def main_get_abstract():
    load_dotenv()
    pubmed_api_key = os.getenv("PUBMED_API_KEY")
    pubmed = PubMedAPI(api_key=pubmed_api_key)

    # Step 1: Search for PMIDs
    term = "EGFR"
    pmids = pubmed.search_ids(term=term, retmax=3)
    print(f"PMIDs: {pmids}")

    # Step 2: Fetch details for the PMIDs
    details = pubmed.fetch_details(pmids)
    for detail in details:
        print(detail)


def main_save_abstract():
    # .env 등에 저장된 PUBMED_API_KEY를 불러와 사용한다고 가정
    api_key = settings.PUBMED_API_KEY
    term = "EGFR"  # 검색어 예시
    retmax = 20
    batch_size = 10
    collection_name = "pubmed_articles"

    pubmed_api = PubMedAPI(api_key=api_key)
    pubmed_api.batch_fetch_and_store(
        term, retmax=retmax, batch_size=batch_size, collection_name=collection_name
    )


if __name__ == "__main__":
    main_save_abstract()
