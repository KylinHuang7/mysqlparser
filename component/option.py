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
import component.definition

class MySQLNumericOptionValueComponent(component.MySQLComponent):
    def get_fsm_map(self):
        return (
            (0, token.MySQLOperatorToken, '=', 1),
            ((0, 1), token.MySQLNumericToken, None, self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLNumericOptionValueComponent()
        end_pos = c.parse_by_fsm(token_list, verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            token_list.reset(end_pos)
            return c, token_list

class MySQLBooleanOptionValueComponent(component.MySQLComponent):
    def get_fsm_map(self):
        return (
            (0, token.MySQLOperatorToken, '=', 1),
            ((0, 1), token.MySQLNumericToken, 0, self.get_final_status()),
            ((0, 1), token.MySQLNumericToken, 1, self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLBooleanOptionValueComponent()
        end_pos = c.parse_by_fsm(token_list, verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            token_list.reset(end_pos)
            return c, token_list

class MySQLStringOptionValueComponent(component.MySQLComponent):
    def get_fsm_map(self):
        return (
            (0, token.MySQLOperatorToken, '=', 1),
            ((0, 1), token.MySQLStringToken, None, self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLStringOptionValueComponent()
        end_pos = c.parse_by_fsm(token_list, verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            token_list.reset(end_pos)
            return c, token_list


#   [DEFAULT] CHARACTER SET [=] charset_name
# | [DEFAULT] COLLATE [=] collation_name
class MySQLDatabaseOptionComponent(component.MySQLComponent):
    def get_fsm_map(self):
        #   ／-------CHARACRTER--------↘              ／------charset_name-------↘
        # 0 --DEFAULT--> 1 --CHARACTER--> 2 --SET--> 3 -- = --> 4 --charset_name--->
        #                  ＼--COLLATE---> 5 -- = --> 6 -------collation_name-----↗
        #   ＼----------COLLATE--------↗   ＼-----------collation_name-----------↗
        return (
            (0, token.MySQLKeywordToken, 'DEFAULT', 1),
            ((0, 1), token.MySQLKeywordToken, 'CHARACTER', 2),
            ((0, 1), token.MySQLKeywordToken, 'COLLATE', 5),
            (2, token.MySQLKeywordToken, 'SET', 3),
            ((0, 1), token.MySQLKeywordToken, 'CHARSET', 3),
            (3, token.MySQLOperatorToken, '=', 4),
            ((3, 4), component.identifier.MySQLCharsetNameComponent, None, self.get_final_status()),
            (5, token.MySQLOperatorToken, '=', 6),
            ((5, 6), component.identifier.MySQLCollationNameComponent, None, self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLDatabaseOptionComponent()
        end_pos = c.parse_by_fsm(token_list, verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            token_list.reset(end_pos)
            return c, token_list


# table_option:
#   AUTO_INCREMENT [=] value
# | AVG_ROW_LENGTH [=] value
# | [DEFAULT] CHARACTER SET [=] charset_name
# | CHECKSUM [=] {0 | 1}
# | [DEFAULT] COLLATE [=] collation_name
# | COMMENT [=] 'string'
# | CONNECTION [=] 'connect_string'
# | {DATA|INDEX} DIRECTORY [=] 'absolute path to directory'
# | DELAY_KEY_WRITE [=] {0 | 1}
# | ENGINE [=] engine_name
# | INSERT_METHOD [=] { NO | FIRST | LAST }
# | KEY_BLOCK_SIZE [=] value
# | MAX_ROWS [=] value
# | MIN_ROWS [=] value
# | PACK_KEYS [=] {0 | 1 | DEFAULT}
# | PASSWORD [=] 'string'
# | ROW_FORMAT [=] {DEFAULT|DYNAMIC|FIXED|COMPRESSED|REDUNDANT|COMPACT}
# | TABLESPACE tablespace_name [STORAGE {DISK|MEMORY|DEFAULT}]
# | UNION [=] (tbl_name[,tbl_name]...)
class MySQLTableOptionComponent(component.MySQLComponent):
    def get_fsm_map(self):
        #0 --AUTO_INCREMENT--> 1 --numeric_option_value--> 
        #  ＼--AVG_ROW_LENGTH--> 2 --numeric_option_value-↗
        #  ＼--database_option--↗
        #  ＼--CHECKSUM--> 3 --boolean_option_value-↗
        #  ＼--COMMENT--> 4 --string_option_value-↗ 
        #  ＼--CONNECTION--> 5 --string_option_value-↗ 
        #  ＼--DATA----> 6 --DIRECTORY--> 7 --string_option_value-↗ 
        #  ＼--INDEX--↗ 
        #  ＼--DELAY_KEY_WRITE--> 8 --boolean_option_value-↗
        #  ＼--ENGINE--> 9 -- = --> 25 --engine_name-↗ 
        #                  ＼------engine_name-------↗ 
        #  ＼--INSERT_METHOD--> 10 -- = --> 11 -----NO----↗ 
        #                                      ＼--FIRST--↗ 
        #                                      ＼---LAST--↗ 
        #                          ＼----------NO---------↗ 
        #                          ＼--------FIRST--------↗ 
        #                          ＼---------LAST--------↗ 
        #  ＼--KEY_BLOCK_SIZE--> 12 --numeric_option_value--> 
        #  ＼--MAX_ROWS--> 13 --numeric_option_value--> 
        #  ＼--MIN_ROWS--> 14 --numeric_option_value--> 
        #  ＼--PACK_KEYS--> 15 -- = --> 16 -------0------↗ 
        #                                  ＼-----1------↗ 
        #                                  ＼---DEFAULT--↗ 
        #                      ＼------------0-----------↗ 
        #                      ＼------------1-----------↗ 
        #                      ＼---------DEFAULT--------↗ 
        #  ＼--PASSWORD--> 17 --string_option_value-↗ 
        #  ＼--ROW_FORMAT--> 18 -- = --> 19 -------DEFAULT------↗ 
        #                                  ＼------DYNAMIC------↗ 
        #                                  ＼--------FIXED------↗ 
        #                                  ＼-----COMPRESSED----↗ 
        #                                  ＼-----REDUNDANT-----↗ 
        #                                  ＼-------COMPACT-----↗ 
        #                       ＼-----------DEFAULT------------↗ 
        #                       ＼-----------DYNAMIC------------↗ 
        #                       ＼-------------FIXED------------↗ 
        #                       ＼----------COMPRESSED----------↗ 
        #                       ＼----------REDUNDANT-----------↗ 
        #                       ＼------------COMPACT-----------↗ 
        #  ＼--TABLESPACE--> 20 --tablespace_name--> 21 -->
        #                                               ＼--STORAGE--> 22 -----DISK----↗
        #                                                                 ＼---MEMORY--↗ 
        #                                                                 ＼--DEFAULT--↗ 
        #  ＼--UNION--> 23 --> = --> 24 --> table_name_list -->
        #                  ＼--------table_name_list---------↗ 
        return (
            (0, token.MySQLKeywordToken, 'AUTO_INCREMENT', 1),
            (1, MySQLNumericOptionValueComponent, None, self.get_final_status()),
            (0, token.MySQLKeywordToken, 'AVG_ROW_LENGTH', 2),
            (2, MySQLNumericOptionValueComponent, None, self.get_final_status()),
            (0, MySQLDatabaseOptionComponent, None, self.get_final_status()),
            (0, token.MySQLKeywordToken, 'CHECKSUM', 3),
            (3, MySQLBooleanOptionValueComponent, 0, self.get_final_status()),
            (0, token.MySQLKeywordToken, 'COMMENT', 4),
            (4, MySQLStringOptionValueComponent, None, self.get_final_status()),
            (0, token.MySQLKeywordToken, 'CONNECTION', 5),
            (5, MySQLStringOptionValueComponent, None, self.get_final_status()),
            (0, token.MySQLKeywordToken, 'DATA', 6),
            (0, token.MySQLKeywordToken, 'INDEX', 6),
            (6, token.MySQLKeywordToken, 'DIRECTORY', 7),
            (7, MySQLStringOptionValueComponent, None, self.get_final_status()),
            (0, token.MySQLKeywordToken, 'DELAY_KEY_WRITE', 8),
            (8, MySQLBooleanOptionValueComponent, 0, self.get_final_status()),
            (0, token.MySQLKeywordToken, 'ENGINE', 9),
            (9, token.MySQLOperatorToken, '=', 25),
            ((9, 25), component.identifier.MySQLEngineNameComponent, None, self.get_final_status()),
            (0, token.MySQLKeywordToken, 'INSERT_METHOD', 10),
            (10, token.MySQLOperatorToken, '=', 11),
            ((10, 11), token.MySQLKeywordToken, 'NO', self.get_final_status()),
            ((10, 11), token.MySQLKeywordToken, 'FIRST', self.get_final_status()),
            ((10, 11), token.MySQLKeywordToken, 'LAST', self.get_final_status()),
            (0, token.MySQLKeywordToken, 'KEY_BLOCK_SIZE', 12),
            (12, MySQLNumericOptionValueComponent, None, self.get_final_status()),
            (0, token.MySQLKeywordToken, 'MAX_ROWS', 13),
            (13, MySQLNumericOptionValueComponent, None, self.get_final_status()),
            (0, token.MySQLKeywordToken, 'MIN_ROWS', 14),
            (14, MySQLNumericOptionValueComponent, None, self.get_final_status()),
            (0, token.MySQLKeywordToken, 'PACK_KEYS', 15),
            (15, token.MySQLOperatorToken, '=', 16),
            ((15, 16), token.MySQLNumericToken, 0, self.get_final_status()),
            ((15, 16), token.MySQLNumericToken, 1, self.get_final_status()),
            ((15, 16), token.MySQLKeywordToken, 'DEFAULT', self.get_final_status()),
            (0, token.MySQLKeywordToken, 'PASSWORD', 17),
            (17, MySQLStringOptionValueComponent, None, self.get_final_status()),
            (0, token.MySQLKeywordToken, 'INSERT_METHOD', 18),
            (18, token.MySQLOperatorToken, '=', 19),
            ((18, 19), token.MySQLKeywordToken, 'DEFAULT', self.get_final_status()),
            ((18, 19), token.MySQLKeywordToken, 'DYNAMIC', self.get_final_status()),
            ((18, 19), token.MySQLKeywordToken, 'FIXED', self.get_final_status()),
            ((18, 19), token.MySQLKeywordToken, 'COMPRESSED', self.get_final_status()),
            ((18, 19), token.MySQLKeywordToken, 'REDUNDANT', self.get_final_status()),
            ((18, 19), token.MySQLKeywordToken, 'COMPACT', self.get_final_status()),
            (0, token.MySQLKeywordToken, 'TABLESPACE', 20),
            (20, component.identifier.MySQLIdentifierComponent, None, 21),
            (21, token.MySQLKeywordToken, 'STORAGE', 22),
            (22, token.MySQLKeywordToken, 'DISK', self.get_final_status()),
            (22, token.MySQLKeywordToken, 'MEMORY', self.get_final_status()),
            (22, token.MySQLKeywordToken, 'DEFAULT', self.get_final_status()),
            (0, token.MySQLKeywordToken, 'UNION', 23),
            (23, token.MySQLOperatorToken, '=', 24),
            ((23, 24), component.identifier.MySQLTableNameListComponent, None, self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLTableOptionComponent()
        end_pos = c.parse_by_fsm(token_list, [21], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            token_list.reset(end_pos)
            return c, token_list

# table_options:
#   table_option [[,] table_option] ...
class MySQLTableOptionListComponent(component.MySQLComponent):
    def get_fsm_map(self):
        return (
            ((0, 1, 2), MySQLTableOptionComponent, None, 1),
            (1, token.MySQLDelimiterToken, ',', 2),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLTableOptionListComponent()
        end_pos = c.parse_by_fsm(token_list, [1], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            token_list.reset(end_pos)
            return c, token_list

# index_type:
#   USING {BTREE | HASH}
class MySQLIndexTypeComponent(component.MySQLComponent):
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'USING', 1),
            (1, token.MySQLKeywordToken, 'BTREE', self.get_final_status()),
            (1, token.MySQLKeywordToken, 'HASH', self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLIndexTypeComponent()
        end_pos = c.parse_by_fsm(token_list, verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            token_list.reset(end_pos)
            return c, token_list

# index_option:
#   KEY_BLOCK_SIZE [=] value
# | index_type
# | WITH PARSER parser_name
# | COMMENT 'string'
class MySQLIndexOptionComponent(component.MySQLComponent):
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'KEY_BLOCK_SIZE', 1),
            (1, MySQLNumericOptionValueComponent, None, self.get_final_status()),
            (0, MySQLIndexTypeComponent, None, self.get_final_status()),
            (0, token.MySQLKeywordToken, 'WITH', 2),
            (2, token.MySQLKeywordToken, 'PARSER', 3),
            (3, component.identifier.MySQLIdentifierComponent, None, self.get_final_status()),
            (0, token.MySQLKeywordToken, 'COMMENT', 4),
            (4, token.MySQLStringToken, None, self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLIndexOptionComponent()
        end_pos = c.parse_by_fsm(token_list, verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            token_list.reset(end_pos)
            return c, token_list

# reference_option:
#   RESTRICT | CASCADE | SET NULL | NO ACTION | SET DEFAULT
class MySQLReferenceOptionComponent(component.MySQLComponent):
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'RESTRICT', self.get_final_status()),
            (0, token.MySQLKeywordToken, 'CASCADE', self.get_final_status()),
            (0, token.MySQLKeywordToken, 'SET', 1),
            (1, token.MySQLNullToken, 'NULL', self.get_final_status()),
            (1, token.MySQLKeywordToken, 'DEFAULT', self.get_final_status()),
            (0, token.MySQLKeywordToken, 'NO', 2),
            (2, token.MySQLKeywordToken, 'ACTION', self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLReferenceOptionComponent()
        end_pos = c.parse_by_fsm(token_list, verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            token_list.reset(end_pos)
            return c, token_list

# partition_options:
#    PARTITION BY
#        { [LINEAR] HASH(expr)
#        | [LINEAR] KEY [ALGORITHM={1|2}] (column_list)
#        | RANGE{(expr) | COLUMNS(column_list)}
#        | LIST{(expr) | COLUMNS(column_list)} }
#    [PARTITIONS num]
#    [SUBPARTITION BY
#        { [LINEAR] HASH(expr)
#        | [LINEAR] KEY [ALGORITHM={1|2}] (column_list) }
#      [SUBPARTITIONS num]
#    ]
#    [(partition_definition [, partition_definition] ...)]
class MySQLPartitionOptionComponent(component.MySQLComponent):
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'PARTITION', 1),
            (1, token.MySQLKeywordToken, 'BY', 2),
            (2, component.expression.MySQLPartitioningExpressionComponent, None, 3),
            (3, token.MySQLKeywordToken, 'PARTITIONS', 4),
            (4, token.MySQLNumericToken, None, 5),
            ((3, 5), token.MySQLKeywordToken, 'SUBPARTITION', 6),
            (6, token.MySQLKeywordToken, 'BY', 7),
            (7, component.expression.MySQLSubPartitioningExpressionComponent, None, 8),
            (8, token.MySQLKeywordToken, 'SUBPARTITIONS', 9),
            (9, token.MySQLNumericToken, None, 10),
            ((3, 5, 8, 10, 12), component.definition.MySQLPartitionDefinitionComponent, None, 11),
            (11, token.MySQLDelimiterToken, ',', 12),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLPartitionOptionComponent()
        end_pos = c.parse_by_fsm(token_list, [3, 5, 8, 10, 11], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            token_list.reset(end_pos)
            return c, token_list

# order_options:
#   {col_name | expr | position}
#   [ASC | DESC]
class MySQLOrderOptionComponent(component.MySQLComponent):
    def get_fsm_map(self):
        return (
            (0, component.expression.MySQLExpressionComponent, None, 1),
            (0, component.identifier.MySQLColumnNameComponent, None, 1),
            (0, token.MySQLNumericToken, None, 1),
            (1, token.MySQLKeywordToken, 'ASC', self.get_final_status()),
            (1, token.MySQLKeywordToken, 'DESC', self.get_final_status()),
       )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLOrderOptionComponent()
        end_pos = c.parse_by_fsm(token_list, [1], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            token_list.reset(end_pos)
            return c, token_list

class MySQLOrderListOptionComponent(component.MySQLComponent):
    def get_fsm_map(self):
        return (
            ((0, 2), MySQLOrderOptionComponent, None, 1),
            (1, token.MySQLDelimiterToken, ',', 2),
       )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLOrderListOptionComponent()
        end_pos = c.parse_by_fsm(token_list, [1], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            token_list.reset(end_pos)
            return c, token_list

# index_hint:
#    USE {INDEX|KEY}
#      [FOR {JOIN|ORDER BY|GROUP BY}] ([index_list])
#  | IGNORE {INDEX|KEY}
#      [FOR {JOIN|ORDER BY|GROUP BY}] (index_list)
#  | FORCE {INDEX|KEY}
#      [FOR {JOIN|ORDER BY|GROUP BY}] (index_list)
class MySQLIndexHintOptionComponent(component.MySQLComponent):
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'USE', 1),
            (1, token.MySQLKeywordToken, 'INDEX', 2),
            (1, token.MySQLKeywordToken, 'KEY', 2),
            (2, token.MySQLKeywordToken, 'FOR', 3),
            (3, token.MySQLKeywordToken, 'JOIN', 5),
            (3, token.MySQLKeywordToken, 'ORDER', 4),
            (3, token.MySQLKeywordToken, 'GROUP', 4),
            (4, token.MySQLKeywordToken, 'BY', 5),
            ((2, 5), token.MySQLOperatorToken, '(', 6),
            ((6, 8), component.identifier.MySQLIdentifierComponent, None, 7),
            (7, token.MySQLDelimiterToken, ',', 8),
            ((6, 7, 15), token.MySQLOperatorToken, ')', self.get_final_status()),
            (0, token.MySQLKeywordToken, 'IGNORE', 9),
            (0, token.MySQLKeywordToken, 'FORCE', 9),
            (9, token.MySQLKeywordToken, 'INDEX', 10),
            (9, token.MySQLKeywordToken, 'KEY', 10),
            (10, token.MySQLKeywordToken, 'FOR', 11),
            (11, token.MySQLKeywordToken, 'JOIN', 13),
            (11, token.MySQLKeywordToken, 'ORDER', 12),
            (11, token.MySQLKeywordToken, 'GROUP', 12),
            (12, token.MySQLKeywordToken, 'BY', 13),
            ((10, 13), token.MySQLOperatorToken, '(', 14),
            ((14, 16), component.identifier.MySQLIdentifierComponent, None, 15),
            (15, token.MySQLDelimiterToken, ',', 16),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLIndexHintOptionComponent()
        end_pos = c.parse_by_fsm(token_list, verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            token_list.reset(end_pos)
            return c, token_list

# export_options:
#    [{FIELDS | COLUMNS}
#        [TERMINATED BY 'string']
#        [[OPTIONALLY] ENCLOSED BY 'char']
#        [ESCAPED BY 'char']
#    ]
#    [LINES
#        [STARTING BY 'string']
#        [TERMINATED BY 'string']
#    ]
class MySQLExportOptionComponent(component.MySQLComponent):
    def get_fsm_map(self):
        return (
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLExportOptionComponent()
        end_pos = c.parse_by_fsm(token_list, verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            token_list.reset(end_pos)
            return c, token_list
