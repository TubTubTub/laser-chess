from pathlib import Path

root = (Path(__file__).parent / '../../data').resolve()

already_added = [
    '../../data/main.py',
    '../../data/loading_screen.py',
    '../../data/utils/asset_helpers.py',
    '../../data/utils/data_helpers.py',
    '../../data/utils/widget_helpers.py',
    '../../data/managers/theme.py',
    '../../data/states/game/components/laser_draw.py',
    '../../data/states/game/components/particles_draw.py',
    '../../data/widgets/bases/widget.py',
    '../../data/widgets/bases/circular.py',
    '../../data/components/circular_linked_list.py',
    '../../data/components/custom_event.py',
    '../../data/widgets/reactive_icon_button.py',
    '../../data/widgets/reactive_button.py',
    '../../data/widgets/colour_slider.py',
    '../../data/widgets/text_input.py',
    '../../data/states/game/mvc/game_model.py',
    '../../data/states/game/mvc/game_view.py',
    '../../data/states/game/mvc/game_controller.py',
    '../../data/states/game/components/board.py',
    '../../data/states/game/components/bitboard_collection.py',
    '../../data/states/game/cpu/engines/minimax.py',
    '../../data/states/game/cpu/engines/alpha_beta.py',
    '../../data/states/game/cpu/engines/transposition_table.py',
    '../../data/states/game/cpu/engines/iterative_deepening.py',
    '../../data/states/game/cpu/evaluator.py',
    '../../data/states/game/cpu/cpu_thread.py',
    '../../data/states/game/cpu/zobrist_hasher.py',
    '../../data/states/game/cpu/transposition_table.py',
    '../../data/states/review/review.py',
    '../../data/database/migrations/create_games_table_19112024.py',
    '../../data/database/migrations/change_fen_string_column_name_23122024.py',
    '../../data/utils/database_helpers.py',
    '../../data/managers/shader.py',
    '../../data/shaders/fragments/highlight_brightness.frag',
    '../../data/shaders/classes/blur.py',
    '../../data/shaders/fragments/blur.frag',
    '../../data/shaders/classes/bloom.py',
    '../../data/shaders/fragments/occlusion.frag',
    '../../data/shaders/fragments/shadowmap.frag',
    '../../data/shaders/fragments/lightmap.frag',
    '../../data/shaders/classes/rays.py'
]

with open('documentation/source/source.tex', 'w') as f:
    f.writelines([
        '\documentclass[../main/main.tex]{subfiles}\n',
        '\n',
        '\\begin{document}\n',
        '\\newpage\n',
        '\n',
        '\\chapter{Source Code}\n',
        '\\addtocontents{toc}{\setcounter{tocdepth}{-1}}\n',
        '\n'
    ])

    # ADD \label TO WIDGETS FOLDER

    for dir_path, dir_names, file_names in root.walk():
        index = str(dir_path).index('data')
        path_suffix = str(dir_path)[index:]

        if len(file_names) > 0 and dir_path.name != '__pycache__':
            path_name = path_suffix.replace('\\', '\\textbackslash ').replace('_', '\_')
            f.write(f'\section{{{path_name}}}\n')
        
        for file in file_names:
            file_path = f'..\..\{path_suffix}\{file}'.replace('\\', '/')
            extension = file.split('.')[1]
            depth = len(dir_path.parents) - 6

            if extension not in ['py', 'json', 'vert', 'frag']:
                continue
            
            f.write(f'\subsection{{{file.replace('_', '\_')}}}\n')

            if file_path in already_added:
                f.write(f'See Section \\ref{{src:{file_path}}}.\n\n')
                continue
            
            match file.split('.')[1]:
                case 'py':
                    f.write(f'\lstinputlisting{{{file_path}}}\n')
                case 'json':
                    f.write(f'\lstinputlisting[language=json]{{{file_path}}}\n')
                case 'vert':
                    f.write(f'\lstinputlisting[language=GLSL]{{{file_path}}}\n')
                case 'frag':
                    f.write(f'\lstinputlisting[language=GLSL]{{{file_path}}}\n')
            
            label = file_path[6:]
            f.write(f'\label{{src:{label}}}\n\n')
    
    f.write('\end{document}')