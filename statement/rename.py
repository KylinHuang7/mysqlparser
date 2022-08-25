#!/usr/local/ieod-web/python/bin/python
# -*- coding: utf-8 -*-

#=============================================================================
#  @desc       
#  @version    1.0.0
#  @author     kylinshuang
#  @date       2017-12-04
#=============================================================================

import mysqltoken as token
import component.identifier
import statement

# 13.1.32 RENAME TABLE Syntax
# RENAME TABLE
#   tbl_name TO new_tbl_name
#   [, tbl_name2 TO new_tbl_name2] ...
class RenameTableStatement(statement.MySQLStatement):
    def __init__(self):
        super(RenameTableStatement, self).__init__()
        self.database = []
        self.table = []
        self.from_database = []
        self.from_table = []
    
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'RENAME', 1),
            (1, token.MySQLKeywordToken, 'TABLE', 2),
            (2, component.identifier.MySQLTableNameComponent, None, 3),
            (3, token.MySQLKeywordToken, 'TO', 4),
            (4, component.identifier.MySQLTableNameComponent, None, 5),
            (5, token.MySQLDelimiterToken, ',', 2),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        s = RenameTableStatement()
        end_pos = s.parse_by_fsm(token_list, [5], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            i = 0
            for t in s.token_list:
                if type(t) is component.identifier.MySQLTableNameComponent:
                    i += 1
                    if i % 2 == 1:
                        s.from_database.append(t.database)
                        s.from_table.append(t.table)
                    else:
                        s.database.append(t.database)
                        s.table.append(t.table)
            token_list.reset(end_pos)
            return s, token_list

