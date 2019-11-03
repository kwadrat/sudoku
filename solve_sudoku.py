#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pprint
import time

verbose = 0
verb_summary = 0
verb_timed = 1


if 1:
    ##############################################################################
    table_text = '''
    700 000 006
    005 308 100
    002 706 400

    900 030 005
    070 482 030
    100 050 007

    003 801 700
    001 905 200
    600 000 008
    '''
    ##############################################################################
else:
    ##############################################################################
    table_text = '''
    000 000 000
    000 000 000
    000 000 000

    000 000 000
    000 000 000
    000 000 000

    000 000 000
    000 000 000
    000 000 000
    '''
    ##############################################################################
table_text = ''.join(table_text.strip().split())
table_text = map(int, table_text)

class FileSaver(object):
    def __init__(self):
        '''
        FileSaver:
        '''
        self.out_counter = 0

    def execute_save(self, out_txt):
        '''
        FileSaver:
        '''
        file_name = 'g%d' % self.out_counter
        fd = open(file_name, 'wb')
        fd.write(out_txt)
        fd.close()
        print 'Saved to file: %s' % file_name
        self.out_counter += 1

file_saver = FileSaver()

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
        self.last_msg = time.time()
        self.size = 9
        self.siz_e = self.size - 1
        self.table = []
        for i in range(self.size):
            offset = self.size * i
            for j in range(self.size):
                new_elem = GameField(table_text[offset + j])
                self.table.append(new_elem)

    def display_table(self):
        '''
        GameTable:
        '''
        main_ls = []
        for row_nr in range(self.size):
            line_ls = []
            for col_nr in range(self.size):
                one_elem = self.table[row_nr * self.size + col_nr].get_text()
                line_ls.append(one_elem)
            one_line = ' '.join(line_ls)
            main_ls.append(one_line)
            main_ls.append('\n')
        out_txt = ''.join(main_ls)
        file_saver.execute_save(out_txt)

    def wpisz(self, i, j):
        '''
        GameTable:
        '''
        show_on_time = 0
        if verb_timed:
            time_now = time.time()
            if time_now - self.last_msg >= 1.0:
                show_on_time = 1
                self.last_msg = time_now
        if verb_summary or show_on_time:
            k = []
            for index in range(i * self.size + j):
                k.append(self.table[index].get_possib()[0])
            tmp_format = 'i, j, k'; print('\x1b[42mEval\x1b[0m: %s %s' % (tmp_format, eval(tmp_format)))
        game_field = self.table[i * self.size + j]
        mozliwosci = game_field.get_possib()
        if len(mozliwosci) > 1:
            for row_nr in range(self.size):
                if row_nr != i:
                    if verbose:
                        print 'Removing from row = %d' % row_nr
                    game_field.remove_from_list(self.table[row_nr * self.size + j])
            for col_nr in range(self.size):
                if col_nr != j:
                    if verbose:
                        print 'Removing from col = %d' % col_nr
                    game_field.remove_from_list(self.table[i * self.size + col_nr])
            row_offset = (i // 3) * 3
            col_offset = (j // 3) * 3
            for row_nr in range(row_offset, row_offset + 3):
                for col_nr in range(col_offset, col_offset + 3):
                    if row_nr != i and col_nr != j:
                        if verbose:
                            print 'Removing from row = %d col = %d' % (row_nr, col_nr)
                        game_field.remove_from_list(self.table[row_nr * self.size + col_nr])
            mozliwosci = game_field.get_possib()
        if verbose:
            tmp_format = 'mozliwosci'; print('\x1b[41mEval\x1b[0m: %s %s' % (tmp_format, eval(tmp_format)))
        for one_possib in mozliwosci:
            self.table[i * self.size + j].set_current(one_possib)
            if j < self.siz_e:
                self.wpisz(i, j + 1)
            elif i < self.siz_e:
                self.wpisz(i + 1, 0)
            else:
                self.display_table()
        game_field.set_current(None)

game_table = GameTable()
game_table.wpisz(0, 0)
