import requests  
from lxml import html  
import urlparse  
import collections
import re
import sys, time

#spinning cursor script
#def spinning_cursor():
#        while True:
#            for cursor in '|/-\\':
#                yield cursor
#def cursor():
#    spinner = spinning_cursor()
#    for _ in range(20):
#        sys.stdout.write(spinner.next())
#        sys.stdout.flush()
#        time.sleep(0.05)
#        sys.stdout.write('\b')



initial = "http://"
#print initial
postInitial = raw_input(" Enter an url:> http://")
STARTING_URL = initial+postInitial
print "\npinging... %s"%STARTING_URL
#cursor()
try:

    urls_queue = collections.deque()  
    urls_queue.append(STARTING_URL)  
    found_urls = set()  
    found_urls.add(STARTING_URL)
    
    #file open/create
    fopdf = open("pdfLinks.txt", "wb")
    foimg = open("imgLinks.txt", "wb")
    fodoc = open("docLinks.txt", "wb")
    
    #regex 
    pdf = re.compile('(.*?).(pdf)')
    docx = re.compile('(.*?).(?:doc|docx)')
    img = re.compile('(.*?).(?:jpg|gif|png)')
    
    while len(urls_queue):
        
        url = urls_queue.popleft()
    
        response = requests.get(url)
        parsed_body = html.fromstring(response.content)
    
        
    
        # Find all links
        links = {urlparse.urljoin(response.url, url) for url in parsed_body.xpath('//a/@href') if urlparse.urljoin(response.url, url).startswith('http')}
        
        #print links
        
        # Prints the page title
        #print parsed_body.xpath('//title/text()')
        #titl = str(parsed_body.xpath('//title/text()'))
        #fo.write(titl+"\n\n")
        
        # Set difference to find new URLs
        for link in (links - found_urls):
            found_urls.add(link)
            urls_queue.append(link)
            print link
            if pdf.match(link):
                fopdf.write(link+"\n")
            elif docx.match(link):
                fodoc.write(link+"\n")
            elif img.match(link):
                foimg.write(link+"\n")
        
        print "\n"
        #cursor()
     
    
       
     
    fopdf.close()
    fodoc.close()
    foimg.close()
    
except:
    print "No internet connection or invalid url"
    
