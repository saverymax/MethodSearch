import lxml.etree as le
from lxml import objectify
import re
from collections import Counter
from io import BytesIO


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

            for child in body:
                try:
                    # convert the child to text, which the svm can handle
                    # but keep xml tags, as the classifier was trained with
                    # them included.
                    section_xml = le.tostring(child, encoding='unicode', method='xml')
                    location = self.get_location(child, body)

                    yield section_xml, location

                except:
                    # if error in body, let's just move on to next section.
                    print("Error iterating through the body")

    def iterate_sec(self, sec):
        """
        iterate through children of sec in order to improve readability.
        The children are provided by run_model.py
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
        Get the title from the section. This method is used
        to find the title when writing the predicted
        methods to file. This is NOT used by title_featurer
        """

        root = le.fromstring(section)

        # Check to see if the root is a title section, or if there is a
        # title as a child tag
        title = None
        if root.tag == "title":
            title = root.text
        else:
            title = root.find(".//title")
            #print(title)
            if hasattr(title, "text"):
                title = title.text

        return title

    def get_location(self, section, body):
        """
        Get the location of the section of interest, by looking for
        a string match in the body. The location estimate is
        calculated as beginning of match / length of body
        in units of characters
        """

        # get the strings for doing some matching
        body_text = le.tostring(body, encoding='unicode', method='text')
        section_text = le.tostring(section, encoding='unicode', method='text')
        # Preset p
        p = .5

        section_clean = re.sub(r"[\*\?\.\$\(\)\^\-\+\{\}\[\]\\\|]", "", section_text)
        body_clean = re.sub(r"[\*\?\.\$\(\)\^\-\+\{\}\[\]\\\|]", "", body_text)
        #pattern = r'{}'.format(title)
        #search = re.search(title, body_text)
        try:
            search = re.search(section_clean, body_clean)
            if search:
                p = search.start()/len(body_text)

        except re.error:
            print("I'm having some trouble finding the location of the section")

        return p
