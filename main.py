'''
Created on 24 de may. de 2016

@author: Juan
'''
import argparse
from config.setup import Setup
from main_ui import main_ui
from main_no_ui import main_no_ui

parsing_directory = ''


def main(ui_flag, parsing_directory=None, stdout=None):
    Setup({'reset_db': False, 'dummy_db': False})
    if ui_flag:
        main_no_ui(parsing_directory, stdout)
    else:
        main_ui()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--dir', nargs=1, help='Feature directory from project.')
    parser.add_argument('--no-ui', action='store_true',
                        help='Runs parser without UI and creates the csv file. Delimiter=";"')
    parser.add_argument('--stdout', action='store_true', help='Print data on stdout.')

    args = parser.parse_args()
    if args.no_ui:
        main(args.no_ui, args.dir[0], args.stdout)
    else:
        main(args.no_ui, None, None)
