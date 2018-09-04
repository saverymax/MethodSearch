import lxml.etree as le
import re
from collections import Counter


class parser():
    """
    Class to parse sections in body of full text
    """

    def __init___(self):
        """
        initiate parser. Nothing is needed here at the moment
        """
        pass

    def iterate_body(self, root):
        """
        Iterate through sec tags in body. The root is provided by the
        classify function in run_model.py
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
                    # if error in body, let's just move on to next section.
                    print("Error iterating through the body")

    def iterate_sec(self, sec):
        """
        iterate through children of sec, as provided in run_model.py
        These children will be written line by line to
        methods_predicted_fullsec.txt
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
        Get the title from the section. This method is used by get_location
        where the title of a section is used as an estimation of location.
        This method is also used in the code that writes the predicted
        methods to file.
        """

        pattern_title = r'(?<=<title>)(.*?)(?=<\/title>)'
        search = re.search(pattern_title, section)
        title = None
        if search:
            title = search.group(0)

        return title

    def get_location(self, section, body):
        """
        Get the location of the section of interest, using the title as
        estimation of the location of the section.
        """

        p = .5
        title = self.get_title(section)
        if title != None:
            pattern = r'{}'.format(title)
            search = re.search(pattern, body)
            if search:
                p = search.start()/len(body)

        return p
