from dotenv import load_dotenv
import requests
import os
import re
import xml.etree.ElementTree as ET
import json

load_dotenv()
"""
E-utilities
    esearch.fcgi: 특정 키워드로 DB 내 아이템(예: PMIDs) 검색
    efetch.fcgi: 검색된 ID들을 이용해 전체 레코드(예: 논문의 서지정보, 초록 등) 가져오기
    esummary.fcgi: 검색된 ID들의 요약 정보 가져오기
    elink.fcgi: 데이터베이스 간의 상호 연결된 ID들 조회(예: PMC 논문과 PubMed 레코드 연결)
    epost.fcgi: ID 리스트를 NCBI 히스토리에 저장
    egquery.fcgi: 여러 데이터베이스에 대한 검색 결과 개략적 요약
    espell.fcgi: 검색어의 철자 교정 제안
    einfo.fcgi: 데이터베이스 정보 조회
"""
e_utilites = {
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

base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
pubmed_api_key = os.getenv("PUBMED_API_KEY")
get_pmid_params = {
    "db": "pubmed",
    "term": "EGFR",
    "retmax": 1,
    "retmode": "json",
    "api_key": pubmed_api_key,
}

# # get PMID
# response = requests.get(base_url + e_utilites["esearch"], params=get_pmid_params)
# # print(response.content)
# data = json.loads(response.content)
# print(data.keys)

# pmids = data["esearchresult"]["idlist"]
# print(pmids)
# root = ET.fromstring(response.content)
# pmids = [id_elem.text for id_elem in root.findall(".//Id")]

pmids = ["39641495"]
fetch_params = {
    "db": "pubmed",
    "id": ",".join(pmids),
    "retmode": "xml",  # json 지원 안함
    "api_key": pubmed_api_key,
}
# get fetches
fetchs = requests.get(base_url + e_utilites["efetch"], params=fetch_params)
print(fetchs.content)
# data = json.loads(fetchs.content)
# print(data)
# print(fetchs.content)

# root = ET.fromstring(fetchs.content)
# # 제목 추출
# title = root.find(".//ArticleTitle").text

# # 초록 추출 (AbstractText 태그)
# abstract_parts = root.findall(".//AbstractText")
# abstract = " ".join([part.text for part in abstract_parts if part.text])

# print(f"PMID: {pmid}")
# print(f"Title: {title}")
# print(f"Abstract: {abstract}\n")


# 결과 파싱
# if response.status_code == 200:
#     root = ET.fromstring(response.content)
#     pmids = [id_elem.text for id_elem in root.findall(".//Id")]
#     print("PMIDs:", pmids)
# else:
#     print("Error:", response.status_code)


# def search_pubmed(term, retmax=10):
#     """
#     PubMed에서 검색어(term)로 논문 검색을 수행하고, PMID 리스트를 반환합니다.
#     """
#     load_dotenv()
#     pubmed_api_key = os.getenv("PUBMED_API_KEY")
#     base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
#     params = {
#         "db": "pubmed",
#         "term": term,
#         "retmax": retmax,
#         "retmode": "xml",
#         "api_key": pubmed_api_key,
#     }
#     response = requests.get(base_url, params=params)
#     response.raise_for_status()

#     root = ET.fromstring(response.text)
#     id_list = [elem.text for elem in root.findall(".//IdList/Id")]
#     return id_list


# def fetch_summaries(pmid_list):
#     """
#     PMID 리스트를 바탕으로 esummary를 통해 논문 요약정보를 가져와
#     (PMID, 제목, 저널명) 형태의 튜플 리스트를 반환합니다.
#     """
#     load_dotenv()
#     pubmed_api_key = os.getenv("PUBMED_API_KEY")
#     base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
#     params = {
#         "db": "pubmed",
#         "id": ",".join(pmid_list),
#         "retmode": "xml",
#         "api_key": pubmed_api_key,
#     }
#     response = requests.get(base_url, params=params)
#     response.raise_for_status()

#     root = ET.fromstring(response.text)
#     records = []
#     for docsum in root.findall(".//DocSum"):
#         pmid = docsum.find("./Id").text
#         title = None
#         journal = None
#         for item in docsum.findall("./Item"):
#             if item.get("Name") == "Title":
#                 title = item.text
#             elif item.get("Name") == "FullJournalName":
#                 journal = item.text

#         records.append((pmid, title, journal))
#     return records


# if __name__ == "__main__":
#     # 예: 'cancer'라는 키워드로 상위 10개 논문 검색
#     pmids = search_pubmed("EGFR", retmax=10)
#     print("Found PMIDs:", pmids)

#     # PMID 기반으로 요약정보 가져오기
#     summaries = fetch_summaries(pmids)
#     for pmid, title, journal in summaries:
#         print("PMID:", pmid)
#         print("Title:", title)
#         print("Journal:", journal)
#         print("-----")
