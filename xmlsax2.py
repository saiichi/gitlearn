'''

'''

from xml.sax import parse,handler,SAXException
from scipy.sparse import coo_matrix
from scipy.io import savemat
from nltk.corpus import wordnet as wn
from matrixmk import mk2edMatrix


import gv

class parseHandler(handler.ContentHandler):
    def __init__(self):
        self.curSchema=u'root'
        self.parSchema=[]
        self.intags=False
        self.cururl=u''
        self.curtag=u''
        self.curcount=u''
        self.schemacheklist1=[u'name',u'count',u'tags',u'url',u'document',u'documents',]
        self.schemacheklist2=[u'name',u'count',u'tags',u'url',u'documents',]
    def startElement(self,name,attr):
        #for schema in self.schemacheklist1:
        #    if name==schema:
        #        self.parSchema.append(self.curSchema)
        #        self.curSchema = name
        #        return
        #if name==u'tag':
        #    if self.curSchema==name:
        #        self.parSchema.append(self.curSchema)
        #        self.curSchema = name
        if name == u'name':
            self.curSchema = name
        if name == u'count':
            self.curSchema = name
        if name == u'url':
            self.curSchema = name
        
    def endElement(self,name):
        #for schema in self.schemacheklist2:
        #    if name==schema:
        #        self.curSchema = self.parSchema.pop()
        #        return
        #if name==u'document':
        #    self.curSchema = self.parSchema.pop()
        #    gv.endDoc(self.cururl)
        #if name==u'tag':
        #    if self.parSchema[len(self.parSchema)-1] == u'tags':
        #        self.curSchema = self.parSchema.pop()
        #        gv.addTag(self.curtag,self.curcount)
        if name == u'name':
            self.curSchema = u''
        if name == u'count':
            self.curSchema = u''
        if name == u'url':
            self.curSchema = u''
        if name == u'document':
            gv.endDoc(self.cururl) 
    def characters(self,content):
        if self.curSchema==u'name':
            self.curtag = content
        if self.curSchema==u'count':
            #self.curcount = content
            self.curtag = self.curtag.strip()
            if wn.morphy(self.curtag) != None:
                self.curtag = wn.morphy(self.curtag)
            try:
                self.curtag = str(self.curtag)
                if self.curtag.isalpha():
                    gv.addTag(self.curtag,int(content))
            except:
                pass
#            if self.curtag.isalpha():
#                gv.addTag(self.curtag,int(content))
        if self.curSchema==u'url':
            self.cururl = content

def main():
    gv.pstatus = 0
    parse('workdata\social-odp-2k9_annotations.xml', parseHandler())
    coomat = coo_matrix((gv.coomatv,(gv.coomatr,gv.coomatc)),)
    cscmat = coomat.tocsc()
    m2 = mk2edMatrix(cscmat.transpose())
    savemat("workdata/dataset",mdict = {'mat1st':cscmat,'taglist':gv.taglist,\
            'mat2ed':m2})
    gv.save()
    
if __name__=='__main__':
    main()

        