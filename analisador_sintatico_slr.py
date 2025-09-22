

import re

class ErroLexico(Exception):
    def __init__(self, mensagem, posicao):
        super().__init__(mensagem)
        self.posicao = posicao

class ErroSintatico(Exception):
    def __init__(self, mensagem, posicao):
        super().__init__(mensagem)
        self.posicao = posicao

class Token:
    def __init__(self, id, lexema, posicao):
        self.id = id
        self.lexema = lexema
        self.posicao = posicao

class Lexico:
    def __init__(self):
        self.entrada = ""
        self.pos = 0
        self.tokens = [
            ('FUN', r'fun'), ('VAR', r'var'), ('WRITE', r'write'), ('READ', r'read'),
            ('IF', r'if'), ('ELSE', r'else'), ('WHILE', r'while'), ('FOR', r'for'),
            ('LPAREN', r'\('), ('RPAREN', r'\)'), ('LBRACE', r'\{'), ('RBRACE', r'\}'),
            ('SEMI', r';'), ('EQ', r'='), ('PLUS', r'\+'), ('MINUS', r'-'),
            ('MULT', r'\*'), ('DIV', r'/'), ('GT', r'>'), ('LT', r'<'),
            ('GE', r'>='), ('LE', r'<='), ('EQEQ', r'=='), ('NE', r'!='), ('NOT', r'!'),
            ('ID', r'[a-zA-Z][a-zA-Z0-9_]*'), ('NUM', r'[0-9]+'),
            ('WS', r'\s+')
        ]
        self.padrao = '|'.join(f'(?P<{nome}>{regex})' for nome, regex in self.tokens)

    def definir_entrada(self, entrada_str):
        self.entrada = entrada_str
        self.pos = 0

    def proximo_token(self):
        if self.pos >= len(self.entrada):
            return None
        match = re.match(self.padrao, self.entrada[self.pos:])
        if not match:
            raise ErroLexico(f"Caractere inválido: {self.entrada[self.pos]}", self.pos)
        for nome, lexema in match.groupdict().items():
            if lexema:
                self.pos += len(lexema)
                if nome == 'WS':
                    return self.proximo_token()
                return Token(nome, lexema, self.pos - len(lexema))
        raise ErroLexico("Erro léxico", self.pos)

class Sintatico:
    def __init__(self):
        self.tabela = {
            (0, 'FUN'): 's3', (0, 'VAR'): 's4', (0, 'ID'): 's5', (0, 'WRITE'): 's6', (0, 'READ'): 's7', (0, 'IF'): 's8', (0, 'WHILE'): 's9', (0, 'FOR'): 's10', (0, 'P'): 1, (0, 'D'): 2,
            (1, '$'): 'acc',
            (2, 'FUN'): 's3', (2, 'VAR'): 's4', (2, 'ID'): 's5', (2, 'WRITE'): 's6', (2, 'READ'): 's7', (2, 'IF'): 's8', (2, 'WHILE'): 's9', (2, 'FOR'): 's10', (2, '$'): 'r1', (2, 'D'): 11,
            (3, 'ID'): 's12',
            (4, 'ID'): 's13',
            (5, 'EQ'): 's14',
            (6, 'LPAREN'): 's15',
            (7, 'LPAREN'): 's16',
            (8, 'LPAREN'): 's17',
            (9, 'LPAREN'): 's18',
            (10, 'LPAREN'): 's19',
            (11, '$'): 'r2', (11, 'FUN'): 'r2', (11, 'VAR'): 'r2', (11, 'ID'): 'r2', (11, 'WRITE'): 'r2', (11, 'READ'): 'r2', (11, 'IF'): 'r2', (11, 'WHILE'): 'r2', (11, 'FOR'): 'r2',
            (12, 'LPAREN'): 's20',
            (13, 'SEMI'): 's21',
            (14, 'ID'): 's24', (14, 'NUM'): 's25', (14, 'LPAREN'): 's26', (14, 'NOT'): 's27', (14, 'E'): 22, (14, 'T'): 23, (14, 'F'): 28, (14, 'CMP'): 29,
            (15, 'ID'): 's24', (15, 'NUM'): 's25', (15, 'LPAREN'): 's26', (15, 'NOT'): 's27', (15, 'E'): 30, (15, 'T'): 23, (15, 'F'): 28, (15, 'CMP'): 29,
            (16, 'ID'): 's31',
            (17, 'ID'): 's24', (17, 'NUM'): 's25', (17, 'LPAREN'): 's26', (17, 'NOT'): 's27', (17, 'E'): 32, (17, 'T'): 23, (17, 'F'): 28, (17, 'CMP'): 29,
            (18, 'ID'): 's24', (18, 'NUM'): 's25', (18, 'LPAREN'): 's26', (18, 'NOT'): 's27', (18, 'E'): 33, (18, 'T'): 23, (18, 'F'): 28, (18, 'CMP'): 29,
            (19, 'ID'): 's35', (19, 'ATR'): 34,
            (20, 'RPAREN'): 's36',
            (21, '$'): 'r4', (21, 'FUN'): 'r4', (21, 'VAR'): 'r4', (21, 'ID'): 'r4', (21, 'WRITE'): 'r4', (21, 'READ'): 'r4', (21, 'IF'): 'r4', (21, 'WHILE'): 'r4', (21, 'FOR'): 'r4',
            (22, 'PLUS'): 's37', (22, 'MINUS'): 's38', (22, 'SEMI'): 'r5', (22, 'RPAREN'): 'r5',
            (23, 'MULT'): 's39', (23, 'DIV'): 's40', (23, 'PLUS'): 'r6', (23, 'MINUS'): 'r6', (23, 'SEMI'): 'r6', (23, 'RPAREN'): 'r6', (23, 'GT'): 'r6', (23, 'LT'): 'r6', (23, 'GE'): 'r6', (23, 'LE'): 'r6', (23, 'EQEQ'): 'r6', (23, 'NE'): 'r6',
            (24, 'PLUS'): 'r7', (24, 'MINUS'): 'r7', (24, 'MULT'): 'r7', (24, 'DIV'): 'r7', (24, 'SEMI'): 'r7', (24, 'RPAREN'): 'r7', (24, 'GT'): 'r7', (24, 'LT'): 'r7', (24, 'GE'): 'r7', (24, 'LE'): 'r7', (24, 'EQEQ'): 'r7', (24, 'NE'): 'r7',
            (25, 'PLUS'): 'r8', (25, 'MINUS'): 'r8', (25, 'MULT'): 'r8', (25, 'DIV'): 'r8', (25, 'SEMI'): 'r8', (25, 'RPAREN'): 'r8', (25, 'GT'): 'r8', (25, 'LT'): 'r8', (25, 'GE'): 'r8', (25, 'LE'): 'r8', (25, 'EQEQ'): 'r8', (25, 'NE'): 'r8',
            (26, 'ID'): 's24', (26, 'NUM'): 's25', (26, 'LPAREN'): 's26', (26, 'NOT'): 's27', (26, 'E'): 41, (26, 'T'): 23, (26, 'F'): 28, (26, 'CMP'): 29,
            (27, 'ID'): 's24', (27, 'NUM'): 's25', (27, 'LPAREN'): 's26', (27, 'NOT'): 's27', (27, 'E'): 42, (27, 'T'): 23, (27, 'F'): 28, (27, 'CMP'): 29,
            (28, 'PLUS'): 'r9', (28, 'MINUS'): 'r9', (28, 'MULT'): 'r9', (28, 'DIV'): 'r9', (28, 'SEMI'): 'r9', (28, 'RPAREN'): 'r9', (28, 'GT'): 'r9', (28, 'LT'): 'r9', (28, 'GE'): 'r9', (28, 'LE'): 'r9', (28, 'EQEQ'): 'r9', (28, 'NE'): 'r9',
            (29, 'RPAREN'): 's43',
            (30, 'RPAREN'): 's44', (30, 'PLUS'): 's37', (30, 'MINUS'): 's38',
            (31, 'RPAREN'): 's45',
            (32, 'RPAREN'): 's46',
            (33, 'RPAREN'): 's47',
            (34, 'SEMI'): 's48',
            (35, 'EQ'): 's14', (35, 'E'): 49,
            (36, 'LBRACE'): 's50',
            (37, 'ID'): 's24', (37, 'NUM'): 's25', (37, 'LPAREN'): 's26', (37, 'NOT'): 's27', (37, 'T'): 51, (37, 'F'): 28, (37, 'CMP'): 29,
            (38, 'ID'): 's24', (38, 'NUM'): 's25', (38, 'LPAREN'): 's26', (38, 'NOT'): 's27', (38, 'T'): 52, (38, 'F'): 28, (38, 'CMP'): 29,
            (39, 'ID'): 's24', (39, 'NUM'): 's25', (39, 'LPAREN'): 's26', (39, 'NOT'): 's27', (39, 'F'): 53, (39, 'CMP'): 29,
            (40, 'ID'): 's24', (40, 'NUM'): 's25', (40, 'LPAREN'): 's26', (40, 'NOT'): 's27', (40, 'F'): 54, (40, 'CMP'): 29,
            (41, 'RPAREN'): 's55', (41, 'PLUS'): 's37', (41, 'MINUS'): 's38',
            (42, 'GT'): 's56', (42, 'LT'): 's57', (42, 'GE'): 's58', (42, 'LE'): 's59', (42, 'EQEQ'): 's60', (42, 'NE'): 's61',
            (43, 'LBRACE'): 's62',
            (44, 'SEMI'): 'r14',
            (45, 'SEMI'): 'r15',
            (46, 'LBRACE'): 's65',
            (47, 'LBRACE'): 's66',
            (48, 'ID'): 's35', (48, 'ATR'): 67,
            (49, 'SEMI'): 's68',
            (50, 'FUN'): 's3', (50, 'VAR'): 's4', (50, 'ID'): 's5', (50, 'WRITE'): 's6', (50, 'READ'): 's7', (50, 'IF'): 's8', (50, 'WHILE'): 's9', (50, 'FOR'): 's10', (50, 'P'): 69, (50, 'D'): 2,
            (51, 'MULT'): 's39', (51, 'DIV'): 's40', (51, 'PLUS'): 'r10', (51, 'MINUS'): 'r10', (51, 'SEMI'): 'r10', (51, 'RPAREN'): 'r10', (51, 'GT'): 'r10', (51, 'LT'): 'r10', (51, 'GE'): 'r10', (51, 'LE'): 'r10', (51, 'EQEQ'): 'r10', (51, 'NE'): 'r10',
            (52, 'MULT'): 's39', (52, 'DIV'): 's40', (52, 'PLUS'): 'r11', (52, 'MINUS'): 'r11', (52, 'SEMI'): 'r11', (52, 'RPAREN'): 'r11', (52, 'GT'): 'r11', (52, 'LT'): 'r11', (52, 'GE'): 'r11', (52, 'LE'): 'r11', (52, 'EQEQ'): 'r11', (52, 'NE'): 'r11',
            (53, 'PLUS'): 'r12', (53, 'MINUS'): 'r12', (53, 'MULT'): 'r12', (53, 'DIV'): 'r12', (53, 'SEMI'): 'r12', (53, 'RPAREN'): 'r12', (53, 'GT'): 'r12', (53, 'LT'): 'r12', (53, 'GE'): 'r12', (53, 'LE'): 'r12', (53, 'EQEQ'): 'r12', (53, 'NE'): 'r12',
            (54, 'PLUS'): 'r13', (54, 'MINUS'): 'r13', (54, 'MULT'): 'r13', (54, 'DIV'): 'r13', (54, 'SEMI'): 'r13', (54, 'RPAREN'): 'r13', (54, 'GT'): 'r13', (54, 'LT'): 'r13', (54, 'GE'): 'r13', (54, 'LE'): 'r13', (54, 'EQEQ'): 'r13', (54, 'NE'): 'r13',
            (55, 'PLUS'): 'r14', (55, 'MINUS'): 'r14', (55, 'MULT'): 'r14', (55, 'DIV'): 'r14', (55, 'SEMI'): 'r14', (55, 'RPAREN'): 'r14', (55, 'GT'): 'r14', (55, 'LT'): 'r14', (55, 'GE'): 'r14', (55, 'LE'): 'r14', (55, 'EQEQ'): 'r14', (55, 'NE'): 'r14',
            (56, 'ID'): 's24', (56, 'NUM'): 's25', (56, 'LPAREN'): 's26', (56, 'NOT'): 's27', (56, 'E'): 70, (56, 'T'): 23, (56, 'F'): 28, (56, 'CMP'): 29,
            (57, 'ID'): 's24', (57, 'NUM'): 's25', (57, 'LPAREN'): 's26', (57, 'NOT'): 's27', (57, 'E'): 71, (57, 'T'): 23, (57, 'F'): 28, (57, 'CMP'): 29,
            (58, 'ID'): 's24', (58, 'NUM'): 's25', (58, 'LPAREN'): 's26', (58, 'NOT'): 's27', (58, 'E'): 72, (58, 'T'): 23, (58, 'F'): 28, (58, 'CMP'): 29,
            (59, 'ID'): 's24', (59, 'NUM'): 's25', (59, 'LPAREN'): 's26', (59, 'NOT'): 's27', (59, 'E'): 73, (59, 'T'): 23, (59, 'F'): 28, (59, 'CMP'): 29,
            (60, 'ID'): 's24', (60, 'NUM'): 's25', (60, 'LPAREN'): 's26', (60, 'NOT'): 's27', (60, 'E'): 74, (60, 'T'): 23, (60, 'F'): 28, (60, 'CMP'): 29,
            (61, 'ID'): 's24', (61, 'NUM'): 's25', (61, 'LPAREN'): 's26', (61, 'NOT'): 's27', (61, 'E'): 75, (61, 'T'): 23, (61, 'F'): 28, (61, 'CMP'): 29,
            (62, 'FUN'): 's3', (62, 'VAR'): 's4', (62, 'ID'): 's5', (62, 'WRITE'): 's6', (62, 'READ'): 's7', (62, 'IF'): 's8', (62, 'WHILE'): 's9', (62, 'FOR'): 's10', (62, 'P'): 76, (62, 'D'): 2,
            (63, '$'): 'r15', (63, 'FUN'): 'r15', (63, 'VAR'): 'r15', (63, 'ID'): 'r15', (63, 'WRITE'): 'r15', (63, 'READ'): 'r15', (63, 'IF'): 'r15', (63, 'WHILE'): 'r15', (63, 'FOR'): 'r15',
            (64, '$'): 'r16', (64, 'FUN'): 'r16', (64, 'VAR'): 'r16', (64, 'ID'): 'r16', (64, 'WRITE'): 'r16', (64, 'READ'): 'r16', (64, 'IF'): 'r16', (64, 'WHILE'): 'r16', (64, 'FOR'): 'r16',
            (65, 'FUN'): 's3', (65, 'VAR'): 's4', (65, 'ID'): 's5', (65, 'WRITE'): 's6', (65, 'READ'): 's7', (65, 'IF'): 's8', (65, 'WHILE'): 's9', (65, 'FOR'): 's10', (65, 'P'): 77, (65, 'D'): 2,
            (66, 'FUN'): 's3', (66, 'VAR'): 's4', (66, 'ID'): 's5', (66, 'WRITE'): 's6', (66, 'READ'): 's7', (66, 'IF'): 's8', (66, 'WHILE'): 's9', (66, 'FOR'): 's10', (66, 'P'): 78, (66, 'D'): 2,
            (67, 'SEMI'): 's79',
            (68, 'ID'): 's35', (68, 'ATR'): 80,
            (69, 'RBRACE'): 's81',
            (70, 'RPAREN'): 'r17',
            (71, 'RPAREN'): 'r18',
            (72, 'RPAREN'): 'r19',
            (73, 'RPAREN'): 'r20',
            (74, 'RPAREN'): 'r21',
            (75, 'RPAREN'): 'r22',
            (76, 'RBRACE'): 's82',
            (77, 'RBRACE'): 's83',
            (78, 'RBRACE'): 's84', (78, 'ELSE'): 's85',
            (79, 'LBRACE'): 's86',
            (80, 'SEMI'): 's87',
            (81, '$'): 'r23', (81, 'FUN'): 'r23', (81, 'VAR'): 'r23', (81, 'ID'): 'r23', (81, 'WRITE'): 'r23', (81, 'READ'): 'r23', (81, 'IF'): 'r23', (81, 'WHILE'): 'r23', (81, 'FOR'): 'r23',
            (82, '$'): 'r24', (82, 'FUN'): 'r24', (82, 'VAR'): 'r24', (82, 'ID'): 'r24', (82, 'WRITE'): 'r24', (82, 'READ'): 'r24', (82, 'IF'): 'r24', (82, 'WHILE'): 'r24', (82, 'FOR'): 'r24',
            (83, '$'): 'r25', (83, 'FUN'): 'r25', (83, 'VAR'): 'r25', (83, 'ID'): 'r25', (83, 'WRITE'): 'r25', (83, 'READ'): 'r25', (83, 'IF'): 'r25', (83, 'WHILE'): 'r25', (83, 'FOR'): 'r25',
            (84, '$'): 'r26', (84, 'FUN'): 'r26', (84, 'VAR'): 'r26', (84, 'ID'): 'r26', (84, 'WRITE'): 'r26', (84, 'READ'): 'r26', (84, 'IF'): 'r26', (84, 'WHILE'): 'r26', (84, 'FOR'): 'r26',
            (85, 'LBRACE'): 's88',
            (86, 'FUN'): 's3', (86, 'VAR'): 's4', (86, 'ID'): 's5', (86, 'WRITE'): 's6', (86, 'READ'): 's7', (86, 'IF'): 's8', (86, 'WHILE'): 's9', (86, 'FOR'): 's10', (86, 'P'): 89, (86, 'D'): 2,
            (87, '$'): 'r27', (87, 'FUN'): 'r27', (87, 'VAR'): 'r27', (87, 'ID'): 'r27', (87, 'WRITE'): 'r27', (87, 'READ'): 'r27', (87, 'IF'): 'r27', (87, 'WHILE'): 'r27', (87, 'FOR'): 'r27',
            (88, 'FUN'): 's3', (88, 'VAR'): 's4', (88, 'ID'): 's5', (88, 'WRITE'): 's6', (88, 'READ'): 's7', (88, 'IF'): 's8', (88, 'WHILE'): 's9', (88, 'FOR'): 's10', (88, 'P'): 90, (88, 'D'): 2,
            (89, 'RBRACE'): 's91',
            (90, 'RBRACE'): 's92',
            (91, '$'): 'r28', (91, 'FUN'): 'r28', (91, 'VAR'): 'r28', (91, 'ID'): 'r28', (91, 'WRITE'): 'r28', (91, 'READ'): 'r28', (91, 'IF'): 'r28', (91, 'WHILE'): 'r28', (91, 'FOR'): 'r28',
            (92, '$'): 'r29', (92, 'FUN'): 'r29', (92, 'VAR'): 'r29', (92, 'ID'): 'r29', (92, 'WRITE'): 'r29', (92, 'READ'): 'r29', (92, 'IF'): 'r29', (92, 'WHILE'): 'r29', (92, 'FOR'): 'r29'
        }
        self.regras = [
            ('S\'', ['P'], 1),  # 0
            ('P', ['D'], 1),    # 1
            ('P', ['P', 'D'], 2), # 2
            ('D', ['FUN'], 1),  # 3
            ('D', ['VAR'], 1),  # 4
            ('D', ['ATR'], 1),  # 5
            ('D', ['WRT'], 1),  # 6
            ('D', ['RD'], 1),   # 7
            ('D', ['IF'], 1),   # 8
            ('D', ['WHL'], 1),  # 9
            ('D', ['FOR'], 1),  # 10
            ('FUN', ['fun', 'ID', 'LPAREN', 'RPAREN', 'LBRACE', 'P', 'RBRACE'], 7),  # 11
            ('VAR', ['var', 'ID', 'SEMI'], 3),  # 12
            ('ATR', ['ID', 'EQ', 'E', 'SEMI'], 4),  # 13
            ('E', ['E', 'PLUS', 'T'], 3),  # 14
            ('E', ['E', 'MINUS', 'T'], 3),  # 15
            ('E', ['T'], 1),  # 16
            ('T', ['T', 'MULT', 'F'], 3),  # 17
            ('T', ['T', 'DIV', 'F'], 3),  # 18
            ('T', ['F'], 1),  # 19
            ('F', ['ID'], 1),  # 20
            ('F', ['NUM'], 1),  # 21
            ('F', ['LPAREN', 'E', 'RPAREN'], 3),  # 22
            ('F', ['CMP'], 1),  # 23
            ('CMP', ['E', 'GT', 'E'], 3),  # 24
            ('CMP', ['E', 'LT', 'E'], 3),  # 25
            ('CMP', ['E', 'GE', 'E'], 3),  # 26
            ('CMP', ['E', 'LE', 'E'], 3),  # 27
            ('CMP', ['E', 'EQEQ', 'E'], 3),  # 28
            ('CMP', ['E', 'NE', 'E'], 3),  # 29
            ('CMP', ['NOT', 'E'], 2),  # 30
            ('WRT', ['write', 'LPAREN', 'E', 'RPAREN', 'SEMI'], 5),  # 31
            ('RD', ['read', 'LPAREN', 'ID', 'RPAREN', 'SEMI'], 5),  # 32
            ('IF', ['if', 'LPAREN', 'CMP', 'RPAREN', 'LBRACE', 'P', 'RBRACE'], 7),  # 33
            ('IF', ['if', 'LPAREN', 'CMP', 'RPAREN', 'LBRACE', 'P', 'RBRACE', 'else', 'LBRACE', 'P', 'RBRACE'], 11),  # 34
            ('WHL', ['while', 'LPAREN', 'CMP', 'RPAREN', 'LBRACE', 'P', 'RBRACE'], 7),  # 35
            ('FOR', ['for', 'LPAREN', 'ATR', 'SEMI', 'CMP', 'SEMI', 'ATR', 'RPAREN', 'LBRACE', 'P', 'RBRACE'], 11)  # 36
        ]

    def analisar(self, scanner):
        pilha = [0]
        token = scanner.proximo_token()
        while True:
            estado = pilha[-1]
            id_token = token.id if token else '$'
            acao = self.tabela.get((estado, id_token), None)
            print(f"Pilha: {pilha}, Token: {id_token}, Ação: {acao}")
            if not acao:
                raise ErroSintatico(f"Erro sintático em '{token.lexema if token else '$'}' (estado {estado})", token.posicao if token else scanner.pos)
            if acao == 'acc':
                print("Análise concluída com sucesso!")
                return
            if acao.startswith('s'):
                pilha.append(int(acao[1:]))
                token = scanner.proximo_token()
            else:
                indice_regra = int(acao[1:])
                regra = self.regras[indice_regra]
                print(f"Reduzindo por {regra[0]} -> {' '.join(regra[1])}, removendo {len(regra[1])} símbolos")
                for _ in range(len(regra[1])):
                    if pilha:
                        pilha.pop()
                    else:
                        raise ErroSintatico(f"Pilha vazia durante redução de {regra[0]}", token.posicao if token else scanner.pos)
                if not pilha:
                    raise ErroSintatico(f"Pilha vazia após redução de {regra[0]}", token.posicao if token else scanner.pos)
                estado_goto = self.tabela.get((pilha[-1], regra[0]), None)
                if estado_goto is None:
                    raise ErroSintatico(f"Erro no GOTO para {regra[0]} no estado {pilha[-1]}", token.posicao if token else scanner.pos)
                pilha.append(int(estado_goto))
                print(f"GOTO para estado {estado_goto} com {regra[0]}")

def principal():
    lexico = Lexico()
    sintatico = Sintatico()
    entrada_teste = """
    var x;
    x = 5 + 3;
    write(x);
    if (x > 2) { write(1); } else { write(0); }
    while (x < 10) { x = x + 1; }
    for (x = 0; x < 5; x = x + 1) { write(x); }
    fun myfunc() { write(42); }
    """
    try:
        lexico.definir_entrada(entrada_teste)
        print("Tokens gerados:")
        while True:
            token = lexico.proximo_token()
            if token is None:
                break
            print(f"Token: {token.id}, Lexema: {token.lexema}, Posição: {token.posicao}")
        lexico.definir_entrada(entrada_teste)
        sintatico.analisar(lexico)
    except ErroLexico as e:
        print(f"Erro léxico: {e}, posição: {e.posicao}")
    except ErroSintatico as e:
        print(f"Erro sintático: {e}, posição: {e.posicao}")

if __name__ == "__main__":
    principal()
