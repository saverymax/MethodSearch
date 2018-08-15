"""
Main script for the method classifier

Running this script will parse each line of the xml containing the full texts,
and iterate through each section, separating methods from everything else

The methods will be saved in individual? .txt files named with the PMID of the article they were
taken from, the probability of the category assignment, and the title of the method section, if available.

Information regarding the SVM model can be found in README.txt
"""

import parser_fulltext
import re
import lxml.etree as le
from title_feature import title_featurer
from location_feature import location_featurer
from item_select import ItemSelector
from sklearn.externals import joblib
from sklearn.svm import SVC

if __name__ == "__main__":

    # init parser
    fulltext_parser = parser_fulltext.parser()

    # load tyour choice of model
    #model = joblib.load('method_classifier_trigrams.pkl')
    model = joblib.load('method_classifier_location_probability.pkl')
    #model = joblib.load('method_classifier_probability.pkl')
    # Open file to write to
    method_file = open("methods_predicted_fullsec.txt" , "w", encoding="utf")
    method_file.close()
    method_file = open("methods_predicted_fullsec.txt" , "a+", encoding="utf")

    cnt = 0
    # access the full texts!
    with open('C:\\Users\\saveryme\\Documents\\full_text_project\\xml_per_line_1200_jim') as f:
        for line in f:
            cnt += 1
            if cnt % 100 == 0:
                print("Article #", cnt)

            # get id
            pattern_id = r'\d+'
            pmid = re.match(pattern_id, line).group(0)
            # remove pesky id
            pattern = r'\d+\|'
            line = re.sub(pattern, '', line)

            try:
                root = le.fromstring(line)

                # iterate through each section in the body of the article and classify the section
                for section in fulltext_parser.iterate_body(root):

                    #prediction = model.predict([section]) # if single section, make sure to add [sec]
                    data_dict = {'text': section, 'location': location}
                    y_probability = model.predict_proba([section])

                    if y_probability[0][0] > .5:
                        methods, other = zip(model.classes_, y_probability[0])
                        # write the section to file
                        #section_title = fulltext_parser.get_title(section)
                        # method_line = "{0}|{1}|{2}|{3}|{4}\n".format(pmid, section_title, methods, other, section)
                        # method_file.write(method_line)

                        # or write the children of the section:
                        for section_child in fulltext_parser.iterate_sec(section):
                            section_title = fulltext_parser.get_title(section_child)
                            method_line = "{0}|{1}|{2}|{3}|{4}\n".format(pmid, section_title, methods, other, section_child)
                            method_file.write(method_line)

            except le.XMLSyntaxError as e:
                #print("here's the problem", line[57765:57779])
                print("lxml error")

    method_file.close()
