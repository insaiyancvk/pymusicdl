from distutils.core import setup
import setuptools

with open("README.md","r") as f:
    long_description = f.read()

setuptools.setup(
    name = 'pymusicdl',
    packages = setuptools.find_packages(),
    version = '0.0.2',
    license='MIT',
    description = 'Download spotify and youtube playlists!',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author = 'C Vamshi Krishna',
    author_email = 'cvamshik1@gmai.com',
    url = 'https://github.com/insaiyancvk/pymusicdl/tree/pure-python',
    keywords = [
    'spotify', 
    'youtube', 
    'music download',
    'music',
    'youtube download',
    'spotify download'
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
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3.8'
    ]
)