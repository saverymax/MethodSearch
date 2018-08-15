"""
In the section_label.txt file from Jim, pick out all the different ways to say results, methods, conclusion, background, and objective.
The first field contains the variable name. The second field contains a consistent label, which is what I search for
"""

import re
import json

pattern_results = r"(?<=\|)(RESULTS)(?=\|)" # book behind and lookahead to see if there are | around the word. For example, ?=\| will look for | following the regex match
pattern_methods = r"(?<=\|)(METHODS)(?=\|)"
pattern_conclusions = r"(?<=\|)(CONCLUSIONS)(?=\|)"
pattern_background = r"(?<=\|)(BACKGROUND)(?=\|)"
pattern_objective = r"(?<=\|)(OBJECTIVE)(?=\|)"

pattern_list = [pattern_results, pattern_methods, pattern_conclusions, pattern_background, pattern_objective]
rexpression = re.compile('|'.join(pattern_list))

section_pattern = r"(^.*?)(?=\|)"

# probably should save in file
results_list = []
methods_list = []
conclusion_list = []
background_list = []
objective_list = []

with open("C:\\Users\\saveryme\\Documents\\full_text_project\\section_labels_jim.txt") as f:
    for line in f:
        match = rexpression.search(line)
        if match.group(0) == 'RESULTS':
            section = re.match(section_pattern, line)
            results_list.append(section.group(0))
        if match.group(0) == 'METHODS':
            section = re.match(section_pattern, line)
            methods_list.append(section.group(0))
        if match.group(0) == 'CONCLUSIONS':
            section = re.match(section_pattern, line)
            conclusion_list.append(section.group(0))
        if match.group(0) == 'BACKGROUND':
            section = re.match(section_pattern, line)
            background_list.append(section.group(0))
        if match.group(0) == 'OBJECTIVE':
            section = re.match(section_pattern, line)
            objective_list.append(section.group(0))

sections_json = {}

sections_json['results'] = results_list
sections_json['methods'] = methods_list
sections_json['conclusion'] = conclusion_list
sections_json['background'] = background_list
sections_json['objective'] = objective_list

#with open('section_lists.json', 'w') as f:
#    json.dump(sections_json, f)

#print(results_list,"\n")
#print(methods_list,"\n")
#print(conclusion_list,"\n")
#print(background_list,"\n")
print(objective_list,"\n")
