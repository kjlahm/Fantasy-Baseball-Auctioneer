# Ken Lahm <kjlahm@gmail.com>
# myframe.py
# Created: 3/27/2010
# Edited:  3/27/2010

import wx
from AddPlayerManual import *
import xlwt
import string

STYLE_FACTORY = {}
FONT_FACTORY = {}

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(1024,768))
        self.currentPlayer = 0
        self.players       = None
        self.hasPlayers    = False
        self.owners        = None
        self.hasOwners     = False
        self.playersGone   = False
        self.undoList      = []

    def build_main_frame(self, players, owners):
        print "Building the main frame"
        self.players    = players
        self.owners     = owners
        self.hasPlayers = True
        self.hasOwners  = True
        
        self.panel1 = wx.Panel(self, -1)

        self.table = wx.grid.Grid(self.panel1, -1)
        self.table.CreateGrid(12,12)
        font = wx.Font(18, wx.NORMAL, wx.NORMAL, wx.NORMAL)
        bold = wx.Font(18, wx.NORMAL, wx.NORMAL, wx.FONTWEIGHT_BOLD)
        self.table.SetDefaultCellFont(font)
        self.table.SetDefaultColSize(80)
        self.table.SetDefaultRowSize(30)
        self.table.SetColLabelSize(0)
        self.table.SetRowLabelSize(0)
        for x in range(12):
            self.table.SetCellSize(x, 1, 1, 4)
            self.table.SetCellSize(x, 7, 1, 4)
            self.table.SetReadOnly(x, 0, True)
            self.table.SetReadOnly(x, 1, True)
            self.table.SetReadOnly(x, 5, True)
            self.table.SetReadOnly(x, 6, True)
            self.table.SetReadOnly(x, 7, True)
            self.table.SetReadOnly(x, 11, True)

        attr = wx.grid.GridCellAttr()
        attr.SetBackgroundColour(wx.LIGHT_GREY)
        self.table.SetRowAttr(0, attr)

        self.table.SetCellFont(0, 0, bold)
        self.table.SetCellValue(0, 0,  "Num")
        self.table.SetCellFont(0, 1, bold)
        self.table.SetCellValue(0, 1,  "Player")
        self.table.SetCellFont(0, 5, bold)
        self.table.SetCellValue(0, 5,  "Pos")
        self.table.SetCellFont(0, 6, bold)
        self.table.SetCellValue(0, 6,  "Team")
        self.table.SetCellFont(0, 7, bold)
        self.table.SetCellValue(0, 7,  "Owner")
        self.table.SetCellFont(0, 11, bold)
        self.table.SetCellValue(0, 11, "Price")

        ownerLabel = wx.StaticText(self.panel1, -1, "Owner", size=(300,30))
        ownerLabel.SetFont(font)

        priceLabel = wx.StaticText(self.panel1, -1, "Price", size=(80,30))
        priceLabel.SetFont(font)

        ownerList = []
        for owner in self.owners:
            ownerList.append(owner.get_name())
            
        self.options = wx.ComboBox(self.panel1, -1, "", size=(300,30), choices = ownerList)
        self.options.SetFont(font)

        self.price = wx.TextCtrl(self.panel1, -1, "", size=(80,36))
        self.price.SetFont(font)
        
        self.add = wx.Button(self.panel1, -1, "Add")
        self.add.SetFont(font)
        self.panel1.Bind(wx.EVT_BUTTON, self.on_add, self.add)

        self.undo = wx.Button(self.panel1, -1, "Undo")
        self.undo.SetFont(font)
        self.panel1.Bind(wx.EVT_BUTTON, self.on_undo, self.undo)

        self.manual = wx.Button(self.panel1, -1, "Manual")
        self.manual.SetFont(font)
        self.panel1.Bind(wx.EVT_BUTTON, self.on_add_manual, self.manual)

        sizer = wx.GridBagSizer(3,6)
        sizer.Add(self.table,   (1,1))
        sizer.SetItemSpan(self.table, (1,5))
        sizer.Add(ownerLabel,   (3,1))
        sizer.Add(priceLabel,   (3,2))
        sizer.Add(self.options, (4,1))
        sizer.Add(self.price,   (4,2))
        sizer.Add(self.add,     (4,3))
        sizer.Add(self.undo,    (4,4))
        sizer.Add(self.manual,  (4,5))

        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 15)
        self.panel1.SetSizerAndFit(border)

        self.update_table()

    def build_1_to_8(self, owners):
        print "Building frame for players 1-8"

        self.panel2 = wx.Panel(self, -1)
        
        sizer = wx.GridBagSizer(7,2)

        x1 = 0
        x2 = 0
        index = 1
        for owner in owners:
            if index < 5:
                sizer.Add(owner.get_table(), (0, x1))
                x1 += 2
            else:
                sizer.Add(owner.get_table(), (1, x2))
                x2 += 2
            index += 1

        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 15)
        self.panel2.SetSizerAndFit(border)

    def build_9_to_16(self, owners):
        print "Building frame for players 9-16"

        self.panel3 = wx.Panel(self, -1)
        
        sizer = wx.GridBagSizer(7,2)

        x1 = 0
        x2 = 0
        index = 1
        for owner in owners:
            if index < 5:
                sizer.Add(owner.get_table(), (0, x1))
                x1 += 2
            else:
                sizer.Add(owner.get_table(), (1, x2))
                x2 += 2
            index += 1

        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 15)
        self.panel3.SetSizerAndFit(border)

    def update_table(self):
        if self.hasPlayers:
            #self.save_spreadsheet()
            index = 1
            position = self.currentPlayer
            if position < 5:
                top    = 0
                bottom = 10
                temp   = position + 1
            elif position > 294:
                bottom = len(self.players)-1
                top    = bottom -10
                temp   = 12 + (position - len(self.players))
            else:
                top    = position-5
                bottom = position+5
                temp   = 6
            if not self.playersGone:
                attr = wx.grid.GridCellAttr()
                attr.SetBackgroundColour(wx.LIGHT_GREY)
                self.table.SetRowAttr(temp, attr)
                if (temp > 1):
                    attr = wx.grid.GridCellAttr()
                    attr.SetBackgroundColour(wx.WHITE)
                    self.table.SetRowAttr(temp-1, attr)
                if (temp < len(self.players)):
                    attr = wx.grid.GridCellAttr()
                    attr.SetBackgroundColour(wx.WHITE)
                    self.table.SetRowAttr(temp+1, attr)
                    self.table.SetCellValue(temp, 7, "")
                    self.table.SetCellValue(temp, 11, "")
            for x in range(top, bottom+1):
                current = self.players[x]
                self.table.SetCellValue(index, 0, str(x+1))
                self.table.SetCellValue(index, 1, current.get_first_name()+" "+current.get_last_name())
                self.table.SetCellValue(index, 5, current.get_pos())
                self.table.SetCellValue(index, 6, current.get_team())
                if current.has_owner():
                    self.table.SetCellValue(index, 7, current.get_owner().get_name())
                    self.table.SetCellValue(index, 11, str(current.get_price()))
                index += 1

    def on_add(self, event):
        tempPrice = self.price.GetValue()
        if isNum(tempPrice):
            activePrice = int(tempPrice)
            if self.hasOwners and self.hasPlayers and not self.playersGone:
                #print self.players[self.currentPlayer]
                activeOwner  = self.owners[self.options.GetSelection()]
                if activeOwner.get_max_bid() >= activePrice:
                    activePlayer = self.players[self.currentPlayer]
                    activePlayer.set_owner(activeOwner)
                    activePlayer.set_price(float(self.price.GetValue()))
                    activeOwner.buy(activePlayer)
                    if self.currentPlayer == len(self.players)-1:
                        self.playersGone = True
                    self.currentPlayer += 1
                    self.add_to_undo(activePlayer)
                    self.save_spreadsheet()
                    self.update_table()
                else:
                    #print "Not enough money"
                    dial = wx.MessageDialog(self, "Owner doesn't have\nenough money", caption="Error", style=wx.ICON_ERROR)
                    dial.ShowModal()
            else:
                #print "top 300 gone"
                dial = wx.MessageDialog(self, "Top 300 is gone", caption="Error", style=wx.ICON_ERROR)
                dial.ShowModal()
        else:
            dial = wx.MessageDialog(self, "Price input\nisn't a number.", caption="Error", style=wx.ICON_ERROR)
            dial.ShowModal()

    def on_add_manual(self, event):
        print "adding manualy"
        manDial = AddPlayerManual(self, self.owners, self.players)
        manDial.Show()
##        print "LOLOLOLOLOLOLOLOLOLOLOLOL"
##        self.save_spreadsheet()
##        self.update_table()

    def on_undo(self, event):
        print "undo"
        if len(self.undoList) > 0:
            activePlayer = self.undoList[-1]
            activeOwner = activePlayer.get_owner()

            activeOwner.unbuy(activePlayer)
            try:
                self.players.index(activePlayer)
                self.currentPlayer -= 1
                activePlayer.set_owner(None)
                activePlayer.set_price(1)
            except ValueError:
                pass
            
            self.undoList.pop()
            self.save_spreadsheet()
            self.update_table()

        else:
            dial = wx.MessageDialog(self, "Already at the\nstart of the list.", style=wx.ICON_ERROR)
            dial.ShowModal()

    def add_to_undo(self, player):
        self.undoList.append(player)

    def save_spreadsheet(self, workbookName="output.xls"):
        workbook = xlwt.Workbook()
        for owner in self.owners:
            row = 0
            sheet = workbook.add_sheet(owner.get_name())
            self.write(sheet, row, 0, owner.get_name(), {"font": (("bold", True),)})
            row += 1
            players = []
            players = owner.get_players()
            for player in players:
                self.write(sheet, row, 0, player.get_comma_name())
                self.write(sheet, row, 1, player.get_team())
                self.write(sheet, row, 2, player.get_pos())
                self.write(sheet, row, 3, player.get_price())
                row += 1
            sheet.col(0).width = 6000
            sheet.col(1).width = 1500
            sheet.col(2).width = 1500
            sheet.col(3).width = 2000
        workbook.save("output.xls")

    def write(self, ws, row, col, data, style=None):
        if style:
            s = self.get_style(style)
            ws.write(row, col, data, s)
        else:
            ws.write(row,col,data)

    def get_style(self, style):
        """
        Style is a dict mapping key to values.
        Valid keys are: background, format, alignment, border

        The values for keys are lists of tuples containing (attribute,
        value) pairs
        """
        style_key = tuple(style.items())
        s = STYLE_FACTORY.get(style_key,None)
        if s is None:
            s = xlwt.XFStyle()
            for key, values in style.items():
                if key == "background":
                    p = xlwt.Pattern()
                    for attr, value in values:
                        p.__setattr__(attr,value)
                    s.pattern = p
                elif key == "format":
                    s.num_format_str = values
                elif key == "alignment":
                    a = xlwt.Alignment()
                    for attr,value in values:
                        a.__setattr__(attr,value)
                    s.alignment = a
                elif key == "border":
                    b = xlwt.Formatting.Borders()
                    for attr, value in values:
                        b.__setattr__(attr,value)
                    s.borders = b
                elif key == "font":
                    f = self.get_font(values)
                    s.font = f
            STYLE_FACTORY[style_key] = s
        return s

    def get_font(self, values):
        """
        'height' 10pt = 200, 8pt = 160
        """
        font_key = values
        f = FONT_FACTORY.get(font_key, None)
        if f is None:
            f = xlwt.Font()
            for attr, value in values:
                f.__setattr__(attr,value)
            FONT_FACTORY[font_key] = f
        return f

def isNum(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
