from distutils.core import setup
import setuptools

with open("README.md","r") as f:
    long_description = f.read()

setup(
  name = 'pymusicdl',
  packages = setuptools.find_packages(),
  version = '1.0.3.1',
  license='MIT',
  description = 'Download spotify and youtube playlists!',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'C Vamshi Krishna',
  author_email = 'cvamshik1@gmai.com',
  url = 'https://github.com/insaiyancvk/pymusicdl/tree/pure-python',
  download_url = 'https://github.com/insaiyancvk/pymusicdl/archive/refs/heads/pure-python.zip',
  keywords = ['spotify', 'youtube', 'music download','music','youtube download','spotify download'],
  install_requires=['certifi==2020.12.5',
                    'chardet==4.0.0',
                    'colorama==0.4.4',
                    'commonmark==0.9.1',
                    'idna==2.10',
                    'pafy==0.5.5',
                    'Pygments==2.8.1',
                    'pytube==10.7.2',
                    'requests==2.25.1',
                    'rich==10.1.0',
                    'six==1.15.0',
                    'spotipy==2.18.0',
                    'typing-extensions==3.10.0.0',
                    'urllib3==1.26.4',
                    'youtube-dl==2021.4.26',
                    'youtube-title-parse==1.0.0'],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8'
  ],
)