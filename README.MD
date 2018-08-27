# Repository for classification of method sections from full text articles


To install:
```
git clone https://github.com/saverymax/MethodSearch.git
```

To run the model from the windows command line:
```
cd MethodSelector
python run_model.py --path path\to\xml\fulltexts.xml

```
The fulltexts.xml must contain one fulltext per line. 


## Dependencies

Python 3.6.5
[sklearn](http://scikit-learn.org/stable/install.html)
[lxml](https://lxml.de/installation.html)
[nltk](http://www.nltk.org/install.html)

