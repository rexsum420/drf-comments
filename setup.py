from setuptools import setup, find_packages

setup(
    name='drf-comments',
    version='1.2.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'djangorestframework>=3.15.2',
        'Django>=5.0.6',
    ],
    author='Jeffery Springs',
    author_email='rexsum420@gmail.com',
    description='A library for adding comments to models using Django REST Framework.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/rexsum420/drf-comments',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Framework :: Django :: 5.0',
        'Framework :: Django :: 4.0',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
