from analisador_lexico import Lexico, Token, ErroLexico

# Dicionário de não-terminais, mapeando índices para nomes.
NAO_TERMINAL = {
    0:"S'",1:"PROGRAM",2:"STMT_LIST",3:"STMT",4:"VAR_DECL",5:"FUN_DECL",6:"ASSIGN",
    7:"WRITE_STMT",8:"READ_STMT",9:"IF_STMT",10:"ELSE_OPT",11:"WHILE_STMT",12:"FOR_STMT",
    13:"ASSIGN_NS",14:"EXPR_OPT",15:"EXPR_STMT",16:"FUN_CALL_SEMI",17:"ARG_LIST_OPT",
    18:"ARG_LIST",19:"PARAMS_OPT",20:"PARAMS",21:"EXPR",22:"REL",23:"REL_TAIL",
    24:"ADD",25:"MUL",26:"UNARY",27:"PRIMARY",28:"FUN_CALL"
}

# Produções da gramática, mapeando índice para (não-terminal, [símbolos]).
PRODUCOES = {
    0:("S'",["PROGRAM"]),1:("PROGRAM",["STMT_LIST"]),2:("STMT_LIST",["STMT_LIST","STMT"]),
    3:("STMT_LIST",["STMT"]),4:("STMT",["VAR_DECL"]),5:("STMT",["FUN_DECL"]),
    6:("STMT",["ASSIGN"]),7:("STMT",["WRITE_STMT"]),8:("STMT",["READ_STMT"]),
    9:("STMT",["IF_STMT"]),10:("STMT",["WHILE_STMT"]),11:("STMT",["FOR_STMT"]),
    12:("STMT",["EXPR_STMT"]),13:("STMT",["FUN_CALL_SEMI"]),14:("VAR_DECL",["var","id","pv"]),
    15:("FUN_DECL",["fun","id","ap","PARAMS_OPT","fp","ab","STMT_LIST","fb"]),
    16:("ASSIGN",["id","igual","EXPR","pv"]),17:("WRITE_STMT",["write","ap","EXPR","fp","pv"]),
    18:("READ_STMT",["read","ap","id","fp","pv"]),19:("IF_STMT",["if","ap","EXPR","fp","ab","STMT_LIST","fb","ELSE_OPT"]),
    20:("ELSE_OPT",["else","ab","STMT_LIST","fb"]),21:("ELSE_OPT",[]),
    22:("WHILE_STMT",["while","ap","EXPR","fp","ab","STMT_LIST","fb"]),
    23:("FOR_STMT",["for","ap","ASSIGN_NS","pv","EXPR_OPT","pv","ASSIGN_NS","fp","ab","STMT_LIST","fb"]),
    24:("ASSIGN_NS",["id","igual","EXPR"]),25:("EXPR_OPT",["EXPR"]),26:("EXPR_OPT",[]),
    27:("EXPR_STMT",["EXPR","pv"]),28:("FUN_CALL_SEMI",["id","ap","ARG_LIST_OPT","fp","pv"]),
    29:("ARG_LIST_OPT",["ARG_LIST"]),30:("ARG_LIST_OPT",[]),31:("ARG_LIST",["ARG_LIST","v","EXPR"]),
    32:("ARG_LIST",["EXPR"]),33:("PARAMS_OPT",["PARAMS"]),34:("PARAMS_OPT",[]),
    35:("PARAMS",["PARAMS","v","id"]),36:("PARAMS",["id"]),37:("EXPR",["REL"]),
    38:("REL",["ADD","REL_TAIL"]),39:("REL_TAIL",["maior","ADD"]),40:("REL_TAIL",["menor","ADD"]),
    41:("REL_TAIL",["ge","ADD"]),42:("REL_TAIL",["le","ADD"]),43:("REL_TAIL",["eqeq","ADD"]),
    44:("REL_TAIL",["ne","ADD"]),45:("REL_TAIL",[]),46:("ADD",["ADD","mais","MUL"]),
    47:("ADD",["ADD","menos","MUL"]),48:("ADD",["MUL"]),49:("MUL",["MUL","mult","UNARY"]),
    50:("MUL",["MUL","div","UNARY"]),51:("MUL",["UNARY"]),52:("UNARY",["neg","UNARY"]),
    53:("UNARY",["menos","UNARY"]),54:("UNARY",["PRIMARY"]),55:("PRIMARY",["num"]),
    56:("PRIMARY",["id"]),57:("PRIMARY",["ap","EXPR","fp"]),58:("PRIMARY",["FUN_CALL"]),
    59:("FUN_CALL",["id","ap","ARG_LIST_OPT","fp"])
}

class SLR:
    def __init__(self):
        # Tabela AFD com ACTION e GOTO compactados, usando nomes de não-terminais.
        self.afd = {
            0:{"ACTION":{"ap":"S 16","for":"S 30","fun":"S 15","id":"S 21","if":"S 22","menos":"S 2","neg":"S 25","num":"S 13","read":"S 12","var":"S 3","while":"S 9","write":"S 11"},"GOTO":{"ADD":23,"ASSIGN":8,"EXPR":1,"EXPR_STMT":5,"FOR_STMT":27,"FUN_CALL":7,"FUN_CALL_SEMI":6,"FUN_DECL":31,"IF_STMT":19,"MUL":29,"PRIMARY":24,"PROGRAM":20,"READ_STMT":28,"REL":4,"STMT":18,"STMT_LIST":14,"UNARY":32,"VAR_DECL":26,"WHILE_STMT":17,"WRITE_STMT":10}},
            1:{"ACTION":{"pv":"S 33"},"GOTO":{}},
            2:{"ACTION":{"ap":"S 16","id":"S 34","menos":"S 2","neg":"S 25","num":"S 13"},"GOTO":{"FUN_CALL":7,"PRIMARY":24,"UNARY":35}},
            3:{"ACTION":{"id":"S 36"},"GOTO":{}},
            4:{"ACTION":{"fp":"R 37","pv":"R 37","v":"R 37"},"GOTO":{}},
            5:{"ACTION":{"$":"R 12","ap":"R 12","fb":"R 12","for":"R 12","fun":"R 12","id":"R 12","if":"R 12","menos":"R 12","neg":"R 12","num":"R 12","read":"R 12","var":"R 12","while":"R 12","write":"R 12"},"GOTO":{}},
            6:{"ACTION":{"$":"R 13","ap":"R 13","fb":"R 13","for":"R 13","fun":"R 13","id":"R 13","if":"R 13","menos":"R 13","neg":"R 13","num":"R 13","read":"R 13","var":"R 13","while":"R 13","write":"R 13"},"GOTO":{}},
            7:{"ACTION":{"div":"R 58","eqeq":"R 58","fp":"R 58","ge":"R 58","le":"R 58","maior":"R 58","mais":"R 58","menor":"R 58","menos":"R 58","mult":"R 58","ne":"R 58","pv":"R 58","v":"R 58"},"GOTO":{}},
            8:{"ACTION":{"$":"R 6","ap":"R 6","fb":"R 6","for":"R 6","fun":"R 6","id":"R 6","if":"R 6","menos":"R 6","neg":"R 6","num":"R 6","read":"R 6","var":"R 6","while":"R 6","write":"R 6"},"GOTO":{}},
            9:{"ACTION":{"ap":"S 37"},"GOTO":{}},
            10:{"ACTION":{"$":"R 7","ap":"R 7","fb":"R 7","for":"R 7","fun":"R 7","id":"R 7","if":"R 7","menos":"R 7","neg":"R 7","num":"R 7","read":"R 7","var":"R 7","while":"R 7","write":"R 7"},"GOTO":{}},
            11:{"ACTION":{"ap":"S 38"},"GOTO":{}},
            12:{"ACTION":{"ap":"S 39"},"GOTO":{}},
            13:{"ACTION":{"div":"R 55","eqeq":"R 55","fp":"R 55","ge":"R 55","le":"R 55","maior":"R 55","mais":"R 55","menor":"R 55","menos":"R 55","mult":"R 55","ne":"R 55","pv":"R 55","v":"R 55"},"GOTO":{}},
            14:{"ACTION":{"$":"R 1","ap":"S 16","for":"S 30","fun":"S 15","id":"S 21","if":"S 22","menos":"S 2","neg":"S 25","num":"S 13","read":"S 12","var":"S 3","while":"S 9","write":"S 11"},"GOTO":{"ADD":23,"ASSIGN":8,"EXPR":1,"EXPR_STMT":5,"FOR_STMT":27,"FUN_CALL":7,"FUN_CALL_SEMI":6,"FUN_DECL":31,"IF_STMT":19,"MUL":29,"PRIMARY":24,"READ_STMT":28,"REL":4,"STMT":40,"UNARY":32,"VAR_DECL":26,"WHILE_STMT":17,"WRITE_STMT":10}},
            15:{"ACTION":{"id":"S 41"},"GOTO":{}},
            16:{"ACTION":{"ap":"S 16","id":"S 34","menos":"S 2","neg":"S 25","num":"S 13"},"GOTO":{"ADD":23,"EXPR":42,"FUN_CALL":7,"MUL":29,"PRIMARY":24,"REL":4,"UNARY":32}},
            17:{"ACTION":{"$":"R 10","ap":"R 10","fb":"R 10","for":"R 10","fun":"R 10","id":"R 10","if":"R 10","menos":"R 10","neg":"R 10","num":"R 10","read":"R 10","var":"R 10","while":"R 10","write":"R 10"},"GOTO":{}},
            18:{"ACTION":{"$":"R 3","ap":"R 3","fb":"R 3","for":"R 3","fun":"R 3","id":"R 3","if":"R 3","menos":"R 3","neg":"R 3","num":"R 3","read":"R 3","var":"R 3","while":"R 3","write":"R 3"},"GOTO":{}},
            19:{"ACTION":{"$":"R 9","ap":"R 9","fb":"R 9","for":"R 9","fun":"R 9","id":"R 9","if":"R 9","menos":"R 9","neg":"R 9","num":"R 9","read":"R 9","var":"R 9","while":"R 9","write":"R 9"},"GOTO":{}},
            20:{"ACTION":{"$":"ACC"},"GOTO":{}},
            21:{"ACTION":{"ap":"S 43","div":"R 56","eqeq":"R 56","fp":"R 56","ge":"R 56","igual":"S 44","le":"R 56","maior":"R 56","mais":"R 56","menor":"R 56","menos":"R 56","mult":"R 56","ne":"R 56","pv":"R 56","v":"R 56"},"GOTO":{}},
            22:{"ACTION":{"ap":"S 45"},"GOTO":{}},
            23:{"ACTION":{"eqeq":"S 48","fp":"R 45","ge":"S 53","le":"S 54","maior":"S 49","mais":"S 50","menor":"S 46","menos":"S 47","ne":"S 51","pv":"R 45","v":"R 45"},"GOTO":{"REL_TAIL":52}},
            24:{"ACTION":{"div":"R 54","eqeq":"R 54","fp":"R 54","ge":"R 54","le":"R 54","maior":"R 54","mais":"R 54","menor":"R 54","menos":"R 54","mult":"R 54","ne":"R 54","pv":"R 54","v":"R 54"},"GOTO":{}},
            25:{"ACTION":{"ap":"S 16","id":"S 34","menos":"S 2","neg":"S 25","num":"S 13"},"GOTO":{"FUN_CALL":7,"PRIMARY":24,"UNARY":35}},
            26:{"ACTION":{"$":"R 4","ap":"R 4","fb":"R 4","for":"R 4","fun":"R 4","id":"R 4","if":"R 4","menos":"R 4","neg":"R 4","num":"R 4","read":"R 4","var":"R 4","while":"R 4","write":"R 4"},"GOTO":{}},
            27:{"ACTION":{"$":"R 11","ap":"R 11","fb":"R 11","for":"R 11","fun":"R 11","id":"R 11","if":"R 11","menos":"R 11","neg":"R 11","num":"R 11","read":"R 11","var":"R 11","while":"R 11","write":"R 11"},"GOTO":{}},
            28:{"ACTION":{"$":"R 8","ap":"R 8","fb":"R 8","for":"R 8","fun":"R 8","id":"R 8","if":"R 8","menos":"R 8","neg":"R 8","num":"R 8","read":"R 8","var":"R 8","while":"R 8","write":"R 8"},"GOTO":{}},
            29:{"ACTION":{"div":"S 56","eqeq":"R 48","fp":"R 48","ge":"R 48","le":"R 48","maior":"R 48","mais":"R 48","menor":"R 48","menos":"R 48","mult":"S 57","ne":"R 48","pv":"R 48","v":"R 48"},"GOTO":{}},
            30:{"ACTION":{"ap":"S 58"},"GOTO":{}},
            31:{"ACTION":{"$":"R 5","ap":"R 5","fb":"R 5","for":"R 5","fun":"R 5","id":"R 5","if":"R 5","menos":"R 5","neg":"R 5","num":"R 5","read":"R 5","var":"R 5","while":"R 5","write":"R 5"},"GOTO":{}},
            32:{"ACTION":{"div":"R 51","eqeq":"R 51","fp":"R 51","ge":"R 51","le":"R 51","maior":"R 51","mais":"R 51","menor":"R 51","menos":"R 51","mult":"R 51","ne":"R 51","pv":"R 51","v":"R 51"},"GOTO":{}},
            33:{"ACTION":{"$":"R 27","ap":"R 27","fb":"R 27","for":"R 27","fun":"R 27","id":"R 27","if":"R 27","menos":"R 27","neg":"R 27","num":"R 27","read":"R 27","var":"R 27","while":"R 27","write":"R 27"},"GOTO":{}},
            34:{"ACTION":{"div":"R 56","eqeq":"R 56","fp":"R 56","ge":"R 56","le":"R 56","maior":"R 56","mais":"R 56","menor":"R 56","menos":"R 56","mult":"R 56","ne":"R 56","pv":"R 56","v":"R 56"},"GOTO":{}},
            35:{"ACTION":{"div":"R 53","eqeq":"R 53","fp":"R 53","ge":"R 53","le":"R 53","maior":"R 53","mais":"R 53","menor":"R 53","menos":"R 53","mult":"R 53","ne":"R 53","pv":"R 53","v":"R 53"},"GOTO":{}},
            36:{"ACTION":{"pv":"S 60"},"GOTO":{}},
            37:{"ACTION":{"ap":"S 16","id":"S 34","menos":"S 2","neg":"S 25","num":"S 13"},"GOTO":{"ADD":23,"EXPR":61,"FUN_CALL":7,"MUL":29,"PRIMARY":24,"REL":4,"UNARY":32}},
            38:{"ACTION":{"ap":"S 16","id":"S 34","menos":"S 2","neg":"S 25","num":"S 13"},"GOTO":{"ADD":23,"EXPR":62,"FUN_CALL":7,"MUL":29,"PRIMARY":24,"REL":4,"UNARY":32}},
            39:{"ACTION":{"id":"S 63"},"GOTO":{}},
            40:{"ACTION":{"$":"R 2","ap":"R 2","fb":"R 2","for":"R 2","fun":"R 2","id":"R 2","if":"R 2","menos":"R 2","neg":"R 2","num":"R 2","read":"R 2","var":"R 2","while":"R 2","write":"R 2"},"GOTO":{}},
            41:{"ACTION":{"ap":"S 64"},"GOTO":{}},
            42:{"ACTION":{"fp":"S 65"},"GOTO":{}},
            43:{"ACTION":{"ap":"S 16","fp":"R 30","id":"S 34","menos":"S 2","neg":"S 25","num":"S 13"},"GOTO":{"ADD":23,"ARG_LIST":68,"ARG_LIST_OPT":67,"EXPR":66,"FUN_CALL":7,"MUL":29,"PRIMARY":24,"REL":4,"UNARY":32}},
            44:{"ACTION":{"ap":"S 16","id":"S 34","menos":"S 2","neg":"S 25","num":"S 13"},"GOTO":{"ADD":23,"EXPR":69,"FUN_CALL":7,"MUL":29,"PRIMARY":24,"REL":4,"UNARY":32}},
            45:{"ACTION":{"ap":"S 16","id":"S 34","menos":"S 2","neg":"S 25","num":"S 13"},"GOTO":{"ADD":23,"EXPR":70,"FUN_CALL":7,"MUL":29,"PRIMARY":24,"REL":4,"UNARY":32}},
            46:{"ACTION":{"ap":"S 16","id":"S 34","menos":"S 2","neg":"S 25","num":"S 13"},"GOTO":{"ADD":71,"FUN_CALL":7,"MUL":29,"PRIMARY":24,"UNARY":32}},
            47:{"ACTION":{"ap":"S 16","id":"S 34","menos":"S 2","neg":"S 25","num":"S 13"},"GOTO":{"FUN_CALL":7,"MUL":72,"PRIMARY":24,"UNARY":32}},
            48:{"ACTION":{"ap":"S 16","id":"S 34","menos":"S 2","neg":"S 25","num":"S 13"},"GOTO":{"ADD":73,"FUN_CALL":7,"MUL":29,"PRIMARY":24,"UNARY":32}},
            49:{"ACTION":{"ap":"S 16","id":"S 34","menos":"S 2","neg":"S 25","num":"S 13"},"GOTO":{"ADD":74,"FUN_CALL":7,"MUL":29,"PRIMARY":24,"UNARY":32}},
            50:{"ACTION":{"ap":"S 16","id":"S 34","menos":"S 2","neg":"S 25","num":"S 13"},"GOTO":{"FUN_CALL":7,"MUL":75,"PRIMARY":24,"UNARY":32}},
            51:{"ACTION":{"ap":"S 16","id":"S 34","menos":"S 2","neg":"S 25","num":"S 13"},"GOTO":{"ADD":76,"FUN_CALL":7,"MUL":29,"PRIMARY":24,"UNARY":32}},
            52:{"ACTION":{"fp":"R 38","pv":"R 38","v":"R 38"},"GOTO":{}},
            53:{"ACTION":{"ap":"S 16","id":"S 34","menos":"S 2","neg":"S 25","num":"S 13"},"GOTO":{"FUN_CALL":7,"MUL":77,"PRIMARY":24,"UNARY":32}},
            54:{"ACTION":{"ap":"S 16","id":"S 34","menos":"S 2","neg":"S 25","num":"S 13"},"GOTO":{"ADD":78,"FUN_CALL":7,"MUL":29,"PRIMARY":24,"UNARY":32}},
            55:{"ACTION":{"div":"R 52","eqeq":"R 52","fp":"R 52","ge":"R 52","le":"R 52","maior":"R 52","mais":"R 52","menor":"R 52","menos":"R 52","mult":"R 52","ne":"R 52","pv":"R 52","v":"R 52"},"GOTO":{}},
            56:{"ACTION":{"ap":"S 16","id":"S 34","menos":"S 2","neg":"S 25","num":"S 13"},"GOTO":{"FUN_CALL":7,"PRIMARY":24,"UNARY":79}},
            57:{"ACTION":{"ap":"S 16","id":"S 34","menos":"S 2","neg":"S 25","num":"S 13"},"GOTO":{"FUN_CALL":7,"PRIMARY":24,"UNARY":80}},
            58:{"ACTION":{"id":"S 81"},"GOTO":{"ASSIGN_NS":82}},
            59:{"ACTION":{"fp":"R 30","v":"R 30"},"GOTO":{}},
            60:{"ACTION":{"$":"R 14","ap":"R 14","fb":"R 14","for":"R 14","fun":"R 14","id":"R 14","if":"R 14","menos":"R 14","neg":"R 14","num":"R 14","read":"R 14","var":"R 14","while":"R 14","write":"R 14"},"GOTO":{}},
            61:{"ACTION":{"fp":"S 84"},"GOTO":{}},
            62:{"ACTION":{"fp":"S 85"},"GOTO":{}},
            63:{"ACTION":{"fp":"S 86"},"GOTO":{}},
            64:{"ACTION":{"fp":"R 34","id":"S 88"},"GOTO":{"PARAMS":89,"PARAMS_OPT":100}},
            65:{"ACTION":{"div":"R 57","eqeq":"R 57","fp":"R 57","ge":"R 57","le":"R 57","maior":"R 57","mais":"R 57","menor":"R 57","menos":"R 57","mult":"R 57","ne":"R 57","pv":"R 57","v":"R 57"},"GOTO":{}},
            66:{"ACTION":{"fp":"R 32","v":"R 32"},"GOTO":{}},
            67:{"ACTION":{"fp":"S 90"},"GOTO":{}},
            68:{"ACTION":{"fp":"R 29","v":"S 91"},"GOTO":{}},
            69:{"ACTION":{"pv":"S 92"},"GOTO":{}},
            70:{"ACTION":{"fp":"S 93"},"GOTO":{}},
            71:{"ACTION":{"fp":"R 40","mais":"S 50","menos":"S 47","pv":"R 40","v":"R 40"},"GOTO":{}},
            72:{"ACTION":{"div":"S 56","eqeq":"R 47","fp":"R 47","ge":"R 47","le":"R 47","maior":"R 47","mais":"R 47","menor":"R 47","menos":"R 47","mult":"S 57","ne":"R 47","pv":"R 47","v":"R 47"},"GOTO":{}},
            73:{"ACTION":{"fp":"R 43","mais":"S 50","menos":"S 47","pv":"R 43","v":"R 43"},"GOTO":{}},
            74:{"ACTION":{"fp":"R 39","mais":"S 50","menos":"S 47","pv":"R 39","v":"R 39"},"GOTO":{}},
            75:{"ACTION":{"div":"S 56","eqeq":"R 46","fp":"R 46","ge":"R 46","le":"R 46","maior":"R 46","mais":"R 46","menor":"R 46","menos":"R 46","mult":"S 57","ne":"R 46","pv":"R 46","v":"R 46"},"GOTO":{}},
            76:{"ACTION":{"fp":"R 44","mais":"S 50","menos":"S 47","pv":"R 44","v":"R 44"},"GOTO":{}},
            77:{"ACTION":{"fp":"R 41","mais":"S 50","menos":"S 47","pv":"R 41","v":"R 41"},"GOTO":{}},
            78:{"ACTION":{"fp":"R 42","mais":"S 50","menos":"S 47","pv":"R 42","v":"R 42"},"GOTO":{}},
            79:{"ACTION":{"div":"S 56","eqeq":"R 50","fp":"R 50","ge":"R 50","le":"R 50","maior":"R 50","mais":"R 50","menor":"R 50","menos":"R 50","mult":"S 57","ne":"R 50","pv":"R 50","v":"R 50"},"GOTO":{}},
            80:{"ACTION":{"div":"S 56","eqeq":"R 49","fp":"R 49","ge":"R 49","le":"R 49","maior":"R 49","mais":"R 49","menor":"R 49","menos":"R 49","mult":"S 57","ne":"R 49","pv":"R 49","v":"R 49"},"GOTO":{}},
            81:{"ACTION":{"igual":"S 94"},"GOTO":{}},
            82:{"ACTION":{"pv":"S 95"},"GOTO":{}},
            83:{"ACTION":{"fp":"S 96"},"GOTO":{}},
            84:{"ACTION":{"ab":"S 97"},"GOTO":{}},
            85:{"ACTION":{"pv":"S 98"},"GOTO":{}},
            86:{"ACTION":{"pv":"S 99"},"GOTO":{}},
            87:{"ACTION":{"id":"S 88"},"GOTO":{"PARAMS":89}},
            88:{"ACTION":{"fp":"R 36","v":"R 36"},"GOTO":{}}, 
            89:{"ACTION":{"fp":"R 33","v":"S 101"},"GOTO":{}},
            90:{"ACTION":{"div":"R 59","eqeq":"R 59","fp":"R 59","ge":"R 59","le":"R 59","maior":"R 59","mais":"R 59","menor":"R 59","menos":"R 59","mult":"R 59","ne":"R 59","pv":"S 102","v":"R 59"},"GOTO":{}},
            91:{"ACTION":{"ap":"S 16","id":"S 34","menos":"S 2","neg":"S 25","num":"S 13"},"GOTO":{"ADD":23,"EXPR":103,"FUN_CALL":7,"MUL":29,"PRIMARY":24,"REL":4,"UNARY":32}},
            92:{"ACTION":{"$":"R 16","ap":"R 16","fb":"R 16","for":"R 16","fun":"R 16","id":"R 16","if":"R 16","menos":"R 16","neg":"R 16","num":"R 16","read":"R 16","var":"R 16","while":"R 16","write":"R 16"},"GOTO":{}},
            93:{"ACTION":{"ab":"S 104"},"GOTO":{}},
            94:{"ACTION":{"ap":"S 16","id":"S 34","menos":"S 2","neg":"S 25","num":"S 13"},"GOTO":{"ADD":23,"EXPR":105,"FUN_CALL":7,"MUL":29,"PRIMARY":24,"REL":4,"UNARY":32}},
            95:{"ACTION":{"ap":"S 16","id":"S 34","menos":"S 2","neg":"S 25","num":"S 13","pv":"R 26"},"GOTO":{"ADD":23,"EXPR":106,"EXPR_OPT":107,"FUN_CALL":7,"MUL":29,"PRIMARY":24,"REL":4,"UNARY":32}},
            96:{"ACTION":{"div":"R 59","eqeq":"R 59","fp":"R 59","ge":"R 59","le":"R 59","maior":"R 59","mais":"R 59","menor":"R 59","menos":"R 59","mult":"R 59","ne":"R 59","pv":"R 59","v":"R 59"},"GOTO":{}},
            97:{"ACTION":{"ap":"S 16","for":"S 30","fun":"S 15","id":"S 21","if":"S 22","menos":"S 2","neg":"S 25","num":"S 13","read":"S 12","var":"S 3","while":"S 9","write":"S 11"},"GOTO":{"ADD":23,"ASSIGN":8,"EXPR":1,"EXPR_STMT":5,"FOR_STMT":27,"FUN_CALL":7,"FUN_CALL_SEMI":6,"FUN_DECL":31,"IF_STMT":19,"MUL":29,"PRIMARY":24,"READ_STMT":28,"REL":4,"STMT":18,"STMT_LIST":108,"UNARY":32,"VAR_DECL":26,"WHILE_STMT":17,"WRITE_STMT":10}},
            98:{"ACTION":{"$":"R 17","ap":"R 17","fb":"R 17","for":"R 17","fun":"R 17","id":"R 17","if":"R 17","menos":"R 17","neg":"R 17","num":"R 17","read":"R 17","var":"R 17","while":"R 17","write":"R 17"},"GOTO":{}},
            99:{"ACTION":{"$":"R 18","ap":"R 18","fb":"R 18","for":"R 18","fun":"R 18","id":"R 18","if":"R 18","menos":"R 18","neg":"R 18","num":"R 18","read":"R 18","var":"R 18","while":"R 18","write":"R 18"},"GOTO":{}},
            100:{"ACTION":{"fp":"S 128"},"GOTO":{}},            
            101:{"ACTION":{"id":"S 88"},"GOTO":{"PARAMS":110}},
            102:{"ACTION":{"$":"R 28","ap":"R 28","fb":"R 28","for":"R 28","fun":"R 28","id":"R 28","if":"R 28","menos":"R 28","neg":"R 28","num":"R 28","read":"R 28","var":"R 28","while":"R 28","write":"R 28"},"GOTO":{}},
            103:{"ACTION":{"fp":"R 31","v":"R 31"},"GOTO":{}},
            104:{"ACTION":{"ap":"S 16","for":"S 30","fun":"S 15","id":"S 21","if":"S 22","menos":"S 2","neg":"S 25","num":"S 13","read":"S 12","var":"S 3","while":"S 9","write":"S 11"},"GOTO":{"ADD":23,"ASSIGN":8,"EXPR":1,"EXPR_STMT":5,"FOR_STMT":27,"FUN_CALL":7,"FUN_CALL_SEMI":6,"FUN_DECL":31,"IF_STMT":19,"MUL":29,"PRIMARY":24,"READ_STMT":28,"REL":4,"STMT":18,"STMT_LIST":111,"UNARY":32,"VAR_DECL":26,"WHILE_STMT":17,"WRITE_STMT":10}},
            105:{"ACTION":{"fp":"R 24","pv":"R 24"},"GOTO":{}},
            106:{"ACTION":{"pv":"R 25"},"GOTO":{}},
            107:{"ACTION":{"pv":"S 112"},"GOTO":{}},
            108:{"ACTION":{"fb":"S 113"},"GOTO":{}},
            109:{"ACTION":{"ap":"S 16","for":"S 30","fun":"S 15","id":"S 21","if":"S 22","menos":"S 2","neg":"S 25","num":"S 13","read":"S 12","var":"S 3","while":"S 9","write":"S 11"},"GOTO":{"ADD":23,"ASSIGN":8,"EXPR":1,"EXPR_STMT":5,"FOR_STMT":27,"FUN_CALL":7,"FUN_CALL_SEMI":6,"FUN_DECL":31,"IF_STMT":19,"MUL":29,"PRIMARY":24,"READ_STMT":28,"REL":4,"STMT":18,"STMT_LIST":114,"UNARY":32,"VAR_DECL":26,"WHILE_STMT":17,"WRITE_STMT":10}},
            110:{"ACTION":{"fp":"R 35","v":"S 101"},"GOTO":{}},
            111:{"ACTION":{"fb":"S 115"},"GOTO":{}},
            112:{"ACTION":{"id":"S 81"},"GOTO":{"ASSIGN_NS":116}},
            113:{"ACTION":{"$":"R 22","ap":"R 22","fb":"R 22","for":"R 22","fun":"R 22","id":"R 22","if":"R 22","menos":"R 22","neg":"R 22","num":"R 22","read":"R 22","var":"R 22","while":"R 22","write":"R 22"},"GOTO":{}},
            114:{"ACTION":{"ap":"S 16","for":"S 30","fun":"S 15","id":"S 21","if":"S 22","menos":"S 2","neg":"S 25","num":"S 13","read":"S 12","var":"S 3","while":"S 9","write":"S 11","fb":"S 117"},"GOTO":{"ADD":23,"ASSIGN":8,"EXPR":1,"EXPR_STMT":5,"FOR_STMT":27,"FUN_CALL":7,"FUN_CALL_SEMI":6,"FUN_DECL":31,"IF_STMT":19,"MUL":29,"PRIMARY":24,"READ_STMT":28,"REL":4,"STMT":40,"UNARY":32,"VAR_DECL":26,"WHILE_STMT":17,"WRITE_STMT":10}},
            115:{"ACTION":{"else":"S 118"},"GOTO":{"ELSE_OPT":119}},
            116:{"ACTION":{"fp":"S 120"},"GOTO":{}},
            117:{"ACTION":{"$":"R 15","ap":"R 15","fb":"R 15","for":"R 15","fun":"R 15","id":"R 15","if":"R 15","menos":"R 15","neg":"R 15","num":"R 15","read":"R 15","var":"R 15","while":"R 15","write":"R 15"},"GOTO":{}},
            118:{"ACTION":{"ab":"S 121"},"GOTO":{}},
            119:{"ACTION":{"$":"R 19","ap":"R 19","fb":"R 19","for":"R 19","fun":"R 19","id":"R 19","if":"R 19","menos":"R 19","neg":"R 19","num":"R 19","read":"R 19","var":"R 19","while":"R 19","write":"R 19"},"GOTO":{}},
            120:{"ACTION":{"ab":"S 122"},"GOTO":{}},
            121:{"ACTION":{"ap":"S 16","for":"S 30","fun":"S 15","id":"S 21","if":"S 22","menos":"S 2","neg":"S 25","num":"S 13","read":"S 12","var":"S 3","while":"S 9","write":"S 11"},"GOTO":{"ADD":23,"ASSIGN":8,"EXPR":1,"EXPR_STMT":5,"FOR_STMT":27,"FUN_CALL":7,"FUN_CALL_SEMI":6,"FUN_DECL":31,"IF_STMT":19,"MUL":29,"PRIMARY":24,"READ_STMT":28,"REL":4,"STMT":18,"STMT_LIST":123,"UNARY":32,"VAR_DECL":26,"WHILE_STMT":17,"WRITE_STMT":10}},
            122:{"ACTION":{"ap":"S 16","for":"S 30","fun":"S 15","id":"S 21","if":"S 22","menos":"S 2","neg":"S 25","num":"S 13","read":"S 12","var":"S 3","while":"S 9","write":"S 11"},"GOTO":{"ADD":23,"ASSIGN":8,"EXPR":1,"EXPR_STMT":5,"FOR_STMT":27,"FUN_CALL":7,"FUN_CALL_SEMI":6,"FUN_DECL":31,"IF_STMT":19,"MUL":29,"PRIMARY":24,"READ_STMT":28,"REL":4,"STMT":18,"STMT_LIST":124,"UNARY":32,"VAR_DECL":26,"WHILE_STMT":17,"WRITE_STMT":10}},
            123:{"ACTION":{"fb":"S 125"},"GOTO":{}},
            124:{"ACTION":{"fb":"S 126"},"GOTO":{}},
            125:{"ACTION":{"$":"R 20","ap":"R 20","fb":"R 20","for":"R 20","fun":"R 20","id":"R 20","if":"R 20","menos":"R 20","neg":"R 20","num":"R 20","read":"R 20","var":"R 20","while":"R 20","write":"R 20"},"GOTO":{}},
            126:{"ACTION":{"$":"R 23","ap":"R 23","fb":"R 23","for":"R 23","fun":"R 23","id":"R 23","if":"R 23","menos":"R 23","neg":"R 23","num":"R 23","read":"R 23","var":"R 23","while":"R 23","write":"R 23"},"GOTO":{}},
            127:{"ACTION":{"fp":"S 100"},"GOTO":{"PARAMS":89}},
            128:{"ACTION":{"ab":"S 109"},"GOTO":{}}
        }

    def analisar(self, tokens):
        """Executa a análise sintática SLR."""
        stream = [t.tipo for t in tokens] + ['$']  # Adiciona $ ao final.
        pilha = [0]  # Pilha de estados começa com estado inicial.
        pos = 0  # Posição no stream de tokens.
        passos = 0  # Contador de passos.
        print(f"{'Passo':<5} {'Pilha':<30} {'Entrada':<30} {'Ação'}")
        print("-" * 80)
        while True:
            estado = pilha[-1]
            token = stream[pos]
            action_dict = self.afd.get(estado, {}).get('ACTION', {})
            acao = action_dict.get(token)
            # Corrige a exibição da entrada para mostrar os tokens corretos
            entrada_display = ' '.join(stream[pos:min(pos+5, len(stream))])
            print(f"{passos:<5} {','.join(map(str, pilha)):<30} {entrada_display:<30} {acao}")
            if acao is None:
                raise SyntaxError(f"Erro sintático no estado {estado} com token '{token}'")
            if acao.startswith('S'):  # Shift: adiciona estado à pilha.
                pilha.append(int(acao.split()[1]))
                pos += 1
            elif acao.startswith('R'):
                prod_idx = int(acao.split()[1])
                lhs, rhs = PRODUCOES[prod_idx]
                for _ in rhs:  # Remove símbolos da pilha.
                    pilha.pop()
                estado_topo = pilha[-1]
                goto_dict = self.afd.get(estado_topo, {}).get('GOTO', {})
                # Usar o nome do não-terminal diretamente.
                novo_estado = goto_dict.get(lhs)
                if novo_estado is None:
                    raise SyntaxError(f"GOTO não definido para {lhs} no estado {estado_topo} (produção {prod_idx})")
                pilha.append(novo_estado)
            elif acao == 'ACC':  # Aceita: análise concluída.
                print("\nAnálise concluída com sucesso!")
                return True
            passos += 1
            if passos > 10000:  # Evita loop infinito.
                raise RuntimeError("Loop infinito detectado")

# Função principal para testar o analisador.
def main():
    codigo_teste = """
    var x;
    x = 5 + 3 * (2 + 1);
    write(x);
    read(x);
    if (x > 2) { write(1); } else { write(0); }
    while (x < 10) { x = x + 1; }
    for (x = 0; x < 5; x = x + 1) { write(x); }
    fun minhaFunc(a, b) { write(a); write(b); }
    minhaFunc(10, 20);
    """
    lex = Lexico()
    lex.definir_entrada(codigo_teste)
    tokens = []
    while True:
        tk = lex.proximo_token()
        if tk.tipo == '$':
            break
        tokens.append(tk)
    print("=== Tokens encontrados ===")
    for t in tokens:
        print(t)
    print(f"Total de tokens: {len(tokens)}\n")
    print("=== Análise Sintática SLR ===")
    slr = SLR()
    try:
        slr.analisar(tokens)
    except Exception as e:
        print(f"Erro na análise: {e}")

if __name__ == "__main__":
    main()