"""
Make a database of only the children of the children of the body
"""

# for i, row in df.iterrows():
#
#     # iterate through the sections
#     try:
#         root = le.fromstring(row['text'])
#     except BaseException as e:
#         # print(e, row['text'])
#         # print(child.text,"\n\n")
#         pass
#
#     for child in root:
#         try:
#             section = le.tostring(child, encoding = 'unicode', method = 'xml')
#             #print(section,"\n")
#             prediction = model.predict([section])
#             y_predictions.append(prediction)
#             y_true.append(row['label'])
#
#         except BaseException as e:
#             raise
#             #print(e, row['text'])
#             #print(child.text)
