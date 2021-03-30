# Running tests

Prep the environment:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run tests (inside `test.py`):

```
python -m unittest test.FlaskTests
```