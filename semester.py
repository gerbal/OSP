import magic
import string
import re
import PyPDF2
from docx import opendocx, getdocumenttext
import nltk
import odt2txt






def ParseFile(doc):
    '''
    Determines filetype of doc, passes to Parse_filetype_()
    '''
    mimetype = magic.from_buffer(doc.read(1024), mime=True)
    #print mimetype
    if mimetype == "application/vnd.oasis.opendocument.text":
        text = ParseODT(doc)
    elif mimetype == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or mimetype == 'application/msword' or mimetype=='application/zip':
        text = ParseDOCX(doc)
    elif mimetype == "application/pdf":
        text = ParsePDF(doc)
    elif mimetype == "application/postscript":
        text = ParsePS(doc)
    elif mimetype == "text/html":
        text = ParseHTML(doc)

    else:
        print mimetype
        raise Exception("Unknown Filetype")

    betterText = CleanText(text)
    semester =  FindSemester(betterText)
    print semester

def ParsePDF(doc):
    '''
    parses a filetype into plaintext, passes doc to FindSemester
    '''
    pdf = PyPDF2.PdfFileReader(doc)
    text = str()
    for page in pdf.pages:
        text += page.extractText()
    return text

def ParseDOCX(doc):
    document = opendocx(doc)
    paratextlist = getdocumenttext(document)
    newparatextlist = []
    html = str()
    for paratext in paratextlist:
        newparatextlist.append(paratext.encode("utf-8"))
    html = html.join(newparatextlist)
    return ParseHTML(html, True)

def ParseHTML(doc, isString=False):
    if isString:
        text = nltk.clean_html(doc)
    else:
        text = nltk.clean_html(doc.read())
    return text

def ParseODT(doc):
    odt = odt2txt.OpenDocumentTextFile(doc)
    unicode = odt.toString()
    out_utf8 = unicode.encode("utf-8")
    return out_utf8

def ParsePS(doc):
    text = str()
    for line in doc:
        for p in line.replace('\\(','EscapeLP').replace('\\)','EscapeRP').split('(')[1:]:
            text += p[:p.find(')')].replace('EscapeLP','(').replace('EscapeRP',')')
    return text

def FindSemester(doc):
    '''
    returns the semester and year if found in a document
    '''
    semesterNames = [
        'fall', 'spring', 'summer', 'winter', 'maymester', 'mini-mester',
        'interim', 'intersession', 'j-term', 'inter-term', 'may term', 'may-term']
    nameLocations = FindNamesLoc(semesterNames, doc)
    return FindYearNearSemester(nameLocations, doc)
    #if 


def FindNamesLoc(names, doc):
    '''
    returns a dictionary of all the locations of words in names list in doc
    '''
    locations = dict()
    for word in names:
        locations[word] = [doc.find(word)]
        while locations[word][-1] >=0 and doc.find(word, int(locations[word][-1])) >=0:
            locations[word] += [doc.find(word,locations[word][-1]+1)]
    return locations
    # namesIndex = defaultdict(list)
    # doc.split()
    # for pos, term in enumerate(doc.split()):
    #     if term in names:
    #         namesIndex[term].append(pos)
    # return namesIndex


def CleanText(text):
    '''
    cleans a string to alphanum and spaces
    '''
    newtext = text.lower()
    newtext = re.sub('[\W_]+', ' ', newtext)
    #print newtext
    newtext = newtext.strip(string.punctuation)
    return newtext

def FindYearNearSemester(locations, doc):
    possibleSemester = str()
    re1='(\d{4})'  # Year 1
    rg = re.compile(re1,re.IGNORECASE|re.DOTALL)
    for i in locations:
        #print "i:"+ i 
        for n in locations[i]:
            #print "n:" + str(n)
            if n != -1:
                l = re.findall(rg,doc[n-200:n+200])
                #print l
                for m in l:
                    possibleSemester += i +" " + m
    return possibleSemester