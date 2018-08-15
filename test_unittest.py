import unittest
import pandas as pd
import json
import pymongo as pm
import method_constants
import os
import lxml.etree as le
import re


class data_labeler(unittest.TestCase):
    """
    class to add labels to data
    """

    def __init__(self, directory, results):
        """
        Initiate the data labeler
        """

        self.directory = directory
        assert isinstance(self.directory, str)
        self.results_constants = [result.lower() for result in results]
        assert isinstance(self.results_constants, list)
        #self.documents =[]

    def mongo_connection(self):
        """
        Connect to the mongo db
        """

        client = pm.MongoClient('localhost', 27017)
        self.db = client['full_texts'] # creates database if not there
        self.documents = self.db['texts'] # creates new collection if not there
        # data is here: C:\Program Files\MongoDB\Server\4.0\data
        #print(self.documents.find().count())
        self.documents.remove({}) # clears out collection
        print("Remember to clear out db if you need to... Current count:", self.documents.find().count())

    def doc_iterate(self, journal):
        """
        Iterate through docs in a journal and print titles/secs within body
        """

        doc_directory = '{0}\\{1}'.format(self.directory, journal)

        assert isinstance(doc_directory, str)

    def journal_iterate(self):
        """
        Iterate through all journals
        Calls doc_iterate which will iterate through all document in each journal
        """

    def tree_iterate(self, root):
        """
        Iterate through the tree
        """

        for element in root.iter():
            assert element is not None
            try:
                yield element
            except BaseException as e:
                print(e)

    def clean_text(self, text):
        """
        strip whitespace from text and lower the case
        """

        clean_text = re.sub('\s+',' ', text).lower()
        assert element is not None
        assert element is not ""
        return clean_text

    def label_search(self, root):
        """
        Look for children within titles and sections
        """

        try:
            # search through titles
            print("Searching for titles")
            sec = root.findall(".//title")
            label_title = None
            for i in sec:
                if i.text != None:
                    # Clean so I can acutally find a match!
                    text = self.clean_text(i.text)
                    #print(i, i.tag, i. attrib, i.text)
                    if text in self.results_constants:
                        print("Found", i.text)
                        return {'title': i.text}

            print("Sorry, no results to be found")
            return {}

        except BaseException as e:
            print(e)

    def return_label_title(self, root, label_text):
        """
        Using the matched method name, return the methods section
        This isn't working. For it to work, I should just combine it with the above function
        """

        # need parent because title doesn't have any children
        sec_parent = root.xpath("//title[text() = '{}']/..".format(label_text)) # * means all children. If you give .. after a child, the parent will be selected. See doc ref below:

        #print(sec_parent.tag, sec_parent.tag, sec_parent.attrib)
        xml_list = []
        for i in sec_parent:
            xml_list.append(le.tostring(i, encoding='unicode', method='xml'))

        return sec_parent, xml_list

    def get_date(self, root):
        """
        Find the date in the article
        """
        date_list = []
        date_elements = root.find('.//pub-date')
        for i in date_elements:
            if i.tag != 'day':
                date_list.append(i.text)

        date = '-'.join(date_list)
        #print(date,"\n")
        return date

    def add_element_mongo(self, label, journal, article, date):
        """
        Add methods to mongo
        """

        mongo_document = {
            #'branch': str(element),
            'text': label,
            'journal': journal,
            'article': article,
            'date': date
            #'label': label
            }

        # print whole thing:
        #print(mongo_document)
        appended_doc = self.documents.insert_one(mongo_document)
        print('New document: {}'.format(appended_doc.inserted_id))

    def add_element_pandas(self, elements):
        """
        Add elements to dataframe
        """

        for element in elements:
            #if element.tag in html_tags:

            if element.text in self.titles:
                text = element.text
                label = 'method'
            elif 'sec-type' in element.attrib:
                if element.attrib['sec-type'] in self.sec_type:
                    text = element.attrib['sec-type']
                    label = 'method'
            else:
                text = element.text
                label = 'other'

            document = [
                element,
                text,
                label
                ]

            self.documents.append(document)

    def save_dataframe(self):
        """
        Save the DataFrame
        """
        headers = ['branch', 'text', 'label']
        self.df = pd.DataFrame(self.documents, columns = headers)
        print(self.df.head())
        self.df.to_csv('C:\\Users\\saveryme\\Documents\\full_text_project\\data\\labeled_full_text.tsv', sep = '\t', index = False)
        #self.df.to_csv('C:\\Users\\saveryme\\Documents\\full_text_project\\data\\labeled_full_text_all.tsv', sep = '\t', index = False)

if __name__ == '__main__':



    with open('section_lists_custom_dict.json') as f:
        label_lists = json.load(f)

    label_list = label_lists['results']

    directory = 'C:\\Users\\saveryme\\Documents\\full_text_project\\full_texts_sample\\'
    #directory = 'C:\\Users\\saveryme\\Documents\\full_text_project\\full_texts_all\\'
    unittest.main()
    labeler = data_labeler(directory, label_list)
    # intiate for mongo
    labeler.mongo_connection()
    journal_generator = labeler.journal_iterate()

    for journal in journal_generator:
        print(journal)
        document_generator = labeler.doc_iterate(journal)
        for doc in document_generator:
            try:
                tree = le.parse('{0}\\{1}\\{2}'.format(directory, journal, doc))
                root = tree.getroot()
                # Element generator
                elements = labeler.tree_iterate(root)

                # Search for the label!
                label_name_dict = labeler.label_search(root)

                if 'title' in label_name_dict:
                    label, xml_list = labeler.return_label_title(root, label_name_dict['title'])

                else:
                    print("Moving to next document\n")
                    break

                label_text = " ".join(xml_list)
                print("Adding ", label_text)
                xml_string = label_text.strip()
                #print(xml_string, "\n")

                date = labeler.get_date(root)

                # include if it is method, result, etc
                # and if there are other features to add, this is where I should do it. like location of methods... see here:
                # http://www.academia.edu/6679567/A_baseline_feature_set_for_learning_rhetorical_zones_using_full_articles_in_the_biomedical_domain

                # mongo way
                labeler.add_element_mongo(xml_string, journal, doc, date)

                # pandas way
                #labeler.add_element_pandas(elements)

            except BaseException as e:
                if doc == None:
                    print("No journals in this directory!", e)
                    continue
                else:
                    raise
    # pandas way
    #labeler.save_dataframe()
