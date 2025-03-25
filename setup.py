# #!/usr/bin/env python

# from setuptools import setup, find_packages
# import os
# from olp import __version__

# PACKAGE_DIR = os.path.abspath(os.path.dirname(__file__))
# README_PATH = os.path.join(PACKAGE_DIR, 'README.rst')
# os.chdir(PACKAGE_DIR)

# with open(README_PATH) as readme:
#      file_description = readme.read()

# setup(
#     name='olp',
#     version=__version__,
#     url="https://github.com/Rediker-Software/olp",
#     author="Kevin Brown",
#     author_email="kbrown@rediker.com",
#     description="Object-level permissions across multiple models for Django.",
#     long_description=file_description,
#     license="MIT",
#     packages=find_packages(exclude=["tests*", ]),
#     zip_safe=True,
#     include_package_data=True,
#     install_requires=[
#         'Django>=1.3',
#     ],
#     # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
#     classifiers=[
#         'Development Status :: 3 - Alpha',
#         'Environment :: Web Environment',
#         'Framework :: Django',
#         'Intended Audience :: Developers',
#         'License :: OSI Approved :: MIT License',
#         'Programming Language :: Python',
#         'Programming Language :: Python :: 2.7',
#         'Programming Language :: Python :: 3.4',
#     ]
# )


#!/usr/bin/env python

from setuptools import setup, find_packages
import os
from olp import __version__

PACKAGE_DIR = os.path.abspath(os.path.dirname(__file__))
README_PATH = os.path.join(PACKAGE_DIR, 'README.rst')
os.chdir(PACKAGE_DIR)

with open(README_PATH) as readme:
     file_description = readme.read()

setup(
    name='olp',
    version=__version__,
    url="https://github.com/Rediker-Software/olp",
    author="Kevin Brown",
    author_email="kbrown@rediker.com",
    description="Object-level permissions across multiple models for Django.",
    long_description=file_description,
    license="MIT",
    packages=find_packages(exclude=["tests*", ]),
    zip_safe=True,
    include_package_data=True,
    install_requires=[
        'Django==4.2.20',
    ],
    # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.11',
    ]
)

