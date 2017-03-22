import re
import http.client
import requests
import os.path


def GetWebContent(url, webpage):
    connection = http.client.HTTPConnection(url)
    connection.request('GET',webpage)
    httpResponse = connection.getresponse().read()
    return httpResponse


def GetPatternUrlLink(rePattern, sourceCode):
    p = re.compile(rePattern)
    matchResults = re.findall(p, sourceCode)
    return matchResults


def LinkExisted(link, booklist):
    if link in booklist:
        return True
    else:
        return False


def DownloadPdf(pdfLink, saveLocation):
    url = pdfLink
    response = requests.get(url)
    filename = url.split('/')[-1]
    print("["+filename+"]")
    print("Downloading pdf at: " + pdfLink)
    with open(saveLocation + filename, 'wb') as f:
        f.write(response.content)

def SaveDownloadedInfo(filename, bookurl):
    with open(filename, "a") as downloadList:
        downloadList.write(bookurl+"\n")


def LoadDownloadList(filename):
    if not os.path.isfile(filename):
        os.mknod(filename)
    with open(filename,"r+") as f:
        booklist = f.readlines()
        return  booklist

if __name__=="__main__":
    pdfFolder = '/home/john/resdisk02/Ebooks/downloaded/'
    downloadedBookList = "/home/john/resdisk02/Ebooks/DownloadList.txt"
    siteMap = '/sitemap_index.xml'
    website = u'www.allitebooks.com'
    postSiteMapXmlPattern = b'<loc>http://(.*post-sitemap[^<]*)'
    bookPageLinkPattern = b'<loc>http://(www.allitebooks.com/[^<]+)'
    bookPdfLinkPattern = b'(http://file.allitebooks.com/[^"]+)'
    newbookAdded = 0
    bookList = LoadDownloadList(downloadedBookList)
    sourceCodePage = GetWebContent(website, siteMap)
    postSiteMapXmlList = GetPatternUrlLink(postSiteMapXmlPattern, sourceCodePage)
    postSiteMapXmlList.sort(reverse=True)
    for i in postSiteMapXmlList:
       postSiteMapLink = '/' + i.decode("utf-8").split('/')[1]
       #print(postSiteMapLink)
       bookListPageContent = GetWebContent(website, postSiteMapLink)
       bookListUrls = GetPatternUrlLink(bookPageLinkPattern, bookListPageContent)
       for j in bookListUrls:
           #print(j)
           #print(j.decode("utf-8"))
           if LinkExisted(j.decode("utf-8")+"\n", bookList):
               continue
           else:
               bookPagePath = '/' + j.decode("utf-8").split('/')[1] + '/'
               bookPageSource = GetWebContent(website,bookPagePath)
               bookPdfDownloadLink = GetPatternUrlLink(bookPdfLinkPattern,bookPageSource)
               for k in bookPdfDownloadLink:
                   DownloadPdf(k.decode("utf-8"), pdfFolder)
               SaveDownloadedInfo(downloadedBookList, j.decode("utf-8"))
               newbookAdded += 1
    print("Today Have " + newbookAdded + " new books added!")



