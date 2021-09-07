#Python Package Publication

```bash
rm -rf build/
rm -rf dist/
rm -rf zen-publish.egg-info
pip install --upgrade setuptools wheel
python3 setup.py sdist bdist_wheel
pip install --upgrade twine
python3 -m twine upload dist/*
```
