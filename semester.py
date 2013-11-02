import magic
import PyPDF2
#from collections import defaultdict
import string
import re

# class semester:
# 	def __init__(self, doc,uuid,mongo):
# 		self.doc = doc
# 		self.uuid = uuid
# 		self.mongo = mongo


def ParseFile(doc):
    '''
    Determines filetype of doc, passes to Parse_filetype_()
    '''
    mimetype = magic.from_buffer(doc.read(1024), mime=True)
    print mimetype
    if mimetype == "application/vnd.oasis.opendocument.text":
        return ParseODT(doc)
    if mimetype == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or mimetype == 'application/msword':
        return ParseDOCX(doc)
    if mimetype == "application/pdf":
        return ParsePDF(doc)
    if mimetype == "application/postscript":
        return ParsePS(doc)
    if mimetype == "text/html":
        semester =  FindSemester(doc)
        year = FindYear(semester,doc)

    else:
        print mimetype
        raise Exception("Unknown Filetype")


def ParsePDF(doc):
    '''
    parses a filetype into plaintext, passes doc to FindSemester
    '''
    pdf = PyPDF2.PdfFileReader(doc)
    text = str()
    for page in pdf.pages:
        text += page.extractText()
    betterText = CleanText(text)
    FindSemester(betterText)


def FindSemester(doc):
    '''
    returns the semester and year if found in a document
    '''
    semesterNames = [
        'fall', 'spring', 'summer', 'winter', 'maymester', 'mini-mester',
        'interim', 'intersession', 'j-term', 'inter-term', 'may term', 'may-term']
    nameLocations = FindNamesLoc(semesterNames, doc)
    print FindYearNearSemester(nameLocations, doc)
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
    re1='((?:(?:[1]{1}\\d{1}\\d{1}\\d{1})|(?:[2]{1}\\d{3})))(?![\\d])'  # Year 1
    rg = re.compile(re1,re.IGNORECASE|re.DOTALL)
    for i in locations:
        print "i:"+ i 
        for n in locations[i]:
            print "n:" + str(n)
            if n != -1:
                l = re.findall(rg,doc[n-200:n+200])
                print l
                for m in l:
                    possibleSemester += i +" " + m
    return possibleSemester