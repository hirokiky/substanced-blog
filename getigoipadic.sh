#!/bin/bash
# This bash script is to get the IPA dictionary for igo,
# allow to morpholigical analysis of Japanese for this blog application.
# You won't install anything. this script is for just downloading and compiling the dic.
# Actual process for MA is provided by igo-python.
#
# This will do:
# * create 'ipadic' directory here
# * download mecab-ipadic
# * download jar of igo
# * compile dic
#
# And then you will get 'ipadic/igo_ipadic' dictionary file.

if [ ! -a ./ipadic ]
then
    mkdir ./ipadic
fi
cd ipadic

# Get Mecab IPA dictionary
if [ ! -a ./mecab-ipadic-2.7.0-20070801.tar.gz ]; then
    echo "Download IPA dictionary."
    curl -O http://mecab.googlecode.com/files/mecab-ipadic-2.7.0-20070801.tar.gz
fi
tar zxvf mecab-ipadic-2.7.0-20070801.tar.gz

# Get igo to translate IPD dictionary to igo format
# This process wiell need a lot of memory, so this command allow to use 1G memory as heap
if [ ! -a ./igo-0.4.5.jar ]; then
    echo "Download igo to build the dic."
    curl -O http://jaist.dl.sourceforge.jp/igo/55029/igo-0.4.5.jar
fi
java -Xmx1024m -cp igo-0.4.5.jar net.reduls.igo.bin.BuildDic ./igo_ipadic mecab-ipadic-2.7.0-20070801 EUC_JP
