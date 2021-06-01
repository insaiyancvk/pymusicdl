rm -rf dist
python setup.py sdist bdist_wheel
rm -rf build pymusicdl_termux/__pycache__ pymusicdl_termux\modules\__pycache__
twine upload dist/*