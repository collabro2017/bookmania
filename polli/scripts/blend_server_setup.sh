#!/bin/bash

# Install JAVA
sudo yum install -y java-1.8.0-openjdk.x86_64
sed -i '$a export JAVA_HOME=/usr/lib/jvm/jre-1.8.0-openjdk.x86_64' ~/.bash_profile

# Install Development Tools
sudo yum groupinstall -y 'Development Tools'

# Download NLTK Data
/opt/python/run/venv/bin/python -m nltk.downloader 'punkt'

# Install Git
sudo yum install -y git

# Clone Giza++
git clone https://github.com/moses-smt/giza-pp.git /home/ec2-user/giza-pp/
sed -i 's/-DBINARY_SEARCH_FOR_TTABLE -DWORDINDEX_WITH_4_BYTE/ /g' /home/ec2-user/giza-pp/GIZA++-v2/Makefile
cd /home/ec2-user/giza-pp/
make
sed -i '$a export GIZA=/home/ec2-user/giza-pp' ~/.bash_profile

# Standford POS Tagger
cd /home/ec2-user/
wget https://nlp.stanford.edu/software/stanford-postagger-full-2016-10-31.zip
unzip stanford-postagger-full-2016-10-31.zip -d stanford-postagger
rm stanford-postagger-full-2016-10-31.zip
sed -i '$a export STANFORD_POS=/home/ec2-user/stanford-postagger/stanford-postagger-full-2016-10-31' ~/.bash_profile

# Clone Mose Decoder
git clone https://github.com/moses-smt/mosesdecoder.git
sed -i '$a export MOSES=/home/ec2-user/mosesdecoder' ~/.bash_profile