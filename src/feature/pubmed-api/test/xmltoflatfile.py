#! /usr/bin/python

import re


def main():
    pass


def xml2flatfile(xml_file_name, dest_file_name):
    f = open(xml_file_name)
    PMID = ""
    PubYear = ""
    PubMonth = ""
    JournalTitle = ""
    ISOAbbrev = ""
    ArticleTitle = ""
    Abstract = ""
    Affiliation = ""
    AuthorList = ""
    Volume = ""
    Page = ""
    Review = False
    passMedlineCitation = False
    passArticle = False
    passJournal = False
    passJournalIssue = False
    passPubDate = False
    passPagination = False
    passAbstract = False
    passAuthorList = False
    passPublicationTypeList = False
    w = open(dest_file_name, "w")
    for line in f:
        m = re.search("</PubmedArticle>", line)
        if m:
            w.write("PMID\t" + PMID + "\n")
            w.write("Year\t" + PubYear + "\n")
            w.write("Month\t" + PubMonth + "\n")
            w.write("JournalTitle\t" + JournalTitle + "\n")
            w.write("ISOAbbrev\t" + ISOAbbrev + "\n")
            w.write("ArticleTitle\t" + ArticleTitle + "\n")
            w.write("Abstract\t" + Abstract + "\n")
            w.write("Affiliation\t" + Affiliation + "\n")
            w.write("AuthorList\t" + AuthorList[0:-1] + "\n")
            w.write("Volume\t" + Volume + "\n")
            w.write("Page\t" + Page + "\n")
            w.write("Review\t" + str(Review) + "\n")
            w.write("//\n")
            """
			print 'PMID\t',PMID; 
			print 'Year\t',PubYear; 
			print 'Month\t',PubMonth; 
			print 'JournalTitle\t',JournalTitle; 
			print 'ISOAbbrev\t',ISOAbbrev; 
			print 'ArticleTitle\t',ArticleTitle; 
			print 'Abstract\t',Abstract; 
			print 'Affiliation\t',Affiliation; 
			print 'AuthorList\t',AuthorList[0:-1];
			print 'Volume\t',Volume; 
			print 'Page\t',Page; 
			print 'Review\t',Review; 
			print '---------------------------------------------------------';
			"""

            PMID = ""
            PubYear = ""
            PubMonth = ""
            JournalTitle = ""
            ISOAbbrev = ""
            ArticleTitle = ""
            Abstract = ""
            Affiliation = ""
            AuthorList = ""
            Volume = ""
            Page = ""
            Review = False

            continue

        m = re.search("<MedlineCitation .*?>", line)
        if m:
            passMedlineCitation = True
        m = re.search("</MedlineCitation>", line)
        if m:
            passMedlineCitation = False
        m = re.search("<Article .*?>", line)
        if m:
            passArticle = True
        m = re.search("</Article>", line)
        if m:
            passArticle = False
        m = re.search("<Journal>", line)
        if m:
            passJournal = True
        m = re.search("</Journal>", line)
        if m:
            passJournal = False
        m = re.search("<JournalIssue .*?>", line)
        if m:
            passJournalIssue = True
        m = re.search("</JournalIssue>", line)
        if m:
            passJournalIssue = False
        m = re.search("<PubDate>", line)
        if m:
            passPubDate = True
        m = re.search("</PubDate>", line)
        if m:
            passPubDate = False
        m = re.search("<Pagination>", line)
        if m:
            passPagination = True
        m = re.search("</Pagination>", line)
        if m:
            passPagination = False
        m = re.search("<Abstract>", line)
        if m:
            passAbstract = True
        m = re.search("</Abstract>", line)
        if m:
            passAbstract = False
        m = re.search("<AuthorList .*?>", line)
        if m:
            passAuthorList = True
        m = re.search("</AuthorList>", line)
        if m:
            passAuthorList = False
        m = re.search("<PublicationTypeList>", line)
        if m:
            passPublicationTypeList = True
        m = re.search("</PublicationTypeList>", line)
        if m:
            passPublicationTypeList = False

        if (
            passMedlineCitation == True
            and passJournal == True
            and passJournalIssue == True
        ):
            m = re.search("<Volume>(.*?)</Volume>", line)
            if m:
                Volume = m.group(1)
                continue

        if passMedlineCitation == True and passPubDate == False:
            m = re.search("<PMID>(.*?)</PMID>", line)
            if m:
                PMID = m.group(1)
                continue

        if (
            passMedlineCitation == True
            and passArticle == True
            and passPublicationTypeList == True
        ):
            m = re.search("<PublicationType>Review</Publication>", line)
            if m:
                Review = True
                continue

        if (
            passMedlineCitation == True
            and passArticle == True
            and passAuthorList == True
        ):
            m = re.search("</Author>", line)
            if m:
                AuthorList = AuthorList + ","
                continue
            m = re.search("<LastName>(.*?)</LastName>", line)
            if m:
                AuthorList = AuthorList + m.group(1) + " "
                continue
            m = re.search("<ForeName>(.*?)</ForeName>", line)
            if m:
                AuthorList = AuthorList + m.group(1)
                continue

        if passMedlineCitation == True and passArticle == True:
            m = re.search("<Affiliation>(.*?)</Affiliation>", line)
            if m:
                Affiliation = m.group(1)
                continue

        if passMedlineCitation == True and passArticle == True and passAbstract == True:
            m = re.search("<AbstractText>(.*?)</AbstractText>", line)
            if m:
                Abstract = m.group(1)
                continue

        if (
            passMedlineCitation == True
            and passArticle == True
            and passPagination == True
        ):
            m = re.search("<MedlinePgn>(.*?)</MedlinePgn>", line)
            if m:
                Page = m.group(1)
                continue

        if passMedlineCitation == True and passArticle == True:
            m = re.search("<ArticleTitle>(.*?)</ArticleTitle>", line)
            if m:
                ArticleTitle = m.group(1)
                continue

        if passMedlineCitation == True and passArticle == True and passJournal == True:
            m = re.search("<Title>(.*?)</Title>", line)
            if m:
                JournalTitle = m.group(1)
                continue
            m = re.search("<ISOAbbreviation>(.*?)</ISOAbbreviation>", line)
            if m:
                ISOAbbrev = m.group(1)
                continue

        if (
            passMedlineCitation == True
            and passArticle == True
            and passJournal == True
            and passJournalIssue == True
            and passPubDate == True
        ):
            m = re.search("<Year>(.*?)</Year>", line)
            if m:
                PubYear = m.group(1)
            m = re.search("<Month>(.*?)</Month>", line)
            if m:
                PubMonth = m.group(1)

    w.close()


if __name__ == "__main__":
    main()
