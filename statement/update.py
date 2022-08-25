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

# 13.2.11 UPDATE Syntax
#U PDATE [LOW_PRIORITY] [IGNORE] table_reference
#    SET assignment_list
#    [WHERE where_condition]
#    [ORDER BY ...]
#    [LIMIT row_count]
#
# UPDATE [LOW_PRIORITY] [IGNORE] table_references
#    SET assignment_list
#    [WHERE where_condition]
#
# value:
#    {expr | DEFAULT}
class UpdateStatement(statement.MySQLStatement):
    def __init__(self):
        super(UpdateStatement, self).__init__()
        self.database = []
        self.table = []
        self.from_database = []
        self.from_table = []
    
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'UPDATE', 1),
            (1, token.MySQLKeywordToken, 'LOW_PRIORITY', 2),
            ((1, 2), token.MySQLKeywordToken, 'IGNORE', 3),
            ((1, 2, 3), component.reference.TableReferenceListComponent, None, 4),
            (4, token.MySQLKeywordToken, 'SET', 5),
            (5, component.expression.MySQLAssignmentListExpressionComponent, None, 6),
            (6, token.MySQLKeywordToken, 'WHERE', 7),
            (7, component.expression.MySQLExpressionComponent, None, 8),
            ((6, 8), token.MySQLKeywordToken, 'ORDER', 9),
            (9, token.MySQLKeywordToken, 'BY', 10),
            (10, component.expression.MySQLExpressionComponent, None, 11),
            (10, component.identifier.MySQLColumnNameComponent, None, 11),
            (10, token.MySQLNumericToken, None, 11),
            (11, token.MySQLKeywordToken, 'ASC', 12),
            (11, token.MySQLKeywordToken, 'DESC', 12),
            (12, token.MySQLDelimiterToken, ',', 10),
            ((6, 8, 11, 12), token.MySQLKeywordToken, 'LIMIT', 13),
            (13, token.MySQLNumericToken, None, self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        s = UpdateStatement()
        end_pos = s.parse_by_fsm(token_list, [6, 8, 11, 12], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            for t in s.token_list:
                if type(t) is component.reference.TableReferenceListComponent:
                    s.database.extend(t.database)
                    s.table.extend(t.table)
                elif type(t) is component.expression.MySQLExpressionComponent:
                    for tt in filter((lambda x: type(x) is component.reference.SubQueryComponent), t.token_list):
                        s.from_database.extend(tt.database)
                        s.from_database.extend(tt.table)
            token_list.reset(end_pos)
            return s, token_list

