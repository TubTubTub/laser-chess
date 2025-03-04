import fileinput
import sys

for line in fileinput.input("documentation/technical_solution/technical_solution.tex", inplace=True):
    if line.startswith('\\lstinputlisting'):
        path = line.split('{')[1][:-2]
        idx = line.index('{')
        sys.stdout.write(f'{line[:idx]}[label=src:{path}]{line[idx:]}')
    else:
        sys.stdout.write(line)