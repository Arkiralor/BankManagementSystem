python -m pip install pip-tools
pip-compile --resolver=bactracking --output-file=requirements.txt requirements.in 
python -m pip install -r requirements.txt