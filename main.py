'''
Created on 24 de may. de 2016

@author: Juan
'''
import argparse
from config.setup import Setup
from main_ui import main_ui
from main_no_ui import main_no_ui


def main(ui_flag):
    Setup({'reset_db': True, 'dummy_db': False})
    if ui_flag:
        main_ui()
    else:
        main_no_ui()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--no-ui', action='store_const', const=True,
                        help='Runs parser without UI and prints on stdout')
    args = parser.parse_args(['--no-ui'])

    main(args.no_ui)
