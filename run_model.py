"""
Main script for the method classifier

To run this script, a xml file containing one full text article per line
must be provided as input. This script will parse each line
and, using full_text_parser.py, iterate through each section in the article.

Sections predicted to have a probability of being a method
greater than 50% will be written to a file named
methods_predicted_fullsec.txt, line by line.

Should there be an xml error, the parser will print the
line number in the input file and skip that article.

Information regarding the models can be found in README.md
"""

import parser_fulltext
import re
import argparse
import lxml.etree as le
from title_feature import title_featurer
from location_feature import location_featurer
from item_select import ItemSelector
from sklearn.externals import joblib
from sklearn.svm import SVC

def get_parser():
    """
    Set up command line options. Currently, only path to file is an option
    """

    parser = argparse.ArgumentParser(description = "method classifier")
    parser.add_argument("--path",
                        dest = "path",
                        help = "The full path of the full text xml")
    return parser

def classify(args):
    """
    Main function to run the model. This will initiate the parser,
    load the model, and, iterating through the sections, identify the
    method sections and write them to methods_predicted_fullsec.txt
    """

    # init parser
    fulltext_parser = parser_fulltext.parser()

    # load your choice of model
    print("Loading model...\n")
    model = joblib.load('model\\method_classifier_location_probability.pkl')

    # Open file to write to
    method_file = open("predictions\\methods_predicted_fullsec.txt" , "w", encoding="utf")
    method_file.close()
    method_file = open("predictions\\methods_predicted_fullsec.txt" , "a+", encoding="utf")

    cnt = 0
    # access the full texts!
    with open(args.path) as f:

        print("Reading and predicting...\n")

        # pattern to get article id
        pattern_id = r'\d+'
        pattern_carriage = r'\d+\|'

        for line in f:
            cnt += 1
            if cnt % 100 == 0:
                print("I've reached article #", cnt)

            # get id
            pmid = re.match(pattern_id, line).group(0)
            # remove pesky id
            line = re.sub(pattern_carriage, '', line)

            try:
                root = le.fromstring(line)
                # Get rid of namespaces titles can be matched
                le.cleanup_namespaces(root)
                # iterate through each section in the body of the article and classify the section
                for section, location in fulltext_parser.iterate_body(root):
                    data_dict = {'text': [section], 'location': [location]}
                    y_probability = model.predict_proba(data_dict)

                    # Save the method section of the predicted probability is greater than 50%
                    if y_probability[0][0] > .5:
                        methods, other = zip(model.classes_, y_probability[0])

                        # write the whole section to file
                        #section_title = fulltext_parser.get_title(section)
                        # method_line = "{0}|{1}|{2}|{3}|{4}\n".format(pmid, section_title, methods, other, section)
                        # method_file.write(method_line)

                        # or write the children of the section, which might
                        #make for better readability:
                        for section_child in fulltext_parser.iterate_sec(section):
                            section_title = fulltext_parser.get_title(section_child)
                            method_line = "{0}|{1}|{2}|{3}|{4}\n".format(pmid, section_title, methods, other, section_child)
                            method_file.write(method_line)

            except le.XMLSyntaxError as e:
                print("lxml error:", e, "on line", cnt)
                continue

    print("Saving predictions!")
    method_file.close()


if __name__ == "__main__":
    # get the arguments and run the model
    parser = get_parser()
    args = parser.parse_args()
    classify(args)
