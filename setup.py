from distutils.core import setup
import setuptools

with open("README.md","r") as f:
    long_description = f.read()

setuptools.setup(
    name = 'pymusicdl_termux',
    packages = setuptools.find_packages(),
    version = '0.1.0',
    license='MIT',
    description = 'Download spotify and youtube playlists on Termux',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author = 'C Vamshi Krishna',
    author_email = 'cvamshik1@gmail.com',
    url = 'https://github.com/insaiyancvk/pymusicdl/tree/pymusicdl-termux',
    keywords = [
    'spotify', 
    'youtube', 
    'music download',
    'music',
    'youtube download',
    'spotify download',
    'termux'
    ],
    include_package_data=True,
    install_requires=[
      'pafy',
      'pytube',
      'requests',
      'rich',
      'spotipy',
      'urllib3',
      'youtube-dl',
      'youtube-title-parse'
      ],
    classifiers=[
      'Development Status :: 5 - Production/Stable',
      'Intended Audience :: End Users/Desktop ',
      'Topic :: Software Development :: Build Tools',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3.8'
    ]
)