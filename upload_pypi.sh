rm -rf dist &&
python3 setup.py sdist bdist_wheel &&
rm -rf build pymusicdl/__pycache__ pymusicdl\modules\__pycache__ &&
twine upload dist/*