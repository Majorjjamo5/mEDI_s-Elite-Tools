# -*- coding: UTF8

'''
Created on 27.08.2015

@author: mEDI
'''
from PySide import QtCore, QtGui,QtSvg
import PySide
import elite
import timeit
from datetime import datetime, timedelta


class Widget(QtGui.QWidget):
    main = None
    mydb = elite.db
    route = None

    def __init__(self, main):
        super(Widget, self).__init__(main)

        self.main = main
        self.mydb = main.mydb
        self.createActions()
        self.createTimer()

    def getWideget(self):

        gridLayout = QtGui.QGridLayout()

        self.autoUpdateLocation = QtGui.QCheckBox("Location Update")
        self.autoUpdateLocation.setChecked(False)
        self.autoUpdateLocation.stateChanged.connect( self.updateLocation )
        gridLayout.addWidget(self.autoUpdateLocation, 1, 0)


        label = QtGui.QLabel("Min Profit:")
        self.minProfitSpinBox = QtGui.QSpinBox()
        self.minProfitSpinBox.setRange(0, 10000)
        self.minProfitSpinBox.setSuffix("cr")
        self.minProfitSpinBox.setSingleStep(100)
        minTradeProfit = self.mydb.getConfig( 'option_dft_minProfit' )
        if minTradeProfit:
            self.minProfitSpinBox.setValue( minTradeProfit )
        gridLayout.addWidget(label, 1, 1)
        gridLayout.addWidget(self.minProfitSpinBox, 1, 2)


        label = QtGui.QLabel("Max Data Age:")
        self.maxAgeSpinBox = QtGui.QSpinBox()
        self.maxAgeSpinBox.setRange(1, 1000)
        self.maxAgeSpinBox.setSuffix("Day")
        configval = self.mydb.getConfig( 'option_dft_maxAgeDate' )
        if configval:
            self.maxAgeSpinBox.setValue( configval )
        else:
            self.maxAgeSpinBox.setValue( 14 )
        gridLayout.addWidget(label, 1, 3)
        gridLayout.addWidget(self.maxAgeSpinBox, 1, 4)





        label = QtGui.QLabel("Max Star Dist:")
        self.maxStartDistSpinBox = QtGui.QSpinBox()
        self.maxStartDistSpinBox.setRange(10, 7000000)
        self.maxStartDistSpinBox.setSuffix("ls")
        self.maxStartDistSpinBox.setSingleStep(10)
        maxStarDist = self.mydb.getConfig( 'option_maxStarDist' )
        if maxStarDist:
            self.maxStartDistSpinBox.setValue( maxStarDist )
        gridLayout.addWidget(label, 2, 3)
        gridLayout.addWidget(self.maxStartDistSpinBox, 2, 4)





        label = QtGui.QLabel("Min Stock:")
        self.minStockSpinBox = QtGui.QSpinBox()
        self.minStockSpinBox.setRange(0, 1000000)
        self.minStockSpinBox.setSingleStep(100)
        configval = self.mydb.getConfig( 'option_dft_minStock' )
        if configval:
            self.minStockSpinBox.setValue( configval )
        else:
            self.minStockSpinBox.setValue( 100 )
        gridLayout.addWidget(label, 2, 1)
        gridLayout.addWidget(self.minStockSpinBox, 2, 2)



        rawsystemlist = self.mydb.getAllSystems()
        syslist = []
        for system in rawsystemlist:
            syslist.append(system["System"])

        fromsystemlabel = QtGui.QLabel("From System:")
        completer = QtGui.QCompleter(syslist)
        completer.setMaxVisibleItems(20)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.fromSystem = QtGui.QLineEdit()
        configval = self.mydb.getConfig( 'option_dft_fromSystem' )
        if configval:
            self.fromSystem.setText( configval )

        self.fromSystem.setCompleter(completer)
        self.fromSystem.textChanged.connect(self.triggerFromSystemChanged)

        fromstationlabel = QtGui.QLabel("Station:")
        self.fromStation = QtGui.QLineEdit()
        configval = self.mydb.getConfig( 'option_dft_fromStation' )
        if configval:
            self.fromStation.setText( configval )


        tosystemlabel = QtGui.QLabel("To System:")
        completertosystem = QtGui.QCompleter(syslist)
        completertosystem.setMaxVisibleItems(20)
        completertosystem.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.toSystem = QtGui.QLineEdit()
        configval = self.mydb.getConfig( 'option_dft_toSystem' )
        if configval:
            self.toSystem.setText( configval )

        self.toSystem.setCompleter(completertosystem)
        self.toSystem.textChanged.connect(self.triggerToSystemChanged)


        tostationlabel = QtGui.QLabel("Station:")
        self.toStation = QtGui.QLineEdit()
        configval = self.mydb.getConfig( 'option_dft_toStation' )
        if configval:
            self.toStation.setText( configval )

        self.showOptions = QtGui.QCheckBox("Show Options")
        self.showOptions.setChecked(True)
        self.showOptions.stateChanged.connect( self.optionsGroupBoxToggleViewAction )

        self.searchbutton = QtGui.QPushButton("Search")
        self.searchbutton.clicked.connect(self.searchDeals)

        self.locationButton = QtGui.QToolButton()
        self.locationButton.setIcon(self.getIconFromsvg("img/location.svg"))
        self.locationButton.clicked.connect(self.setCurentLocation)
        self.locationButton.setToolTip("Current Location")

        self.switchButton = QtGui.QToolButton()
        self.switchButton.setIcon(self.getIconFromsvg("img/switchTopBottom.svg"))
        self.switchButton.clicked.connect(self.switchLocations)
        self.switchButton.setToolTip("Switch Location")


        searchgridLayout = QtGui.QGridLayout()


        searchgridLayout.addWidget(self.locationButton, 0, 0)

        searchgridLayout.addWidget(fromsystemlabel, 0, 1)
        searchgridLayout.addWidget(self.fromSystem, 0, 2)

        searchgridLayout.addWidget(fromstationlabel, 0, 4)
        searchgridLayout.addWidget(self.fromStation, 0, 5)


        searchgridLayout.addWidget(self.showOptions, 0, 7)

        searchgridLayout.addWidget(self.switchButton, 1, 0)

        searchgridLayout.addWidget(tosystemlabel, 1, 1)
        searchgridLayout.addWidget(self.toSystem, 1, 2)

        searchgridLayout.addWidget(tostationlabel, 1, 4)
        searchgridLayout.addWidget(self.toStation, 1, 5)

        searchgridLayout.addWidget(self.searchbutton, 1, 7)


      

        self.optionsGroupBox = QtGui.QGroupBox("Options")
        self.optionsGroupBox.setLayout(gridLayout)

        self.searchGroupBox = QtGui.QGroupBox("Search")
        self.searchGroupBox.setLayout(searchgridLayout)

        self.dealsview = QtGui.QTreeView()

        self.proxyModel = QtGui.QSortFilterProxyModel()
        self.proxyModel.setDynamicSortFilter(True)

        self.dealsview.setRootIsDecorated(False)
        self.dealsview.setAlternatingRowColors(True)
        self.dealsview.setModel(self.proxyModel)
        self.dealsview.setSortingEnabled(True)


        self.dealsview.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.dealsview.customContextMenuRequested.connect(self.dealslistContextMenuEvent)

        vGroupBox = QtGui.QGroupBox()
        vGroupBox.setFlat(True)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.optionsGroupBox)
        layout.addWidget(self.searchGroupBox)
        layout.addWidget(self.dealsview)



        vGroupBox.setLayout(layout)
        self.triggerFromSystemChanged()
        self.triggerToSystemChanged()
        return vGroupBox

    def getIconFromsvg(self, svgfile):
        svg_renderer = QtSvg.QSvgRenderer(svgfile)
        image = QtGui.QImage(48, 48, QtGui.QImage.Format_ARGB32)
        image.fill(0x00000000)
        svg_renderer.render(QtGui.QPainter(image))
        pixmap = QtGui.QPixmap.fromImage(image)
        icon = QtGui.QIcon(pixmap)
        return icon

    def triggerFromSystemChanged(self):
        system = self.fromSystem.text()
        self.setStationComplete(system, self.fromStation)

    def triggerToSystemChanged(self):
        system = self.toSystem.text()
        self.setStationComplete(system, self.toStation)

    def setStationComplete(self, system, editor):
        rawsystemlist = self.mydb.getStationsFromSystem(system)

        mylist = []
        for system in rawsystemlist:
            mylist.append(system[1])

        completer = QtGui.QCompleter(mylist)
        completer.ModelSorting(QtGui.QCompleter.CaseSensitivelySortedModel)
        completer.setMaxVisibleItems(20)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        completer.setCompletionMode(QtGui.QCompleter.UnfilteredPopupCompletion)
        editor.setCompleter(completer)

    def dealslistContextMenuEvent(self, event):

        menu = QtGui.QMenu(self)

        indexes = self.dealsview.selectionModel().selectedIndexes()
        menu.addAction(self.markFakeItemAct)

        menu.exec_(self.dealsview.viewport().mapToGlobal(event))

    def optionsGroupBoxToggleViewAction(self):
        if not self.optionsGroupBox.isHidden():
            self.optionsGroupBox.hide()
        else:
            self.optionsGroupBox.show()

    def createTimer(self):
        self.autoUpdateLocationTimer = QtCore.QTimer()
        self.autoUpdateLocationTimer.start(1000*60)
        self.autoUpdateLocationTimer.timeout.connect(self.updateLocation)

    def setCurentLocation(self):
        self.fromSystem.setText( self.main.location.getLocation() )
        self.fromStation.setText("")

    def updateLocation(self):
        if self.autoUpdateLocation.isChecked():

            self.autoUpdateLocationTimer.stop()

            self.triggerLocationChanged()

            self.autoUpdateLocationTimer.start()
        else:
            print("stop update location timer")
            self.autoUpdateLocationTimer.stop()


    def triggerLocationChanged(self):
        currentLocation = self.main.location.getLocation()
        if currentLocation != self.fromSystem.text():
            if currentLocation == self.toSystem.text():
                self.switchLocations()
            else:
                self.setCurentLocation()


    def createActions(self):
        self.markFakeItemAct = QtGui.QAction("Set Item as Fake", self,
                statusTip="Set not existing items as Fake and filter it on next search", triggered=self.markFakeItem)



        

    def markFakeItem(self):

        indexes = self.dealsview.selectionModel().selectedIndexes()
 
        id = indexes[self.headerList.index("PriceID")].data()
        print(id)
        if id:
            msg = "Warning: fake items are ignored everywhere and no longer displayed\n"
            msg += "\nSet\n   From Station: %s\n   Item: %s\nas Facke" % (indexes[self.headerList.index("From")].data(), indexes[self.headerList.index("Item")].data() )
            msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                    "Warning", msg,
                    QtGui.QMessageBox.NoButton, self)

            msgBox.addButton("Save as Facke", QtGui.QMessageBox.AcceptRole)
            msgBox.addButton("Cancel", QtGui.QMessageBox.RejectRole)

            if msgBox.exec_() == QtGui.QMessageBox.AcceptRole:
                print("set %s as fakeprice" % id)
                self.main.lockDB()
                self.mydb.setFakePrice(id)
                self.main.unlockDB()
                

    def switchLocations(self):
        fromSystem = self.fromSystem.text()
        self.fromSystem.setText(self.toSystem.text())
        self.toSystem.setText(fromSystem)

        fromStation = self.fromStation.text()
        self.fromStation.setText(self.toStation.text())
        self.toStation.setText(fromStation)
        self.searchDeals()

    def saveOptions(self):
        self.mydb.setConfig( 'option_dft_fromSystem', self.fromSystem.text() )
        self.mydb.setConfig( 'option_dft_fromStation', self.fromStation.text() )
        self.mydb.setConfig( 'option_dft_toSystem', self.toSystem.text() )
        self.mydb.setConfig( 'option_dft_toStation', self.toStation.text() )
        self.mydb.setConfig( 'option_dft_maxAgeDate', self.maxAgeSpinBox.value() )
        self.mydb.setConfig( 'option_dft_minStock', self.minStockSpinBox.value() )
        self.mydb.setConfig( 'option_dft_minProfit', self.minProfitSpinBox.value() )
        
        sectionPosList = []
        for i in range( self.dealsview.header().count() ):
            sectionPosList.append( self.dealsview.header().logicalIndex( i ) )

        sectionPos = ",".join( map( str, sectionPosList ) )
        self.mydb.setConfig( 'option_dft.header.sectionPos', sectionPos )

    
    def searchDeals(self):
        #self.saveOptions()
        firstrun = False
        if not self.dealsview.header().count():
            firstrun = True

        self.headerList = ["PriceID","Item","From","Buy", "Stock","To","Sell","Profit"]

        model = QtGui.QStandardItemModel(0, len(self.headerList), self)
        for x,column in enumerate(self.headerList):
            model.setHeaderData(x, QtCore.Qt.Horizontal, column)

        self.main.lockDB()

        fromSystem = self.fromSystem.text()
        fromSystemID = self.mydb.getSystemIDbyName(fromSystem)
    
        fromStation = self.fromStation.text()
        fromStationID = self.mydb.getStationID(fromSystemID, fromStation)
    
        toSystem = self.toSystem.text()
        toSystemID = self.mydb.getSystemIDbyName(toSystem)
        
        toStation = self.toStation.text()
        toStationID = self.mydb.getStationID(toSystemID, toStation)
            
        maxAgeDate = datetime.utcnow() - timedelta(days = self.maxAgeSpinBox.value() )
        minStock = self.minStockSpinBox.value()
    
        if fromStationID and toStationID:
            deals = self.mydb.getDealsFromTo( fromStationID,  toStationID, maxAgeDate , minStock )

        else:
            deals = []



        for deal in deals:
            if self.minProfitSpinBox.value() <= deal["Profit"]:
                model.insertRow(0)
                
                model.setData(model.index(0, self.headerList.index("PriceID") ), deal["priceAid"])
                model.setData(model.index(0, self.headerList.index("From") ), deal["fromStation"])
                model.setData(model.index(0, self.headerList.index("To") ), deal["toStation"])
                model.setData(model.index(0, self.headerList.index("Item") ), deal["itemName"])
                model.setData(model.index(0, self.headerList.index("Buy") ), deal["StationSell"])
                model.setData(model.index(0, self.headerList.index("Sell") ), deal["StationBuy"])
                model.setData(model.index(0, self.headerList.index("Profit") ), deal["Profit"])
                model.setData(model.index(0, self.headerList.index("Stock") ), deal["Stock"])

        self.dealsview.setModel(model)


        if firstrun:
            sectionPos  = self.mydb.getConfig( 'option_dft.header.sectionPos' )
            if sectionPos:
                sectionPosList = sectionPos.strip().split( ',' )
                for i,pos in  enumerate(sectionPosList):    
                    self.dealsview.header().moveSection( self.dealsview.header().visualIndex( int(pos) ) , i )

            self.dealsview.sortByColumn( self.headerList.index("Profit"), PySide.QtCore.Qt.SortOrder.DescendingOrder )

            self.dealsview.hideColumn(self.headerList.index("PriceID"))

        self.main.unlockDB()

        for i in range(0, len(self.headerList) ):
            self.dealsview.resizeColumnToContents(i)
