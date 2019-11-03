#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pprint

verbose = 1


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

class GameField(object):
    def set_current(self, one_current):
        '''
        GameField:
        '''
        self.int_current = one_current
        if self.int_current is None:
            self.disabled_ls = []

    def __init__(self, initial_value):
        '''
        GameField:
        '''
        self.set_current(None)
        if initial_value == 0:
            self.int_possib = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        else:
            self.int_possib = [initial_value]

    def get_text(self):
        '''
        GameField:
        '''
        if self.int_current is None:
            value = str(self.int_possib)
        else:
            value = str(self.int_current)
        return value

    def get_fixed(self):
        '''
        GameField:
        '''
        return self.int_current

    def get_possib(self):
        '''
        GameField:
        '''
        one_fixed = self.get_fixed()
        if one_fixed is None:
            if verbose:
                tmp_format = 'self.int_possib, self.disabled_ls'; print('Eval: %s %s' % (tmp_format, eval(tmp_format)))
            out_ls = list(set(self.int_possib) - set(self.disabled_ls))
        else:
            out_ls = [one_fixed]
            if verbose:
                tmp_format = 'one_fixed'; print('Eval: %s %s' % (tmp_format, eval(tmp_format)))
        return out_ls

    def remove_from_list(self, one_field):
        '''
        GameField:
        '''
        tmp_ls = one_field.get_possib()
        if tmp_ls:
            if len(tmp_ls) == 1:
                selected_char = tmp_ls[0]
                if selected_char != 0:
                    if selected_char not in self.disabled_ls:
                        self.disabled_ls.append(selected_char)


class GameTable(object):
    def __init__(self):
        '''
        GameTable:
        '''
        self.size = 9
        self.table = []
        for i in range(self.size):
            offset = self.size * i
            line_ls = []
            for j in range(self.size):
                new_elem = GameField(table_text[offset + j])
                line_ls.append(new_elem)
            self.table.append(line_ls)

    def display_table(self):
        '''
        GameTable:
        '''
        for row_nr in range(self.size):
            out_line = []
            for col_nr in range(self.size):
                one_elem = self.table[row_nr][col_nr].get_text()
                out_line.append(one_elem)
            #print ' '.join(out_line)

    def wpisz(self, i, j):
        '''
        GameTable:
        '''
        if verbose:
            tmp_format = 'i, j'; print('\x1b[42mEval\x1b[0m: %s %s' % (tmp_format, eval(tmp_format)))
        game_field = self.table[i][j]
        mozliwosci = game_field.get_possib()
        if len(mozliwosci) > 1:
            for row_nr in range(self.size):
                if row_nr != i:
                    if verbose:
                        print 'Removing from row = %d' % row_nr
                    game_field.remove_from_list(self.table[row_nr][j])
            for col_nr in range(self.size):
                if col_nr != j:
                    if verbose:
                        print 'Removing from col = %d' % col_nr
                    game_field.remove_from_list(self.table[i][col_nr])
            row_offset = (i // 3) * 3
            col_offset = (j // 3) * 3
            for row_nr in range(row_offset, row_offset + 3):
                for col_nr in range(col_offset, col_offset + 3):
                    if row_nr != i and col_nr != j:
                        if verbose:
                            print 'Removing from row = %d col = %d' % (row_nr, col_nr)
                        game_field.remove_from_list(self.table[row_nr][col_nr])
            mozliwosci = game_field.get_possib()
        if verbose:
            tmp_format = 'mozliwosci'; print('\x1b[41mEval\x1b[0m: %s %s' % (tmp_format, eval(tmp_format)))
        for one_possib in mozliwosci:
            self.table[i][j].set_current(one_possib)
            if j < self.size - 1:
                self.wpisz(i, j + 1)
            elif i < self.size - 1:
                self.wpisz(i + 1, 0)
            else:
                self.display_table()
            game_field.set_current(None)

game_table = GameTable()
game_table.wpisz(0, 0)
