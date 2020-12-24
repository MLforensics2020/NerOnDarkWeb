import sys
import re
import urllib.request
import time
from bs4 import BeautifulSoup
import tldextract , os
from modules.checker import urlcanon
# Exclude links that we dont need


def excludes(link, website, outpath):
    # BUG: For NoneType Exceptions, got to find a solution here
    if link is None:
        return True
    # Links
    elif '#' in link:
        return True
        # External links
    elif link.startswith('http') and not link.startswith(website):
        lstfile = open(outpath + '/extlinks.txt', 'w+')
        lstfile.write(str(link) + '\n')
        lstfile.close()
        return True
        # Telephone Number
    elif link.startswith('tel:'):
        lstfile = open(outpath + '/telephones.txt', 'w+')
        lstfile.write(str(link) + '\n')
        lstfile.close()
        return True
        # Mails
    elif link.startswith('mailto:'):
        lstfile = open(outpath + '/mails.txt', 'w+')
        lstfile.write(str(link) + '\n')
        lstfile.close()
        return True
        # Type of files
    elif re.search('^.*\.(pdf|jpg|jpeg|png|gif|doc)$', link, re.IGNORECASE):
        return True


# Canonization of the link
def canonical(link, website):
    # Already formatted
    if link.startswith(website):
        return link
    # For relative paths with / in front
    elif link.startswith('/'):
        if website[-1] == '/':
            finalLink = website[:-1] + link
        else:
            finalLink = website + link
        return finalLink
    # For relative paths without /
    elif re.search('^.*\.(html|htm|aspx|php|doc|css|js|less)$', link, re.IGNORECASE):
        # Pass to
        if website[-1] == '/':
            finalLink = website + link
        else:
            finalLink = website + "/" + link
        return finalLink
    # Clean links from '?page=' arguments

# Check if a link is onion link, if yes return the domain


def checkForOnionLink(link):
    response = tldextract.extract(link)
    if response.suffix == "onion":
        return response.domain + "." + response.suffix
    else:
        return None

# Core of crawler


def crawler(website, cdepth, cpause, outpath, logs, verbose):
    lst = set()
    ordlst = []
    ordlst.insert(0, website)
    ordlstind = 0
    source_pages = []
    if logs:
        global logfile
        logfile = open(outpath + '/log.txt', 'w+')

    print((
        "## Crawler started from " + website +
        " with " + str(cdepth) + " depth crawl and " +
        str(cpause) + " second(s) delay:"
    ))

    # Depth
    for x in range(0, int(cdepth)):
        # For every element of list
        for item in ordlst:
            # Check if is the first element
            if ordlstind > 0:
                try:
                    if item is not None:
                        print("Trying item = ", item)
                        global html_page
                        item = urlcanon(item, True)
                        html_page = urllib.request.urlopen(item,timeout=300)
                except urllib.error.HTTPError as e:
                    print("HTTPError==>",e)
                    continue
                except urllib.error.URLError as e:
                    print("Time out : ", e, " for item = ", item)
                    continue
            else:
                try:
                    html_page = urllib.request.urlopen(website)
                except urllib.error.HTTPError as e:
                    print("HTTPError==>",e)
                    continue
                except urllib.error.URLError as e:
                    print("Time out : ", e, " for item = ", item)
                    continue
                except Exception as e:
                    print("General exception=>",e)                    
                ordlstind += 1
            # print("html_page",html_page.read())
            soup = BeautifulSoup(html_page, features="html.parser")
            print("soup =>", soup)
            domain = tldextract.extract(item).domain
            print("domain=>",domain)
            with open(os.getcwd() + "/source_pages/" + domain +".htm", "w+") as file:
                file.write(str(soup))
            for link in soup.findAll('a'):
                link = link.get('href')
                print("link", link)
                if not link:
                    print("No link")
                    continue
                else:
                    link = checkForOnionLink(link)
                    if link is None:
                        print("Invalid onion")
                        continue
                    else:
                        print("found")
                        pass
                lst.add(link)
            print("list later- ", lst)
            # Pass new on list and re-set it to delete duplicates
            ordlst = ordlst + list(set(lst))
            ordlst = list(set(ordlst))

            if verbose:
                sys.stdout.write("-- Results: " + str(len(ordlst)) + "\r")
                sys.stdout.flush()

            # Pause time
            try:
                if (ordlst.index(item) != len(ordlst) - 1) and float(cpause) > 0:
                    time.sleep(float(cpause))
            except Exception as e:
                print("Exceptio in pause -",e)

            # Keeps logs for every webpage visited
            if logs:
                itcode = html_page.getcode()
                logfile.write("[" + str(itcode) + "] " + str(item) + "\n")

        print(("## Step " + str(x + 1) + " completed with: " +
               str(len(ordlst)) + " result(s)"))

    if logs:
        logfile.close()

    return ordlst
