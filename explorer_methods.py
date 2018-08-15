import xml.etree.ElementTree as ET
import os
import method_constants
import matplotlib.pyplot as plt
import numpy as np
import json

class explore_methods():
    """
    Class to find methods in journal publications
    Methods include the following:
    Count the number of matches between method_constants and sec-type attribute
    Count the number of matches in title
    Count the overlap between the two
    print all sec-type with multiple matches
    visualize counts
    """

    def __init__(self, method_titles, method_sec_type, extended_methods):
        """
        Initiate class for method retrieval
        """

        self.titles = method_titles
        self.sec_type = method_sec_type
        self.extended_methods = explore_methods.lower_the_case(extended_methods)

    @staticmethod
    def lower_the_case(label_list):
        """
        Lower the case of section label list
        Static methods can be called with or without instance init.
        """

        new_list = [i.lower() for i in label_list]
        return(new_list)

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

    def print_xml(self, root, doc = None):
        """
        Print xml nicely
        """

        self.indent(root)
        # Prints everything
        ET.dump(root)
        print("\n\n\n")

    def write_xml(self, tree, root, doc, description):
        """
        Write pubs to a folder based on descriptionn of methods content
        """

        if description == False:
            tree.write('C:\\Users\\saveryme\\Documents\\full_text_project\\no_methods_xml\\{}'.format(doc))
        if description == True:
            tree.write('C:\\Users\\saveryme\\Documents\\full_text_project\\methods_xml\\{}'.format(doc))

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

        #section = root.findall('body/*/title')
        section = root.findall('.//title')

        # Iterate through section in an article
        for i in section:
            try:
                if i.text.lower() in self.titles:
                    return True
                if i.text.lower() in self.extended_methods:
                    return True
            except AttributeError as e:
                continue

        return False

    def check_sec_type(self, root, journal, document):
        """
        To to see if methods sec-type is in the document
        """

        # Both work; * is wildcard though...
        #sec = root.findall(".//sec[@sec-type]")
        sec = root.findall(".//*[@sec-type]")

        for i in sec:
            try:
                if i.attrib['sec-type'].lower() in self.sec_type:
                    return True
                if i.attrib['sec-type'].lower() in self.extended_methods:
                    return True
            except AttributeError as e:
                continue

        return False

    def check_titleandsec(self, root, journal, document):
        """
        See how many docs have methods in both the title and the sec
        """

        title = root.findall('.//title')
        title_boolean = False

        # Iterate through section in an article
        for i in title:
            try:
                if i.text in self.titles:
                    title_boolean = True
                    break
                if i.text.lower() in self.extended_methods:
                    title_boolean = True
                    break
            except AttributeError as e:
                continue

        if title_boolean == True:
            sec = root.findall(".//*[@sec-type]")

            for i in sec:
                try:
                    if i.attrib['sec-type'] in self.sec_type:
                        return True
                    if i.attrib['sec-type'].lower() in self.extended_methods:
                        return True
                except AttributeError as e:
                    continue

        return False

    def check_multiple_sec(self, root):
        """
        Look at the docs that have multiple sec
        """

        # Both work; * is wildcard though...
        #sec = root.findall(".//sec[@sec-type]")
        sec = root.findall(".//*[@sec-type]")
        sec_cnt = 0

        for i in sec:
            try:
                #if i.attrib['sec-type'] in self.sec_type:
                if i.attrib['sec-type'].lower() in self.extended_methods:
                    sec_cnt += 1
            except AttributeError as e:
                continue

            if sec_cnt > 1:
                self.print_xml(root)

    def check_no_methods(self, root, doc = None):
        """
        Check to see which articles have no methods mentioned in title and sec tags
        """

        title = root.findall('.//title')
        title_boolean = False
        sec_boolean = False

        # Iterate through section in an article
        for i in title:

            try:
                if i.text in self.titles:
                    title_boolean = True
                if i.text.lower() in self.extended_methods:
                    title_boolean = True
                    break
            except AttributeError as e:
                continue

        sec = root.findall(".//*[@sec-type]")
        for i in sec:

            try:
                if i.attrib['sec-type'] in self.sec_type:
                    sec_boolean = True
                if i.attrib['sec-type'].lower() in self.extended_methods:
                    sec_boolean = True
                    break
            except AttributeError as e:
                continue

        if sec_boolean == False and title_boolean == False:
            return False
        else:
            return True

    def visualize(self, frequencies):
        """
        Visualize number of articles with and without methods
        """

        print("Visualizing...")
        figure, axis = plt.subplots(figsize=(10, 5))
        indexes = np.arange(len(frequencies))
        font = {'fontsize': 10}
        labels = [
            'Articles with no <title> methods',
            'Articles with <title> methods',
            'Articles with no <sec> methods',
            'Articles with <sec> methods',
            'Overlap between title and sec',
            'No methods anywhere',
            'At least one method somewhere'
            ]
        #labels = ['Overlap between title and sec']
        axis.bar(indexes, frequencies)
        axis.set_xticks(indexes)
        axis.set_xticklabels(((labels)), fontdict = font, rotation = 55)
        figure.savefig('method_frequencies_whole_article.png', bbox_inches = 'tight')
        plt.show()
        plt.close()

if __name__ == '__main__':

    total_no_title_methods = 0
    total_title_methods = 0
    total_no_sec_methods = 0
    total_sec_methods = 0
    total_no_methods = 0
    total_methods = 0
    overlap_total = 0
    doc_cnt = 0
    journal_cnt = 0

    # section strings from json
    with open('section_lists.json', 'r') as f:
        label_lists = json.load(f)

    #results_list = label_lists['results']
    methods_lists = label_lists['methods']
    #conclusion_lists = label_lists['conclusion']
    #objective_list = label_lists['objective']
    #discussion_list = label_lists['discussion']

    directory = 'C:\\Users\\saveryme\\Documents\\full_text_project\\full_texts_all\\'
    #directory = 'C:\\Users\\saveryme\\Documents\\full_text_project\\full_texts_sample\\'

    search = explore_methods(method_constants.titles, method_constants.sections, methods_lists)
    journal_generator = search.journal_iterate(directory)

    # Iterate through journals and docs
    for journal in journal_generator:
        print(journal)
        journal_cnt += 1
        document_generator = search.doc_iterate(directory, journal)
        for doc in document_generator:
            try:
                doc_cnt += 1
                tree = ET.parse('{0}\\{1}\\{2}'.format(directory, journal, doc))
                root = tree.getroot()
                #search.check_multiple_sec(root)
                method_boolean = search.check_no_methods(root, doc)
                title_boolean = search.check_titles(root, journal, doc)
                sec_boolean = search.check_sec_type(root, journal, doc)
                title_sec_boolean = search.check_titleandsec(root, journal, doc)

                # The code below can write articles to different dirs depending on whether or not they contain methods
                # Really should be it's own .py file
                if not method_boolean:
                    total_no_methods += 1
                    #search.write_xml(tree, root, doc, description = method_boolean)
                else:
                    total_methods += 1
                    #search.write_xml(tree, root, doc, description = method_boolean)

                # Code for producing counts necessary for visualization
                if title_boolean:
                    total_title_methods += 1
                else:
                    total_no_title_methods += 1
                if sec_boolean:
                    total_sec_methods += 1
                else:
                    total_no_sec_methods += 1
                if title_sec_boolean:
                    overlap_total += 1

            except BaseException as e:
                if doc == None:
                    print("No journals in this directory!", e)
                    continue
                else:
                    raise

    search.visualize([total_no_title_methods, total_title_methods, total_no_sec_methods, total_sec_methods, overlap_total, total_no_methods, total_methods])
    #search.visualize([overlap_total])
