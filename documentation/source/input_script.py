from pathlib import Path

root = (Path(__file__).parent / '../../data').resolve()

with open('documentation/source/input_lines.txt', 'w') as f:
    for dir_path, dir_names, file_names in root.walk():
        index = str(dir_path).index('data')
        path_suffix = str(dir_path)[index:]

        if len(file_names) > 0 and dir_path.name != '__pycache__':
            f.write(f'\section{{{path_suffix}}}\n')
        
        for file in file_names:
            file_path = f'..\..\{path_suffix}\{file}'.replace('\\', '/')
            extension = file.split('.')[1]
            depth = len(dir_path.parents) - 6

            if extension not in ['py', 'json']:
                continue
            
            f.write(f'\subsection{{{file}}}\n')
            
            if file.split('.')[1] == 'py':
                f.write(f'\lstinputlisting{{{file_path}}}\n')
            
            elif file.split('.')[1] == 'json':
                f.write(f'\lstinputlisting[language=json]{{{file_path}}}\n')