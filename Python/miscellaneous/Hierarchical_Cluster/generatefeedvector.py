import feedparser
import re
import operator
import collections
from collections import OrderedDict


# Returns title and dictionary of word counts for an RSS feed
def getwordcounts(url):
# Parse the feed
    d=feedparser.parse(url)
    wc={}
    if (not d.feed.get('title')):
        print 'fail parsing '+url+' the program will continue'
        return
    # Loop over all the entries
    for e in d.entries:
        if 'summary' in e: summary=e.summary
        else: summary=e.description
     # Extract a list of words
        words=getwords(e.title+' '+summary)
        for word in words:
            wc.setdefault(word,0)
            wc[word]+=1
        sorted_wc =OrderedDict(sorted(wc.items(),key=operator.itemgetter(1),reverse=True))
    return (d.feed.title,sorted_wc)


def getwords(html):
     # Remove all the HTML tags
     txt=re.compile(r'<[^>]+>').sub('',html)
     # Split words by all non-alpha characters
     words=re.compile(r'[^A-Z^a-z]+').split(txt)
     # Convert to lowercase
     return [word.lower( ) for word in words if word!='']


apcount={}
wordcounts={}
feedlist = [line for line in file('feedlist.txt')]
for feedurl in feedlist:
    res=getwordcounts(feedurl)
    if res!=None:
        title,wc=res
        wordcounts[title]=wc
        for (word,count) in wc.items():
            apcount.setdefault(word,0)
            if count>1:
                apcount[word]+=1


wordlist=[]
for w,bc in apcount.items():
       frac=float(bc)/len(feedlist)
       if frac>0.1 and frac<0.5: wordlist.append(w)


out = file('blogdata.txt', 'w')
for word in wordlist:
    out.write('\t%s' % word)
out.write('\n')

for (blog, wc) in wordcounts.items():
    print blog
    blog=blog.encode('utf-8')
    out.write(blog)
    for word in wordlist:
        if word in wc:
            out.write('\t%d' % wc[word])
        else:
            out.write('\t0')
    out.write('\n')
# # Returns title and dictionary of word counts for an RSS feed
# def getwordcounts(url):
#  # Parse the feed
#  d=feedparser.parse(url)
#  wc={}
#  # Loop over all the entries
#  for e in d.entries:
#     if 'summary' in e: summary=e.summary
#     else: summary=e.description
#     # Extract a list of words
#     words=getwords(e.title+' '+summary)
#     for word in words:
#         wc.setdefault(word,0)
#         wc[word]+=1
#  sorted_wc =sorted(wc.items(),key=operator.itemgetter(1),reverse=True)
#  return sorted_wc


# def getlinks(url):
#      d=feedparser.parse(url)
#      links=[]
#      for item in d.entries:
#          links.append(item.link)
#      return links


# def runlinkswordsparser(url):
#     links=getlinks(url)
#     wordCounter={}
#     print links[1]
#     print getwordcounts(str(links[1]))
    # for link in links:
    #     #  print link
    #     res=getwordcounts(str(link))
    #     print res
    #     for word in res:
    #         print word
            # wordCounter.setdefault(word,0)
            # wordCounter[word]+=res[wordCount][word]
    # return wordCounter
