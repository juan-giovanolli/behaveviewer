import sys
from PyQt4 import QtGui
from service.entity_service import EntityService
from view.main_window import MainBehaveWindow


def main_ui():
    app = QtGui.QApplication(sys.argv)
    MainBehaveWindow(EntityService())
    sys.exit(app.exec_())
