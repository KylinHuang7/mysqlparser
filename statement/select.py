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

# 13.2.9 SELECT Syntax
# SELECT
#    [ALL | DISTINCT | DISTINCTROW ]
#      [HIGH_PRIORITY]
#      [STRAIGHT_JOIN]
#      [SQL_SMALL_RESULT] [SQL_BIG_RESULT] [SQL_BUFFER_RESULT]
#      [SQL_CACHE | SQL_NO_CACHE] [SQL_CALC_FOUND_ROWS]
#    select_expr [, select_expr ...]
#    [FROM table_references
#    [WHERE where_condition]
#    [GROUP BY {col_name | expr | position}
#      [ASC | DESC], ... [WITH ROLLUP]]
#    [HAVING where_condition]
#    [ORDER BY {col_name | expr | position}
#      [ASC | DESC], ...]
#    [LIMIT {[offset,] row_count | row_count OFFSET offset}]
#    [PROCEDURE procedure_name(argument_list)]
#    [INTO OUTFILE 'file_name'
#        [CHARACTER SET charset_name]
#        export_options
#      | INTO DUMPFILE 'file_name'
#      | INTO var_name [, var_name]]
#    [FOR UPDATE | LOCK IN SHARE MODE]]
class SelectStatement(statement.MySQLStatement):
    def __init__(self):
        super(SelectStatement, self).__init__()
        self.database = []
        self.table = []
    
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'SELECT', 1),
            (1, token.MySQLKeywordToken, 'ALL', 2),
            (1, token.MySQLKeywordToken, 'DISTINCT', 2),
            (1, token.MySQLKeywordToken, 'DISTINCTROW', 2),
            ((1, 2), token.MySQLKeywordToken, 'HIGH_PRIORITY', 3),
            ((1, 2, 3), token.MySQLKeywordToken, 'STRAIGHT_JOIN', 4),
            ((1, 2, 3, 4), token.MySQLKeywordToken, 'SQL_SMALL_RESULT', 5),
            ((1, 2, 3, 4, 5), token.MySQLKeywordToken, 'SQL_BIG_RESULT', 6),
            ((1, 2, 3, 4, 5, 6), token.MySQLKeywordToken, 'SQL_BUFFER_RESULT', 7),
            ((1, 2, 3, 4, 5, 6, 7), token.MySQLKeywordToken, 'SQL_CACHE', 8),
            ((1, 2, 3, 4, 5, 6, 7), token.MySQLKeywordToken, 'SQL_NO_CACHE', 8),
            ((1, 2, 3, 4, 5, 6, 7, 8), token.MySQLKeywordToken, 'SQL_CALC_FOUND_ROWS', 9),
            ((1, 2, 3, 4, 5, 6, 7, 8, 9, 11), component.expression.MySQLExpressionComponent, None, 10),
            (10, token.MySQLKeywordToken, 'AS', 51),
            (51, token.MySQLStringToken, None, 52),
            (51, component.identifier.MySQLIdentifierComponent, None, 52),
            ((10, 52), token.MySQLDelimiterToken, ',', 11),
            ((10, 52), token.MySQLKeywordToken, 'FROM', 12),
            (12, component.reference.TableReferenceListComponent, None, 13),
            (13, token.MySQLKeywordToken, 'WHERE', 14),
            (14, component.expression.MySQLExpressionComponent, None, 15),
            ((13, 15), token.MySQLKeywordToken, 'GROUP', 16),
            (16, token.MySQLKeywordToken, 'BY', 17),
            (17, component.expression.MySQLExpressionComponent, None, 18),
            (17, component.identifier.MySQLColumnNameComponent, None, 18),
            (17, token.MySQLNumericToken, None, 18),
            (18, token.MySQLKeywordToken, 'ASC', 19),
            (18, token.MySQLKeywordToken, 'DESC', 19),
            ((18, 19), token.MySQLDelimiterToken, ',', 17),
            ((18, 19), token.MySQLKeywordToken, 'WITH', 20),
            (20, token.MySQLKeywordToken, 'ROLLUP', 21),
            ((13, 15, 18, 19, 21), token.MySQLKeywordToken, 'HAVING', 22),
            (22, component.expression.MySQLExpressionComponent, None, 23),
            ((13, 15, 18, 19, 21, 23), token.MySQLKeywordToken, 'ORDER', 24),
            (24, token.MySQLKeywordToken, 'BY', 25),
            (25, component.expression.MySQLExpressionComponent, None, 26),
            (25, component.identifier.MySQLColumnNameComponent, None, 26),
            (25, token.MySQLNumericToken, None, 26),
            (26, token.MySQLKeywordToken, 'ASC', 27),
            (26, token.MySQLKeywordToken, 'DESC', 27),
            ((26, 27), token.MySQLDelimiterToken, ',', 25),
            ((13, 15, 18, 19, 21, 23, 26, 27), token.MySQLKeywordToken, 'LIMIT', 28),
            (28, token.MySQLNumericToken, None, 29),
            (29, token.MySQLDelimiterToken, ',', 30),
            (29, token.MySQLKeywordToken, 'OFFSET', 30),
            (30, token.MySQLNumericToken, None, 31),
            ((13, 15, 18, 19, 21, 23, 26, 27, 29, 31), token.MySQLKeywordToken, 'PROCEDURE', 32),
            (32, component.identifier.MySQLIdentifierComponent, None, 33),
            (33, token.MySQLOperatorToken, '(', 34),
            (34, component.identifier.MySQLIdentifierComponent, None, 35),
            (35, token.MySQLOperatorToken, ')', 36),
            (35, token.MySQLDelimiterToken, ',', 34),
            ((13, 15, 18, 19, 21, 23, 26, 27, 29, 31, 36), token.MySQLKeywordToken, 'INTO', 37),
            (37, token.MySQLKeywordToken, 'OUTFILE', 38),
            (38, token.MySQLStringToken, None, 39),
            (39, token.MySQLKeywordToken, 'CHARACTER', 40),
            (40, token.MySQLKeywordToken, 'SET', 41),
            (39, token.MySQLKeywordToken, 'CHARSET', 41),
            (41, component.identifier.MySQLCharsetNameComponent, None, 42),
            ((39, 42), component.option.MySQLExportOptionComponent, None, 43),
            (37, token.MySQLKeywordToken, 'DUMPFILE', 44),
            (44, token.MySQLStringToken, None, 43),
            ((37, 46), token.MySQLVariableToken, None, 45),
            (45, token.MySQLDelimiterToken, ',', 46),
            ((13, 15, 18, 19, 21, 23, 26, 27, 29, 31, 36, 39, 42, 43, 45), token.MySQLKeywordToken, 'FOR', 47),
            (47, token.MySQLKeywordToken, 'UPDATE', 53),
            ((13, 15, 18, 19, 21, 23, 26, 27, 29, 31, 36, 39, 42, 43, 45), token.MySQLKeywordToken, 'LOCK', 48),
            (48, token.MySQLKeywordToken, 'IN', 49),
            (49, token.MySQLKeywordToken, 'SHARE', 50),
            (50, token.MySQLKeywordToken, 'MODE', 53),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        s = SelectStatement()
        end_pos = s.parse_by_fsm(token_list, [10, 13, 15, 18, 19, 21, 23, 26, 27, 29, 31, 36, 39, 42, 43, 45, 52, 53], verbose_func=verbose_func)
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
                        s.database.extend(tt.database)
                        s.table.extend(tt.table)
            token_list.reset(end_pos)
            return s, token_list

# 13.2.9.3 UNION Syntax
# SELECT ...
# UNION [ALL | DISTINCT] SELECT ...
# [UNION [ALL | DISTINCT] SELECT ...]
#
# (SELECT a FROM t1 WHERE a=10 AND B=1 ORDER BY a LIMIT 10)
#  UNION
# (SELECT a FROM t2 WHERE a=11 AND B=2 ORDER BY a LIMIT 10);
#
# (SELECT a FROM t1 WHERE a=10 AND B=1)
#  UNION
# (SELECT a FROM t2 WHERE a=11 AND B=2)
#  ORDER BY a LIMIT 10;

class UnionStatement(statement.MySQLStatement):
    def __init__(self):
        super(UnionStatement, self).__init__()
        self.database = []
        self.table = []
    
    def get_fsm_map(self):
        return (
            (0, SelectStatement, None, 1),
            ((1, 4), token.MySQLKeywordToken, 'UNION', 2),
            (2, token.MySQLKeywordToken, 'ALL', 3),
            (2, token.MySQLKeywordToken, 'DISTINCT', 3),
            ((2, 3), SelectStatement, None, 4),
            (0, token.MySQLOperatorToken, '(', 5),
            (5, SelectStatement, None, 6),
            (6, token.MySQLOperatorToken, ')', 7),
            ((7, 12), token.MySQLKeywordToken, 'UNION', 8),
            (8, token.MySQLKeywordToken, 'ALL', 9),
            (8, token.MySQLKeywordToken, 'DISTINCT', 9),
            ((8, 9), token.MySQLOperatorToken, '(', 10),
            (10, SelectStatement, None, 11),
            (11, token.MySQLOperatorToken, ')', 12),
            (12, token.MySQLKeywordToken, 'ORDER', 13),
            (13, token.MySQLKeywordToken, 'BY', 14),
            (14, component.expression.MySQLExpressionComponent, None, 15),
            (14, component.identifier.MySQLColumnNameComponent, None, 15),
            (14, token.MySQLNumericToken, None, 15),
            (15, token.MySQLKeywordToken, 'ASC', 16),
            (15, token.MySQLKeywordToken, 'DESC', 16),
            (16, token.MySQLDelimiterToken, ',', 14),
            ((12, 15, 16), token.MySQLKeywordToken, 'LIMIT', 17),
            (17, token.MySQLNumericToken, None, 18),
            (18, token.MySQLDelimiterToken, ',', 19),
            (18, token.MySQLKeywordToken, 'OFFSET', 19),
            (19, token.MySQLNumericToken, None, self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        s = UnionStatement()
        end_pos = s.parse_by_fsm(token_list, [4, 12, 15, 16, 18], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            for t in s.token_list:
                if type(t) is SelectStatement:
                    s.database.extend(t.database)
                    s.table.extend(t.table)
            token_list.reset(end_pos)
            return s, token_list

