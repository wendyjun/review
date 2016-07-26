import os

if __name__ == "__main__":
	os.chdir("/home/gxj/Downloads/baidu1")
	os.system("/usr/local/bin/scrapy crawl baidu")
	print 'the end'
