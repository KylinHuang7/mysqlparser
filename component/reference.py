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
import component.option
import statement
import statement.select

class SubQueryComponent(component.MySQLComponent):
    def __init__(self):
        super(SubQueryComponent, self).__init__()
        self.database = []
        self.table = []
    
    def get_fsm_map(self):
        return (
            (0, token.MySQLOperatorToken, '(', 1),
            (1, statement.select.UnionStatement, None, 2),
            (1, statement.select.SelectStatement, None, 2),
            (2, token.MySQLOperatorToken, ')', self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        s = SubQueryComponent()
        end_pos = s.parse_by_fsm(token_list, verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            for t in s.token_list:
                if type(t) is statement.select.SelectStatement:
                    s.database.extend(t.database)
                    s.table.extend(t.table)
                elif type(t) is statement.select.UnionStatement:
                    s.database.extend(t.database)
                    s.table.extend(t.table)
            token_list.reset(end_pos)
            return s, token_list

# table_factor:
#    tbl_name [[AS] alias] [index_hint_list]
#  | table_subquery [AS] alias
#  | ( table_references )
class TableFactorComponent(component.MySQLComponent):
    def __init__(self):
        super(TableFactorComponent, self).__init__()
        self.database = []
        self.table = []
    
    def get_fsm_map(self):
        return (
            (0, component.identifier.MySQLTableNameComponent, None, 1),
            (1, token.MySQLKeywordToken, 'AS', 2),
            ((1, 2), component.identifier.MySQLIdentifierComponent, None, 3),
            ((1, 3, 5), component.option.MySQLIndexHintOptionComponent, None, 4),
            (4, token.MySQLDelimiterToken, ',', 5),
            (0, SubQueryComponent, None, 6),
            (6, token.MySQLKeywordToken, 'AS', 7),
            ((6, 7), component.identifier.MySQLIdentifierComponent, None, self.get_final_status()),
            (0, token.MySQLOperatorToken, '(', 8),
            (8, TableReferenceComponent, None, 9),
            (9, token.MySQLOperatorToken, ')', self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        s = TableFactorComponent()
        end_pos = s.parse_by_fsm(token_list, [1, 3, 4], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            for t in s.token_list:
                if type(t) is SubQueryComponent:
                    s.database.extend(t.database)
                    s.table.extend(t.table)
                elif type(t) is component.identifier.MySQLTableNameComponent:
                    s.database.append(t.database)
                    s.table.append(t.table)
            token_list.reset(end_pos)
            return s, token_list

# table_reference:
#    table_factor
#  | join_table
#
# join_table:
#    table_reference [INNER | CROSS] JOIN table_factor [join_condition]
#  | table_reference STRAIGHT_JOIN table_factor
#  | table_reference STRAIGHT_JOIN table_factor ON conditional_expr
#  | table_reference {LEFT|RIGHT} [OUTER] JOIN table_reference join_condition
#  | table_reference NATURAL [{LEFT|RIGHT} [OUTER]] JOIN table_factor
#
# join_condition:
#    ON conditional_expr
#  | USING (column_list)

class TableReferenceComponent(component.MySQLComponent):
    def __init__(self):
        super(TableReferenceComponent, self).__init__()
        self.database = []
        self.table = []
    
    def get_fsm_map(self):
        return (
            (0, TableFactorComponent, None, 1),
            (1, token.MySQLKeywordToken, 'INNER', 2),
            (1, token.MySQLKeywordToken, 'CROSS', 2),
            ((1, 2), token.MySQLKeywordToken, 'JOIN', 3),
            (3, TableFactorComponent, None, 4),
            ((4, 10, 14), token.MySQLKeywordToken, 'ON', 5),
            (5, component.expression.MySQLExpressionComponent, None, 1),
            ((4, 14), token.MySQLKeywordToken, 'USING', 6),
            (6, token.MySQLOperatorToken, '(', 7),
            (7, component.identifier.MySQLColumnNameListComponent, None, 8),
            (8, token.MySQLOperatorToken, ')', 1),
            (1, token.MySQLKeywordToken, 'STRAIGHT_JOIN', 9),
            (9, TableFactorComponent, None, 10),
            (1, token.MySQLKeywordToken, 'LEFT', 11),
            (1, token.MySQLKeywordToken, 'RIGHT', 11),
            (11, token.MySQLKeywordToken, 'OUTER', 12),
            ((11, 12), token.MySQLKeywordToken, 'JOIN', 13),
            (13, TableFactorComponent, None, 14),
            (1, token.MySQLKeywordToken, 'NATURAL', 15),
            (15, token.MySQLKeywordToken, 'LEFT', 16),
            (15, token.MySQLKeywordToken, 'RIGHT', 16),
            (16, token.MySQLKeywordToken, 'OUTER', 17),
            ((15, 16, 17), token.MySQLKeywordToken, 'JOIN', 18),
            (18, TableFactorComponent, None, 1),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        s = TableReferenceComponent()
        end_pos = s.parse_by_fsm(token_list, [1, 4, 10], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            for t in s.token_list:
                if type(t) is TableFactorComponent:
                    s.database.extend(t.database)
                    s.table.extend(t.table)
                elif type(t) is component.expression.MySQLExpressionComponent:
                    for tt in filter((lambda x: type(x) is component.reference.SubQueryComponent), t.token_list):
                        s.database.extend(tt.database)
                        s.table.extend(tt.table)
            token_list.reset(end_pos)
            return s, token_list

# table_references:
#    escaped_table_reference [, escaped_table_reference] ...
#
# escaped_table_reference:
#    table_reference
#  | { OJ table_reference }
#
class TableReferenceListComponent(component.MySQLComponent):
    def __init__(self):
        super(TableReferenceListComponent, self).__init__()
        self.database = []
        self.table = []
    
    def get_fsm_map(self):
        return (
            ((0, 2, 3), TableReferenceComponent, None, 1),
            ((0, 3), token.MySQLKeywordToken, 'OJ', 2),
            (1, token.MySQLDelimiterToken, ',', 3),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        s = TableReferenceListComponent()
        end_pos = s.parse_by_fsm(token_list, [1], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            for t in s.token_list:
                if type(t) is TableReferenceComponent:
                    s.database.extend(t.database)
                    s.table.extend(t.table)
            token_list.reset(end_pos)
            return s, token_list
