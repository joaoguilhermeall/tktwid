start ./env/Scripts/activate.bat
pip freeze | Out-File -encoding ascii requirements.txt
python setup.py install
python setup.py upgrade
deactivate