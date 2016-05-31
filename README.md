#Installation

##Ubuntu

>$ sudo apt-get install build-essential

Download from http://www.riverbankcomputing.com/software/sip/download

>$ python configure.py

>$ make

>$ sudo make install

Then copy
/usr/local/lib/python2.7/site-packages/sipconfig.py
   
/usr/local/lib/python2.7/site-packages/sipdistutils.py
   
/usr/local/lib/python2.7/site-packages/sip.pyi
   
/usr/local/lib/python2.7/site-packages/sip.so 
   
to the .../site-packages directory in virtualenv environment

>$ sudo apt-get install qt4-dev-tools

Download from http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.4/PyQt-x11-gpl-4.11.4.tar.gz

>$ python configure.py

>$ make

>$ sudo make install 

Then install extra project requirements using pip
>$ pip install requirements.txt

#####PyQt in virtualenv:

Copy /usr/local/lib/python2.7/site-packages/PyQt4 directory into the .../site-packages directory in virtualenv environment


##Fedora

>$ sudo dnf install gcc-c++

>$ sudo dnf install PyQt4

Install sip from source https://www.riverbankcomputing.com/software/sip/download/

>$ python configure.py

>$ make

>$ sudo make install

Then install extra project requirements using pip
>$ pip install requirements.txt

#####PyQt in virtualenv:

Copy /usr/local/lib/python2.7/site-packages/PyQt4 directory into the .../site-packages directory in virtualenv environment

##Windows

#####Requirements:
* PyQt4
* pip
* python2.7



