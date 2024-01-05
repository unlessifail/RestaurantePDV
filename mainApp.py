import customtkinter as ctk
import tkinter as tk
import sqlite3
from tkinter import StringVar
from tkinter import messagebox
from PIL import Image, ImageTk
from pathlib import Path
import random
import string
import warnings

conexao = sqlite3.connect("cardapio.db")
cursor = conexao.cursor()
warnings.filterwarnings("ignore", category=UserWarning, module="customtkinter")

mainApp = ctk.CTk()
mainApp.title('Restaurante | ')
mainApp.geometry('1440x870')
mainApp.after(0, lambda:mainApp.state('zoomed'))
# mainApp.attributes('-alpha', 0.9)

pesquisa_prato_var = StringVar(mainApp)
prato_selecionado_bg_frame = None
icone_label = None
bottom_fix_bar_frame = None
nome_do_prato_pesquisadoLabel = None
categoria_do_prato_pesquisadoLabel = None
desc_do_prato_pesquisadoLabel = None
preco_do_prato_pesquisadoLabel = None
serve_prato_pesquisadoLabel = None
disponibilidade_do_prato_pesquisadoLabel = None
qtd_item_prato_selecionado_label = None
num_pedido_sel_frame_label = None
subtotal_pedido_frame_label = None
qtd_prato_selecionado_optMenu = None
add_prato_selecionado_button = None
del_prato_selecionado_button = None
btn_avancar = None
carrinho = None

# Funcs

def gerar_id_pedido():
    # Gera uma string aleatória de 7 caracteres
    caracteres_aleatorios = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
    
    # Constrói o ID de pedido com o formato desejado
    id_pedido = f"#{random.randint(1000, 9999)}p{caracteres_aleatorios}"
    
    return id_pedido

class Carrinho:
    
    def __init__(self, id_pedido):
        self.id_pedido = id_pedido
        self.itens = []  # Lista de itens no carrinho

    def adicionar_item(self, item):
        """
        Adiciona um item ao carrinho.
        """
        self.itens.append(item)
        # Lógica adicional para adicionar item ao carrinho, se necessário

    def remover_item(self, item):
        """
        Remove um item do carrinho.
        """
        if item in self.itens:
            self.itens.remove(item)
        # Lógica adicional para remover item do carrinho, se necessário

    def alterar_quantidade(self, item, nova_quantidade):
        """
        Altera a quantidade de um item no carrinho.
        """
        for i, carrinho_item in enumerate(self.itens):
            if carrinho_item == item:
                self.itens[i].quantidade = nova_quantidade
        # Lógica adicional para alterar a quantidade de um item no carrinho, se necessário

    def calcular_total(self):
        """
        Calcula o total do carrinho com base nos itens e suas quantidades.
        """
        total = 0.0
        for item in self.itens:
            total += item.preco * item.quantidade
        return total

def limpar_detalhes_prato():
    # Limpe os detalhes do prato exibidos na interface gráfica
    nome_do_prato_pesquisadoLabel.configure(text="Nome do Prato: ")
    desc_do_prato_pesquisadoLabel.configure(text="Descrição: ")
    categoria_do_prato_pesquisadoLabel.configure(text="Categoria: ")
    disponibilidade_do_prato_pesquisadoLabel.configure(text="Disponível: ")
    preco_do_prato_pesquisadoLabel.configure(text="Preço: ")
    serve_prato_pesquisadoLabel.configure(text="Serve: ")
    icone_label.configure(image=None)

def buscar_prato_selecionado():
    prato_selecionado = pesquisa_prato_optMenu.get()

    if not prato_selecionado:
        messagebox.showerror("Erro", "Selecione um prato antes de exibir detalhes")
        return

    cursor.execute("SELECT * FROM cardapio WHERE nome_prato=?", (prato_selecionado,))
    prato = cursor.fetchone()

    if not prato:
        messagebox.showerror("Erro", "Prato não encontrado no banco de dados")
        return

    nome_do_prato_pesquisadoLabel.configure(text=f"Nome do Prato: {prato[1]}")
    desc_do_prato_pesquisadoLabel.configure(text=f"Descrição: {prato[2]}")
    categoria_do_prato_pesquisadoLabel.configure(text=f"Categoria: {prato[3]}")
    disponibilidade_do_prato_pesquisadoLabel.configure(text=f"Disponível: {prato[5]}")
    preco_do_prato_pesquisadoLabel.configure(text=f"Preço: {prato[4]}")
    serve_prato_pesquisadoLabel.configure(text=f"Serve: {prato[6]}")

    nome_prato = prato[1].replace(" ", "_").lower()
    caminho_imagem = Path("pratos_icons") / f"{nome_prato}.png"

    try:
        imagem = Image.open(caminho_imagem)
        imagem = imagem.resize((150, 150), Image.LANCZOS)
        imagem_prato = ImageTk.PhotoImage(imagem)
        icone_label.configure(image=imagem_prato)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar a imagem: {e}")

def adicionar_item_no_carrinho():
    prato_selecionado = pesquisa_prato_optMenu.get()

    if not prato_selecionado:
        messagebox.showerror("Erro", "Selecione um prato antes de adicionar ao carrinho")
        return

    cursor.execute("SELECT * FROM cardapio WHERE nome_prato=?", (prato_selecionado,))
    prato = cursor.fetchone()

    if not prato:
        messagebox.showerror("Erro", "Prato não encontrado no banco de dados")
        return

    # Supondo que você já tenha criado a instância da classe Carrinho
    id_pedido = gerar_id_pedido()
    carrinho = Carrinho(id_pedido)

    carrinho.adicionar_item(prato)
    texto_item_adicionado = nome_do_prato_pesquisadoLabel.cget('text')
    texto_qtd_item_adicionado = qtd_prato_selecionado_optMenu.cget('text')
    messagebox.showinfo("Sucesso", f"{texto_qtd_item_adicionado} {texto_item_adicionado} adicionado ao carrinho")


# Frames

bgFrame = ctk.CTkFrame(mainApp,
                       width=1440,
                       height=870,
                       corner_radius=0,
                       fg_color="#181A18",
                       bg_color="#181A18",
                       )
bgFrame.place(x=0,y=0)

top_toolbar_frame = ctk.CTkFrame(mainApp,
                       width=1440,
                       height=35,
                       corner_radius=0,
                       fg_color="#505050",
                       bg_color="#181A18",
                       )
top_toolbar_frame.place(x=0,y=0)

# ToolbarLabel

restaurante_top_label = ctk.CTkLabel(mainApp,
                                     text='Restaurante',
                                     text_color="#33840D",
                                     font=('Pacifico', 23),
                                     bg_color="#505050",
                                     )
restaurante_top_label.place(x=705,y=-11)

status_loja_label = ctk.CTkLabel(mainApp,
                                 text='Status: Fechado',
                                     text_color="#A01111",
                                     font=('Pacifico', 20),
                                     bg_color="#505050",
                                     )
status_loja_label.place(x=981,y=-5)

# Func Toolbar OptionMenu

def obter_nomes_pratos():
    cursor.execute("SELECT nome_prato FROM cardapio")
    nomes_pratos = [row[0] for row in cursor.fetchall()]
    return nomes_pratos

nomes_pratos = obter_nomes_pratos()

# Toolbar OptionMenu

pesquisa_prato_optMenu = ctk.CTkOptionMenu(mainApp,
                                           width=439,
                                           height=24,
                                           fg_color="#808080",
                                           bg_color="#505050",
                                           button_color="#505050",
                                           button_hover_color="#505050",
                                           dropdown_hover_color="#33840D",
                                           corner_radius=50,
                                           dropdown_fg_color="#505050",
                                           dropdown_text_color="#000000",
                                           values= nomes_pratos,
                                           state='enabled'
                                           )
pesquisa_prato_optMenu.place(x=155, y=5)

def fechar_pedido():
    prato_selecionado_bg_frame.destroy()
    icone_label.destroy()
    bottom_fix_bar_frame.destroy()
    nome_do_prato_pesquisadoLabel.destroy()
    categoria_do_prato_pesquisadoLabel.destroy()
    desc_do_prato_pesquisadoLabel.destroy()
    preco_do_prato_pesquisadoLabel.destroy()
    serve_prato_pesquisadoLabel.destroy()
    disponibilidade_do_prato_pesquisadoLabel.destroy()
    qtd_item_prato_selecionado_label.destroy()
    num_pedido_sel_frame_label.destroy()
    subtotal_pedido_frame_label.destroy()
    qtd_prato_selecionado_optMenu.destroy()
    add_prato_selecionado_button.destroy()
    del_prato_selecionado_button.destroy()
    btn_avancar.destroy()
    btn_cancelar_pedido.destroy()

def iniciar_novo_pedido():
    global prato_selecionado_bg_frame, icone_label, bottom_fix_bar_frame
    global nome_do_prato_pesquisadoLabel, categoria_do_prato_pesquisadoLabel, desc_do_prato_pesquisadoLabel
    global preco_do_prato_pesquisadoLabel, serve_prato_pesquisadoLabel, disponibilidade_do_prato_pesquisadoLabel
    global qtd_item_prato_selecionado_label, num_pedido_sel_frame_label, subtotal_pedido_frame_label
    global qtd_prato_selecionado_optMenu, add_prato_selecionado_button, del_prato_selecionado_button, btn_avancar, btn_cancelar_pedido
    global carrinho, texto_item_adicionado, texto_qtd_item_adicionado

    id_pedido = gerar_id_pedido()
    carrinho = Carrinho(id_pedido)

    # Remova os elementos antigos se existirem
    if prato_selecionado_bg_frame:
        prato_selecionado_bg_frame.destroy()

    if icone_label:
        icone_label.destroy()

    if bottom_fix_bar_frame:
        bottom_fix_bar_frame.destroy()

    if nome_do_prato_pesquisadoLabel:
        nome_do_prato_pesquisadoLabel.destroy()

    if categoria_do_prato_pesquisadoLabel:
        categoria_do_prato_pesquisadoLabel.destroy()

    if desc_do_prato_pesquisadoLabel:
        desc_do_prato_pesquisadoLabel.destroy()

    if preco_do_prato_pesquisadoLabel:
        preco_do_prato_pesquisadoLabel.destroy()

    if serve_prato_pesquisadoLabel:
        serve_prato_pesquisadoLabel.destroy()

    if disponibilidade_do_prato_pesquisadoLabel:
        disponibilidade_do_prato_pesquisadoLabel.destroy()

    if qtd_item_prato_selecionado_label:
        qtd_item_prato_selecionado_label.destroy()

    if num_pedido_sel_frame_label:
        num_pedido_sel_frame_label.destroy()

    if subtotal_pedido_frame_label:
        subtotal_pedido_frame_label.destroy()

    if qtd_prato_selecionado_optMenu:
        qtd_prato_selecionado_optMenu.destroy()

    if add_prato_selecionado_button:
        add_prato_selecionado_button.destroy()

    if del_prato_selecionado_button:
        del_prato_selecionado_button.destroy()

    if btn_avancar:
        btn_avancar.destroy()

    # Frames Prato Selecionado
    prato_selecionado_bg_frame = ctk.CTkFrame(mainApp,
                                              width=968,
                                              height=230,
                                              fg_color="#808080",
                                              bg_color="#181A18",
                                              corner_radius=0,
                                              border_width=0,
                                              )
    prato_selecionado_bg_frame.place(x=0, y=35)

    icone_label = ctk.CTkLabel(mainApp,
                               width=150,
                               height=150,
                               fg_color="#505050",
                               bg_color="#808080",
                               corner_radius=0,
                               image=None,
                               text=None,
                               )
    icone_label.place(x=5, y=40)

    bottom_fix_bar_frame = ctk.CTkFrame(mainApp,
                                        width=241,
                                        height=59,
                                        fg_color="#303030",
                                        bg_color="#808080",
                                        corner_radius=0,
                                        border_width=1,
                                        border_color="#33840D",
                                        )
    bottom_fix_bar_frame.place(x=366, y=203)

    # Prato Selecionado Label
    nome_do_prato_pesquisadoLabel = ctk.CTkLabel(mainApp,
                                                 text='Nome do Prato: ',
                                                 text_color="#D9FFC8",
                                                 bg_color="#808080",
                                                 font=("Pacifico", 20),
                                                 )
    nome_do_prato_pesquisadoLabel.place(x=160, y=40)

    categoria_do_prato_pesquisadoLabel = ctk.CTkLabel(mainApp,
                                                      text='Categoria: ',
                                                      text_color="#D9FFC8",
                                                      bg_color="#808080",
                                                      font=("Pacifico", 20),
                                                      )
    categoria_do_prato_pesquisadoLabel.place(x=160, y=75)

    desc_do_prato_pesquisadoLabel = ctk.CTkLabel(mainApp,
                                                  text='Descrição: ',
                                                  text_color="#D9FFC8",
                                                  bg_color="#808080",
                                                  font=("Pacifico", 15),
                                                  )
    desc_do_prato_pesquisadoLabel.place(x=160, y=115)

    preco_do_prato_pesquisadoLabel = ctk.CTkLabel(mainApp,
                                                   text='Preço: ',
                                                   text_color="#D9FFC8",
                                                   bg_color="#808080",
                                                   font=("Pacifico", 15),
                                                   )
    preco_do_prato_pesquisadoLabel.place(x=160, y=236)

    serve_prato_pesquisadoLabel = ctk.CTkLabel(mainApp,
                                                text='Serve: ',
                                                text_color="#D9FFC8",
                                                bg_color="#808080",
                                                font=("Pacifico", 15),
                                                )
    serve_prato_pesquisadoLabel.place(x=160, y=187)

    disponibilidade_do_prato_pesquisadoLabel = ctk.CTkLabel(mainApp,
                                                            text='Disponível: ',
                                                            text_color="#D9FFC8",
                                                            bg_color="#808080",
                                                            font=("Pacifico", 15),
                                                            )
    disponibilidade_do_prato_pesquisadoLabel.place(x=160, y=211)

    qtd_item_prato_selecionado_label = ctk.CTkLabel(mainApp,
                                                     text='Quantidade: ',
                                                     text_color="#B5B5B5",
                                                     bg_color="#303030",
                                                     font=("Square", 12),
                                                     )
    qtd_item_prato_selecionado_label.place(x=388, y=215)

    num_pedido_sel_frame_label = ctk.CTkLabel(mainApp,
                                              text='PEDIDO #00000',
                                              text_color="#FFFFFF",
                                              bg_color="#303030",
                                              font=("Square", 12),
                                              )
    num_pedido_sel_frame_label.place(x=482, y=210)

    subtotal_pedido_frame_label = ctk.CTkLabel(mainApp,
                                               text='Subtotal: ',
                                               text_color="#FFFFFF",
                                               bg_color="#303030",
                                               font=("Square", 12),
                                               )
    subtotal_pedido_frame_label.place(x=482, y=230)

    # OptionMenu qtd de itens no pedido
    qtd_prato_selecionado_optMenu = ctk.CTkOptionMenu(mainApp,
                                                       width=67,
                                                       height=18,
                                                       text_color="#FFFFFF",
                                                       dropdown_text_color="#FFFFFF",
                                                       dropdown_hover_color="#1C1C1C",
                                                       button_hover_color="#40AF0B",
                                                       button_color="#33840D",
                                                       fg_color="#A2A2A2",
                                                       bg_color="#303030",
                                                       values=['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10'],
                                                       )
    qtd_prato_selecionado_optMenu.place(x=388, y=235)

    # prato selecionado btns
    add_prato_selecionado_button = ctk.CTkButton(mainApp,
                                                text='ADICIONAR',
                                                text_color="#D9FFC8",
                                                font=('Russian', 15),
                                                width=150,
                                                height=15,
                                                fg_color="#545454",
                                                bg_color="#505050",
                                                border_width=1,
                                                border_color="#33840D",
                                                hover_color="#454545",
                                                corner_radius=0,
                                                command=adicionar_item_no_carrinho,
                                                )
    add_prato_selecionado_button.place(x=5, y=201)

# Func add item no carrinho
    
    del_prato_selecionado_button = ctk.CTkButton(mainApp,
                                                  text='REMOVER',
                                                  text_color="#D9FFC8",
                                                  font=('Russian', 15),
                                                  border_width=1,
                                                  border_color="#33840D",
                                                  width=150,
                                                  height=15,
                                                  fg_color="#545454",
                                                  bg_color="#505050",
                                                  hover_color="#454545",
                                                  corner_radius=0,
                                                  )
    del_prato_selecionado_button.place(x=5, y=231)

    btn_avancar = ctk.CTkButton(mainApp,
                                width=150,
                                height=40,
                                text='AVANÇAR',
                                text_color="#3FA011",
                                fg_color="#303030",
                                bg_color="#303030",
                                border_color="#3FA011",
                                border_width=1,
                                corner_radius=0,
                                hover_color='#70D142',
                                )
    btn_avancar.place(x=612, y=213)

    btn_cancelar_pedido = ctk.CTkButton(mainApp,
                                    width=150,
                                    height=40,
                                    text='CANCELAR PEDIDO',
                                    text_color="#3FA011",
                                    fg_color="#303030",
                                    bg_color="#303030",
                                    border_color="#3FA011",
                                    border_width=1,
                                    corner_radius=0,
                                    hover_color='#70D142',
                                    command=fechar_pedido,
                                    )
    btn_cancelar_pedido.place(x=784, y=213)

# Toolbar BTNs

btn_buscar_prato = ctk.CTkButton(mainApp,
                                        text='IR',
                                        font=('Russian', 15),
                                        width=50,
                                        height=25,
                                        fg_color="#505050",
                                        bg_color="#505050",
                                        border_color="#33840D",
                                        hover_color="#33840D",
                                        border_width=1,
                                        text_color="#EDEDED",
                                        corner_radius=0,
                                        command=buscar_prato_selecionado,
                                        )

btn_buscar_prato.place(x=497,y=5)

limpar_prato_selecionado = ctk.CTkButton(mainApp,
                                        text='Limpar',
                                        font=('Russian', 15),
                                        width=50,
                                        height=25,
                                        fg_color="#505050",
                                        bg_color="#505050",
                                        border_color="#33840D",
                                        hover_color="#A01111",
                                        border_width=1,
                                        text_color="#EDEDED",
                                        corner_radius=0,
                                        command=limpar_detalhes_prato,
                                        )

limpar_prato_selecionado.place(x=547,y=5)

btn_novo_pedido = ctk.CTkButton(mainApp,
                                        text='NOVO PEDIDO',
                                        font=('Russian', 15),
                                        width=145,
                                        height=25,
                                        fg_color="#505050",
                                        bg_color="#505050",
                                        border_color="#33840D",
                                        hover_color="#33840D",
                                        border_width=1,
                                        text_color="#EDEDED",
                                        corner_radius=0,
                                        command=iniciar_novo_pedido,
                                        )
btn_novo_pedido.place(x=5,y=5)

mainApp.mainloop()