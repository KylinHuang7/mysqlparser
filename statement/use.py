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
import component.expression
import component.reference
import statement

# 13.8.4 USE Syntax
# USE db_name
class UseStatement(statement.MySQLStatement):
    def __init__(self):
        super(UseStatement, self).__init__()
        self.database = ''
    
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'USE', 1),
            (1, component.identifier.MySQLDatabaseNameComponent, None, self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        s = UseStatement()
        end_pos = s.parse_by_fsm(token_list, verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            for t in s.token_list:
                if type(t) is component.identifier.MySQLDatabaseNameComponent:
                    s.database = t.database
            token_list.reset(end_pos)
            return s, token_list

