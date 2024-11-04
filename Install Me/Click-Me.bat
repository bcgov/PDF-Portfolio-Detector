@echo off


:start
cls

set python_ver=39

python ./get-pip.py

cd \
cd \python%python_ver%\Scripts\
pip install Spire.Pdf==10.1.1
pip install pypdf2
pip install Pillow==9.5.0
pip install tk
pip install pypdf
pip install pycryptodome
pip install pygame


pause
exit