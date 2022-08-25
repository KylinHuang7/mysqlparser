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

# 13.1.21 DROP DATABASE Syntax
# DROP { DATABASE | SCHEMA } [IF EXISTS] db_name
class DropDatabaseStatement(statement.MySQLStatement):
    def __init__(self):
        super(DropDatabaseStatement, self).__init__()
        self.database = ''
    
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'DROP', 1),
            (1, token.MySQLKeywordToken, 'DATABASE', 2),
            (1, token.MySQLKeywordToken, 'SCHEMA', 2),
            (2, token.MySQLKeywordToken, 'IF', 3),
            (3, token.MySQLKeywordToken, 'EXISTS', 4),
            ((2, 4), component.identifier.MySQLDatabaseNameComponent, None, self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        statement = DropDatabaseStatement()
        end_pos = statement.parse_by_fsm(token_list, verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            for t in statement.token_list:
                if type(t) is component.identifier.MySQLDatabaseNameComponent:
                    statement.database = t.database
            token_list.reset(end_pos)
            return statement, token_list

# 13.1.28 DROP TABLE Syntax
# DROP [TEMPORARY] TABLE [IF EXISTS] tbl_name
#   tbl_name [, tbl_name] ...
#   [RESTRICT | CASCADE]
class DropTableStatement(statement.MySQLStatement):
    def __init__(self):
        super(DropTableStatement, self).__init__()
        self.database = ''
        self.table = ''
    
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'DROP', 1),
            (1, token.MySQLKeywordToken, 'TEMPORARY', 2),
            ((1, 2), token.MySQLKeywordToken, 'TABLE', 3),
            (3, token.MySQLKeywordToken, 'IF', 4),
            (4, token.MySQLKeywordToken, 'EXISTS', 5),
            ((3, 5), component.identifier.MySQLTableNameListComponent, None, 6),
            (6, token.MySQLKeywordToken, 'RESTRICT', self.get_final_status()),
            (6, token.MySQLKeywordToken, 'CASCADE', self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        s = DropTableStatement()
        end_pos = s.parse_by_fsm(token_list, [6], verbose_func=verbose_func)
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

#  13.1.24 DROP INDEX Syntax
# DROP [ONLINE|OFFLINE] INDEX index_name ON tbl_name
class DropIndexStatement(statement.MySQLStatement):
    def __init__(self):
        super(DropIndexStatement, self).__init__()
        self.database = ''
        self.table = ''
    
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'DROP', 1),
            (1, token.MySQLKeywordToken, 'ONLINE', 2),
            (1, token.MySQLKeywordToken, 'OFFLINE', 2),
            ((1, 2),  token.MySQLKeywordToken, 'INDEX', 3),
            (3, component.identifier.MySQLIdentifierComponent, None, 4),
            (4, token.MySQLKeywordToken, 'ON', 5),
            (5, component.identifier.MySQLTableNameComponent, None, self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        s = DropIndexStatement()
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
