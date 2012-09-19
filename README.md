Fantasy-Baseball-Auctioneer
===========================

Creators
========
Ken Lahm
Derek Guenther

Overview
========

This python program allows you to run a fantasy baseball auction (although it could be used for 
other sports). The list of players is populated from the input file players.xls and the list of 
owners from owners.xls. Every action within the system saves the current state of the program to 
output.xls. If the program fails during your auction and you lose data you have been forewarned; 
hopefully the output.xls file will contain all of your data to this point. I know some of the code 
is pretty unclean; Derek and I slung this together the night before the auction. If you feel so 
compelled to fix our mistakes/terrible design choices you're encouraged to do so and commit your 
changes.

Installation
============

The program is targeted for Python 2.7 but may work on different versions. The GUI framework used
is wxPython so you will need to have the proper version of wx installed. There are also two 
libraries included which allow for saving and reading from Excel files: xlrd and xlwt. These are 
included in the Libraries folder and need to be installed before running.

Running the program
===================

To run the program you simply need to run driver.py with a players.xls and owners.xls file in 
the same directory.