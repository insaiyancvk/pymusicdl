python setup.py sdist bdist_wheel
rm -rf build
twine upload --repository testpypi dist/*