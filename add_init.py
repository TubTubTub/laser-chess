import pathlib

for one, two, three in pathlib.Path('test').walk():
    if '__init__.py' not in three:
        with open('__init__.py', 'w') as f:
            f.write('')