SubstanceD blog
===============

Blog engine on SubstanceD_
This repository originated from demo blog app provided by SubstanceD_ itself.

Now this project is experimental and for learning SubstanceD_. 

Additional features
-------------------
This project contains a variety of additional features compared with original demo app:

* Tag
* Flat Page
* Search (English/Japanese)

Installation
------------
::

    $ # Install substanced
    $ git clone https://github.com/Pylons/substanced
    $ cd substanced
    $ python setup.py develop
    $ cd ..
    $ # Install guess_langueage for Python3
    $ hg clone https://bitbucket.org/spirit/guess_language
    $ cd guess_language
    $ python setup.py install
    $ cd ..
    $ # Install substanced-blog
    $ git clone https://github.com/hirokiky/substanced-blog/
    $ cd substanced-blog
    $ python sedup.py develop
    $ # Setup IPA dictionary for Japanese MA
    $ bash getigoipadic.sh


.. _SubstanceD: http://substanced.net/

Run
---
::

    $ pserve development.ini

