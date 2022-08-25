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
import component.option
import component.specification
import statement

# 13.1.1 ALTER DATABASE Syntax
# ALTER { DATABASE | SCHEMA } [db_name]
#   alter_specification ...
# ALTER { DATABASE | SCHEMA } db_name
#   UPGRADE DATA DIRECTORY NAME
class AlterDatabaseStatement(statement.MySQLStatement):
    def __init__(self):
        super(AlterDatabaseStatement, self).__init__()
        self.database = ''
    
    def get_fsm_map(self):
        # 0 --ALTER--> 1 --DATABASE--> 2 --db_name--> 3 -----------------database_option----------------------->
        #                ＼-SCHEMA--↗  ＼----------------------------database_option-------------------------↗
        #                                               ＼--UPGRADE--> 4 --DATA--> 5 --DIRECTORY--> 6 --NAME--↗
        return (
            (0, token.MySQLKeywordToken, 'ALTER', 1),
            (1, token.MySQLKeywordToken, 'DATABASE', 2),
            (1, token.MySQLKeywordToken, 'SCHEMA', 2),
            (2, component.identifier.MySQLDatabaseNameComponent, None, 3),
            ((2, 3, 7), component.option.MySQLDatabaseOptionComponent, None, 7),
            (3, token.MySQLKeywordToken, 'UPGRADE', 4),
            (4, token.MySQLKeywordToken, 'DATA', 5),
            (5, token.MySQLKeywordToken, 'DIRECTORY', 6),
            (6, token.MySQLKeywordToken, 'NAME', self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        s = AlterDatabaseStatement()
        end_pos = s.parse_by_fsm(token_list, [7], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            for t in s.token_list:
                if type(t) is component.identifier.MySQLDatabaseNameComponent:
                    s.database = t.database
            token_list.reset(end_pos)
            return s, token_list

# 13.1.7 ALTER TABLE Syntax
# ALTER [ONLINE|OFFLINE] [IGNORE] TABLE tbl_name
#   [alter_specification [, alter_specification] ...]
#   [partition_options]
#
class AlterTableStatement(statement.MySQLStatement):
    def __init__(self):
        super(AlterTableStatement, self).__init__()
        self.database = ''
        self.table = ''
    
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'ALTER', 1),
            (1, token.MySQLKeywordToken, 'ONLINE', 2),
            (1, token.MySQLKeywordToken, 'OFFLINE', 2),
            ((1, 2), token.MySQLKeywordToken, 'IGNORE', 3),
            ((1, 2, 3), token.MySQLKeywordToken, 'TABLE', 4),
            (4, component.identifier.MySQLTableNameComponent, None, 5),
            ((5, 7), component.specification.MySQLAlterTableSpecificationComponent, None, 6),
            (6, token.MySQLDelimiterToken, ',', 7),
            ((5, 6, 7), component.option.MySQLPartitionOptionComponent, None, self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        s = AlterTableStatement()
        end_pos = s.parse_by_fsm(token_list, [5, 6], verbose_func=verbose_func)
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

