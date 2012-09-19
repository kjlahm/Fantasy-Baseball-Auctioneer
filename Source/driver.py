# Ken Lahm <kjlahm@gmail.com>
# driver.py
# Created: 3/27/2010
# Edited:  3/27/2010

from Player import *
from Owner import *
from MyFrame import *
import wx
import wx.grid
import xlrd
import string

class MyApp(wx.App):
    def OnInit(self):
        # Import Data
        self.mainFrame    = MyFrame(parent=None, id=-1, title="CBS Top 300")
        self.players1to8  = MyFrame(parent=None, id=-1, title="Owners 1-8")
        self.players9to16 = MyFrame(parent=None, id=-1, title="Owners 9-16")
        self.players      = self.import_players()
        self.owners       = self.import_owners()

        # Build GUI
        self.mainFrame.build_main_frame(self.players, self.owners)
        self.mainFrame.Show(True)
        self.SetTopWindow(self.mainFrame)

        self.players1to8.build_1_to_8(self.owners[:8])
        self.players1to8.Show(True)
        self.SetTopWindow(self.players1to8)

        self.players9to16.build_9_to_16(self.owners[8:len(self.owners)])
        self.players9to16.Show(True)
        self.SetTopWindow(self.players9to16)

        return True

    def import_players(self, workbookName='players.xls'):
        players = []
        workbook = xlrd.open_workbook(workbookName)
        sheet = workbook.sheet_by_index(0)
        for rownum in range(1,sheet.nrows):
            firstName = ""
            lastName = ""
            team = ""
            position = ""
            row = sheet.row_values(rownum)
            testBlanks = ""
            for x in range(len(row)):
                testBlanks += row[x]
            if testBlanks != "": # If the row is blank, ignore it
                name = string.split(row[0],', ')
                if len(name) != 2:
                    print "Name formatting error in row " + str(rownum+1)
                    print row
                else:
                    firstName = string.strip(name[1])
                    lastName = string.strip(name[0])
                    team = row[1]
                    position = row[2]
                    players.append(Player(firstName,lastName,team,position))
        return players

    def import_owners(self, workbookName='owners.xls'):
        owners = []
        workbook = xlrd.open_workbook(workbookName)
        sheet = workbook.sheet_by_index(0)
        for rownum in range(1,sheet.nrows):
            name = ""
            cash = 0
            bonus = 0
            row = sheet.row_values(rownum)
            testBlanks = ""
            for x in range(len(row)):
                testBlanks += str(row[x])
            if testBlanks != "": # If the row is blank, ignore it
                name = row[0]
                if (isNum(row[1]) & isNum(row[2])):
                    cash = row[1]
                    bonus = row[2]
                    if rownum <= 8:
                        owners.append(Owner(self.players1to8,name,bonus,cash))
                    else:
                        owners.append(Owner(self.players9to16,name,bonus,cash))
                    #print owners[-1]
                else:
                    print "Invalid numbers on line " + rownum
        return owners

def isNum(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def main():
    app = MyApp(wx.App)
    app.MainLoop()

if __name__ == "__main__":
    main()
