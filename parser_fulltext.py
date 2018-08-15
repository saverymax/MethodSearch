import lxml.etree as le
import re


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
            # get the length of the body here
            #body_string = le.tostring(body, encoding = 'unicode', method = 'xml')
            #body_len = len(body_string
            for child in body:
                try:
                    # convert the child to something the svm can handle
                    section = le.tostring(child, encoding = 'unicode', method = 'xml')
                    # find where section is in body, return that/body_len
                    yield section
                except BaseException as e:
                    print("Error iterating through the body;", e)

    def iterate_sec(self, sec):
        """
        iterate through children of sec to get more granularity
        """

        bit = le.fromstring(sec)
        len_bit = len(bit)
        if len_bit == 0:
            yield le.tostring(bit, encoding = 'unicode', method = 'xml')
        else:
            for child_bit in bit:
                 yield le.tostring(child_bit, encoding = 'unicode', method = 'xml')

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
