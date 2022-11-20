from setuptools import setup, find_packages

setup(
    name='sife',
    version='3.0.0',
    py_modules=['sife'],
    install_requires=[
        'Click', 'termcolor', 'dropbox', 'random2', 'pyperclip', 'openpyexcel', 'pygithub'
    ],
    entry_points={
        'console_scripts': [
            'sife = sife:cli'
        ]
    }
    
)
