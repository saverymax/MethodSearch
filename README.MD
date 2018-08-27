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

For example, the command below will pull the method sections from the sample texts provided with the repository. 
```
python run_model.py --path C:\Users\saveryme\Documents\MethodSearch\sample_texts\sample_fulltexts.txt
```
The methods are saved, line by line, in a .txt file in the predictions directory. The name of the file is currently 
hard coded to methods_predicted_fullsec.txt

The fulltexts must be a text file with one fulltext per line. 

## Dependencies

Python 3.6.5<br>
[sklearn](http://scikit-learn.org/stable/install.html)<br>
[lxml](https://lxml.de/installation.html)<br>
[nltk](http://www.nltk.org/install.html)<br>

## Debugging

The parser may encounter xml formatting errors. In these cases, the article will be skipped and the error and line number of the 
of the article will be printed.
