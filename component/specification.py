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
import component.option
import component.definition
import component.expression

# alter_specification:
#   table_options
# | ADD [COLUMN] col_name column_definition
#       [FIRST | AFTER col_name]
# | ADD [COLUMN] (col_name column_definition,...)
# | ADD {INDEX|KEY} [index_name]
#       [index_type] (index_col_name,...) [index_option] ...
# | ADD [CONSTRAINT [symbol]] PRIMARY KEY
#       [index_type] (index_col_name,...) [index_option] ...
# | ADD [CONSTRAINT [symbol]]
#       UNIQUE [INDEX|KEY] [index_name]
#       [index_type] (index_col_name,...) [index_option] ...
# | ADD FULLTEXT [INDEX|KEY] [index_name]
#       (index_col_name,...) [index_option] ...
# | ADD SPATIAL [INDEX|KEY] [index_name]
#       (index_col_name,...) [index_option] ...
# | ADD [CONSTRAINT [symbol]]
#       FOREIGN KEY [index_name] (index_col_name,...)
#       reference_definition
# | ALTER [COLUMN] col_name {SET DEFAULT literal | DROP DEFAULT}
# | CHANGE [COLUMN] old_col_name new_col_name column_definition
#       [FIRST|AFTER col_name]
# | [DEFAULT] CHARACTER SET [=] charset_name [COLLATE [=] collation_name]
# | CONVERT TO CHARACTER SET charset_name [COLLATE collation_name]
# | {DISABLE|ENABLE} KEYS
# | {DISCARD|IMPORT} TABLESPACE
# | DROP [COLUMN] col_name
# | DROP {INDEX|KEY} index_name
# | DROP PRIMARY KEY
# | DROP FOREIGN KEY fk_symbol
# | FORCE
# | MODIFY [COLUMN] col_name column_definition
#       [FIRST | AFTER col_name]
# | ORDER BY col_name [, col_name] ...
# | RENAME [TO|AS] new_tbl_name
# | ADD PARTITION (partition_definition)
# | DROP PARTITION partition_names
# | TRUNCATE PARTITION {partition_names | ALL}
# | COALESCE PARTITION number
# | REORGANIZE PARTITION [partition_names INTO (partition_definitions)]
# | ANALYZE PARTITION {partition_names | ALL}
# | CHECK PARTITION {partition_names | ALL}
# | OPTIMIZE PARTITION {partition_names | ALL}
# | REBUILD PARTITION {partition_names | ALL}
# | REPAIR PARTITION {partition_names | ALL}
# | REMOVE PARTITIONING
class MySQLAlterTableSpecificationComponent(component.MySQLComponent):
    def get_fsm_map(self):
        return (
            (0, component.option.MySQLTableOptionListComponent, None, self.get_final_status()),
            (0, token.MySQLKeywordToken, 'ADD', 1),
            (1, token.MySQLKeywordToken, 'COLUMN', 2),
            ((1, 2, 58, 59, 81), component.identifier.MySQLColumnNameComponent, None, 3),
            (3, component.definition.MySQLColumnDefinitionComponent, None, 4),
            (4, token.MySQLKeywordToken, 'FIRST', self.get_final_status()),
            (4, token.MySQLKeywordToken, 'AFTER', 5),
            (5, component.identifier.MySQLColumnNameComponent, None, self.get_final_status()),
            ((1, 2), token.MySQLOperatorToken, '(', 6),
            ((6, 9), component.identifier.MySQLColumnNameComponent, None, 7),
            (7, component.definition.MySQLColumnDefinitionComponent, None, 8),
            (8, token.MySQLDelimiterToken, ',', 9),
            (8, token.MySQLOperatorToken, ')', self.get_final_status()),
            ((1, 20), token.MySQLKeywordToken, 'INDEX', 10),
            ((1, 20), token.MySQLKeywordToken, 'KEY', 10),
            ((10, 20), component.identifier.MySQLIdentifierComponent, None, 11),
            ((10, 11), component.option.MySQLIndexTypeComponent, None, 12),
            ((10, 11, 12, 21, 22), token.MySQLOperatorToken, '(', 13),
            ((13, 15), component.identifier.MySQLIndexColumnNameComponent, None, 14),
            (14, token.MySQLOperatorToken, ')', 16),
            (14, token.MySQLDelimiterToken, ',', 15),
            (16, component.option.MySQLIndexOptionComponent, None, 16),
            (1, token.MySQLKeywordToken, 'CONSTRAINT', 17),
            (17, component.identifier.MySQLIdentifierComponent, None, 18),
            ((1, 17, 18), token.MySQLKeywordToken, 'PRIMARY', 19),
            (19, token.MySQLKeywordToken, 'KEY', 11),
            ((1, 17, 18), token.MySQLKeywordToken, 'UNIQUE', 20),
            (1, token.MySQLKeywordToken, 'FULLTEXT', 21),
            (1, token.MySQLKeywordToken, 'SPATIAL', 21),
            (21, token.MySQLKeywordToken, 'INDEX', 22),
            (21, token.MySQLKeywordToken, 'KEY', 22),
            ((21, 22), component.identifier.MySQLIdentifierComponent, None, 12),
            ((1, 17, 18), token.MySQLKeywordToken, 'FOREIGN', 23),
            (23, token.MySQLKeywordToken, 'KEY', 24),
            (24, component.identifier.MySQLIdentifierComponent, None, 25),
            ((24, 25), token.MySQLOperatorToken, '(', 26),
            ((26, 28), component.identifier.MySQLIndexColumnNameComponent, None, 27),
            (27, token.MySQLOperatorToken, ')', 29),
            (27, token.MySQLDelimiterToken, ',', 28),
            (29, component.definition.MySQLReferenceDefinitionComponent, None, self.get_final_status()),
            (0, token.MySQLKeywordToken, 'ALTER', 30),
            (30, token.MySQLKeywordToken, 'COLUMN', 31),
            ((30, 31), component.identifier.MySQLColumnNameComponent, None, 32),
            (32, token.MySQLKeywordToken, 'SET', 33),
            (33, token.MySQLKeywordToken, 'DEFAULT', 34),
            (34, token.MySQLStringToken, None, self.get_final_status()),
            (32, token.MySQLKeywordToken, 'DROP', 35),
            (35, token.MySQLKeywordToken, 'DEFAULT', self.get_final_status()),
            (0, token.MySQLKeywordToken, 'CHANGE', 36),
            (36, token.MySQLKeywordToken, 'COLUMN', 37),
            ((36, 37), component.identifier.MySQLColumnNameComponent, None, 81),
            (0, token.MySQLKeywordToken, 'DEFAULT', 38),
            ((0, 38), token.MySQLKeywordToken, 'CHARACTER', 39),
            (39, token.MySQLKeywordToken, 'SET', 40),
            ((0, 38), token.MySQLKeywordToken, 'CHARSET', 40),
            (40, token.MySQLOperatorToken, '=', 41),
            ((40, 41), component.identifier.MySQLCharsetNameComponent, None, 42),
            (42, token.MySQLKeywordToken, 'COLLATE', 43),
            (43, token.MySQLOperatorToken, '=', 44),
            ((43, 44), component.identifier.MySQLCollationNameComponent, None, self.get_final_status()),
            (0, token.MySQLKeywordToken, 'CONVERT', 45),
            (45, token.MySQLKeywordToken, 'TO', 46),
            (46, token.MySQLKeywordToken, 'CHARACTER', 47),
            (47, token.MySQLKeywordToken, 'SET', 48),
            (46, token.MySQLKeywordToken, 'CHARSET', 48),
            (48, component.identifier.MySQLCharsetNameComponent, None, 49),
            (49, token.MySQLKeywordToken, 'COLLATE', 50),
            (50, component.identifier.MySQLCollationNameComponent, None, self.get_final_status()),
            (0, token.MySQLKeywordToken, 'DISABLE', 51),
            (0, token.MySQLKeywordToken, 'ENABLE', 51),
            (51, token.MySQLKeywordToken, 'KEYS', self.get_final_status()),
            (0, token.MySQLKeywordToken, 'DISCARD', 52),
            (0, token.MySQLKeywordToken, 'IMPORT', 52),
            (52, token.MySQLKeywordToken, 'TABLESPACE', self.get_final_status()),
            (0, token.MySQLKeywordToken, 'DROP', 53),
            (53, token.MySQLKeywordToken, 'COLUMN', 54),
            ((53, 54), component.identifier.MySQLColumnNameComponent, None, self.get_final_status()),
            (53, token.MySQLKeywordToken, 'INDEX', 55),
            (53, token.MySQLKeywordToken, 'KEY', 55),
            (55, component.identifier.MySQLIdentifierComponent, None, self.get_final_status()),
            (53, token.MySQLKeywordToken, 'PRIMARY', 56),
            (56, token.MySQLKeywordToken, 'KEY', self.get_final_status()),
            (53, token.MySQLKeywordToken, 'FOREIGN', 57),
            (57, token.MySQLKeywordToken, 'KEY', 55),
            (0, token.MySQLKeywordToken, 'FORCE', self.get_final_status()),
            (0, token.MySQLKeywordToken, 'MODIFY', 58),
            (58, token.MySQLKeywordToken, 'COLUMN', 59),
            (0, token.MySQLKeywordToken, 'ORDER', 60),
            (60, token.MySQLKeywordToken, 'BY', 61),
            (61, component.identifier.MySQLColumnNameComponent, None, 62),
            (62, token.MySQLDelimiterToken, ',', 61),
            (0, token.MySQLKeywordToken, 'RENAME', 63),
            (63, token.MySQLKeywordToken, 'TO', 64),
            (63, token.MySQLKeywordToken, 'AS', 64),
            ((63, 64), component.identifier.MySQLTableNameComponent, None, self.get_final_status()),
            (1, token.MySQLKeywordToken, 'PARTITION', 65),
            (65, token.MySQLOperatorToken, '(', 66),
            (66, component.definition.MySQLPartitionDefinitionComponent, None, 67),
            (67, token.MySQLOperatorToken, ')', 68),
            (53, token.MySQLKeywordToken, 'PARTITION', 69),
            ((69, 72), component.identifier.MySQLIdentifierComponent, None, 70),
            (70, token.MySQLDelimiterToken, ',', 69),
            (0, token.MySQLKeywordToken, 'TRUNCATE', 71),
            (0, token.MySQLKeywordToken, 'ANALYZE', 71),
            (0, token.MySQLKeywordToken, 'CHECK', 71),
            (0, token.MySQLKeywordToken, 'OPTIMIZE', 71),
            (0, token.MySQLKeywordToken, 'REBUILD', 71),
            (0, token.MySQLKeywordToken, 'REPAIR', 71),
            (71, token.MySQLKeywordToken, 'PARTITION', 72),
            (72, token.MySQLKeywordToken, 'ALL', self.get_final_status()),
            (0, token.MySQLKeywordToken, 'COALESCE', 73),
            (73, token.MySQLKeywordToken, 'PARTITION', 74),
            (74, token.MySQLNumericToken, None, self.get_final_status()),
            (0, token.MySQLKeywordToken, 'REORGANIZE', 75),
            (75, token.MySQLKeywordToken, 'PARTITION', 76),
            (76, component.identifier.MySQLIdentifierComponent, None, 77),
            (77, token.MySQLDelimiterToken, ',', 76),
            (77, token.MySQLKeywordToken, 'INTO', 65),
            (0, token.MySQLKeywordToken, 'REMOVE', 78),
            (78, token.MySQLKeywordToken, 'PARTITIONING', self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLAlterTableSpecificationComponent()
        end_pos = c.parse_by_fsm(token_list, [4, 16, 42, 49, 62, 68, 70, 76], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            token_list.reset(end_pos)
            return c, token_list
