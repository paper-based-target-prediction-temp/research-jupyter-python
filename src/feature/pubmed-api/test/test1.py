import os
import requests
import xml.etree.ElementTree as ET
from dotenv import load_dotenv


def get_pmid_list_from_xml(xml_content):
    """
    PubMed ESearch 결과 XML 문자열에서 PMID 리스트를 추출한다.
    """
    root = ET.fromstring(xml_content)
    pmids = [elem.text for elem in root.findall(".//Id")]
    return pmids


def fetch_article_information(pmid, dest_file_name):
    """
    주어진 PMID에 해당하는 PubMed 논문 정보를 XML로 가져와 파일에 저장한다.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": pmid,
        "retmode": "xml",
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()

    with open(dest_file_name, "w", encoding="utf-8") as f:
        f.write(response.text)
    return True


def main():
    load_dotenv()
    pubmed_api_key = os.getenv("PUBMED_API_KEY")

    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    search_text = "EGFR"

    search_params = {
        "db": "pubmed",
        "term": search_text,
        "retmax": 10,
        "api_key": pubmed_api_key,
    }

    # PubMed 검색
    response = requests.get(base_url, params=search_params)
    response.raise_for_status()

    # PMID 리스트 추출
    search_pmid = get_pmid_list_from_xml(response.text)

    print("검색 결과 PMID 리스트:", search_pmid)

    # 예시: 첫 번째 PMID에 대한 정보 가져오기
    if search_pmid:
        fetch_article_information(search_pmid[0], "article_info.xml")
        print(
            f"{search_pmid[0]} PMID에 대한 정보가 'article_info.xml'에 저장되었습니다."
        )


if __name__ == "__main__":
    main()
