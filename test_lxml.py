import lxml.etree as le
import os
import re
from sklearn.externals import joblib
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from title_feature import title_featurer
import parser_fulltext
import method_constants

# Learning how to use lxml

def print_xml(tree):
    """
    Print xml
    """

    print(le.tostring(tree, pretty_print=True, encoding='unicode', method='xml'))

def doc_iterate(directory):
    """
    Iterate through docs in a journal and print titles/secs within body
    """

    for document in os.listdir(directory):
        yield(document)

def tree_iterate(root):
    """
    test iterating through lxml tree
    This only iterates through front, body and back
    """

    for child in root:
        print(child.tag)
        print(child.text)

def tree_full_iterate(root):
    """
    Test iterating through full lxml tree
    """

    for element in root.iter():
        print(element.tag)

def test_striptag(tree, root):
    """
    Test strip_tag method
    """
    for i in root.iter():
        print(i.text)
    le.strip_tags(root, 'italic')
    print("\n\n\n\n\n\n\n")

    for i in root.iter():
        print(i.text)

def test_tostring(root):
    """
    test how to tostring parent and get_sec_children
    """

    print(le.tostring(root, pretty_print=True, encoding='unicode', method='xml'))

def methods_search(root):
    """
    Look for methods/all children within titles and sections
    """

    try:
        # search through sec-type first
        sec = root.findall(".//*[@sec-type]")
        methods_sec = None
        print("Searching for sec-type")
        for i in sec:
            if i.attrib['sec-type'] in method_constants.sections:
                methods_sec = (i.attrib['sec-type'])
                return {'sec': methods_sec}

        # then search through titles
        print("Searching for titles")
        sec = root.findall(".//title")
        methods_title = None
        for i in sec:
            #print(i, i.tag, i. attrib, i.text)
            if i.text in method_constants.titles:
                methods_title = i.text
                return {'title': methods_title}

        print("Sorry, no methods to be found")

    except BaseException as e:
        print(e)

def return_methodsviatitle(root, methods_text):
    """
    Using the matched method name, return the methods section
    This isn't working. For it to work, I should just combine it with the above function
    """

    # need parent because title doesn't have any children
    sec_parent = root.xpath("body//title[text() = '{}']/..".format(methods_text)) # * means all children. If you give .. after a child, the parent will be selected. See doc ref below:
    # 'year' nodes that are children of nodes with name='Singapore'
    #root.findall(".//*[@name='Singapore']/year")
    #print(sec_parent.tag, sec_parent.tag, sec_parent.attrib)
    xml_list = []
    for i in sec_parent:
        xml_list.append(le.tostring(i, encoding='unicode', method='xml'))

    return sec_parent, xml_list

def return_methodsvsisectype(root, methods_name):
    """
    Using the matched method name, return the methods section
    """

    sec = root.findall("./body//*sec[@sec-type='{}']".format(methods_name)) # * means any node with the following condition.  //*sec[@sec-type='{}']/.. means the parent and all descendants will be included
    print(sec)
    xml_list = []
    for i in sec:
        xml_list.append(le.tostring(i, encoding='unicode', method='xml'))

    return sec, xml_list

def get_date(root):
    """
    Pull the day, month, and year out of the articles
    """

    date = root.find('.//pub-date')
    for i in date:
        print(i.tag, i.text)

def body_iterate(root):
    """
    Iterate through the body
    """

    body = root.find('body')
    for i in body.iter():
        if i.text == None:
            pass
        else:
            print(i.text)

def sec_iterate(root):
    """
    Testing how to parse out sections in body without using string matches
    """

    body = root.find('body')
    for sec in body:
        print(sec.attrib)
        #print(le.tostring(sec, encoding = 'unicode', method = 'text'))
        #print(le.tostring(sec, encoding = 'unicode', method = 'xml'))

def test_line_by_line_xml():
    """
    Test iterating over the fulltexts, 1 per line
    """

    fulltext_parser = parser_fulltext.parser()

    with open('C:\\Users\\saveryme\\Documents\\full_text_project\\xml_per_line_1200_jim') as f:
        for line in f:
            pattern = r'\d+\|'
            line = re.sub(pattern, '', line)
            try:
                root = le.fromstring(line)
                # iterate through each section in the body of the article and classify the section
                for section in fulltext_parser.iterate_body(root):
                    fulltext_parser.iterate_sec(section)
                    #for child in fulltext_parser.iterate_sec(section):
                    #     pass
                        #print(child, "\n")
            except le.XMLSyntaxError as e:
                #print("here's the problem", line[57765:57779])
                print("lxml error")


def test_classifier(root, filename):
    """
    see if my svm can classify a method...
    """

    pattern = r'PMC\d+'
    pmid = re.match(pattern, filename).group(0)
    method_classifier = joblib.load('method_classifier_probability.pkl')

    body = root.find('body')
    for child in body:
        #for child in sec:
            #print(le.tostring(sec, encoding = 'unicode', method = 'text'))
        X = le.tostring(child, encoding = 'unicode', method = 'xml')
        pattern_title = r'(?<=<title>)(.*?)(?=<\/title>)'
        search = re.search(pattern_title, X)
        title = None
        if search:
            title = search.group(0)

        y_predictions = method_classifier.predict_proba([X])
        methods, other = zip(method_classifier.classes_, y_predictions[0])

        print("PMID:", pmid)
        print(title)
        print(methods, other)
        print(X, "\n")


def test_iterpaser(root):
    """
    test iterparse
    """
    pass

filename = 'PMC3339586.NXML'
#tree = le.parse('C:\\Users\\saveryme\\Documents\\full_text_project\\full_texts_sample\\3_Biotech\\{}'.format(filename))
#tree = le.parse('C:\\Users\\saveryme\\Documents\\full_text_project\\full_texts_sample\\Acta_Biomater\\PMC4298359.NXML')
#directory = 'C:\\Users\\saveryme\\Documents\\full_text_project\\full_texts_all\\BMJ_Open\'
tree = le.parse('C:\\Users\\saveryme\\Documents\\full_text_project\\full_texts_sample\\Acta_Anaesthesiol_Scand\\PMC4171781.NXML')
root = tree.getroot()

test_line_by_line_xml()

#print_xml(root)
#tree_full_iterate(root)
#test_striptag(tree, root)
#test_tostring(root)

# sec_iterate(root)
#test_classifier(root, filename)
# Nice way to write file
#tree.write(<output_file_name>, pretty_print=True)

# title search:
# methods_name_dict = methods_search(root)
# print(methods_name_dict)
# if 'title' in methods_name_dict:
#      method, xml_list = return_methodsviatitle(root, methods_name_dict['title'])
# #
# if 'sec' in methods_name_dict:
#      method, xml_list = return_methodsvsisectype(root, methods_name_dict ['sec'])
# #
# method_text = " ".join(xml_list)
# xml_string = method_text.strip()
# print(xml_string)

# looking for dates:
#get_date(root)

#body_iterate(root)
#test_location(root, methods_name_dict['title'])
