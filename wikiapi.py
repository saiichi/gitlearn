from sgmllib import SGMLParser
import urllib
from multiprocessing.dummy import Pool

class InfoParser(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.ns=""
        self.title=""
        self.redirect=False
        self.missing=False
    def start_page(self,attrs):
        for k,v in attrs:
            if k == u'ns':
                self.ns = v
            elif k == u'title':
                self.title = v
            elif k == u'redirect':
                self.redirect = True
            elif k== u'missing':
                self.missing = True

class LinksParser(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.title=""
        self.haslinks=False
    def start_links(self,attrs):
        self.haslinks = True
        self.links = []
    def start_pl(self,attrs):
        dict = {}
        for k,v in attrs:
            dict.setdefault(k,v)
        self.links.append(dict)

class RedirectsParser(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.title=""
        self.hasredirects=False
    def start_redirects(self,attrs):
        self.hasredirects = True
        self.redirects=[]
        #print u'in redirects'
    def start_rd(self,attrs):
        #print u'in rd'
        dict={}
        for k,v in attrs:
            dict.setdefault(k,v)
        #print dict
        self.redirects.append(dict)

class WikiApi():
    def __init__(self):
        self.pc = [u' ', u'"' , u'%' , u'-' , u'.' , u'<' , u'>' , u'\\' ,u'^',u'_',u'`',u'{',u'|',u'}',u'~']
        self.pec = [u'%20', u'%22',u'%25',u'%2D',u'%2E',u'%3C',u'%3E',u'%5C',u'%5E',u'%5F',u'%60',u'%7B',u'%7C',u'%7D',u'%7E']
        self.title=""
        self.redirect=False
        self.missing=False
        self.haslink=False
        self.hasredirect=False
        self.baseurl = u'https://en.wikipedia.org/w/api.php'
        self.url=""
    def generateTitle(self,title):
        if type(title) != type(u''):
            raise TypeError,u'title must be unicode type'
        self.title = title
        for i in range(len(self.pc)):
            self.title.replace(self.pc[i],self.pec[i])
    def generateUrl(self, **param):
        self.url = self.baseurl
        flag = True
        for key in param.keys():
            if flag:
                self.url = self.url + u'?' + unicode(key) + u'=' +param[key]
                flag = False
            else:
                self.url = self.url + u'&' + unicode(key) + u'=' +param[key]
        self.url = self.url + u'&titles=' + self.title
        print self.url
    def getInfo(self):
        self.generateUrl(action=u'query',prop=u'info',redirects=u'yes',format=u'xml')
        xml = urllib.urlopen(self.url)
        parser = InfoParser()
        parser.feed(xml.read())
        #print parser.title
        self.title = parser.title
        self.redirect = parser.redirect
        self.missing = parser.missing
        parser.close()
        xml.close()
    def getLinks(self,**additions):
        self.generateUrl(action=u'query',prop=u'links',redirects=u'yes',format=u'xml')
        for key in additions.keys():
            self.url = self.url+u'&'+unicode(key)+u'='+additions[key]
        xml = urllib.urlopen(self.url)
        parser = LinksParser()
        parser.feed(xml.read())
        self.haslink = parser.haslinks
        if self.haslink:
            self.links = parser.links
        parser.close()
        xml.close()
    def getRedirects(self,**additions):
        self.generateUrl(action=u'query',prop=u'redirects',redirects=u'yes',format=u'xml')
        for key in additions.keys():
            self.url = self.url+u'&'+unicode(key)+u'='+additions[key]
        xml = urllib.urlopen(self.url)
        parser = RedirectsParser()
        parser.feed(xml.read())
        self.hasredirect = parser.hasredirects
        if self.hasredirect:
            self.redirects = parser.redirects
        parser.close()
        xml.close()
    def execute(self,title):
        self.generateTitle(title)
        self.getInfo()
        if not self.missing:
            self.getLinks(pllimit=u'500')
            self.getRedirects(rdlimit=u'500')
            result = (not self.missing),self.title,self.links,self.redirects
        else:
            result = (not self.missing),self.title,[],[]
        return result
        
    def multiProcessesExecute(self,titlelist):
        pool = Pool(8)
        result = pool.map(self.execute,titlelist)
        return result
        
            
            
w = WikiApi()
w.execute(u'main page')
print w.title
print w.links
print w.redirects
        
        
     
                
                
         
        
        
        
    