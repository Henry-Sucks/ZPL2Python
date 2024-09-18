class BasicToken:
    EOF             = 0   # End of file
    LET             = 1   # LET keyword
    LIST            = 2   # LIST command
    PRINT           = 3   # PRINT command
    RUN             = 4   # RUN command
    FOR             = 5   # FOR keyword
    NEXT            = 6   # NEXT keyword
    IF              = 7   # IF keyword
    THEN            = 8   # THEN keyword
    ELSE            = 9   # ELSE keyword
    ASSIGNOP        = 10  # '='
    LEFTPAREN       = 11  # '('
    RIGHTPAREN      = 12  # ')'
    PLUS            = 13  # '+'
    MINUS           = 14  # '-'
    TIMES           = 15  # '*'
    DIVIDE          = 16  # '/'
    NEWLINE         = 17  # End of line
    UNSIGNEDINT     = 18  # Integer
    NAME            = 19  # Identifier that is not a keyword
    EXIT            = 20  # Used to quit the interpreter
    DIM             = 21  # DIM keyword
    GREATER         = 22  # '>'
    LESSER          = 23  # '<'
    STEP            = 24  # STEP keyword
    GOTO            = 25  # GOTO keyword
    GOSUB           = 26  # GOSUB keyword
    INPUT           = 27  # INPUT keyword
    REM             = 28  # REM keyword
    RETURN          = 29  # RETURN keyword
    SAVE            = 30  # SAVE command
    LOAD            = 31  # LOAD command
    NOTEQUAL        = 32  # '<>'
    LESSEQUAL       = 33  # '<='
    GREATEQUAL      = 34  # '>='
    UNSIGNEDFLOAT   = 35  # Floating point number
    STRING          = 36  # String values
    TO              = 37  # TO keyword
    NEW             = 38  # NEW command
    EQUAL           = 39  # '='
    COMMA           = 40  # ','
    STOP            = 41  # STOP keyword
    COLON           = 42  # ':'
    ON              = 43  # ON keyword
    POW             = 44  # Power function
    SQR             = 45  # Square root function
    ABS             = 46  # Absolute value function
    DIM             = 47  # DIM keyword
    RANDOMIZE       = 48  # RANDOMIZE keyword
    RND             = 49  # RND keyword
    ATN             = 50  # Arctangent function
    COS             = 51  # Cosine function
    EXP             = 52  # Exponential function
    LOG             = 53  # Natural logarithm function
    SIN             = 54  # Sine function
    TAN             = 55  # Tangent function
    DATA            = 56  # DATA keyword
    READ            = 57  # READ keyword
    INT             = 58  # INT function
    CHR             = 59  # CHR$ function
    ASC             = 60  # ASC function
    STR             = 61  # STR$ function
    MID             = 62  # MID$ function
    MODULO          = 63  # MODULO operator
    TERNARY         = 64  # TERNARY functions
    VAL             = 65  # VAL function
    LEN             = 66  # LEN function
    UPPER           = 67  # UPPER function
    LOWER           = 68  # LOWER function
    ROUND           = 69  # ROUND function
    MAX             = 70  # MAX function
    MIN             = 71  # MIN function
    INSTR           = 72  # INSTR function
    AND             = 73  # AND operator
    OR              = 74  # OR operator
    NOT             = 75  # NOT operator
    PI              = 76  # PI constant
    RNDINT          = 77  # RNDINT function
    OPEN            = 78  # OPEN keyword
    HASH            = 79  # "#"
    CLOSE           = 80  # CLOSE keyword
    FSEEK           = 81  # FSEEK keyword
    APPEND          = 82  # APPEND keyword
    OUTPUT          = 83  # OUTPUT keyword
    RESTORE         = 84  # RESTORE keyword
    TAB             = 85  # TAB function
    SEMICOLON       = 86  # SEMICOLON
    LEFT            = 87  # LEFT$ function
    RIGHT           = 88  # RIGHT$ function

    token_names = ['EOF', 'LET', 'LIST', 'PRINT', 'RUN',
        'FOR', 'NEXT', 'IF', 'THEN', 'ELSE', 'ASSIGNOP',
        'LEFTPAREN', 'RIGHTPAREN', 'PLUS', 'MINUS', 'TIMES',
        'DIVIDE', 'NEWLINE', 'UNSIGNEDINT', 'NAME', 'EXIT',
        'DIM', 'GREATER', 'LESSER', 'STEP', 'GOTO', 'GOSUB',
        'INPUT', 'REM', 'RETURN', 'SAVE', 'LOAD',
        'NOTEQUAL', 'LESSEQUAL', 'GREATEQUAL',
        'UNSIGNEDFLOAT', 'STRING', 'TO', 'NEW', 'EQUAL',
        'COMMA', 'STOP', 'COLON', 'ON', 'POW', 'SQR', 'ABS',
        'DIM', 'RANDOMIZE', 'RND', 'ATN', 'COS', 'EXP',
        'LOG', 'SIN', 'TAN', 'DATA', 'READ', 'INT',
        'CHR', 'ASC', 'STR', 'MID', 'MODULO', 'TERNARY',
        'VAL', 'LEN', 'UPPER', 'LOWER', 'ROUND',
        'MAX', 'MIN', 'INSTR', 'AND', 'OR', 'NOT', 'PI',
        'RNDINT', 'OPEN', 'HASH', 'CLOSE', 'FSEEK', 'APPEND',
        'OUTPUT', 'RESTORE', 'TAB', 'SEMICOLON',
        'LEFT', 'RIGHT']

    symbols_dict = {'=': ASSIGNOP, 
                    '(': LEFTPAREN, 
                    ')': RIGHTPAREN,
                    '+': PLUS, 
                    '-': MINUS, 
                    '*': TIMES, 
                    '/': DIVIDE,
                    # '\n': NEWLINE, 
                    '<': LESSER,
                    '>': GREATER, 
                    '<>': NOTEQUAL,
                    '<=': LESSEQUAL, 
                    '>=': GREATEQUAL, 
                    ',': COMMA,
                    ':': COLON, 
                    '%': MODULO, 
                    '!=': NOTEQUAL, 
                    '#': HASH,
                    ';': SEMICOLON}


    keywords_dict = {'LET': LET, 
                    'LIST': LIST, 
                    'PRINT': PRINT,
                    'FOR': FOR, 
                    'RUN': RUN, 
                    'NEXT': NEXT,
                    'IF': IF, 
                    'THEN': THEN, 
                    'ELSE': ELSE,
                    'EXIT': EXIT, 
                    'DIM': DIM, 
                    'STEP': STEP,
                    'GOTO': GOTO, 
                    'GOSUB': GOSUB,
                    'INPUT': INPUT, 
                    'REM': REM, 
                    'RETURN': RETURN,
                    'SAVE': SAVE, 
                    'LOAD': LOAD, 
                    'NEW': NEW,
                    'STOP': STOP, 
                    'TO': TO, 
                    'ON':ON, 
                    'POW': POW,
                    'SQR': SQR, 
                    'ABS': ABS,
                    'RANDOMIZE': RANDOMIZE, 
                    'RND': RND,
                    'ATN': ATN, 
                    'COS': COS, 
                    'EXP': EXP,
                    'LOG': LOG, 
                    'SIN': SIN, 
                    'TAN': TAN,
                    'DATA': DATA, 
                    'READ': READ, 
                    'INT': INT,
                    'CHR$': CHR, 
                    'ASC': ASC, 
                    'STR$': STR,
                    'MID$': MID, 
                    'MOD': MODULO,
                    'IF$': TERNARY, 
                    'IFF': TERNARY,
                    'VAL': VAL, 
                    'LEN': LEN,
                    'UPPER$': UPPER, 
                    'LOWER$': LOWER,
                    'ROUND': ROUND, 
                    'MAX': MAX, 
                    'MIN': MIN,
                    'INSTR': INSTR, 
                    'END': STOP,
                    'AND': AND, 
                    'OR': OR, 
                    'NOT': NOT,
                    'PI': PI, 
                    'RNDINT': RNDINT, 
                    'OPEN': OPEN,
                    'CLOSE': CLOSE, 
                    'FSEEK': FSEEK,
                    'APPEND': APPEND, 
                    'OUTPUT':OUTPUT,
                    'RESTORE': RESTORE, 
                    'TAB': TAB,
                    'LEFT$': LEFT, 
                    'RIGHT$': RIGHT}