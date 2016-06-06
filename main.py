'''
Created on 24 de may. de 2016

@author: Juan
'''
import argparse
from config.setup import Setup
from main_ui import main_ui
from main_no_ui import main_no_ui

parsing_directory = ''


def main(ui_flag, parsing_directory=None):
    Setup({'reset_db': False, 'dummy_db': False})
    if ui_flag:
        main_no_ui(parsing_directory)
    else:
        main_ui()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--dir', nargs=1)
    parser.add_argument('--no-ui', action='store_true',
                        help='Runs parser without UI and creates the csv file')

    import sys
    print "HOLA        ", sys.argv
    args = parser.parse_args()
    print args.dir
    main(args.no_ui, args.dir[0])
