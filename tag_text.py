import lxml.etree as le
import os
import method_constants
import html_tags
import matplotlib.pyplot as plt
import numpy as np
import operator
import json


class count_tags():
    """
    Class to count all xml tags, using lxml
    """

    def __init__(self, method_titles, method_sec_type):
        """
        Initiate class for method retrieval
        """

        self.titles = method_titles
        self.sec_type = method_sec_type

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

    def body_iterate(self, root):
        """
        Iterate through the body
        """

        body = root.find('body')
        if body != None:
            for element in body.iter():
                try:
                    if element.tag not in html_tags.tags:
                        yield element
                    else:
                        pass
                except BaseException as e:
                    print(e)

    def count_elements(self, elements):
        """
        Count all the texts in the body
        """

        element_dict = {}

        for element in elements:
            if element.text in element_dict and element.text != None and len(element.text.strip()) > 5:
                element_dict[element.text] += 1
            else:
                element_dict[element.text] = 1

        return element_dict

    def visualize(self, tag_dict):
        """
        Visualize number of articles with and without methods
        """

        print("Visualizing...")
        # would like the 100 most freqent or something
        sorted_tags = sorted(tag_dict.items(), key=operator.itemgetter(1))#, reverse = True)
        sorted_tags = sorted_tags[-75:]
        labels, frequencies = zip(*sorted_tags)
        print(labels, frequencies)
        figure, axis = plt.subplots(figsize=(25, 15))
        indexes = np.arange(len(sorted_tags))
        font = {'fontsize': 8}

        axis.barh(indexes, frequencies)
        axis.set_title('Tag frequencies in full text articles', fontsize = 22)
        axis.set_yticks(indexes)
        axis.set_yticklabels(((labels)), fontdict = font)#, rotation = 75)
        axis.ticklabel_format(style = 'plain', scilimits = (0, 0), axis = 'x')
        #figure.savefig('tag_text_frequencies_body.png', bbox_inches = 'tight')
        figure.savefig('tag_attrib_text_frequencies_body.png', bbox_inches = 'tight')
        plt.show()
        plt.close()

if __name__ == '__main__':

    """
    Iterate through all journals and all documents, count all the tags, and plot them
    """

    directory = 'C:\\Users\\saveryme\\Documents\\full_text_project\\full_texts_all\\'
    #directory = 'C:\\Users\\saveryme\\Documents\\full_text_project\\full_texts_sample\\'

    search = count_tags(method_constants.titles, method_constants.sections)
    journal_generator = search.journal_iterate(directory)

    #parser = le.XMLParser() can be used for setup options

    tag_dict = {}

    # Iterate through journals and docs
    for journal in journal_generator:
        print(journal)
        document_generator = search.doc_iterate(directory, journal)
        for doc in document_generator:
            try:
                tree = le.parse('{0}\\{1}\\{2}'.format(directory, journal, doc))
                root = tree.getroot()

                # Element generator
                elements = search.body_iterate(root)
                element_dict = search.count_elements(elements)

                for key, value in element_dict.items():
                    if key in tag_dict:
                        tag_dict[key] += value
                    else:
                        tag_dict[key] = value

            except BaseException as e:
                if doc == None:
                    print("No journals in this directory!", e)
                    continue
                else:
                    raise

    sorted_tag_dict = dict(sorted(tag_dict.items(), key=operator.itemgetter(1), reverse = True))
    with open("tag_text_counts.json", "w") as f:
        json.dump(sorted_tag_dict, f, separators=(',', ': '), indent=2)
    #search.visualize(tag_dict)
