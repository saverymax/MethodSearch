"""
Script to parse the list of serials indexed for online users:
ftp://ftp.nlm.nih.gov/online/journals/
The file contains the citation and indexing info for each serial,
including indexing history and current status
"""

import lxml.etree as le
import re
from collections import Counter


class parser():
    """
    Class to parse sections in body of full text
    """

    def __init___(self):
        """
        initiate parser
        """
        pass

    def iterate_body(self, root):
        """
        Iterate through sec tags in body
        """

        body = root.find('body')

        if body != None:
            # Need the body string to get the location
            body_text = le.tostring(body, encoding='unicode', method='text')

            for child in body:
                try:
                    # convert the child to something the svm can handle
                    # I want the xml version for the classifier,
                    # and the text version so I can match strings
                    # in get_location
                    section_xml = le.tostring(child, encoding='unicode', method='xml')
                    section_text = le.tostring(child, encoding='unicode', method='text')
                    # find where section is in body, return that/body_len
                    location = self.get_location(section_text, body_text)
                    yield section_xml, location

                except:
                   print("Error iterating through the body;")
                

    def iterate_sec(self, sec):
        """
        iterate through children of sec to get more granularity
        """

        bit = le.fromstring(sec)
        len_bit = len(bit)
        if len_bit == 0:
            yield le.tostring(bit, encoding='unicode', method='xml')
        else:
            for child_bit in bit:
                 yield le.tostring(child_bit, encoding='unicode', method='xml')

    def get_title(self, section):
        """
        get the title from the section
        """

        pattern_title = r'(?<=<title>)(.*?)(?=<\/title>)'
        search = re.search(pattern_title, section)
        title = None
        if search:
            title = search.group(0)

        return title

    def get_location(self, section, body):
        """
        get the location of the section of interest
        """

        p = .5
        title = self.get_title(section)
        if title != None:
            pattern = r'{}'.format(title)
            search = re.search(pattern, body)
            if search:
                p = search.start()/len(body)
            else:
                print(title, body)

        return p


if __name__ == '__main__':
    fulltext_parser = parser()
    with open('C:\\Users\\saveryme\\Documents\\full_text_project\\xml_per_line_1200_jim') as f:
        for line in f:
            print(line)
            #print(line)
            pattern = r'\d+\|'
            pattern1 = r'\d+'
            pmid = re.match(pattern1, line).group(0)
            line = re.sub(pattern, '', line)
            root = le.fromstring(line)
            for child in fulltext_parser.iterate_body(root):
                print(child)
