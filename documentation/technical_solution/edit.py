import fileinput
import sys

for line in fileinput.input("documentation/technical_solution/technical_solution.tex", inplace=True):
    if line.startswith('\\lstinputlisting'):
        path = line.split('{')[1][:-2]
        idx = line.index('{')

        if '.frag' in line or '.vert' in line:
            sys.stdout.write(f'\lstinputlisting[language=GLSL, label=src:{path}]{line[idx:]}')
        else:
            sys.stdout.write(f'\lstinputlisting[label=src:{path}]{line[idx:]}')
    else:
        sys.stdout.write(line)