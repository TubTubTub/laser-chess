import pathlib

for one, two, three in pathlib.Path('data').walk():
    if '__init__.py' not in three:
        with open((one / '__init__.py').resolve(), 'w') as f:
            f.write('')