from setuptools import setup, find_packages

setup(
    name='subscription_management',
    version='1.0.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'psycopg2-binary==2.9.3',
        'python-dotenv==0.20.0',
        'structlog==22.1.0',
        'flask==2.3.2',
        'gunicorn==20.1.0'
    ],
    extras_require={
        'dev': [
            'pytest==7.1.2',
            'pytest-cov==4.0.0',
            'flake8==6.0.0',
            'black==23.3.0',
            'mypy==1.3.0'
        ]
    },
    author='Craig Erdmann',
    author_email='craig.erdmann@postman.com',
    description='Subscription Management System',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)