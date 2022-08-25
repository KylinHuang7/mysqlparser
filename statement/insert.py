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

# 13.2.5 INSERT Syntax
# INSERT [LOW_PRIORITY | DELAYED | HIGH_PRIORITY] [IGNORE]
#    [INTO] tbl_name
#    [(col_name [, col_name] ...)]
#    {VALUES | VALUE} (value_list) [, (value_list)] ...
#    [ON DUPLICATE KEY UPDATE assignment_list]
#
# INSERT [LOW_PRIORITY | DELAYED | HIGH_PRIORITY] [IGNORE]
#    [INTO] tbl_name
#    SET assignment_list
#    [ON DUPLICATE KEY UPDATE assignment_list]
#
# INSERT [LOW_PRIORITY | HIGH_PRIORITY] [IGNORE]
#    [INTO] tbl_name
#    [(col_name [, col_name] ...)]
#    SELECT ...
#    [ON DUPLICATE KEY UPDATE assignment_list]
#
# value:
#    {expr | DEFAULT}
#
# value_list:
#    value [, value] ...
#
class InsertStatement(statement.MySQLStatement):
    def __init__(self):
        super(InsertStatement, self).__init__()
        self.database = []
        self.table = []
        self.from_database = []
        self.from_table = []
    
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'INSERT', 1),
            (1, token.MySQLKeywordToken, 'LOW_PRIORITY', 2),
            (1, token.MySQLKeywordToken, 'HIGH_PRIORITY', 2),
            (1, token.MySQLKeywordToken, 'DELAYED', 2),
            ((1, 2), token.MySQLKeywordToken, 'IGNORE', 3),
            ((1, 2, 3), token.MySQLKeywordToken, 'INTO', 4),
            ((1, 2, 3, 4), component.identifier.MySQLTableNameComponent, None, 5),
            (5, token.MySQLOperatorToken, '(', 6),
            (6, component.identifier.MySQLColumnNameListComponent, None, 7),
            (7, token.MySQLOperatorToken, ')', 8),
            ((5, 8), token.MySQLKeywordToken, 'VALUES', 9),
            ((5, 8), token.MySQLKeywordToken, 'VALUE', 9),
            (9, token.MySQLOperatorToken, '(', 10),
            (10, token.MySQLKeywordToken, 'DEFAULT', 11),
            (10, component.expression.MySQLExpressionComponent, None, 11),
            (11, token.MySQLDelimiterToken, ',', 10),
            (11, token.MySQLOperatorToken, ')', 12),
            (12, token.MySQLDelimiterToken, ',', 9),
            (5, token.MySQLKeywordToken, 'SET', 13),
            (13, component.expression.MySQLAssignmentListExpressionComponent, None, 14),
            ((5, 8), statement.select.UnionStatement, None, 15),
            ((5, 8), statement.select.SelectStatement, None, 15),
            ((12, 14, 15), token.MySQLKeywordToken, 'ON', 16),
            (16, token.MySQLKeywordToken, 'DUPLICATE', 17),
            (17, token.MySQLKeywordToken, 'KEY', 18),
            (18, token.MySQLKeywordToken, 'UPDATE', 19),
            (19, component.expression.MySQLAssignmentListExpressionComponent, None, self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        s = InsertStatement()
        end_pos = s.parse_by_fsm(token_list, [12, 14, 15], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            for t in s.token_list:
                if type(t) is component.identifier.MySQLTableNameComponent:
                    s.database.append(t.database)
                    s.table.append(t.table)
                elif type(t) is component.expression.MySQLExpressionComponent:
                    for tt in filter((lambda x: type(x) is component.reference.SubQueryComponent), t.token_list):
                        s.from_database.extend(tt.database)
                        s.from_table.extend(tt.table)
                elif type(t) is statement.select.SelectStatement:
                    s.from_database.extend(t.database)
                    s.from_table.extend(t.table)
                elif type(t) is statement.select.UnionStatement:
                    s.from_database.extend(t.database)
                    s.from_table.extend(t.table)
            token_list.reset(end_pos)
            return s, token_list

