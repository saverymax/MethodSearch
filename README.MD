# Classification of method sections

This repository contains the SVM model and python modules used to identify method sections in full text articles. 


To install:
```
git clone https://github.com/saverymax/MethodSearch.git
```

To run the model from the windows command line:
```
cd MethodSelector-master
python run_model.py --path path\to\xml\fulltexts.txt

```

For example:
```
python run_model.py --path C:\Users\saveryme\Documents\MethodSearch\sample_xml\sample_xml.txt
```
will pull the method sections from the sample texts provided with repository

The fulltexts must be a text file with one fulltext per line. 

## Dependencies

Python 3.6.5
[sklearn](http://scikit-learn.org/stable/install.html)\n
[lxml](https://lxml.de/installation.html)\n
[nltk](http://www.nltk.org/install.html)

## Debugging
