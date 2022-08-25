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
import statement.select

# 13.8.2 EXPLAIN Syntax
# {EXPLAIN | DESCRIBE | DESC}
#    tbl_name [col_name | wild]
#
# {EXPLAIN | DESCRIBE | DESC}
#    [explain_type] SELECT select_options
#
# explain_type: {EXTENDED | PARTITIONS}

class ExplainStatement(statement.MySQLStatement):
    def __init__(self):
        super(ExplainStatement, self).__init__()
        self.database = []
        self.table = []
    
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'EXPLAIN', 1),
            (0, token.MySQLKeywordToken, 'DESCRIBE', 1),
            (0, token.MySQLKeywordToken, 'DESC', 1),
            (1, component.identifier.MySQLTableNameComponent, None, 2),
            (2, component.identifier.MySQLColumnNameComponent, None, self.get_final_status()),
            (2, token.MySQLStringToken, None, self.get_final_status()),
            (1, token.MySQLKeywordToken, 'EXTENDED', 3),
            (1, token.MySQLKeywordToken, 'PARTITIONS', 3),
            ((1, 3), statement.select.UnionStatement, None, self.get_final_status()),
            ((1, 3), statement.select.SelectStatement, None, self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        s = ExplainStatement()
        end_pos = s.parse_by_fsm(token_list, [2], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            for t in s.token_list:
                if type(t) is component.identifier.MySQLTableNameComponent:
                    s.database.append(t.database)
                    s.table.append(t.table)
                elif type(t) is statement.select.SelectStatement:
                    s.database.extend(t.database)
                    s.table.extend(t.table)
                elif type(t) is statement.select.UnionStatement:
                    s.database.extend(t.database)
                    s.table.extend(t.table)
            token_list.reset(end_pos)
            return s, token_list

