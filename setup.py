
from setuptools import setup, find_packages
 
setup(
    name='django-oauth2app-management',
    version='0.1.1dev',
    description="Client & Token management interface for django-oauth2app",
    author='Gabriel Grant',
    author_email='g@briel.ca',
    url='https://github.com/gabrielgrant/django-oauth2app-management/',
    packages=find_packages(),
    zip_safe=False,
    install_requires=['oauth2app'],
)
