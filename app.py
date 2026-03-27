import gspread
from google.oauth2.service_account import Credentials
import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime

# ========================
# CONFIG GOOGLE
# ========================

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file("projeto-escala.json", scopes=scope)
client = gspread.authorize(creds)

planilha = client.open_by_key("1cvGJ2WLMaJNIXdmPbHkHfRIzE3Ph2DbBJs4otGtqn5E")

aba_dados = planilha.worksheet("Banco de Dados")
aba_ferias = planilha.worksheet("Férias")

# ========================
# CACHE GLOBAL
# ========================

cache_nomes_ferias = {}
cache_linhas_ferias = {}

def carregar_cache_ferias():
    global cache_nomes_ferias, cache_linhas_ferias

    dados = aba_ferias.get_all_values()

    cache_nomes_ferias = {}
    cache_linhas_ferias = {}

    for i, linha in enumerate(dados[1:], start=2):
        nome = linha[0].strip().lower()
        cache_nomes_ferias[nome] = linha[1:]
        cache_linhas_ferias[nome] = i

carregar_cache_ferias()

# ========================
# CORES
# ========================

bg = "#0f2a36"
fg = "#e6f2f5"
highlight = "#2a8fb8"
btn_dia_cor = "#173d4f"
verde = "#2ecc71"

# ========================
# AUXILIARES
# ========================

def buscar_linha(nome, aba):
    nomes_lista = aba.col_values(1)
    for i, nome_planilha in enumerate(nomes_lista):
        if nome_planilha.strip().lower() == nome.strip().lower():
            return i + 1
    return None

def filtrar_nomes(event, combo, lista_original):
    texto = combo.get().lower()
    filtrados = [n for n in lista_original if texto in n.lower()]
    combo['values'] = filtrados

nomes = aba_dados.col_values(1)[1:]

# ========================
# MÓDULO 1
# ========================

def safe_date(valor):
    try:
        return datetime.strptime(valor, "%d/%m/%Y")
    except:
        return datetime.now()

def carregar_dados(event=None):
    nome = combo_nome.get()
    linha = buscar_linha(nome, aba_dados)

    if not linha:
        return

    dados = aba_dados.row_values(linha)

    entry_final_semana.set_date(safe_date(dados[1] if len(dados) > 1 else ""))
    entry_noturno.set_date(safe_date(dados[2] if len(dados) > 2 else ""))
    entry_recesso.set_date(safe_date(dados[3] if len(dados) > 3 else ""))
    entry_apoio.set_date(safe_date(dados[4] if len(dados) > 4 else ""))

    label_nome.config(text=f"Editando: {nome}")

def atualizar_nome(nome, final_semana, noturno, recesso, apoio):
    linha = buscar_linha(nome, aba_dados)

    if not linha:
        messagebox.showerror("Erro", "Nome não encontrado")
        return

    aba_dados.update(f"B{linha}:E{linha}", [[final_semana, noturno, recesso, apoio]])
    messagebox.showinfo("Sucesso", "Atualizado!")

# ========================
# MÓDULO 2
# ========================

botoes_dias = []
estado_dias = []

def carregar_ferias(event=None):
    nome = combo_nome_ferias.get().strip().lower()

    if nome not in cache_nomes_ferias:
        return

    valores = cache_nomes_ferias[nome]

    for i in range(len(botoes_dias)):
        valor = valores[i] if i < len(valores) else "FALSE"
        estado_dias[i] = (valor == "TRUE")
        botoes_dias[i].config(bg=verde if estado_dias[i] else btn_dia_cor)

def toggle_dia(i):
    estado_dias[i] = not estado_dias[i]
    botoes_dias[i].config(bg=verde if estado_dias[i] else btn_dia_cor)

def salvar_ferias():
    nome = combo_nome_ferias.get().strip().lower()

    if nome not in cache_linhas_ferias:
        return

    linha = cache_linhas_ferias[nome]

    aba_ferias.update(f"B{linha}:AL{linha}", [[bool(v) for v in estado_dias]])

    carregar_cache_ferias()
    messagebox.showinfo("Sucesso", "Férias atualizadas!")

def limpar_ferias_nome():
    nome = combo_nome_ferias.get().strip().lower()

    if nome not in cache_linhas_ferias:
        return

    linha = cache_linhas_ferias[nome]

    vazio = [False] * 31
    aba_ferias.update(f"B{linha}:AL{linha}", [vazio])

    carregar_cache_ferias()
    carregar_ferias()

    messagebox.showinfo("Sucesso", "Férias do nome limpas!")

def limpar_todas_ferias():
    confirm = messagebox.askyesno("Confirmação", "Deseja apagar TODAS as férias?")
    if not confirm:
        return

    dados = aba_ferias.get_all_values()

    for i in range(2, len(dados)+1):
        vazio = [False] * 31
        aba_ferias.update(f"B{i}:AL{i}", [vazio])

    carregar_cache_ferias()
    messagebox.showinfo("Sucesso", "Todas as férias foram apagadas!")

# ========================
# INTERFACE
# ========================

janela = tk.Tk()
janela.title("Sistema de Escala")
janela.geometry("700x600")
janela.configure(bg=bg)

notebook = ttk.Notebook(janela)
notebook.pack(expand=True, fill="both")

# ===== MÓDULO 1 =====
frame_plantao = tk.Frame(notebook, bg=bg)
notebook.add(frame_plantao, text="Plantões")

label_nome = tk.Label(frame_plantao, text="Selecione um nome", bg=bg, fg=fg)
label_nome.pack(pady=5)

frame_busca1 = tk.Frame(frame_plantao, bg=bg)
frame_busca1.pack(pady=15)

combo_nome = ttk.Combobox(frame_busca1, values=nomes)
combo_nome.pack(ipadx=10, ipady=3)

combo_nome.set("Digite ou selecione um nome")
combo_nome.bind("<KeyRelease>", lambda e: filtrar_nomes(e, combo_nome, nomes))
combo_nome.bind("<<ComboboxSelected>>", carregar_dados)

frame_campos = tk.Frame(frame_plantao, bg=bg)
frame_campos.pack(pady=10)

tk.Label(frame_campos, text="Final de Semana", bg=bg, fg=fg).grid(row=0, column=0, padx=5, pady=5)
entry_final_semana = DateEntry(frame_campos)
entry_final_semana.grid(row=0, column=1)

tk.Label(frame_campos, text="Noturno", bg=bg, fg=fg).grid(row=1, column=0, padx=5, pady=5)
entry_noturno = DateEntry(frame_campos)
entry_noturno.grid(row=1, column=1)

tk.Label(frame_campos, text="Recesso", bg=bg, fg=fg).grid(row=2, column=0, padx=5, pady=5)
entry_recesso = DateEntry(frame_campos)
entry_recesso.grid(row=2, column=1)

tk.Label(frame_campos, text="Apoio", bg=bg, fg=fg).grid(row=3, column=0, padx=5, pady=5)
entry_apoio = DateEntry(frame_campos)
entry_apoio.grid(row=3, column=1)

tk.Button(frame_plantao, text="Atualizar",
          bg=highlight, fg="white",
          command=lambda: atualizar_nome(
              combo_nome.get(),
              entry_final_semana.get(),
              entry_noturno.get(),
              entry_recesso.get(),
              entry_apoio.get()
          )).pack(pady=10)

# ===== MÓDULO 2 =====
frame_ferias = tk.Frame(notebook, bg=bg)
notebook.add(frame_ferias, text="Férias")

frame_busca2 = tk.Frame(frame_ferias, bg=bg)
frame_busca2.pack(pady=15)

combo_nome_ferias = ttk.Combobox(frame_busca2, values=nomes)
combo_nome_ferias.pack(ipadx=10, ipady=3)

combo_nome_ferias.set("Digite ou selecione um nome")
combo_nome_ferias.bind("<KeyRelease>", lambda e: filtrar_nomes(e, combo_nome_ferias, nomes))
combo_nome_ferias.bind("<<ComboboxSelected>>", carregar_ferias)

frame_dias = tk.Frame(frame_ferias, bg=bg)
frame_dias.pack()

for i in range(31):
    estado_dias.append(False)

    btn = tk.Button(frame_dias, text=str(i+1), width=4,
                    command=lambda i=i: toggle_dia(i))
    btn.grid(row=i//7, column=i%7)
    botoes_dias.append(btn)

tk.Button(frame_ferias, text="Salvar",
          bg=highlight, fg="white",
          command=salvar_ferias).pack(pady=5)

tk.Button(frame_ferias, text="Limpar Férias do Nome",
          bg=highlight, fg="white",
          command=limpar_ferias_nome).pack(pady=5)

tk.Button(frame_ferias, text="Limpar TODAS as Férias",
          bg="#c0392b", fg="white",
          command=limpar_todas_ferias).pack(pady=5)

janela.mainloop()