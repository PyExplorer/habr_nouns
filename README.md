habr_nouns
==

Parse n pages of the general feed of habr.com,  pull out the headings and dates of the articles from them. 
Put all nouns in a normal form and output the three most popular nouns for each week.

Example
--

**From command line:**

*$ python3 habr_nouns.py* 

-------------------------------------------------------------

| Начало недели | Конец недели | Популярные слова           |

-------------------------------------------------------------
|   23/04/2018  |  29/04/2018  | часть, разработка, система |

|   30/04/2018  |  06/05/2018  | плагин, миф, часть         |

-------------------------------------------------------------

Requirements
--

- at least python 3.5

- bs4

- pymorphy2

- pymorphy2-dicts-ru


Installation
--

just clone the project and install the requirements:


*$ git clone https://github.com/PyExplorer/habr_nouns.git*

*$ cd habr_nouns*

*$ pip3 install -r requirements.txt*


Docs
--

The script has 1 option to run:

**-p (--pages)** - number of pages for parsing 

**default:** 20 

*example:* *$ python3 habr_nouns.py -p 2*


Contributing
--

To contribute, pick an issue to work on and leave a comment saying that you've taken the issue. Don't forget to mention when you want to submit the pull request.


Launch tests
--

*$ python3 -m unittest*
