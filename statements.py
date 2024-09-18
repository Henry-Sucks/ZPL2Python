class Statement:
    def __init__(self, name, definition):
        self.name = name
        self.definition = definition

class Statements:
    stmt_header = """
        stmt:
    """
    # PRINT语句
    print_stmt = Statement("print_stmt","""
    print_stmt: "PRINT" print_list
    print_list: expression "," print_list
                | expression
                |
    """)

    # LABEL语句
    label_stmt = Statement("label_stmt","""
    label_stmt: "LABEL" label_id
    label_id: label_num 
            | label_text
    label_num: NATURAL_NUMBER       // 大于 0 的整数
    label_text: IDENTIFIER // 不得包含空格或者用作分隔符的其它特殊字符
    """)

    # 赋值语句
    assign_stmt = Statement("assign_stmt", """
    assign_stmt: id "=" expression
    """)

    # IF语句
    if_stmt = Statement("if_stmt", """
    if_stmt: "IF" expression "THEN" stmt
        | "IF" expression stmt "ELSE" stmt "ENDIF"
    """)

    # GOTO语句
    goto_stmt = Statement("goto_stmt", """
    goto_stmt: "GOTO" expression
    """)