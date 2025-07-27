import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os
import webbrowser

INFO_TEXT = (
    '製作者: soramame72\n'
    'webサイト: https://soramame72.22web.org/software/fumo_la/index.html\n'
    'version: 0.0.1'
)

class FumoEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Fumo Editor')
        self.geometry('800x600')
        self.create_widgets()
        self.filename = None

    def create_widgets(self):
        # メニューバー
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='開く', command=self.open_file)
        filemenu.add_command(label='保存', command=self.save_file)
        filemenu.add_command(label='名前を付けて保存', command=self.save_file_as)
        filemenu.add_separator()
        filemenu.add_command(label='退出', command=self.quit)
        menubar.add_cascade(label='ファイル', menu=filemenu)
        # 情報メニュー
        infomenu = tk.Menu(menubar, tearoff=0)
        infomenu.add_command(label='バージョン情報', command=self.show_info)
        menubar.add_cascade(label='情報', menu=infomenu)
        self.config(menu=menubar)

        # テキストエリア
        self.text = scrolledtext.ScrolledText(self, font=('Consolas', 14))
        self.text.pack(fill=tk.BOTH, expand=True)

        # 実行ボタンと結果表示
        frame = tk.Frame(self)
        frame.pack(fill=tk.X)
        run_btn = tk.Button(frame, text='実行', command=self.run_fumo)
        run_btn.pack(side=tk.LEFT, padx=5, pady=5)
        self.result = scrolledtext.ScrolledText(self, height=8, font=('Consolas', 12), bg='#f0f0f0')
        self.result.pack(fill=tk.BOTH, expand=False)
        self.result.config(state=tk.DISABLED)

    def show_info(self):
        info_win = tk.Toplevel(self)
        info_win.title('Fumo Editor 情報')
        info_win.geometry('400x200')
        info_label = tk.Label(info_win, text='製作者: soramame72\nwebサイト: ', anchor='w', justify='left')
        info_label.pack(anchor='w', padx=10, pady=(10,0))
        # クリック可能なリンク
        link = tk.Label(info_win, text='https://soramame72.22web.org/software/fumo_la/index.html', fg='blue', cursor='hand2')
        link.pack(anchor='w', padx=20)
        link.bind('<Button-1>', lambda e: webbrowser.open('https://soramame72.22web.org/software/fumo_la/index.html'))
        ver_label = tk.Label(info_win, text='version: 0.0.1', anchor='w', justify='left')
        ver_label.pack(anchor='w', padx=10, pady=(10,0))
        info_win.transient(self)
        info_win.grab_set()

    def open_file(self):
        fname = filedialog.askopenfilename(filetypes=[('Fumo files', '*.fumo'), ('All files', '*.*')])
        if fname:
            with open(fname, encoding='utf-8') as f:
                self.text.delete('1.0', tk.END)
                self.text.insert(tk.END, f.read())
            self.filename = fname
            self.title(f'Fumo Editor - {os.path.basename(fname)}')

    def save_file(self):
        if not self.filename:
            self.save_file_as()
            return
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(self.text.get('1.0', tk.END))
        messagebox.showinfo('保存', 'ファイルを保存しました')

    def save_file_as(self):
        fname = filedialog.asksaveasfilename(defaultextension='.fumo', filetypes=[('Fumo files', '*.fumo'), ('All files', '*.*')])
        if fname:
            self.filename = fname
            self.save_file()

    def run_fumo(self):
        code = self.text.get('1.0', tk.END)
        tmpfile = '___tmp_fumo_run.fumo'
        with open(tmpfile, 'w', encoding='utf-8') as f:
            f.write(code)
        exe = 'fumo_interpreter.exe' if os.path.exists('fumo_interpreter.exe') else 'python fumo_interpreter.py'
        try:
            if exe.endswith('.exe'):
                # Windows: コンソールを出さずに実行
                result = subprocess.run(
                    [exe, tmpfile],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                result = subprocess.run(
                    exe.split() + [tmpfile],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
            output = result.stdout + result.stderr
        except Exception as e:
            output = str(e)
        os.remove(tmpfile)
        self.result.config(state=tk.NORMAL)
        self.result.delete('1.0', tk.END)
        self.result.insert(tk.END, output)
        self.result.config(state=tk.DISABLED)

if __name__ == '__main__':
    app = FumoEditor()
    app.mainloop() 
