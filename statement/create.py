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
import component.definition
import statement

# 13.1.10 CREATE DATABASE Syntax
# CREATE { DATABASE | SCHEMA } [IF NOT EXISTS] db_name
#   [create_specification] ...
class CreateDatabaseStatement(statement.MySQLStatement):
    def __init__(self):
        super(CreateDatabaseStatement, self).__init__()
        self.database = ''
    
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'CREATE', 1),
            (1, token.MySQLKeywordToken, 'DATABASE', 2),
            (1, token.MySQLKeywordToken, 'SCHEMA', 2),
            (2, token.MySQLKeywordToken, 'IF', 3),
            (3, token.MySQLKeywordToken, 'NOT', 4),
            (4, token.MySQLKeywordToken, 'EXISTS', 5),
            ((2, 5), component.identifier.MySQLDatabaseNameComponent, None, 6),
            ((6, 7), component.option.MySQLDatabaseOptionComponent, None, 7),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        s = CreateDatabaseStatement()
        end_pos = s.parse_by_fsm(token_list, [6, 7], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            for t in s.token_list:
                if type(t) is component.identifier.MySQLDatabaseNameComponent:
                    s.database = t.database
            token_list.reset(end_pos)
            return s, token_list

# 13.1.17 CREATE TABLE Syntax
# CREATE [TEMPORARY] TABLE [IF NOT EXISTS] tbl_name
#   (create_specification ...)
#   [table_options]
#   [partition_options]
#
# CREATE [TEMPORARY] TABLE [IF NOT EXISTS] tbl_name
#   (create_specification ...)
#   [table_options]
#   [partition_options]
#   [IGNORE | REPLACE]
#   [AS] query_expression
#
# CREATE [TEMPORARY] TABLE [IF NOT EXISTS] tbl_name
#   { LIKE old_tbl_name | (LIKE old_tbl_name) }
class CreateTableStatement(statement.MySQLStatement):
    def __init__(self):
        super(CreateTableStatement, self).__init__()
        self.database = ''
        self.table = ''
        self.from_database = ''
        self.from_table = ''
    
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'CREATE', 1),
            (1, token.MySQLKeywordToken, 'TEMPORARY', 2),
            ((1, 2), token.MySQLKeywordToken, 'TABLE', 3),
            (3, token.MySQLKeywordToken, 'IF', 4),
            (4, token.MySQLKeywordToken, 'NOT', 5),
            (5, token.MySQLKeywordToken, 'EXISTS', 6),
            ((3, 6), component.identifier.MySQLTableNameComponent, None, 7),
            (7, token.MySQLOperatorToken, '(', 8),
            ((8, 17), component.definition.MySQLCreateTableDefinitionComponent, None, 9),
            (9, token.MySQLDelimiterToken, ',', 17),
            (9, token.MySQLOperatorToken, ')', 10),
            (10, component.option.MySQLTableOptionListComponent, None, 11),
            ((10, 11), component.option.MySQLPartitionOptionComponent, None, 12),
            ((10, 11, 12), token.MySQLKeywordToken, 'IGNORE', 13),
            ((10, 11, 12), token.MySQLKeywordToken, 'REPLACE', 13),
            ((10, 11, 12, 13), token.MySQLKeywordToken, 'AS', 14),
            ((10, 11, 12, 13, 14), component.expression.MySQLExpressionComponent, None, self.get_final_status()),
            (7, token.MySQLKeywordToken, 'LIKE', 15),
            (15, component.identifier.MySQLTableNameComponent, None, self.get_final_status()),
            (8, token.MySQLKeywordToken, 'LIKE', 16),
            (16, token.MySQLOperatorToken, ')', self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        s = CreateTableStatement()
        end_pos = s.parse_by_fsm(token_list, [10, 11, 12], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            for t in s.token_list:
                if type(t) is component.identifier.MySQLTableNameComponent:
                    if s.table:
                        s.from_database = t.database
                        s.from_table = t.table
                    else:
                        s.database = t.database
                        s.table = t.table
                elif type(t) is component.expression.MySQLExpressionComponent:
                    for tt in filter((lambda x: type(x) is component.reference.SubQueryComponent), t.token_list):
                        s.database.extend(tt.database)
                        s.table.extend(tt.table)
            token_list.reset(end_pos)
            return s, token_list

#  13.1.13 CREATE INDEX Syntax
# CREATE [ONLINE|OFFLINE] [UNIQUE|FULLTEXT|SPATIAL] INDEX index_name
#    [index_type]
#    ON tbl_name (index_col_name,...)
#    [index_option] ...
class CreateIndexStatement(statement.MySQLStatement):
    def __init__(self):
        super(CreateIndexStatement, self).__init__()
        self.database = ''
        self.table = ''
    
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'CREATE', 1),
            (1, token.MySQLKeywordToken, 'ONLINE', 2),
            (1, token.MySQLKeywordToken, 'OFFLINE', 2),
            ((1, 2), token.MySQLKeywordToken, 'UNIQUE', 3),
            ((1, 2), token.MySQLKeywordToken, 'FULLTEXT', 3),
            ((1, 2), token.MySQLKeywordToken, 'SPATIAL', 3),
            ((1, 2, 3),  token.MySQLKeywordToken, 'INDEX', 4),
            (4, component.identifier.MySQLIdentifierComponent, None, 5),
            (5, component.option.MySQLIndexTypeComponent, None, 6),
            ((5, 6), token.MySQLKeywordToken, 'ON', 7),
            (7, component.identifier.MySQLTableNameComponent, None, 8),
            (8, token.MySQLOperatorToken, '(', 9),
            (9, component.identifier.MySQLIndexColumnNameListComponent, None, 10),
            (10, token.MySQLOperatorToken, ')', 11),
            ((11, 12), component.option.MySQLIndexOptionComponent, None, 12),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        s = CreateIndexStatement()
        end_pos = s.parse_by_fsm(token_list, [11, 12], verbose_func=verbose_func)
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
