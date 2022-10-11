from bs4 import BeautifulSoup
import urllib.request
#from urllib.request import Request

seed_url = "https://www.sec.gov/news/pressreleases"

urls = [seed_url]    #queue of urls to crawl
seen = [seed_url]    #stack of urls seen so far
opened = []          #we keep track of seen urls so that we don't revisit them
contain_charges = []
text = []

maxNumUrl = 20; #set the maximum number of urls to visit
# print("Starting with url="+str(urls))
while len(urls) > 0 and len(contain_charges) < maxNumUrl:
    # DEQUEUE A URL FROM urls AND TRY TO OPEN AND READ IT
    try:
        curr_url=urls.pop(0)
        # print("num. of URLs in stack: %d " % len(urls))
        # print("Trying to access= "+curr_url)
        req = urllib.request.Request(curr_url,headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        opened.append(curr_url)

    except Exception as ex:
        print("Unable to access= "+curr_url)
        print(ex)
        continue    #skip code below

    # IF URL OPENS, CHECK WHICH URLS THE PAGE CONTAINS
    # ADD THE URLS FOUND TO THE QUEUE url AND seen
    soup = BeautifulSoup(webpage)  #creates object soup

    # o_text = soup.get_text()
    # lower_text = o_text.lower()
    # if "charges" in lower_text:
    #     contain_charges.append(curr_url)
    check_url = "https://www.sec.gov/news/press-release"
    # Put child URLs into the stack
    for tag in soup.find_all('a', href = True): #find tags with links
        childUrl = tag['href'] #extract just the link
        o_childurl = childUrl
        childUrl = urllib.parse.urljoin(seed_url, childUrl)
        
        # print("seed_url in childUrl=" + str(seed_url in childUrl))
        # print("Have we seen this childUrl=" + str(childUrl in seen))
        if check_url in childUrl and childUrl not in seen and len(contain_charges) < maxNumUrl:
            # print("seed_url=" + seed_url)
            # print("original childurl=" + o_childurl)
            # print("childurl=" + childUrl)
            #print("***urls.append and seen.append***")
            urls.append(childUrl)
            seen.append(childUrl)
            linked_text = tag.get_text().lower()
            if "charges" in linked_text:
                contain_charges.append(childUrl)
                text.append(linked_text)
        else:
            #print("######")
            pass

# print("num. of URLs seen = %d, and scanned = %d" % (len(seen), len(opened)))
# print("List of seen URLs:")
# for seen_url in seen:
#     print(seen_url)
print("output:")
# print(len(contain_charges))
# print(len(text))
for k in range(len(contain_charges)):
    print(contain_charges[k])
    print(text[k])

# print(len(contain_charges))
# print(len(urls))
# print(len(opened))