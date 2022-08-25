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

# 13.2.2 DELETE Syntax
# DELETE [LOW_PRIORITY] [QUICK] [IGNORE] FROM tbl_name
#    [WHERE where_condition]
#    [ORDER BY ...]
#    [LIMIT row_count]
#
# DELETE [LOW_PRIORITY] [QUICK] [IGNORE]
#    tbl_name[.*] [, tbl_name[.*]] ...
#    FROM table_references
#    [WHERE where_condition]
#
# DELETE [LOW_PRIORITY] [QUICK] [IGNORE]
#    FROM tbl_name[.*] [, tbl_name[.*]] ...
#    USING table_references
#    [WHERE where_condition]
class DeleteStatement(statement.MySQLStatement):
    def __init__(self):
        super(DeleteStatement, self).__init__()
        self.database = []
        self.table = []
    
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'DELETE', 1),
            (1, token.MySQLKeywordToken, 'LOW_PRIORITY', 2),
            ((1, 2), token.MySQLKeywordToken, 'QUICK', 3),
            ((1, 2, 3), token.MySQLKeywordToken, 'IGNORE', 4),
            ((1, 2, 3, 4), token.MySQLKeywordToken, 'FROM', 5),
            (5, component.identifier.MySQLTableNameComponent, None, 6),
            (6, token.MySQLKeywordToken, 'WHERE', 7),
            (7, component.expression.MySQLExpressionComponent, None, 8),
            ((6, 8), token.MySQLKeywordToken, 'ORDER', 9),
            (9, token.MySQLKeywordToken, 'BY', 10),
            (10, component.option.MySQLOrderListOptionComponent, None, 11),
            ((6, 8, 11), token.MySQLKeywordToken, 'LIMIT', 12),
            (12, token.MySQLNumericToken, None, self.get_final_status()),
            ((6, 16), token.MySQLOperatorToken, '.', 13),
            (13, token.MySQLOperatorToken, '*', 14),
            (14, token.MySQLDelimiterToken, ',', 15),
            (15, component.identifier.MySQLTableNameComponent, None, 16),
            ((6, 14, 16), token.MySQLKeywordToken, 'USING', 17),
            ((1, 2, 3, 4), component.identifier.MySQLTableNameComponent, None, 18),
            (18, token.MySQLOperatorToken, '.', 19),
            (19, token.MySQLOperatorToken, '*', 20),
            (20, token.MySQLDelimiterToken, ',', 18),
            (20, token.MySQLKeywordToken, 'FROM', 17),
            (17, component.reference.TableReferenceListComponent, None, 21),
            (21, token.MySQLKeywordToken, 'WHERE', 22),
            (22, component.expression.MySQLExpressionComponent, None, self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        s = DeleteStatement()
        end_pos = s.parse_by_fsm(token_list, [6, 8, 11, 21], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            for t in s.token_list:
                if type(t) is component.identifier.MySQLTableNameComponent:
                    s.database.append(t.database)
                    s.table.append(t.table)
                elif type(t) is component.reference.TableReferenceListComponent:
                    s.database.extend(t.database)
                    s.table.extend(t.table)
                elif type(t) is component.expression.MySQLExpressionComponent:
                    for tt in filter((lambda x: type(x) is component.reference.SubQueryComponent), t.token_list):
                        s.database.extend(tt.database)
                        s.table.extend(tt.table)
            token_list.reset(end_pos)
            return s, token_list

