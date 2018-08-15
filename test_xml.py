import xml.etree.ElementTree as ET
import os
import method_constants
#cwd = os.getcwd()
#print(cwd)

# Don't know how this or tree object work
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def print_xml(root):
    indent(root)
    # Prints everything
    ET.dump(root)

def get_all_text(root):
    """
    Print all text in doc
    """
    for child in root.itertext():
        print(child)

def get_sec_children(root):
    """
    Print children of sec
    """
    sec = root.findall(".//sec//") #
    for i in sec:
        print(i.text)

def get_sec_text(root):
    """
    Print text within all sec tags
    """
    for child in root.iter(tag='sec'):
        print(child.tag, child.attrib)
        for text in child.itertext():
            print(text)

def find_sec_id(root):
    """
    Returns first child with given tag
    """
    section = root.findall('body/sec')
    for i in section:
        try:
            print(i.attrib['id'])
        except KeyError as e:
            print("Id error: {0}; Error: {1}".format(i.tag, e))

def find_sec_type(root):
    """
    Find attribute sec-type of sec children under body
    """
    section = root.findall('body/sec')
    for i in section:
        try:
            print(i.attrib['sec-type'])
        except KeyError as e:
            print("Sec-type error: {0}; Error: {1}".format(i.tag, e))

def find_title_tags(root):
    """
    Find the text of tag title; children of sec of body
    """
    section = root.findall('body/sec/title')
    for i in section:
        print(i.text)
    print("\n")

def get_tag_attributes(root):
    """
    access specific tag attribute. In this case Sec2 of sec
    """
    try:
        sec = root.findall(".//sec[@id='Sec2']//") # I could of used *[@id='Sec2'], which means all children with the id attribute. If you give .. after a child, the parent will be selected. See doc ref below:
        # 'year' nodes that are children of nodes with name='Singapore'
        #root.findall(".//*[@name='Singapore']/year")
        for i in sec:
            print(i.attrib, i.tag)
    except BaseException as e:
        print("No Sec2:", e)

def find_methods_viatitle(root):
    """
    Find the methods section. Find a title that has a match, then get parents
    """

    try:
        sec = root.findall(".//title")
        print(sec)
        methods_name = None
        for i in sec:

            #print(i, i.tag, i. attrib, i.text)
            if i.text in method_constants.titles:
                #print(i.attrib['sec-type'])
                methods_name = (i.text)
                break

    except BaseException as e:
        print(e)

    if methods_name != None:
        return methods_name
    else:
        print("Sorry, no methods to be found")

def return_methodsviatitle(root, methods_text):
    """
    Using the matched method name, return the methods section
    This isn't working. But it does work with lxml
    """

    print("WARNING! DEPRECATED. SEE test_lxml.py!")


def find_methods_viasectype(root):
    """
    Find the methods section!
    """

    try:
        sec = root.findall(".//*[@sec-type]")
        methods_name = None
        for i in sec:
            if i.attrib['sec-type'] in method_constants.sections:
                #print(i.attrib['sec-type'])
                methods_name = (i.attrib['sec-type'])
                break

    except BaseException as e:
        print(e)

    if methods_name != None:
        return methods_name
    else:
        print("Sorry, no methods to be found")

def return_methodsvsisectype(root, methods_name):
    """
    Using the matched method name, return the methods section
    """

    sec = root.findall(".//*sec[@sec-type='{}']".format(methods_name)) # * means any node with the following condition.  //*sec[@sec-type='{}']/.. means the parent and all descendants will be included
    print(sec)
    xml_list = []
    for i in sec:

        xml_list.append(ET.tostring(i, encoding='unicode', method='xml'))

    return sec, xml_list

def write_methods_xml(methods, filename):
    """
    Write methods to a new file
    not working
    """

    for i in methods:
        i.write('C:\\Users\\saveryme\\Documents\\full_text_project\\methods_xml\\{}_methods'.format(filename))

def test_write(root, tree, methods_name):
    """
    Test writing methods
    """

    # Get
    sec = root.findall(".//sec[@sec-type='{}']//".format(methods_name))
    print(sec)

    # This works! But I think it only gets rid of the front and back. Not anything in body or the article tag
    for child in root:
        if child not in sec:
            root.remove(child)

    print_xml(root)
    for child in root.findall(".//body//"):
        try:

            if child not in sec:
                print(child.attrib, "not in sec")
                parent = root.find(".//{}/..".format(child.tag))
                print(parent)
                parent.remove(child)

            else:
                print(child, "in sec")
        except ValueError as e:
            print(e)
            tree.write('C:\\Users\\saveryme\\Documents\\full_text_project\\methods_xml\\{}_methods.xml'.format('test'))
            break

def check_titles(root):
    """
    Check to see if a methods title is in the document
    """

    section = root.findall('body/sec/title')
    # Iterate through section in an article
    for i in section:
        if i.text in method_constants.titles:
            print(i.text)
        else:
            print("No method found")

def check_sec_type(root):
    """
    Check to see if a sec type contains methods
    """
    try:
        sec = root.findall(".//*[@sec-type]") # I could of used *[@id='Sec2'], which means all children with the id attribute. If you give .. after a child, the parent will be selected. See doc ref below:
        # 'year' nodes that are children of nodes with name='Singapore'
        #root.findall(".//*[@name='Singapore']/year")
        for i in sec:
            if i.attrib['sec-type'] in method_constants.sections:
                print(i.attrib['sec-type'])

    except BaseException as e:
        print(e)

def doc_iterate(journal=None):
    """
    Iterate through docs in a journal and print titles/secs within body
    """
    if journal == None:
        directory = 'C:\\Users\\saveryme\\Documents\\full_text_project\\full_texts_sample\\AAPS_J'
    else:
        directory = 'C:\\Users\\saveryme\\Documents\\full_text_project\\full_texts_sample\\{}'.format(journal)

    for filename in os.listdir(directory):
        print(journal)
        print(filename)

        tree = ET.parse('{0}\\{1}'.format(directory, filename))
        root = tree.getroot()

        #find_sec_type(root)
        #find_sec_id(root)
        get_tag_attributes(root)
        #find_title_tags(root)

def journal_iterate():
    """
    Iterate through all journals
    Calls doc_iterate which will iterate through all articles in each journal
    """
    journal_directory = 'C:\\Users\\saveryme\\Documents\\full_text_project\\full_texts_sample'
    for journal in os.listdir(journal_directory):
        print(journal)
        doc_iterate(journal)


# Must use \\
filename = 'PMC3339586.NXML'
#tree = ET.parse('C:\\Users\\saveryme\\Documents\\full_text_project\\full_texts_sample\\3_Biotech\\{}'.format(filename))
tree = ET.parse('C:\\Users\\saveryme\\Documents\\full_text_project\\full_texts_sample\\Acta_Biomater\\PMC4298359.NXML')
#tree = ET.parse('C:\\Users\\saveryme\\Documents\\full_text_project\\methods_xml\\test_methods.xml')
#tree = ET.parse('C:\\Users\\saveryme\\Documents\\full_text_project\\methods_xml\\PMC6000029.NXML')
#tree = ET.parse('C:\\Users\\saveryme\\Documents\\full_text_project\\no_methods_xml\\PMC3937585.NXML')
#tree = ET.parse('C:\\Users\\saveryme\\Documents\\full_text_project\\no_methods_xml\\PMC3300825.NXML')
#tree = ET.parse('C:\\Users\\saveryme\\Documents\\full_text_project\\full_texts_sample\\AAPS_J\\PMC4406961.NXML')
#tree = ET.parse('C:\\Users\\saveryme\\Documents\\full_text_project\\full_texts_sample\\Acta_Biomater\\PMC4362771.nxml')
#tree = ET.parse('C:\\Users\\saveryme\\Documents\\full_text_project\\full_texts_sample\\A_A_Pract\\PMC5895136.nxml')
#tree = ET.parse('C:\\Users\\saveryme\\Documents\\full_text_project\\full_texts_sample\\Acta_Anaesthesiol_Scand\\PMC4171781.nxml')
root = tree.getroot()
print_xml(root)
#get_all_text(root)
#get_sec_text(root)
#get_sec_children(root)
#find_sec_id(root)
#find_sec_type(root)
# within a sec-type there is a cooresponding title tag
#find_title_tags(root)
#get_tag_attributes(root)


#title search
# methods_name = find_methods_viatitle(root)
# print(methods_name)
# method, xml_list = return_methodsviatitle(root, methods_name)

# secytpe search:
# methods_name = find_methods_viasectype(root)
# method, xml_list = return_methodsvsisectype(root, methods_name)
# method_text = " ".join(xml_list)
# print(method_text)
# xml_string = method_text.strip()
#print(xml_string)
# with open('C:\\Users\\saveryme\\Documents\\full_text_project\\methods_xml\\test_methods_1.xml', 'w') as f:
#     f.write(xml_string)

#test_write(root, tree, methods_name)
#write_methods_xml(method, filename)

#journal_iterate()
#check_titles(root)
#check_sec_type(root)
