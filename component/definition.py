#!/usr/local/ieod-web/python/bin/python
# -*- coding: utf-8 -*-

#=============================================================================
#  @desc       
#  @version    1.0.0
#  @author     kylinshuang
#  @date       2017-12-04
#=============================================================================

import mysqltoken as token
import component
import component.identifier
import component.expression
import component.option

# data_type:
#    BIT[(length)]
#  | TINYINT[(length)] [UNSIGNED] [ZEROFILL]
#  | SMALLINT[(length)] [UNSIGNED] [ZEROFILL]
#  | MEDIUMINT[(length)] [UNSIGNED] [ZEROFILL]
#  | INT[(length)] [UNSIGNED] [ZEROFILL]
#  | INTEGER[(length)] [UNSIGNED] [ZEROFILL]
#  | BIGINT[(length)] [UNSIGNED] [ZEROFILL]
#  | REAL[(length,decimals)] [UNSIGNED] [ZEROFILL]
#  | DOUBLE[(length,decimals)] [UNSIGNED] [ZEROFILL]
#  | FLOAT[(length,decimals)] [UNSIGNED] [ZEROFILL]
#  | DECIMAL[(length[,decimals])] [UNSIGNED] [ZEROFILL]
#  | NUMERIC[(length[,decimals])] [UNSIGNED] [ZEROFILL]
#  | DATE
#  | TIME
#  | TIMESTAMP
#  | DATETIME
#  | YEAR
#  | CHAR[(length)]
#      [CHARACTER SET charset_name] [COLLATE collation_name]
#  | VARCHAR(length)
#      [CHARACTER SET charset_name] [COLLATE collation_name]
#  | BINARY[(length)]
#  | VARBINARY(length)
#  | TINYBLOB
#  | BLOB[(length)]
#  | MEDIUMBLOB
#  | LONGBLOB
#  | TINYTEXT
#      [CHARACTER SET charset_name] [COLLATE collation_name]
#  | TEXT[(length)]
#      [CHARACTER SET charset_name] [COLLATE collation_name]
#  | MEDIUMTEXT
#      [CHARACTER SET charset_name] [COLLATE collation_name]
#  | LONGTEXT
#      [CHARACTER SET charset_name] [COLLATE collation_name]
#  | ENUM(value1,value2,value3,...)
#      [CHARACTER SET charset_name] [COLLATE collation_name]
#  | SET(value1,value2,value3,...)
#      [CHARACTER SET charset_name] [COLLATE collation_name]
#  | spatial_type
class MySQLDataTypeComponent(component.MySQLComponent):
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'DATE', self.get_final_status()),
            (0, token.MySQLKeywordToken, 'TIME', self.get_final_status()),
            (0, token.MySQLKeywordToken, 'TIMESTAMP', self.get_final_status()),
            (0, token.MySQLKeywordToken, 'DATETIME', self.get_final_status()),
            (0, token.MySQLKeywordToken, 'YEAR', self.get_final_status()),
            (0, token.MySQLKeywordToken, 'TINYBLOB', self.get_final_status()),
            (0, token.MySQLKeywordToken, 'MEDIUMBLOB', self.get_final_status()),
            (0, token.MySQLKeywordToken, 'LONGBLOB', self.get_final_status()),
            (0, token.MySQLKeywordToken, 'BIT', 1),
            (0, token.MySQLKeywordToken, 'BINARY', 1),
            (0, token.MySQLKeywordToken, 'BLOB', 1),
            (1, token.MySQLOperatorToken, '(', 2),
            (2, token.MySQLNumericToken, None, 3),
            (3, token.MySQLOperatorToken, ')', self.get_final_status()),
            (0, token.MySQLKeywordToken, 'TINYINT', 4),
            (0, token.MySQLKeywordToken, 'SMALLINT', 4),
            (0, token.MySQLKeywordToken, 'MEDIUMINT', 4),
            (0, token.MySQLKeywordToken, 'INT', 4),
            (0, token.MySQLKeywordToken, 'INTEGER', 4),
            (0, token.MySQLKeywordToken, 'BIGINT', 4),
            (0, token.MySQLKeywordToken, 'INTEGER', 4),
            (4, token.MySQLOperatorToken, '(', 5),
            (5, token.MySQLNumericToken, None, 6),
            ((6, 13, 16, 18), token.MySQLOperatorToken, ')', 7),
            ((4, 7), token.MySQLKeywordToken, 'UNSIGNED', 8),
            ((4, 7, 8), token.MySQLKeywordToken, 'ZEROFILL', self.get_final_status()),
            (0, token.MySQLKeywordToken, 'REAL', 9),
            (0, token.MySQLKeywordToken, 'DOUBLE', 9),
            (0, token.MySQLKeywordToken, 'FLOAT', 9),
            (9, token.MySQLOperatorToken, '(', 10),
            (10, token.MySQLNumericToken, None, 11),
            (11, token.MySQLDelimiterToken, ',', 12),
            (12, token.MySQLNumericToken, None, 13),
            (0, token.MySQLKeywordToken, 'DECIMAL', 14),
            (0, token.MySQLKeywordToken, 'NUMERIC', 14),
            (14, token.MySQLOperatorToken, '(', 15),
            (15, token.MySQLNumericToken, None, 16),
            (16, token.MySQLDelimiterToken, ',', 17),
            (17, token.MySQLNumericToken, None, 18),
            (0, token.MySQLKeywordToken, 'TINYTEXT', 19),
            (0, token.MySQLKeywordToken, 'MEDIUMTEXT', 19),
            (0, token.MySQLKeywordToken, 'LONGTEXT', 19),
            ((19, 24), token.MySQLKeywordToken, 'CHARACTER', 20),
            (20, token.MySQLKeywordToken, 'SET', 21),
            ((19, 24), token.MySQLKeywordToken, 'CHARSET', 21),
            (21, component.identifier.MySQLCharsetNameComponent, None, 22),
            ((19, 22, 24), token.MySQLKeywordToken, 'COLLATE', 23),
            (23, component.identifier.MySQLCollationNameComponent, None, self.get_final_status()),
            (0, token.MySQLKeywordToken, 'CHAR', 24),
            (0, token.MySQLKeywordToken, 'TEXT', 24),
            (24, token.MySQLOperatorToken, '(', 25),
            (25, token.MySQLNumericToken, None, 26),
            ((26, 30), token.MySQLOperatorToken, ')', 19),
            (0, token.MySQLKeywordToken, 'VARCHAR', 27),
            (27, token.MySQLOperatorToken, '(', 25),
            (0, token.MySQLKeywordToken, 'ENUM', 28),
            (0, token.MySQLKeywordToken, 'SET', 28),
            (28, token.MySQLOperatorToken, '(', 29),
            ((29, 31), token.MySQLStringToken, None, 30),
            (30, token.MySQLDelimiterToken, ',', 31),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLDataTypeComponent()
        end_pos = c.parse_by_fsm(token_list, [1, 4, 7, 8, 9, 14, 19, 22, 24], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            token_list.reset(end_pos)
            return c, token_list

# reference_definition:
#    REFERENCES tbl_name (index_col_name,...)
#      [MATCH FULL | MATCH PARTIAL | MATCH SIMPLE]
#      [ON DELETE reference_option]
#      [ON UPDATE reference_option]
class MySQLReferenceDefinitionComponent(component.MySQLComponent):
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'REFERENCES', 1),
            (0, component.identifier.MySQLTableNameComponent, None, 2),
            (2, token.MySQLOperatorToken, '(', 3),
            (3, component.identifier.MySQLIndexColumnNameListComponent, None, 4),
            (4, token.MySQLOperatorToken, ')', 5),
            (5, token.MySQLKeywordToken, 'MATCH', 6),
            (6, token.MySQLKeywordToken, 'FULL', 7),
            (6, token.MySQLKeywordToken, 'PARTIAL', 7),
            (6, token.MySQLKeywordToken, 'SIMPLE', 7),
            ((5, 7), token.MySQLKeywordToken, 'ON', 8),
            (8, token.MySQLKeywordToken, 'DELETE', 9),
            (9, component.option.MySQLReferenceOptionComponent, None, 10),
            (10, token.MySQLKeywordToken, 'ON', 11),
            ((8, 11), token.MySQLKeywordToken, 'UPDATE', 12),
            (12, component.option.MySQLReferenceOptionComponent, None, self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLReferenceDefinitionComponent()
        end_pos = c.parse_by_fsm(token_list, [5, 7, 10], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            token_list.reset(end_pos)
            return c, token_list

# column_definition:
#    data_type [NOT NULL | NULL] [DEFAULT default_value]
#      [AUTO_INCREMENT | ON UPDATE CURRENT_TIMESTAMP] [UNIQUE [KEY]] [[PRIMARY] KEY]
#      [COMMENT 'string']
#      [COLUMN_FORMAT {FIXED|DYNAMIC|DEFAULT}]
#      [STORAGE {DISK|MEMORY|DEFAULT}]
#      [reference_definition]
class MySQLColumnDefinitionComponent(component.MySQLComponent):
    def get_fsm_map(self):
        return (
            (0, MySQLDataTypeComponent, None, 1),
            ((1, 5, 6), token.MySQLKeywordToken, 'NOT', 2),
            ((1, 2), token.MySQLNullToken, 'NULL', 3),
            ((1, 3, 5, 6), token.MySQLKeywordToken, 'DEFAULT', 4),
            (4, token.MySQLStringToken, None, 5),
            (4, token.MySQLNumericToken, None, 5),
            (4, token.MySQLNullToken, None, 5),
            (4, token.MySQLKeywordToken, 'CURRENT_TIMESTAMP', 5),
            ((1, 3, 5), token.MySQLKeywordToken, 'ON', 17),
            (17, token.MySQLKeywordToken, 'UPDATE', 18),
            (18, token.MySQLKeywordToken, 'CURRENT_TIMESTAMP', 6),
            ((1, 3, 5), token.MySQLKeywordToken, 'AUTO_INCREMENT', 6),
            ((1, 3, 5, 6), token.MySQLKeywordToken, 'UNIQUE', 7),
            (7, token.MySQLKeywordToken, 'KEY', 8),
            ((1, 3, 5, 6, 7, 8), token.MySQLKeywordToken, 'PRIMARY', 9),
            ((1, 9), token.MySQLKeywordToken, 'KEY', 10),
            ((3, 5, 6, 7, 8), token.MySQLKeywordToken, 'KEY', 9),
            ((1, 3, 5, 6, 7, 8, 10), token.MySQLKeywordToken, 'COMMENT', 11),
            (11, token.MySQLStringToken, None, 12),
            ((1, 3, 5, 6, 7, 8, 10, 12), token.MySQLKeywordToken, 'COLUMN_FORMAT', 13),
            (13, token.MySQLKeywordToken, 'FIXED', 14),
            (13, token.MySQLKeywordToken, 'DYNAMIC', 14),
            (13, token.MySQLKeywordToken, 'DEFAULT', 14),
            ((1, 3, 5, 6, 7, 8, 10, 12, 14), token.MySQLKeywordToken, 'STORAGE', 15),
            (15, token.MySQLKeywordToken, 'DISK', 16),
            (15, token.MySQLKeywordToken, 'MEMORY', 16),
            (15, token.MySQLKeywordToken, 'DEFAULT', 16),
            ((1, 3, 5, 6, 7, 8, 10, 12, 14, 16), MySQLReferenceDefinitionComponent, None, self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLColumnDefinitionComponent()
        end_pos = c.parse_by_fsm(token_list, [1, 3, 5, 6, 7, 8, 10, 12, 14, 16], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            token_list.reset(end_pos)
            return c, token_list

# subpartition_definition:
#    SUBPARTITION logical_name
#        [[STORAGE] ENGINE [=] engine_name]
#        [COMMENT [=] 'string' ]
#        [DATA DIRECTORY [=] 'data_dir']
#        [INDEX DIRECTORY [=] 'index_dir']
#        [MAX_ROWS [=] max_number_of_rows]
#        [MIN_ROWS [=] min_number_of_rows]
#        [TABLESPACE [=] tablespace_name]
#        [NODEGROUP [=] node_group_id]
class MySQLSubPartitionDefinitionComponent(component.MySQLComponent):
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'SUBPARTITION', 1),
            (1, component.identifier.MySQLIdentifierComponent, None, 2),
            (2, token.MySQLKeywordToken, 'STORAGE', 3),
            ((2, 3), token.MySQLKeywordToken, 'ENGINE', 4),
            (4, token.MySQLOperatorToken, '=', 5),
            ((4, 5), component.identifier.MySQLEngineNameComponent, None, 6),
            ((2, 6), token.MySQLKeywordToken, 'COMMENT', 7),
            (7, component.option.MySQLStringOptionValueComponent, None, 8),
            ((2, 6, 8), token.MySQLKeywordToken, 'DATA', 9),
            (9, token.MySQLKeywordToken, 'DIRECTORY', 10),
            (10, component.option.MySQLStringOptionValueComponent, None, 11),
            ((2, 6, 8, 11), token.MySQLKeywordToken, 'INDEX', 12),
            (12, token.MySQLKeywordToken, 'DIRECTORY', 13),
            (13, component.option.MySQLStringOptionValueComponent, None, 14),
            ((2, 6, 8, 11, 14), token.MySQLKeywordToken, 'MAX_ROWS', 15),
            (15, component.option.MySQLNumericOptionValueComponent, None, 16),
            ((2, 6, 8, 11, 14, 16), token.MySQLKeywordToken, 'MIN_ROWS', 17),
            (17, component.option.MySQLNumericOptionValueComponent, None, 18),
            ((2, 6, 8, 11, 14, 16, 18), token.MySQLKeywordToken, 'TABLESPACE', 19),
            (19, token.MySQLOperatorToken, '=', 20),
            ((19, 20), component.identifier.MySQLIdentifierComponent, None, 21),
            ((2, 6, 8, 11, 14, 16, 18, 21), token.MySQLKeywordToken, 'NODEGROUP', 22),
            (22, component.option.MySQLNumericOptionValueComponent, None, self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLSubPartitionDefinitionComponent()
        end_pos = c.parse_by_fsm(token_list, [2, 6, 8, 11, 14, 16, 18, 21], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            token_list.reset(end_pos)
            return c, token_list

# partition_definition:
#    PARTITION partition_name
#        [VALUES
#            {LESS THAN {(expr | value_list) | MAXVALUE}
#            |
#            IN (value_list)}]
#        [[STORAGE] ENGINE [=] engine_name]
#        [COMMENT [=] 'string' ]
#        [DATA DIRECTORY [=] 'data_dir']
#        [INDEX DIRECTORY [=] 'index_dir']
#        [MAX_ROWS [=] max_number_of_rows]
#        [MIN_ROWS [=] min_number_of_rows]
#        [TABLESPACE [=] tablespace_name]
#        [NODEGROUP [=] node_group_id]
#        [(subpartition_definition [, subpartition_definition] ...)]
class MySQLPartitionDefinitionComponent(component.MySQLComponent):
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'PARTITION', 1),
            (1, component.identifier.MySQLIdentifierComponent, None, 2),
            (2, token.MySQLKeywordToken, 'VALUES', 3),
            (3, token.MySQLKeywordToken, 'LESS', 4),
            (4, token.MySQLKeywordToken, 'THAN', 5),
            (5, token.MySQLOperatorToken, '(', 6),
            (6, token.MySQLNumericToken, None, 7),
            (6, token.MySQLKeywordToken, 'MAXVALUE', 7),
            ((7, 11), token.MySQLOperatorToken, ')', 8),
            (7, token.MySQLDelimiterToken, ',', 6),
            (5, token.MySQLKeywordToken, 'MAXVALUE', 8),
            (3, token.MySQLKeywordToken, 'IN', 9),
            (9, token.MySQLOperatorToken, '(', 10),
            (10, token.MySQLNumericToken, None, 11),
            (11, token.MySQLDelimiterToken, ',', 10),
            ((2, 8), token.MySQLKeywordToken, 'STORAGE', 12),
            ((2, 8), token.MySQLKeywordToken, 'ENGINE', 13),
            (12, token.MySQLKeywordToken, 'ENGINE', 13),
            (13, token.MySQLOperatorToken, '=', 14),
            ((13, 14), component.identifier.MySQLEngineNameComponent, None, 15),
            ((2, 8, 15), token.MySQLKeywordToken, 'COMMENT', 16),
            (16, component.option.MySQLStringOptionValueComponent, None, 17),
            ((2, 8, 15, 17), token.MySQLKeywordToken, 'DATA', 18),
            (18, token.MySQLKeywordToken, 'DIRECTORY', 19),
            (19, component.option.MySQLStringOptionValueComponent, None, 20),
            ((2, 8, 15, 17, 20), token.MySQLKeywordToken, 'INDEX', 21),
            (21, token.MySQLKeywordToken, 'DIRECTORY', 22),
            (22, component.option.MySQLStringOptionValueComponent, None, 23),
            ((2, 8, 15, 17, 20, 23), token.MySQLKeywordToken, 'MAX_ROWS', 24),
            (24, component.option.MySQLNumericOptionValueComponent, None, 25),
            ((2, 8, 15, 17, 20, 23, 25), token.MySQLKeywordToken, 'MIN_ROWS', 26),
            (26, component.option.MySQLNumericOptionValueComponent, None, 27),
            ((2, 8, 15, 17, 20, 23, 25, 27), token.MySQLKeywordToken, 'TABLESPACE', 28),
            (28, token.MySQLOperatorToken, '=', 29),
            ((28, 29), component.identifier.MySQLIdentifierComponent, None, 30),
            ((2, 8, 15, 17, 20, 23, 25, 27, 30), token.MySQLKeywordToken, 'NODEGROUP', 31),
            (31, component.option.MySQLNumericOptionValueComponent, None, 32),
            ((2, 8, 15, 17, 20, 23, 25, 27, 30, 32, 8, 15, 17, 20, 23, 25, 27, 30), token.MySQLOperatorToken, '(', 33),
            (33, MySQLSubPartitionDefinitionComponent, None, 34),
            (34, token.MySQLOperatorToken, ')', self.get_final_status()),
            (34, token.MySQLDelimiterToken, ',', 33),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLPartitionDefinitionComponent()
        end_pos = c.parse_by_fsm(token_list, [2, 8, 15, 17, 20, 23, 25, 27, 30, 32], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            token_list.reset(end_pos)
            return c, token_list

# create_definition:
#    col_name column_definition
#  | [CONSTRAINT [symbol]] PRIMARY KEY [index_type] (index_col_name,...)
#      [index_option] ...
#  | {INDEX|KEY} [index_name] [index_type] (index_col_name,...)
#      [index_option] ...
#  | [CONSTRAINT [symbol]] UNIQUE [INDEX|KEY]
#      [index_name] [index_type] (index_col_name,...)
#      [index_option] ...
#  | {FULLTEXT|SPATIAL} [INDEX|KEY] [index_name] (index_col_name,...)
#      [index_option] ...
#  | [CONSTRAINT [symbol]] FOREIGN KEY
#      [index_name] (index_col_name,...) reference_definition
#  | CHECK (expr)
class MySQLCreateTableDefinitionComponent(component.MySQLComponent):
    def get_fsm_map(self):
        return (
            (0, component.identifier.MySQLColumnNameComponent, None, 1),
            (1, MySQLColumnDefinitionComponent, None, self.get_final_status()),
            (0, token.MySQLKeywordToken, 'CONSTRAINT', 2),
            (2, component.identifier.MySQLIdentifierComponent, None, 3),
            ((0, 2, 3), token.MySQLKeywordToken, 'PRIMARY', 4),
            (4, token.MySQLKeywordToken, 'KEY', 5),
            ((5, 10, 11), component.option.MySQLIndexTypeComponent, None, 6),
            ((5, 6, 10, 11), token.MySQLOperatorToken, '(', 7),
            (7, component.identifier.MySQLIndexColumnNameComponent, None, 8),
            (8, token.MySQLOperatorToken, ')', 9),
            (8, token.MySQLDelimiterToken, ',', 7),
            (9, component.option.MySQLIndexOptionComponent, None, 9),
            ((0, 11), token.MySQLKeywordToken, 'INDEX', 10),
            ((0, 11), token.MySQLKeywordToken, 'KEY', 10),
            ((10, 11), component.identifier.MySQLIdentifierComponent, None, 5),
            ((0, 2, 3), token.MySQLKeywordToken, 'UNIQUE', 11),
            (0, token.MySQLKeywordToken, 'FULLTEXT', 11),
            (0, token.MySQLKeywordToken, 'SPATIAL', 11),
            ((0, 2, 3), token.MySQLKeywordToken, 'FOREIGN', 12),
            (12, token.MySQLKeywordToken, 'KEY', 13),
            (13, component.identifier.MySQLIdentifierComponent, None, 14),
            ((13, 14), token.MySQLOperatorToken, '(', 15),
            (15, component.identifier.MySQLIndexColumnNameComponent, None, 16),
            (16, token.MySQLOperatorToken, ')', 17),
            (16, token.MySQLDelimiterToken, ',', 15),
            (17, MySQLReferenceDefinitionComponent, None, self.get_final_status()),
            (0, token.MySQLKeywordToken, 'CHECK', 18),
            (18, token.MySQLOperatorToken, '(', 19),
            (19, component.expression.MySQLPartitioningExpressionComponent, None, 20),
            (20, token.MySQLOperatorToken, ')', self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLCreateTableDefinitionComponent()
        end_pos = c.parse_by_fsm(token_list, [9], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            token_list.reset(end_pos)
            return c, token_list
