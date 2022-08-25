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

# 13.1.33 TRUNCATE TABLE Syntax
# TRUNCATE [TABLE] tbl_name
class TruncateTableStatement(statement.MySQLStatement):
    def __init__(self):
        super(TruncateTableStatement, self).__init__()
        self.database = ''
        self.table = ''
    
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'TRUNCATE', 1),
            (1, token.MySQLKeywordToken, 'TABLE', 2),
            ((1, 2), component.identifier.MySQLTableNameComponent, None, self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        s = TruncateTableStatement()
        end_pos = s.parse_by_fsm(token_list, verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            for t in s.token_list:
                if type(t) is component.identifier.MySQLTableNameComponent:
                    s.database = t.database
                    s.table = t.table
            token_list.reset(end_pos)
            return s, token_list

