import sys
import re

# =============================
# Fumo言語 割り当て・仕様定義
# =============================
TOKENS = {
    'VAR': 'Fumo',         # 変数宣言
    'ASSIGN': 'fumo',      # 代入
    'PRINT': 'Fumo!',      # 出力
    'INPUT': 'fumofumo!',  # 入力
    'ADD': 'fumo!',        # 加算
    'SUB': 'FumoFumo',     # 減算
    'MUL': 'fumofumo',     # 乗算
    'DIV': 'FumoFumo!',    # 除算
    'IF': 'フモ',           # if
    'ELSE': 'FumoFumoFumo',# else
    'WHILE': 'フモ!',       # while
    'EQ': 'ふも',           # ==
    'NEQ': 'ふも!',         # !=
    'LT': 'ふもふも',       # <
    'GT': 'ふもふも!',      # >
    'LE': 'ふもふもふも',   # <=
    'GE': 'ふもふもふも!',  # >=
    'AND': 'フモフモ',      # and
    'OR': 'フモフモ!',      # or
    'NOT': 'ふもふもふも',  # not
    'FOR': 'FumoFumoFumo',   # for
    'DEF': 'ふもふもふもふも',    # def
    'RETURN': 'Fumo!Fumo',      # return
    'LIST': 'ふもふもふもふも!',    # list
    'DICT': 'ふもふもふもふもふ',   # dict
    'APPEND': 'フモフモフモ',        # append
    'LEN': 'フモフモフモ!',         # len
    'BREAK': 'フモ!フモ!',         # break
    'CONTINUE': 'フモ!フモ',      # continue
    'TRY': 'ふもふもふもふも!',      # try
    'EXCEPT': 'ふもふもふもふもふ',  # except
    'OPEN': 'Fumofumo',      # open
    'READ': 'fumoFumo',     # read
    'WRITE': 'Fumofumo!',   # write
    'CLOSE': 'fumoFumo!',   # close/import
    'IMPORT': 'フモフモフモフモ!!!',    # import
}

# 出力割り当て表
FUMO_TO_CHAR = {
    'Fumo': 'A', 'fumo': 'B', 'Fumo!': 'C', 'fumo!': 'D',
    'フモ': 'E', 'フモ!': 'F', 'FumoFumo': 'G', 'fumofumo': 'H',
    'FumoFumo!': 'I', 'fumofumo!': 'J', 'ふも': 'K', 'ふも!': 'L',
    'ふもふも': 'M', 'ふもふも!': 'N', 'フモフモ': 'O', 'フモフモ!': 'P',
    'Fumofumo': 'Q', 'fumoFumo': 'R', 'Fumofumo!': 'S', 'fumoFumo!': 'T',
    'FumoFumoFumo': 'U', 'fumoFumoFumo': 'V', 'FumoFumoFumo!': 'W', 'fumoFumoFumo!': 'X',
    'FumofumoFumo': 'Y', 'fumofumoFumo': 'Z',
    'FumoFumo!Fumo': '0', 'FumoFumo!fumo': '1', 'FumoFumo!Fumo!': '2', 'FumoFumo!fumo!': '3',
    'FumoFumo!フモ': '4', 'FumoFumo!フモ!': '5', 'FumoFumo!FumoFumo': '6', 'FumoFumo!fumofumo': '7',
    'FumoFumo!FumoFumo!': '8',
    'FumoFumo!fumofumo!': '9',
    # 記号
    'Fumo!Fumo!': '!', 'fumo!fumo!': '?', 'Fumo!fumo!': '.', 'fumo!Fumo!': ',',
    'Fumo!フモ!': '-', 'Fumo!フモ': '+', 'Fumo!FumoFumo': '/', 'Fumo!fumofumo': ':',
    'Fumo!FumoFumo!': ';', 'Fumo!fumofumo!': '(', 'Fumo!Fumofumo!': ')',
    # スペース
    'Fumo!フモフモ!': ' ',
    # 小文字 a〜z（a,bは別のユニークなワードに割り当て直す）
    'FumoFumo!FumoFumo!!': 'a',
    'FumoFumo!fumofumo!!': 'b',
    'FumoFumo!Fumofumo!': 'c',
    'FumoFumo!fumoFumo!': 'd',
    'FumoFumo!FumoFumoFumo': 'e',
    'FumoFumo!fumoFumoFumo': 'f',
    'FumoFumo!FumofumoFumo': 'g',
    'FumoFumo!fumoFumoFumo!': 'h',
    'FumoFumo!FumofumoFumo!': 'i',
    'FumoFumo!fumoFumoFumoFumo': 'j',
    'FumoFumo!FumofumoFumoFumo': 'k',
    'FumoFumo!fumoFumoFumoFumo!': 'l',
    'FumoFumo!FumofumoFumoFumo!': 'm',
    'FumoFumo!fumoFumoFumoFumoFumo': 'n',
    'FumoFumo!FumofumoFumoFumoFumo': 'o',
    'FumoFumo!fumoFumoFumoFumoFumo!': 'p',
    'FumoFumo!FumofumoFumoFumoFumo!': 'q',
    'FumoFumo!fumoFumoFumoFumoFumoFumo': 'r',
    'FumoFumo!FumofumoFumoFumoFumoFumo': 's',
    'FumoFumo!fumoFumoFumoFumoFumoFumo!': 't',
    'FumoFumo!FumofumoFumoFumoFumoFumo!': 'u',
    'FumoFumo!fumoFumoFumoFumoFumoFumoFumo': 'v',
    'FumoFumo!FumofumoFumoFumoFumoFumoFumo': 'w',
    'FumoFumo!fumoFumoFumoFumoFumoFumoFumo!': 'x',
    'FumoFumo!FumofumoFumoFumoFumoFumoFumo!': 'y',
    'FumoFumo!fumoFumoFumoFumoFumoFumoFumoFumo': 'z',
}
# フモ系ワード一覧を割り当て表のキー＋従来のワードで自動生成
FUMO_WORDS = set(FUMO_TO_CHAR.keys()) | set(TOKENS.values())

# =============================
# 字句解析・パース
# =============================
WORD_PATTERN = re.compile(r'( +|\S+)')

def tokenize_line(line):
    tokens = []
    pos = 0
    while pos < len(line):
        m = WORD_PATTERN.match(line, pos)
        if not m:
            break
        word = m.group(0)
        if word.isspace():
            tokens.append(('INDENT', len(word)))
        else:
            tokens.append(('WORD', word))
        pos = m.end()
    return tokens

def parse_lines(lines):
    stmts = []
    stack = [(0, stmts)]  # (indent, block)
    for raw in lines:
        if '\t' in raw:
            raise ValueError('タブ文字（TAB）は使用禁止です。スペースのみを使ってください。')
        if raw.rstrip('\n').endswith(' '):
            raise ValueError('行末のスペースは禁止です。行末は何もないか改行のみで終わってください。')
        if not raw.strip():
            continue
        tokens = tokenize_line(raw.rstrip('\n'))
        indent = 0
        while tokens and tokens[0][0] == 'INDENT':
            indent += tokens.pop(0)[1]
        words = [w for t, w in tokens if t == 'WORD']
        if not words:
            continue
        validate_fumo_only(words, raw, allow_print=True)
        while indent < stack[-1][0]:
            stack.pop()
        if indent > stack[-1][0]:
            new_block = []
            stack[-1][1][-1]['body'] = new_block
            stack.append((indent, new_block))
            stack[-1][1].append({'words': words, 'body': None})
        else:
            stack[-1][1].append({'words': words, 'body': None})
    return stmts

# =============================
# バリデーション・値変換
# =============================
def is_fumo_word(s):
    return s in FUMO_WORDS

def validate_fumo_only(parts, line, allow_print=False):
    if allow_print and parts and parts[0] == 'Fumo!':
        for p in parts[1:]:
            if not is_fumo_word(p):
                raise ValueError(f'Fumo! の出力内容もフモ系ワードのみ許可: {p} in line: {line}')
        if len(parts) == 1:
            raise ValueError(f'Fumo! の後に出力内容がありません: {line}')
        if not is_fumo_word(parts[0]):
            raise ValueError(f'Fumo系ワード以外は使えません: {parts[0]} in line: {line}')
        return
    for p in parts:
        if not is_fumo_word(p):
            raise ValueError(f'Fumo系ワード以外は使えません: {p} in line: {line}')

def value_to_fumo_words(val):
    s = str(val)
    digit_map = {
        '0': 'FumoFumo!Fumo', '1': 'FumoFumo!fumo', '2': 'FumoFumo!Fumo!', '3': 'FumoFumo!fumo!',
        '4': 'FumoFumo!フモ', '5': 'FumoFumo!フモ!', '6': 'FumoFumo!FumoFumo', '7': 'FumoFumo!fumofumo',
        '8': 'FumoFumo!FumoFumo!', '9': 'FumoFumo!fumofumo!'
    }
    return [digit_map.get(c, '?') for c in s]

def parse_value_fumo(words):
    digit_map = {k: v for k, v in FUMO_TO_CHAR.items() if v in '0123456789'}
    digits = []
    for w in words:
        if not is_fumo_word(w):
            raise ValueError(f'Fumo系ワード以外は値に使えません: {w}')
        if w in digit_map:
            digits.append(digit_map[w])
        else:
            digits = None
            break
    if digits is not None and digits:
        return int(''.join(digits))
    return len(words)

# =============================
# 実行エンジン
# =============================
variables = {}
functions = {}
file_handles = {}

def eval_expr(words):
    return parse_value_fumo(words)

def exec_block(stmts, local_vars=None):
    global variables, file_handles, functions
    if local_vars is not None:
        old_vars = variables
        variables = local_vars
    i = 0
    while i < len(stmts):
        stmt = stmts[i]
        words = stmt['words']
        validate_fumo_only(words, ' '.join(words), allow_print=True)
        # 変数宣言
        if words[0] == TOKENS['VAR'] and len(words) == 2:
            # ループ変数として使われる場合は初期化しない
            if any(s['words'][0] == TOKENS['FOR'] and s['words'][1] == words[1] for s in stmts):
                print(f'WARNING: {words[1]} はfor文のループ変数として使われるため、グローバル初期化をスキップします')
            else:
                variables[words[1]] = 0
        # 代入
        elif words[0] == TOKENS['ASSIGN'] and len(words) >= 3:
            # ループ変数として使われる場合はグローバルに上書き
            if any(s['words'][0] == TOKENS['FOR'] and s['words'][1] == words[1] for s in stmts):
                variables[words[1]] = parse_value_fumo(words[2:])
            else:
                variables[words[1]] = parse_value_fumo(words[2:])
        # 出力
        elif words[0] == TOKENS['PRINT'] and len(words) >= 2:
            if len(words) == 2 and words[1] in variables and isinstance(variables[words[1]], int):
                fumo_words = value_to_fumo_words(variables[words[1]])
                out = ''.join(FUMO_TO_CHAR.get(w, '?') for w in fumo_words)
                print(out)
            else:
                out = ''.join(FUMO_TO_CHAR.get(w, '?') for w in words[1:])
                print(out)
        # 入力（禁止: フモ系以外入力不可）
        elif words[0] == TOKENS['INPUT']:
            print('入力はサポートされません（フモ系ワードのみ許可）')
        # 加算
        elif words[0] == TOKENS['ADD'] and len(words) >= 4:
            n = (len(words) - 2) // 2
            left = words[2:2+n]
            right = words[2+n:]
            variables[words[1]] = parse_value_fumo(left) + parse_value_fumo(right)
        # 減算
        elif words[0] == TOKENS['SUB'] and len(words) >= 4:
            n = (len(words) - 2) // 2
            left = words[2:2+n]
            right = words[2+n:]
            variables[words[1]] = parse_value_fumo(left) - parse_value_fumo(right)
        # 乗算
        elif words[0] == TOKENS['MUL'] and len(words) >= 4:
            n = (len(words) - 2) // 2
            left = words[2:2+n]
            right = words[2+n:]
            variables[words[1]] = parse_value_fumo(left) * parse_value_fumo(right)
        # 除算
        elif words[0] == TOKENS['DIV'] and len(words) >= 4:
            n = (len(words) - 2) // 2
            left = words[2:2+n]
            right = words[2+n:]
            denominator = parse_value_fumo(right)
            if denominator == 0:
                print('ZeroDivisionError')
                variables[words[1]] = 0
            else:
                variables[words[1]] = parse_value_fumo(left) // denominator
        # if文
        elif words[0] == TOKENS['IF'] and stmt['body']:
            cond = eval_expr(words[1:])
            if cond:
                exec_block(stmt['body'])
        # else文
        elif words[0] == TOKENS['ELSE'] and stmt['body']:
            exec_block(stmt['body'])
        # while文
        elif words[0] == TOKENS['WHILE'] and stmt['body']:
            while eval_expr(words[1:]):
                # 修正: local_varsを絶対に渡さない
                res = exec_block(stmt['body'], None)
                if isinstance(res, dict):
                    if 'break' in res:
                        break
                    if 'continue' in res:
                        continue
        # for文: FumoFumoFumo var start end
        elif words[0] == TOKENS['FOR']:
            var = words[1]
            if var in variables:
                print(f'WARNING: {var} はグローバル変数として初期化されています。for文のループ変数として上書きします。')
            if len(words) == 4 and stmt['body']:
                start = eval_expr([words[2]])
                end = eval_expr([words[3]])
                for v in range(start, end):
                    variables[var] = v
                    res = exec_block(stmt['body'], None)
                    if isinstance(res, dict):
                        if 'break' in res:
                            break
                        if 'continue' in res:
                            continue
        # 関数定義: ふもふもふもふも name param1 param2 ...
        elif words[0] == TOKENS['DEF'] and len(words) >= 2 and stmt['body']:
            fname = words[1]
            params = words[2:]
            functions[fname] = {'params': params, 'body': stmt['body']}
        # 関数呼び出し: name arg1 arg2 ...
        elif words[0] in functions:
            func = functions[words[0]]
            args = words[1:]
            local = dict(zip(func['params'], [eval_expr([a]) for a in args]))
            ret = exec_block(func['body'], local)
            if local_vars is not None:
                variables = old_vars
            if isinstance(ret, dict) and 'return' in ret:
                return ret['return']
        # return: Fumo!Fumo value
        elif words[0] == TOKENS['RETURN'] and len(words) == 2:
            val = eval_expr([words[1]])
            if local_vars is not None:
                variables = old_vars
            return {'return': val}
        # break: フモ!フモ!
        elif words[0] == TOKENS['BREAK']:
            if local_vars is not None:
                variables = old_vars
            return {'break': True}
        # continue: フモ!フモ
        elif words[0] == TOKENS['CONTINUE']:
            if local_vars is not None:
                variables = old_vars
            return {'continue': True}
        # try/except
        elif words[0] == TOKENS['TRY'] and stmt['body']:
            try:
                exec_block(stmt['body'])
            except Exception as e:
                # 次の文がexceptなら実行
                if i+1 < len(stmts):
                    next_stmt = stmts[i+1]
                    if next_stmt['words'][0] == TOKENS['EXCEPT'] and next_stmt['body']:
                        exec_block(next_stmt['body'])
                        i += 1  # except分をスキップ
        # except単体はスキップ
        elif words[0] == TOKENS['EXCEPT']:
            pass
        # open: Fumofumo var filename mode
        elif words[0] == TOKENS['OPEN'] and len(words) == 4:
            var, fname, mode = words[1], words[2], words[3]
            f = open(fname, mode)
            file_handles[var] = f
            variables[var] = var
        # read: fumoFumo var target
        elif words[0] == TOKENS['READ'] and len(words) == 3:
            fvar, tvar = words[1], words[2]
            f = file_handles.get(fvar)
            if f:
                variables[tvar] = f.read()
        # write: Fumofumo! var value
        elif words[0] == TOKENS['WRITE'] and len(words) == 3:
            fvar, val = words[1], words[2]
            f = file_handles.get(fvar)
            if f:
                f.write(str(eval_expr([val])))
        # close: fumoFumo! var
        elif words[0] == TOKENS['CLOSE'] and len(words) == 2:
            fvar = words[1]
            f = file_handles.get(fvar)
            if f:
                f.close()
                del file_handles[fvar]
        # import: fumoFumo! filename
        elif words[0] == TOKENS['CLOSE'] and len(words) == 2 and words[1].endswith('.fumo'):
            fname = words[1]
            try:
                with open(fname, encoding='utf-8') as f:
                    lines = f.readlines()
                stmts2 = parse_lines(lines)
                exec_block(stmts2)
            except Exception as e:
                print(f'ImportError: {e}')
        # import: フモフモフモフモ!!! filename
        elif words[0] == TOKENS['IMPORT'] and len(words) == 2:
            fname = words[1]
            if not fname.endswith('.fumo'):
                fname += '.fumo'
            try:
                with open(fname, encoding='utf-8') as f:
                    lines = f.readlines()
                stmts2 = parse_lines(lines)
                exec_block(stmts2)
            except Exception as e:
                print(f'ImportError: {e}')
        else:
            print(f'Unknown or invalid statement: {words}')
        i += 1
    if local_vars is not None:
        variables = old_vars

INFO_TEXT = (
    '製作者: soramame72\n'
    'webサイト: https://soramame72.22web.org/software/fumo_la/index.html\n'
    'version: 0.0.1'
)

def main():
    import platform
    import os
    if len(sys.argv) < 2:
        print('Fumo REPL (type "exit" or "退出" to quit, "clear" to clear screen, "help" for help, "info" for version info)')
        lines = []
        while True:
            try:
                line = input('> ')
            except EOFError:
                break
            cmd = line.strip().lower()
            if cmd == 'exit' or cmd == '退出':
                break
            if cmd == 'clear':
                if platform.system() == 'Windows':
                    os.system('cls')
                else:
                    os.system('clear')
                continue
            if cmd == 'help':
                print('''Fumo REPL ヘルプ:
  Fumo言語の1行または複数行を入力し、空行で実行
  exit/退出  : REPLを終了
  clear : 画面をクリア
  help  : このヘルプを表示
  info  : バージョン情報を表示
  ファイル実行: fumo_interpreter.exe ファイル名.fumo
''')
                continue
            if cmd == 'info':
                print(INFO_TEXT)
                continue
            lines.append(line)
            # 空行で実行
            if not line.strip():
                stmts = parse_lines(lines)
                exec_block(stmts)
                lines = []
        return
    with open(sys.argv[1], encoding='utf-8') as f:
        lines = f.readlines()
    stmts = parse_lines(lines)
    exec_block(stmts)

if __name__ == '__main__':
    main() 
