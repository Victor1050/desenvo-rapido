# Banco de Dados
import sqlite3
import tkinter as tk
from tkinter import messagebox

# Inicializa o banco de dados
def init_db():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pessoas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Inserir pessoa
def inserir_pessoa():
    nome = entry_nome.get()
    idade = entry_idade.get()
    if nome and idade:
        try:
            idade = int(idade)
        except ValueError:
            messagebox.showerror("Erro", "Idade deve ser um número inteiro.")
            return
        conn = sqlite3.connect("banco.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pessoas (nome, idade) VALUES (?, ?)", (nome, idade))
        conn.commit()
        conn.close()
        listar_pessoas()
        entry_nome.delete(0, tk.END) # limpar as caixas de texto
        entry_idade.delete(0, tk.END) # limpar as caixas de texto
    else:
        messagebox.showwarning("Aviso", "Preencha todos os campos.")

# Listar pessoas na Listbox
def listar_pessoas():
    listbox.delete(0, tk.END)
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, idade FROM pessoas")
    for row in cursor.fetchall():                 # traz todos os registros que o select buscou
        listbox.insert(tk.END, f"{row[0]} - {row[1]} ({row[2]} anos)")
    conn.close()

# Selecionar pessoa da Listbox
def selecionar_pessoa(event):
    selecionado = listbox.curselection()
    if selecionado:
        index = selecionado[0]
        texto = listbox.get(index)
        id_pessoa = int(texto.split(" - ")[0])
        conn = sqlite3.connect("banco.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nome, idade FROM pessoas WHERE id=?", (id_pessoa,))
        row = cursor.fetchone()
        conn.close()
        entry_nome.delete(0, tk.END)
        entry_idade.delete(0, tk.END)
        entry_nome.insert(0, row[0])
        entry_idade.insert(0, row[1])
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(index)
        listbox.activate(index)

# Atualizar pessoa
def atualizar_pessoa():
    selecionado = listbox.curselection()
    if selecionado:
        index = selecionado[0]
        texto = listbox.get(index)
        id_pessoa = int(texto.split(" - ")[0])
        novo_nome = entry_nome.get()
        nova_idade = entry_idade.get()
        if novo_nome and nova_idade:
            try:
                nova_idade = int(nova_idade)
            except ValueError:
                messagebox.showerror("Erro", "Idade deve ser um número inteiro.")
                return
            conn = sqlite3.connect("banco.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE pessoas SET nome=?, idade=? WHERE id=?", (novo_nome, nova_idade, id_pessoa))
            conn.commit()
            conn.close()
            listar_pessoas()
            messagebox.showinfo("Atualizar", "Pessoa atualizada com sucesso.")
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")

# Deletar pessoa
def deletar_pessoa():
    selecionado = listbox.curselection()
    if selecionado:
        index = selecionado[0]
        texto = listbox.get(index)
        id_pessoa = int(texto.split(" - ")[0])
        conn = sqlite3.connect("banco.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pessoas WHERE id=?", (id_pessoa,))
        conn.commit()
        conn.close()
        listar_pessoas()
        entry_nome.delete(0, tk.END)
        entry_idade.delete(0, tk.END)
    else:
        messagebox.showwarning("Aviso", "Selecione uma pessoa para excluir.")

# Interface gráfica
init_db()

root = tk.Tk()
root.title("Cadastro de Pessoas")  # Título da janela

# Título principal
tk.Label(root, text="Cadastro de Pessoas", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=4, pady=10)

# Formulário
tk.Label(root, text="Nome").grid(row=1, column=0, padx=5, pady=5)
entry_nome = tk.Entry(root)
entry_nome.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Idade").grid(row=2, column=0, padx=5, pady=5)
entry_idade = tk.Entry(root)
entry_idade.grid(row=2, column=1, padx=5, pady=5)

# Botões
tk.Button(root, text="Inserir", command=inserir_pessoa).grid(row=3, column=0, padx=5, pady=5)
tk.Button(root, text="Atualizar", command=atualizar_pessoa).grid(row=3, column=1, padx=5, pady=5)
tk.Button(root, text="Deletar", command=deletar_pessoa).grid(row=3, column=2, padx=5, pady=5)
tk.Button(root, text="Listar", command=listar_pessoas).grid(row=3, column=3, padx=5, pady=5)

# Listbox
listbox = tk.Listbox(root, width=50)
listbox.grid(row=4, column=0, columnspan=4, padx=5, pady=10)
listbox.bind("<<ListboxSelect>>", selecionar_pessoa)

listar_pessoas()
root.mainloop()