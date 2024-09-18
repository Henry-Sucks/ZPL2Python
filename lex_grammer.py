from basictoken import BasicToken as Token

lex_grammer = ""

lex_grammer_header = """
    %import common.ESCAPED_STRING   -> STRING
    %import common.SIGNED_NUMBER    -> NUMBER
    %import common.WS
    %ignore WS
"""
lex_grammer += lex_grammer_header

lex_keywords = ""
for key, value in Token.keywords_dict.items():
    lex_keywords += Token.token_names[value] + ": " + "\"" + key + "\"i\n"
lex_grammer += lex_keywords

lex_symbols = ""
for key, value in Token.symbols_dict.items():
    lex_symbols += Token.token_names[value] + ": " + "\"" + key + "\"\n"
lex_grammer += lex_symbols

print(lex_grammer)







