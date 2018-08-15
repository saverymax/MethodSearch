import xml.etree.ElementTree as ET
import os
import method_constants
import matplotlib.pyplot as plt
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


class string_extractor():
    """
    Class to look for method strings not in method constants.
    """

    def __init__(self, method_titles, method_sec_type, new_method_titles, new_method_sec):
        """
        Initiate class for method retrieval
        """

        self.titles = method_titles
        self.sec_type = method_sec_type
        self.new_title = new_method_titles
        self.new_sec_type = new_method_sec

    def indent(self, elem, level=0):
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def print_xml(self, root):
        """
        Print xml nicely
        """

        self.indent(root)
        # Prints everything
        ET.dump(root)
        print("\n\n\n")

    def doc_iterate(self, directory, journal):
        """
        Iterate through docs in a journal and print titles/secs within body
        """

        doc_directory = '{0}\\{1}'.format(directory, journal)

        for document in os.listdir(doc_directory):
            yield document

    def journal_iterate(self, journal_directory):
        """
        Iterate through all journals
        Calls doc_iterate which will iterate through all document in each journal
        """

        for journal in os.listdir(journal_directory):
            yield journal


    def check_titles(self, root, journal, document):
        """
        Check to see if a methods title is in the document
        """

        section = root.findall('body/*/title')

        # Iterate through section in an article
        for i in section:
            if i.text.lower in self.titles:
                return True

        return False

    def check_sec_type(self, root, journal, document):
        """
        To to see if methods sec-type is in the document
        """

        # Both work; * is wildcard though...
        #sec = root.findall(".//sec[@sec-type]")
        sec = root.findall(".//*[@sec-type]")

        sec_boolean = False
        for i in sec:
            if i.attrib['sec-type'].lower() in self.new_sec_type:
                if i.attrib['sec-type'] not in self.sec_type:
                    if i.attrib['sec-type'] != 'results' and i.attrib['sec-type'] != 'discussion':
                        print(i.attrib['sec-type'])
                        sec_boolean = True

        # Why were there no matches?
        #if not sec_boolean:
        #    print_xml(root)

    def visualize(self, frequencies):
        """
        Visualize number of articles with and without methods
        """

        print("Visualizing...")
        figure, axis = plt.subplots(figsize=(10, 5))
        indexes = np.arange(len(frequencies))
        font = {'fontsize': 10}
        labels = ['Articles with no <title> methods', 'Articles with <title> methods', 'Articles with no <sec> methods', 'Articles with <sec> methods', 'Overlap between title and sec']
        #labels = ['Overlap between title and sec']
        axis.bar(indexes, frequencies)
        axis.set_xticks(indexes)
        axis.set_xticklabels(((labels)), fontdict = font, rotation = 55)
        figure.savefig('method_frequencies.png', bbox_inches = 'tight')
        plt.show()
        plt.close()

def clean_methods(process):
    """
    Decorator of process_strings
    """

    def wrapper(method_constants):
        """
        Wrapper of process_strings
        Just testing wrapper. This is unecessary!
        """

        new_methods = process(method_constants)
        stop = stopwords.words('english')
        new_methods = [i.lower() for i in new_methods]
        new_methods = [i for i in new_methods if i not in stop]

        return new_methods

    return wrapper

@clean_methods
def process_strings(method_constants):
    """
    Tokenize method constants
    """

    tokenized_methods = [word_tokenize(method) for method in method_constants]
    flattened_list = [word for method in tokenized_methods for word in method]

    return flattened_list

if __name__ == '__main__':

    directory = 'C:\\Users\\saveryme\\Documents\\full_text_project\\full_texts_all\\'

    new_method_sec = process_strings(method_constants.sections)
    new_method_titles = process_strings(method_constants.titles)
    search = string_extractor(method_constants.titles, method_constants.sections, new_method_titles, new_method_sec)
    journal_generator = search.journal_iterate(directory)

    # Iterate through journals and docs
    for journal in journal_generator:
        print(journal)
        document_generator = search.doc_iterate(directory, journal)
        for doc in document_generator:
            try:
                tree = ET.parse('{0}\\{1}\\{2}'.format(directory, journal, doc))
                root = tree.getroot()
                #title_boolean = search.check_titles(root, journal, doc)
                search.check_sec_type(root, journal, doc)

            except BaseException as e:
                if doc == None:
                    print("No journals in this directory!", e)
                    continue
                else:
                    print("e")

    #search.visualize([total_no_title_methods, total_title_methods, total_no_sec_methods, total_sec_methods, overlap_total])
    #search.visualize([overlap_total])
