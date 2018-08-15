import pandas as pd
import json
import pymongo as pm
import method_constants
import os
import lxml.etree as le
import re


class data_labeler():
    """
    class to add labels to data
    """

    def __init__(self, directory, labels):
        """
        Initiate the data labeler
        """

        self.directory = directory
        self.label_constants = [label.lower() for label in labels]
        #self.documents =[]

    def mongo_connection(self):
        """
        Connect to the mongo db
        """

        client = pm.MongoClient('localhost', 27017)
        self.db = client['full_texts'] # creates database if not there
        #self.documents = self.db['texts'] # creates new collection if not there
        self.documents = self.db['texts_v2']
        # data is here: C:\Program Files\MongoDB\Server\4.0\data
        #print(self.documents.find().count())
        #self.documents.remove({}) # clears out collection
        print("Remember to clear out db if you need to... Current count:", self.documents.find().count())

    def doc_iterate(self, journal):
        """
        Iterate through docs in a journal and print titles/secs within body
        """

        doc_directory = '{0}\\{1}'.format(self.directory, journal)

        for document in os.listdir(doc_directory):
            yield document

    def journal_iterate(self):
        """
        Iterate through all journals
        Calls doc_iterate which will iterate through all document in each journal
        """

        for journal in os.listdir(self.directory):
            yield journal

    def tree_iterate(self, root):
        """
        Iterate through the tree
        """

        for element in root.iter():
            try:
                yield element
            except BaseException as e:
                print(e)

    def clean_text(self, text):
        """
        strip whitespace from text and lower the case
        """

        clean_text = re.sub('\s+',' ', text).lower()
        return clean_text

    def label_search(self, root):
        """
        Look for children within titles and sections
        """

        try:
            # search through titles
            #print("Searching for titles")
            sec = root.findall("./body//title")
            label_title = None
            for i in sec:
                if i.text != None:
                    # Clean so I can acutally find a match!
                    text = self.clean_text(i.text)
                    #print(i, i.tag, i. attrib, i.text)
                    if text in self.label_constants:
                        if '&' in i.text:
                            text_amp = re.sub('&', '&amp;', i.text)
                            return {'title': text_amp}
                        #print("Found", i.text)
                        return {'title': i.text}

            #print("Sorry, no conclusions to be found")
            return {}

        except BaseException as e:
            print(e)

    def return_label_title(self, root, label_text, doc):
        """
        Using the matched method name, return the methods section
        This isn't working. For it to work, I should just combine it with the above function
        """

        # need parent because title doesn't have any children
        try:
            sec_parent = root.xpath("body//title[text() = '{}']/..".format(label_text)) # * means all children. If you give .. after a child, the parent will be selected. See doc ref below:
        except BaseException as e:
            print(e, doc, label_text)
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

    def get_location(self, root, method_string):
        """
        Testing how to divide up into numerical locations
        """

        body = root.find('body')
        if body != None:
            xml_string = le.tostring(body, encoding = 'unicode', method = 'xml')
            pattern = r'{}'.format(method_string)
            search = re.search(pattern, xml_string)
            if search:
                return search.start()/len(xml_string)
            else:
                return None
        else:
            return None

    def add_element_mongo(self, label, text, journal, article, date, location):
        """
        Add methods to mongo
        """

        mongo_document = {
            #'branch': str(element),
            'text': text,
            'journal': journal,
            'article': article,
            'date': date,
            'label': label,
            'location': location
            }

        # print whole thing:
        #print(mongo_document)
        appended_doc = self.documents.insert_one(mongo_document)
        #print('New document: {}'.format(appended_doc.inserted_id))


if __name__ == '__main__':

    with open('section_lists_custom_dict.json') as f:
        label_lists = json.load(f)

    label_list = label_lists['conclusion']

    #directory = 'C:\\Users\\saveryme\\Documents\\full_text_project\\full_texts_sample\\'
    directory = 'C:\\Users\\saveryme\\Documents\\full_text_project\\full_texts_all\\'

    labeler = data_labeler(directory, label_list)
    # intiate for mongo
    labeler.mongo_connection()
    journal_generator = labeler.journal_iterate()

    total_label = 0
    total_no_label= 0

    for journal in journal_generator:
        #print(journal)
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
                    total_label += 1
                    label, xml_list = labeler.return_label_title(root, label_name_dict['title'], doc)
                    label_text = " ".join(xml_list)
                    #print("Adding ", label_text)
                    xml_string = label_text.strip()
                    #print(xml_string, "\n")

                    date = labeler.get_date(root)
                    location = labeler.get_location(root, label_name_dict['title'])

                    if location == None:
                        print(label_name_dict['title'])
                        print(xml_string, "\n")

                    # mongo way
                    labeler.add_element_mongo('conclusion', xml_string, journal, doc, date, location)

                else:
                    #print("Moving to next document\n")
                    total_no_label += 1

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
    print("Conclusions {0}!, no conclusions {1}".format(total_label, total_no_label))
