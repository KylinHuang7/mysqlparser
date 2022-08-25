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

# 13.7.4.1 SET Syntax for Variable Assignment
# SET variable_assignment [, variable_assignment] ...
#
# variable_assignment:
#      user_var_name = expr
#    | param_name = expr
#    | local_var_name = expr
#    | [GLOBAL | SESSION]
#        system_var_name = expr
#    | [@@global. | @@session. | @@]
#        system_var_name = expr
#
# SET ONE_SHOT system_var_name = expr
#
# 13.7.4.2 SET CHARACTER SET Syntax
# SET {CHARACTER SET | CHARSET}
#    {'charset_name' | DEFAULT}
#
# 13.7.4.3 SET NAMES Syntax
# SET NAMES {'charset_name'
#    [COLLATE 'collation_name'] | DEFAULT}
#
class SetStatement(statement.MySQLStatement):
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'SET', 1),
            ((1, 6), token.MySQLKeywordToken, 'GLOBAL', 2),
            ((1, 6), token.MySQLKeywordToken, 'SESSION', 2),
            ((1, 6), token.MySQLVariableToken, None, 3),
            ((1, 2, 6), token.MySQLUnquotedIdentifierToken, None, 3),
            ((1, 2, 6), token.MySQLKeywordToken, None, 3),
            (3, token.MySQLOperatorToken, '=', 4),
            (4, component.expression.MySQLExpressionComponent, None, 5),
            (5, token.MySQLDelimiterToken, ',', 6),
            (1, token.MySQLKeywordToken, 'ONE_SHOT', 7),
            (7, token.MySQLUnquotedIdentifierToken, None, 8),
            (7, token.MySQLKeywordToken, None, 8),
            (8, token.MySQLOperatorToken, '=', 9),
            (9, component.expression.MySQLExpressionComponent, None, self.get_final_status()),
            (1, token.MySQLKeywordToken, 'CHARACTER', 10),
            (10, token.MySQLKeywordToken, 'SET', 11),
            (1, token.MySQLKeywordToken, 'CHARSET', 11),
            (11, token.MySQLKeywordToken, 'DEFAULT', self.get_final_status()),
            (11, component.identifier.MySQLCharsetNameComponent, None, self.get_final_status()),
            (1, token.MySQLKeywordToken, 'NAMES', 12),
            (12, token.MySQLKeywordToken, 'DEFAULT', self.get_final_status()),
            (12, component.identifier.MySQLCharsetNameComponent, None, 13),
            (13, token.MySQLKeywordToken, 'COLLATE', 14),
            (14, component.identifier.MySQLCollationNameComponent, None, self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        s = SetStatement()
        end_pos = s.parse_by_fsm(token_list, [5, 13], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            token_list.reset(end_pos)
            return s, token_list

