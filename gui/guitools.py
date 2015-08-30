'''
Created on 30.08.2015

@author: mEDI
'''
from PySide import QtCore, QtGui,QtSvg


class guitools(object):


    def __init__(self, parent):
        self.parent = parent
        

    def getIconFromsvg(self, svgfile):
        svg_renderer = QtSvg.QSvgRenderer(svgfile)
        image = QtGui.QImage(48, 48, QtGui.QImage.Format_ARGB32)
        image.fill(0x00000000)
        svg_renderer.render(QtGui.QPainter(image))
        pixmap = QtGui.QPixmap.fromImage(image)
        icon = QtGui.QIcon(pixmap)
        return icon

    def setSystemComplete(self, station, editor):

        rawSysList = self.parent.mydb.getSystemsWithStationName(station)

        mylist = []
        for system in rawSysList:
            mylist.append(system["System"])

        completer = QtGui.QCompleter(mylist)
        completer.ModelSorting(QtGui.QCompleter.CaseSensitivelySortedModel)
        completer.setMaxVisibleItems(20)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        editor.setCompleter(completer)


    def setStationComplete(self, system, editor):
        rawsystemlist = self.parent.mydb.getStationsFromSystem(system)

        mylist = []
        for system in rawsystemlist:
            mylist.append(system[1])

        completer = QtGui.QCompleter(mylist)
        completer.ModelSorting(QtGui.QCompleter.CaseSensitivelySortedModel)
        completer.setMaxVisibleItems(20)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        completer.setCompletionMode(QtGui.QCompleter.UnfilteredPopupCompletion)
        editor.setCompleter(completer)

class LineEdit(QtGui.QLineEdit):
    def __init__(self, parent=None):
        QtGui.QLineEdit.__init__(self, parent)

    def focusInEvent(self, event):
        QtGui.QLineEdit.focusInEvent(self, event)
        self.completer().complete()

