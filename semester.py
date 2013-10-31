import magic
import PyPDF2
from collections import defaultdict

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
        return FindSemester(doc)
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
    print nameLocations


def FindNamesLoc(names, doc):
    '''
    returns a dictionary of all the locations of words in names list in doc
    '''
    namesIndex = defaultdict(list)
    for pos, term in enumerate(doc.split()):
        if term in names:
            namesIndex[term].append(pos)
    return namesIndex


def CleanText(text):
    newText = text.lower()
    return newText
