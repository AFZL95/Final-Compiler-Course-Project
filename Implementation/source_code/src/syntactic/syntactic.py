import ply.yacc as yacc

from ..lexical import MyLex
from ..lexical.tokrules import *



def syntactic(string):
    # declaring the 'Rule-Function' methods to give soul to the bodies !
    # 'p' is a string (in better words, expressions)
    # which consists of a few valid tokens
    # every token is accessible via it's occurence order index
    # For Example : p[1] is the second token of the expression

    # Class Area 

    # class list is the list of global variables (TYPEID)
    # which comes in the first sentences of the COOL class
    def p_class_list_many(p):
        '''class_list : class_list class SEMI'''
        p[0] = p[1] + [p[2]]

    def p_class_list_single(p):
        '''class_list : class SEMI'''
        p[0] = [p[1]]
    # "feature_list" means class parameters
    def p_class(p):
        '''class : CLASS TYPEID LBRACE feature_list RBRACE'''
        p[0] = Class(p[2], "Object", p[4])

    def p_class_inherits(p):
        '''class : CLASS TYPEID INHERITS TYPEID LBRACE feature_list RBRACE'''
        p[0] = Class(p[2], p[4], p[6])

    # Feature List Area

    # "feature_list" means class parameters
    def p_feature_list_many(p):
        '''feature_list : feature_list feature SEMI'''
        p[0] = p[1] + [p[2]]

    def p_feature_list_single(p):
        '''feature_list : feature SEMI'''
        p[0] = [p[1]]

    def p_feature_list_empty(p):
        '''feature_list : '''
        p[0] = []

    def p_feature_method(p):
        '''feature : OBJECTID LPAREN formal_list RPAREN COLON TYPEID LBRACE expression RBRACE'''
        p[0] = Method(p[1], p[3], p[6], p[8])

    def p_feature_method_no_formals(p):
        '''feature : OBJECTID LPAREN RPAREN COLON TYPEID LBRACE expression RBRACE'''
        p[0] = Method(p[1], [], p[5], p[7])

    def p_feature_attr_initialized(p):
        '''feature : OBJECTID COLON TYPEID ASSIGN expression'''
        p[0] = Attr(p[1], p[3], p[5])
    
    # simple attribute assigning
    def p_feature_attr(p):
        '''feature : OBJECTID COLON TYPEID'''
        p[0] = Attr(p[1], p[3], None)

    
    # a list consist of a few sub-lists
    def p_formal_list_many(p):
        '''formal_list : formal_list COMMA formal'''
        p[0] = p[1] + [p[3]]
    # a list which has one cell
    def p_formal_list_single(p):
        '''formal_list : formal'''
        p[0] = [p[1]]
    # declaring type of some variable
    def p_formal(p):
        '''formal : OBJECTID COLON TYPEID'''
        p[0] = (p[1], p[3])
    
    # Variable Area

    def p_expression_object(p):
        '''expression : OBJECTID'''
        p[0] = Object(p[1])

    def p_expression_int(p):
        '''expression : INT_CONST'''
        p[0] = Int(p[1])

    def p_expression_bool(p):
        '''expression : BOOL_CONST'''
        p[0] = Bool(p[1])

    def p_expression_str(p):
        '''expression : STR_CONST'''
        p[0] = Str(p[1])

    # paranthesis area
    def p_expression_block(p):
        '''expression : LBRACE block_list RBRACE'''
        p[0] = Block(p[2])
  
    # Block Area (explained in manual)

    def p_block_list_many(p):
        '''block_list : block_list expression SEMI'''
        p[0] = p[1] + [p[2]]

    def p_block_list_single(p):
        '''block_list : expression SEMI'''
        p[0] = [p[1]]

    # Expression Area

    def p_expression_assignment(p):
        '''expression : OBJECTID ASSIGN expression'''
        p[0] = Assign(Object(p[1]), p[3])

    # e.g : method call
    def p_expression_dispatch(p):
        '''expression : expression DOT OBJECTID LPAREN expr_list RPAREN'''
        p[0] = Dispatch(p[1], p[3], p[5])

    def p_expr_list_many(p):
        '''expr_list : expr_list COMMA expression'''
        p[0] = p[1] + [p[3]]

    def p_expr_list_single(p):
        '''expr_list : expression'''
        p[0] = [p[1]]

    def p_expr_list_empty(p):
        '''expr_list : '''
        p[0] = []

    def p_expression_static_dispatch(p):
        '''expression : expression AT TYPEID DOT OBJECTID LPAREN expr_list RPAREN'''
        p[0] = StaticDispatch(p[1], p[3], p[5], p[7])

    def p_expression_self_dispatch(p):
        '''expression : OBJECTID LPAREN expr_list RPAREN'''
        p[0] = Dispatch("self", p[1], p[3])

    def p_expression_basic_math(p):
        '''
        expression : expression PLUS expression
                   | expression MINUS expression
                   | expression MULT expression
                   | expression DIV expression
        '''
        if p[2] == '+':
            p[0] = Plus(p[1], p[3])
        elif p[2] == '-':
            p[0] = Sub(p[1], p[3])
        elif p[2] == '*':
            p[0] = Mult(p[1], p[3])
        elif p[2] == '/':
            p[0] = Div(p[1], p[3])

    def p_expression_numerical_comparison(p):
        '''
        expression : expression LT expression
                   | expression LE expression
                   | expression EQ expression
        '''
        if p[2] == '<':
            p[0] = Lt(p[1], p[3])
        elif p[2] == '<=':
            p[0] = Le(p[1], p[3])
        elif p[2] == '=':
            p[0] = Eq(p[1], p[3])

    def p_expression_with_parenthesis(p):
        '''expression : LPAREN expression RPAREN'''
        p[0] = p[2]

    # Conditional Statements Area

    def p_expression_if(p):
        '''expression : IF expression THEN expression ELSE expression FI'''
        p[0] = If(p[2], p[4], p[6])

    def p_expression_while(p):
        '''expression : WHILE expression LOOP expression POOL'''
        p[0] = While(p[2], p[4])

    def p_expression_let(p):
        """expression : LET OBJECTID COLON TYPEID IN expression
           expression : LET OBJECTID COLON TYPEID COMMA inner_lets"""
        p[0] = Let(p[2], p[4], None, p[6])

    def p_expression_let_initialized(p):
        """expression : LET OBJECTID COLON TYPEID ASSIGN expression IN expression
           expression : LET OBJECTID COLON TYPEID ASSIGN expression COMMA inner_lets"""
        p[0] = Let(p[2], p[4], p[6], p[8])

    def p_expression_let_with_error_in_first_decl(p):
        """expression : LET error COMMA OBJECTID COLON TYPEID IN expression
           expression : LET error COMMA OBJECTID COLON TYPEID COMMA inner_lets"""
        p[0] = Let(p[4], p[6], None, p[8])

    def p_expression_let_initialized_with_error_in_first_decl(p):
        """expression : LET error COMMA OBJECTID COLON TYPEID ASSIGN expression IN expression
           expression : LET error COMMA OBJECTID COLON TYPEID ASSIGN expression COMMA inner_lets"""
        p[0] = Let(p[4], p[6], p[8], p[10])

    def p_inner_lets_simple(p):
        """inner_lets : OBJECTID COLON TYPEID IN expression
           inner_lets : OBJECTID COLON TYPEID COMMA inner_lets """
        p[0] = Let(p[1], p[3], None, p[5])

    def p_inner_lets_initialized(p):
        """inner_lets : OBJECTID COLON TYPEID ASSIGN expression IN expression
           inner_lets : OBJECTID COLON TYPEID ASSIGN expression COMMA inner_lets"""
        p[0] = Let(p[1], p[3], p[5], p[7])

    def p_expression_case(p):
        '''expression : CASE expression OF case_list ESAC'''
        p[0] = Case(p[2], p[4])

    def p_case_list_one(p):
        '''case_list : case'''
        p[0] = [p[1]]

    def p_case_list_many(p):
        '''case_list : case_list case'''
        p[0] = p[1] + [p[2]]

    # see the "case.cl" example
    def p_case_expr(p):
        '''case : OBJECTID COLON TYPEID DARROW expression SEMI'''
        p[0] = (p[1], p[3], p[5])

    def p_expression_new(p):
        '''expression : NEW TYPEID'''
        p[0] = New(p[2])

    def p_expression_isvoid(p):
        '''expression : ISVOID expression'''
        p[0] = Isvoid(p[2])

    def p_expression_neg(p):
        '''expression : NEG expression'''
        p[0] = Neg(p[2])

    def p_expression_not(p):
        '''expression : NOT expression'''
        p[0] = Not(p[2])


    # creating a list for collecting the collecting the syntax errors
    serror = []

    # error rule for syntax errors
    def p_error(p):
        # getting the details of the error
        er = (p.type, p.value[0], p.lineno, p.lexpos)
        # appending the subsequent error to our error list
        serror.append(er)
        # and apperantly print out the error
        print('parser error: {}'.format(p))

    # build the parser
    parser = yacc.yacc()
    # instantiating the lexer module
    l = MyLex()
    # calling the lexer function from the instatiated object
    lexer = l.lexer
    # fire-up the engine !
    result = parser.parse(string, lexer=lexer)
    # returninig the produced parsing result
    return result, serror


if __name__ == '__main__':
    import sys
    # if we have an input .cl file...
    # take it as a argument
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as file:
            data = file.read()
        # calling the syntactical process function
        # and returning the results and the errors.
        result, errors = syntactic(data)
        if result:
            print('\nOK!\n')
    else:
        print('A cool file is required.')
