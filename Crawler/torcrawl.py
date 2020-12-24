import socket
import socks

# TorCrawl Modules
from Crawler.modules.crawler import crawler
from Crawler.modules.extractor import extractor
from Crawler.modules.checker import *

# Set socket and connection with TOR network
def connecttor():
	try:
		port = 9050
		# Set socks proxy and wrap the urllib module
		socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', port)
		socket.socket = socks.socksocket

		# Perform DNS resolution through the socket
		def getaddrinfo(*args):
			return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

		socket.getaddrinfo = getaddrinfo
	except:
		e = sys.exc_info()[0]
		print(("Error: %s" % e + "\n## Can't establish connection with TOR"))


def crawl(urls):
	# Initialize necessary variables
	cpause = 0.5
	cdepth = 1

	# Parse arguments to variables
	inputFile = "Crawler/links.txt"
	outputfile = "Crawler/source_pages"
	checktor()
	connecttor()
	checkip()
	
	# try:
	# 	global f
	# 	f = open(inputFile, 'r')
	# except IOError:
	# 	e = sys.exc_info()[0]
	# 	print(("Error: %s" % e + "\n## Can't open " + inputFile))
	# else:
	for url in urls:
		print("url - ",url)
		global website
		global outpath
		outpath = "Crawler/output"
		website = urlcanon(url,True)
		lst = crawler(website, cdepth, cpause, outpath, True, True)
		print("list->",lst)
		lstfile = open(outpath + '/onionlinks.txt', 'a')
		for item in lst:
			lstfile.write("%s\n" % item)
		lstfile.close()
		print(("## File created on " + os.getcwd() + "/" + outpath + "/onionlinks.txt"))
	return lst

# if __name__ == "__main__":
# 	main()
