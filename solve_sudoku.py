#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pprint


table_text = '''
610 900 073
200 400 000
000 020 001

900 000 580
030 060 004
000 000 000

000 000 010
047 030 000
060 000 905
'''
table_text = ''.join(table_text.strip().split())
table_text = map(int, table_text)

class GameTable(object):
    def __init__(self):
        '''
        GameTable:
        '''
        self.size = 9
        self.table = []
        for i in range(self.size):
            self.table.append([0] * self.size)
        for i in range(self.size):
            offset = self.size * i
            for j in range(self.size):
                self.table[i][j] = table_text[offset + j]

    def display_table(self):
        '''
        GameTable:
        '''
        pprint.pprint(self.table)

    def wpisz(self, i, j):
        '''
        GameTable:
        '''
        znak = self.table[i][j]
        if znak == 0:
            mozliwosci = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        else:
            mozliwosci = [znak]

game_table = GameTable()
game_table.wpisz(0, 0)
game_table.display_table()
