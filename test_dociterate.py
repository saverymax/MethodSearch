import os

def doc_iterate(directory, journal):
    """
    Iterate through docs in a journal and print titles/secs within body
    """

    doc_directory = '{0}\\{1}'.format(directory, journal)

    for document in os.listdir(doc_directory):
        yield document

def journal_iterate(directory):
    """
    Iterate through all journals
    Calls doc_iterate which will iterate through all document in each journal
    """

    for journal in os.listdir(directory):
        yield journal

directory = 'C:\\Users\\saveryme\\Documents\\full_text_project\\full_texts_all\\'

journal_generator = journal_iterate(directory)

doc_cnt = 0
j_cnt = 0

for journal in journal_generator:
    j_cnt += 1
    document_generator = doc_iterate(directory, journal)
    for doc in document_generator:
        doc_cnt += 1

print("journals", j_cnt)
print("docs", doc_cnt)
