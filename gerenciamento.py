import tkinter as tk
from tkinter import messagebox
import sqlite3


def adicionar_produto():
    nome = entry_nome.get()
    try:
        quantidade = int(entry_quantidade.get())
        preco = float(entry_preco.get())
    except ValueError:
        messagebox.showerror("Erro", "Quantidade e preço devem ser números")
        return

    if nome:
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)
        ''', (nome, quantidade, preco))
        conn.commit()
        conn.close()
        carregar_produtos()
        limpar_campos()
    else:
        messagebox.showwarning("Erro", "Todos os campos são obrigatórios")

def carregar_produtos():
    lista_produtos.delete(0, tk.END)
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos')
    for row in cursor.fetchall():
        lista_produtos.insert(tk.END, row)
    conn.close()

def selecionar_produto(event):
    try:
        global produto_selecionado
        index = lista_produtos.curselection()[0]
        produto_selecionado = lista_produtos.get(index)

        entry_nome.delete(0, tk.END)
        entry_nome.insert(tk.END, produto_selecionado[1])
        entry_quantidade.delete(0, tk.END)
        entry_quantidade.insert(tk.END, produto_selecionado[2])
        entry_preco.delete(0, tk.END)
        entry_preco.insert(tk.END, produto_selecionado[3])
    except IndexError:
        pass

def atualizar_produto():
    nome = entry_nome.get()
    try:
        quantidade = int(entry_quantidade.get())
        preco = float(entry_preco.get())
    except ValueError:
        messagebox.showerror("Erro", "Quantidade e preço devem ser números")
        return

    if nome:
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE produtos SET nome=?, quantidade=?, preco=? WHERE id=?
        ''', (nome, quantidade, preco, produto_selecionado[0]))
        conn.commit()
        conn.close()
        carregar_produtos()
        limpar_campos()
    else:
        messagebox.showwarning("Erro", "Todos os campos são obrigatórios")

def deletar_produto():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM produtos WHERE id=?', (produto_selecionado[0],))
    conn.commit()
    conn.close()
    carregar_produtos()
    limpar_campos()

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    entry_preco.delete(0, tk.END)


root = tk.Tk()
root.title("Gerenciamento de Estoque")


tk.Label(root, text="Nome do Produto").grid(row=0, column=0)
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1)

tk.Label(root, text="Quantidade").grid(row=1, column=0)
entry_quantidade = tk.Entry(root)
entry_quantidade.grid(row=1, column=1)

tk.Label(root, text="Preço").grid(row=2, column=0)
entry_preco = tk.Entry(root)
entry_preco.grid(row=2, column=1)


tk.Button(root, text="Adicionar Produto", command=adicionar_produto).grid(row=3, column=0, pady=10)
tk.Button(root, text="Atualizar Produto", command=atualizar_produto).grid(row=3, column=1)
tk.Button(root, text="Deletar Produto", command=deletar_produto).grid(row=4, column=0)
tk.Button(root, text="Limpar Campos", command=limpar_campos).grid(row=4, column=1)


lista_produtos = tk.Listbox(root, height=8, width=50)
lista_produtos.grid(row=5, column=0, columnspan=2)
lista_produtos.bind('<<ListboxSelect>>', selecionar_produto)


menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)

menu_bar.add_cascade(label="Arquivo", menu=file_menu)
root.config(menu=menu_bar)


carregar_produtos()


root.mainloop()
