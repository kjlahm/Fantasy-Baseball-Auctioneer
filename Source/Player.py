# Ken Lahm <kjlahm@gmail.com>
# Player.py
# Created: 3/27/2010
# Edited:  3/27/2010

"""Implements a player an owner can purchase"""
class Player:

    def __init__(self, firstName="Default", lastName="Name", team="DEF", pos="PL", price=1, owner=None):
        self.firstName = firstName
        self.lastName  = lastName
        self.team      = team
        self.pos       = pos
        self.price     = price
        self.owner     = owner

    def __str__(self):
        stringValue  = "%s, %s %s %s " % (self.lastName, self.firstName, self.pos, self.team)
        stringValue += str(self.price) + ""
        return stringValue

    def get_first_name(self):
        return self.firstName

    def get_last_name(self):
        return self.lastName

    def get_comma_name(self):
        return self.lastName + ", " + self.firstName

    def get_team(self):
        return self.team

    def get_pos(self):
        return self.pos

    def get_price(self):
        return self.price

    def has_owner(self):
        if self.owner == None:
            return False
        else:
            return True

    def get_owner(self):
        return self.owner

    def set_price(self, newPrice):
        self.price = newPrice

    def set_owner(self, newOwner):
        self.owner = newOwner
