# Ken Lahm <kjlahm@gmail.com>
# myframe.py
# Created: 3/27/2010
# Edited:  3/27/2010

import wx
from Owner import *
from Player import *

class AddPlayerManual(wx.MiniFrame):
    def __init__(self, parent, owners, players):
        self.parent = parent
        self.owners  = owners
        self.players = players
        wx.MiniFrame.__init__(self,None,-1, 'Add a Player', size=(500,200))
        panel = wx.Panel(self, -1, size=(300,100))
        
        self.firstNameLabel = wx.StaticText(panel, -1, "First Name", pos=(20,15))
        self.firstNameText  = wx.TextCtrl(panel, -1, "", pos=(15,30))
        self.lastNameLabel  = wx.StaticText(panel, -1, "Last Name", pos=(125,15))
        self.lastNameText   = wx.TextCtrl(panel, -1, "", pos=(120,30))
        self.teamLabel      = wx.StaticText(panel, -1, "Team", pos=(230,15))
        self.teamText       = wx.TextCtrl(panel, -1, "", pos=(225,30))
        self.posLabel       = wx.StaticText(panel, -1, "Position", pos=(335,15))
        self.posText        = wx.TextCtrl(panel, -1, "", pos=(330,30))
        self.priceLabel     = wx.StaticText(panel, -1, "Price", pos=(20,60))
        self.priceText      = wx.TextCtrl(panel, -1, "", pos=(15,75))

        ownerText = wx.StaticText(panel, -1, "Owner", pos=(125,60))
        ownerList = []
        for owner in self.owners:
            ownerList.append(owner.get_name())
        self.ownerBox = wx.ComboBox(panel, -1, "", size=(300,30), choices = ownerList, pos=(125,75)) 

        addButton = wx.Button(panel, -1, "Add", pos=(310,130))
        closeButton = wx.Button(panel, -1, "Close", pos=(390,130))
        
        self.Bind(wx.EVT_BUTTON, self.on_close_me, closeButton)
        self.Bind(wx.EVT_CLOSE, self.on_close_window)

        self.Bind(wx.EVT_BUTTON, self.on_add, addButton)

    def on_close_me(self, event):
        self.Close(True)

    def on_close_window(self, event):
        self.Destroy()

    def on_add(self, event):
        activeOwner = self.owners[self.ownerBox.GetSelection()]
        firstName   = self.firstNameText.GetValue()
        lastName    = self.lastNameText.GetValue()
        team        = self.teamText.GetValue()
        pos         = self.posText.GetValue()
        price       = self.priceText.GetValue()
        isValid     = True
        try:
            price = float(price)
        except ValueError:
            isValid = False
            dlg = wx.MessageDialog(self, "Please enter a valid price.", caption="Error", style=wx.OK | wx.ICON_ERROR | wx.STAY_ON_TOP, pos=(200,200))
            dlg.ShowModal()
            dlg.Destroy()
        if (isValid):
            for player in self.players:
                if (firstName == player.get_first_name()) and (lastName == player.get_last_name()) and (team == player.get_team()):
                    isValid = False
                    dlg = wx.MessageDialog(self, "This player already exists.", caption="Error", style=wx.OK | wx.ICON_ERROR | wx.STAY_ON_TOP, pos=(200,200))
                    dlg.ShowModal()
                    dlg.Destroy()
        if (isValid):
            if activeOwner.get_max_bid() >= price:
                newPlayer = Player(firstName, lastName, team, pos, price, activeOwner)
                activeOwner.buy(newPlayer)
                if self.parent.currentPlayer == len(self.parent.players)-1:
                    print "end of the list"
                    self.parent.currentPlayer += 1
                self.parent.save_spreadsheet()
                self.parent.update_table()
                self.parent.add_to_undo(newPlayer)
                self.Close(True)
            else:
                dlg2 = wx.MessageDialog(self, "Owner Doesn't have\nenough money.", caption="Error", style=wx.OK | wx.ICON_ERROR | wx.STAY_ON_TOP, pos=(200,200))
                dlg2.ShowModal()
                dlg2.Destroy()
            

