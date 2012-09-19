# Ken Lahm <kjlahm@gmail.com>
# Owner.py
# Created: 3/27/2010
# Edited:  3/27/2010

import wx
import wx.grid

NEW_PLAYER_BONUS = 10
MAX_PLAYERS      = 26

"""Implements a league owner"""
class Owner:

    def __init__(self, parent, name="Name", bonus=0, cash=260):
        # Class variables
        self.name       = name
        self.players    = []
        self.maxPlayers = MAX_PLAYERS
        self.cash       = cash + bonus
        self.startCash  = self.cash
        self.maxBid     = 0
        self.find_max_bid()

        # Class GUI
        self.table = wx.grid.Grid(parent, -1)
        self.build_table()
        self.update_table()

    def __str__(self):
        stringValue  = "%s\n" % (self.name)
        stringValue += "Cash: %s\n" % (self.cash)
        stringValue += "Max Bid: %s\n" % (self.maxBid)
        for player in self.players:
            stringValue += "%s\n" % (player)
        return stringValue

    def find_max_bid(self):
        playersNeeded = self.maxPlayers - len(self.players)
        self.maxBid = self.cash - (playersNeeded -1)

    def build_table(self):
        self.table.CreateGrid(28,8)
        font = wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL)
        self.table.SetDefaultCellFont(font)
        self.table.SetDefaultColSize(32)
        self.table.SetDefaultRowSize(8)
        self.table.SetColLabelSize(0)
        self.table.SetRowLabelSize(0)

        self.table.SetCellSize(0, 0, 1, 4)
        self.table.SetCellSize(0, 4, 1, 2)
        for x in range(1,28):
            self.table.SetCellSize(x, 0, 1, 4)

        self.table.SetCellValue(0, 0, self.name)
        self.table.SetCellValue(0, 4, "Max bid:")
        self.table.SetCellValue(0, 7, str(self.startCash))

    def update_table(self):
        # First Row
        self.table.SetCellValue(0, 6, str(self.maxBid))

        # Second Row
        self.table.SetCellValue(1, 0, "Player")
        self.table.SetCellValue(1, 4, "Pos")
        self.table.SetCellValue(1, 5, "Team")
        self.table.SetCellValue(1, 6, "Price")
        self.table.SetCellValue(1, 7, "$ Left")

        index = 2
        moneyLeft = self.startCash
        for player in self.players:
            moneyLeft -= player.get_price()
            self.table.SetCellValue(index, 0, player.get_last_name() + ", " +player.get_first_name())
            self.table.SetCellValue(index, 4, player.get_pos())
            self.table.SetCellValue(index, 5, player.get_team())
            self.table.SetCellValue(index, 6, str(player.get_price()))
            self.table.SetCellValue(index, 7, str(moneyLeft))
            index += 1

    def buy(self, player):
##        print str(player.get_price())+" <= "+str(self.maxBid)
##        print str(len(self.players))+" < "+str(self.maxPlayers)
        if player.get_price() <= self.maxBid and len(self.players) < self.maxPlayers:
            self.players.append(player)
            self.cash -= player.get_price()
            self.find_max_bid()
            self.update_table()
        else:
            print "Cannot buy player"

    def unbuy(self, oldPlayer):
        self.cash += oldPlayer.get_price()
        index = 2
        for player in self.players:
            self.table.SetCellValue(index, 0, "")
            self.table.SetCellValue(index, 4, "")
            self.table.SetCellValue(index, 5, "")
            self.table.SetCellValue(index, 6, "")
            self.table.SetCellValue(index, 7, "")
            index += 1
        self.players.remove(oldPlayer)
        self.find_max_bid()
        self.update_table()

    def get_table(self):
        return self.table

    def get_name(self):
        return self.name

    def get_max_bid(self):
        return self.maxBid

    def get_players(self):
        return self.players
