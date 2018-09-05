# Classification of method sections

This repository contains the SVM model and python modules used to identify method sections in full text articles.


To install:
```
git clone https://github.com/saverymax/MethodSearch.git
```

To run the model from the windows command line:
```
cd MethodSelector
python run_model.py --path path\to\xml\fulltexts.txt

```

For example, if you have successfully navigated to the MethodSearch directory,
the command below will pull the method sections from the sample texts provided with the repository.
```
python run_model.py --path sample_texts\sample_fulltexts.txt
```
The methods are saved, line by line, in a .txt file in the predictions directory. The name of the file is currently hard coded to methods_predicted_fullsec.txt

The fulltexts must be a text file with one fulltext per line.

## Dependencies

Python 3<br>
[sklearn](http://scikit-learn.org/stable/install.html) version 0.19.1<br>
[lxml](https://lxml.de/installation.html) version 4.2.1 <br>
[nltk](http://www.nltk.org/install.html) version 3.3 <br>

## Model and Features

The model currently used can be found in the model directory. It is accessed
in run_model.py. It is an SVM with a linear kernel, and default hyperparameters.
To see defaults and for more details go to http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html. The features used
are as follow:
  1. TF-IDF bag-of-words of section
  2. Location of section
  3. Binary label indicating whether or not title of section appears in a constant
  list of synonyms/phrases for "method". 

## Debugging

The parser may encounter xml formatting errors. In these cases, the article will be skipped and the lxml error and line number of the of the article will be printed. If an error occurs while parsing the body or sections of the text, parser_fulltext.py will let you know but continue with the next body or section. This isn't necessarily a
reliable way to handle errors that the parser generator might throw, but it works.

Since most of the work is done in run_model.py, that is the best place to start debugging
if a non-obvious error is thrown.

The most difficult type of bugs to fix are those that occur within the model, as these usually result from data-format errors relating to the sklearn pipelines used to construct and train the model. In this case, an error traceback should lead to model.predict_proba(data_dict). In these cases it is best to look at the custom features (location_feature.py, title_feature.py, and item_select.py).
