from setuptools import find_packages, setup

setup(
    name='flask_module',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
    'async>=1.10',
    'attrs>=22.1.0',
    'bcrypt>=4.0.1',
    'beautifulsoup4>=4.11.1',
    'blinker>=4.0.1',
    'certifi>=2022.9.24',
    'cffi>=1.15.1',
    'charset-normalizer>=2.1.1',
    'click>=8.1.3',
    'colorama>=0.4.5',
    'comtypes>=1.1.14',
    'cryptography>=38.0.1',
    'dnspython>=2.2.1',
    'email-validator>=1.3.0',
    'exceptiongroup>=1.0.0rc9',
    'Flask>=2.2.2',
    'Flask-Admin>=1.6.0',
    'Flask-Bcrypt>=1.0.1',
    'Flask-JWT>=0.3.2',
    'Flask-Login>=0.6.2',
    'Flask-Mail>=0.9.1',
    'flask-module>=1.0.0',
    'Flask-RESTful>=0.3.9',
    'Flask-SQLAlchemy>=3.0.0',
    'Flask-WTF>=1.0.1',
    'sniffio>=1.3.0',
    'sortedcontainers>=2.4.0',
    'soupsieve>=2.3.2.post1',
    'SQLAlchemy>=1.4.41',
    'tqdm>=4.64.1',
    'trio>=0.22.0',
    'trio-websocket>=0.9.2',
    'twilio>=7.15.1',
    'urllib3>=1.26.12',
    'webdriver-manager>=3.8.3',
    'Werkzeug>=2.2.2',
    'wsproto>=1.2.0',
    'WTForms>=3.0.1',
]
)