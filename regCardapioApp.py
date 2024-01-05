import customtkinter as ctk
import tkinter as tk
import sqlite3
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import filedialog
from pathlib import Path
import warnings

conexao = sqlite3.connect("cardapio.db")
cursor = conexao.cursor()
warnings.filterwarnings("ignore", category=UserWarning, module="customtkinter")
appCardapio = ctk.CTk()

appCardapio.title('Restaurante | Registro de Pratos')
appCardapio.resizable(False,False)
appCardapio.geometry('1440x870')
appCardapio.after(0, lambda:appCardapio.state('zoomed'))

nomes_campos = [
    'nome_prato', 'descricao_prato', 'categoria_prato', 'disponibilidade_prato',
    'preco_prato', 'serve_prato', 'caminhoImagem'
]

selCampo = None

# Funcs

def editar_prato_selecionado():
    prato_selecionado = buscar_prato_menuOption.get()

    if not prato_selecionado:
        messagebox.showerror("Erro", "Selecione um prato antes de editar")
        return

    cursor.execute("SELECT * FROM cardapio WHERE nome_prato=?", (prato_selecionado,))
    prato = cursor.fetchone()

    if not prato:
        messagebox.showerror("Erro", "Prato não encontrado no banco de dados")
        return

    # Obter o novo valor do campo selecionado
    campo_selecionado = selCampo.get()
    novo_valor = novoValorEntry.get()

    # Verificar se o novo valor está vazio
    if not novo_valor:
        messagebox.showerror("Erro", "Informe um novo valor antes de editar")
        return

    try:
        # Atualizar o valor do campo no banco de dados
        cursor.execute(f"UPDATE cardapio SET {campo_selecionado.lower()}=? WHERE nome_prato=?",
                       (novo_valor, prato_selecionado))
        conexao.commit()

        messagebox.showinfo("Sucesso", f"{campo_selecionado} do prato '{prato_selecionado}' atualizado com sucesso!")

        # Atualizar a lista de nomes de pratos no OptionMenu
        global nomes_pratos
        nomes_pratos = obter_nomes_pratos()
        buscar_prato_menuOption.set_values(nomes_pratos)

        # Limpar os detalhes exibidos após a edição
        limpar_detalhes_prato()

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao editar o prato: {e}")

def atualizar_option_menu():
    global selCampo

    # Obtém o valor atual selecionado no OptionMenu (se houver)
    valor_selecionado = selCampo.get()

    # Destroi o OptionMenu existente
    if selCampo:
        selCampo.destroy()

    # Cria um novo OptionMenu com os valores atualizados
    selCampo = ctk.CTkOptionMenu(appCardapio,
                                 width=232,
                                 height=40,
                                 corner_radius=15,
                                 bg_color="#555555",
                                 fg_color="#D9D9D9",
                                 font=("Square", 20),
                                 text_color="#1C1C1C",
                                 button_color="#1C1C1C",
                                 button_hover_color="#0C0C0C",
                                 values=nomes_campos,
                                 )
    selCampo.place(x=970, y=633)

    # Define novamente o valor selecionado (se estiver disponível)
    if valor_selecionado:
        selCampo.set(valor_selecionado)

    # Reagende a função após 20 segundos
    appCardapio.after(20000, atualizar_option_menu)

def excluir_prato_selecionado():
    prato_selecionado = buscar_prato_menuOption.get()

    if not prato_selecionado:
        messagebox.showerror("Erro", "Selecione um prato antes de excluir")
        return

    confirmacao = messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o prato '{prato_selecionado}'?")

    if confirmacao:
        try:
            cursor.execute("DELETE FROM cardapio WHERE nome_prato=?", (prato_selecionado,))
            conexao.commit()
            messagebox.showinfo("Sucesso", "Prato excluído com sucesso!")

            # Limpe os detalhes exibidos após a exclusão
            limpar_detalhes_prato()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir o prato: {e}")

def limpar_detalhes_prato():
    # Limpe os detalhes do prato exibidos na interface gráfica
    nome_do_prato_pesquisadoLabel.configure(text="Nome do Prato: ")
    desc_do_prato_pesquisadoLabel.configure(text="Descrição: ")
    categoria_do_prato_pesquisadoLabel.configure(text="Categoria: ")
    disponibilidade_do_prato_pesquisadoLabel.configure(text="Disponibilidade: ")
    preco_do_prato_pesquisadoLabel.configure(text="Preço: ")
    serve_prato_pesquisadoLabel.configure(text="Serve: ")

def cadastrar_prato():
    # Obter os valores dos campos
    nome_prato = nome_do_pratoEntry.get()
    descricao_prato = desc_do_pratoEntry.get()
    categoria_prato = categoria_do_pratoMenuOption.get()
    disponibilidade_prato = disponibilidade_do_pratoMenuOption.get()
    preco_prato = preco_do_pratoEntry.get()
    serve_prato = serve_pratoMenuOption.get()

    # Verificar se todos os campos estão preenchidos
    if not nome_prato or not descricao_prato or not categoria_prato or not disponibilidade_prato or not preco_prato or not serve_prato:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")
        return

    try:

        cursor.execute("INSERT INTO cardapio (nome_prato, descricao_prato, categoria_prato, disponibilidade_prato, preco_prato, serve_prato) VALUES (?, ?, ?, ?, ?, ?)",
                       (nome_prato, descricao_prato, categoria_prato, disponibilidade_prato, preco_prato, serve_prato))
        conexao.commit()
        messagebox.showinfo("Sucesso", "Prato cadastrado com sucesso!")

        nome_do_pratoEntry.delete(0, 'end')
        desc_do_pratoEntry.delete(0, 'end')
        preco_do_pratoEntry.delete(0, 'end')

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao cadastrar o prato: {e}")

def carregar_imagem():
    file_path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.gif")])

    if not file_path:
        messagebox.showerror("Erro", "Nenhuma imagem selecionada")
        return

    try:
        imagem = Image.open(file_path)

        imagem = imagem.resize((150, 150), Image.LANCZOS)

        nome_prato = nome_do_pratoEntry.get().replace(" ", "_").lower()
        caminho_salvar = Path("pratos_icons") / f"{nome_prato}.png"

        imagem.save(caminho_salvar)
        btnEnviar.configure(state='Normal')

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar a imagem: {e}")

def obter_nomes_pratos():
    cursor.execute("SELECT nome_prato FROM cardapio")
    nomes_pratos = [row[0] for row in cursor.fetchall()]
    return nomes_pratos

nomes_pratos = obter_nomes_pratos()

def buscar_prato_selecionado():
    prato_selecionado = buscar_prato_menuOption.get()
    
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
    disponibilidade_do_prato_pesquisadoLabel.configure(text=f"Disponibilidade: {prato[5]}")
    preco_do_prato_pesquisadoLabel.configure(text=f"Preço: {prato[4]}")
    serve_prato_pesquisadoLabel.configure(text=f"Serve: {prato[6]}")

    nome_prato = prato[1].replace(" ", "_").lower()
    caminho_imagem = Path("pratos_icons") / f"{nome_prato}.png"

    try:
        imagem = Image.open(caminho_imagem)
        imagem = imagem.resize((150, 150), Image.LANCZOS)
        imagem_prato = ImageTk.PhotoImage(imagem)
        icone_label.configure(image=imagem_prato)
        icone_label.image = imagem_prato

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar a imagem: {e}")

# Frames

bgFrame = ctk.CTkFrame(appCardapio,
                       width=1440,
                       height=870,
                       corner_radius=0,
                       fg_color="#555555",
                       bg_color="#555555",
                       ).place(x=0,y=0)

headerLineFrame = ctk.CTkFrame(appCardapio,
                       width=1400,
                       height=5,
                       corner_radius=100,
                       fg_color="#FFFFFF",
                       bg_color="#555555",
                       ).place(x=20,y=129)

nome_do_prato_lineFrame = ctk.CTkFrame(appCardapio,
                       width=700,
                       height=2,
                       corner_radius=100,
                       fg_color="#FFFFFF",
                       bg_color="#555555",
                       ).place(x=20,y=191)

desc_do_prato_lineFrame = ctk.CTkFrame(appCardapio,
                       width=700,
                       height=2,
                       corner_radius=100,
                       fg_color="#FFFFFF",
                       bg_color="#555555",
                       ).place(x=20,y=287)

categoria_do_pratolineFrame = ctk.CTkFrame(appCardapio,
                       width=700,
                       height=2,
                       corner_radius=100,
                       fg_color="#FFFFFF",
                       bg_color="#555555",
                       ).place(x=20,y=386)

preco_do_pratolineFrame = ctk.CTkFrame(appCardapio,
                       width=700,
                       height=2,
                       corner_radius=100,
                       fg_color="#FFFFFF",
                       bg_color="#555555",
                       )
preco_do_pratolineFrame.place(x=20,y=485)

# Labels

headerLabel = ctk.CTkLabel(appCardapio,
                    text="Restaurante | Registro de Pratos",
                    font=("Pacifico", 50),
                    text_color="#FFFFFF",
                    bg_color="#555555",
                    ).place(x=20,y=25)

nome_do_prato_entry_label = ctk.CTkLabel(appCardapio,
                    text="Nome do Prato:",
                    font=("Modern M", 20),
                    text_color="#FFFFFF",
                    bg_color="#555555",
                    ).place(x=20,y=147)

desc_do_prato_entry_label = ctk.CTkLabel(appCardapio,
                    text="Descrição:",
                    font=("Modern M", 20),
                    text_color="#FFFFFF",
                    bg_color="#555555",
                    ).place(x=20,y=243)

categoria_do_prato_entry_label = ctk.CTkLabel(appCardapio,
                    text="Categoria:",
                    font=("Modern M", 20),
                    text_color="#FFFFFF",
                    bg_color="#555555",
                    ).place(x=20,y=342)

disponibilidade_do_prato_entry_label = ctk.CTkLabel(appCardapio,
                    text="Disponibilidade:",
                    font=("Modern M", 20),
                    text_color="#FFFFFF",
                    bg_color="#555555",
                    ).place(x=370,y=342)

preco_do_prato_entry_label = ctk.CTkLabel(appCardapio,
                    text="Preço:",
                    font=("Modern M", 20),
                    text_color="#FFFFFF",
                    bg_color="#555555",
                    ).place(x=20,y=441)

serve_prato_entry_label = ctk.CTkLabel(appCardapio,
                    text="Serve:",
                    font=("Modern M", 20),
                    text_color="#FFFFFF",
                    bg_color="#555555",
                    ).place(x=370,y=441)

rightHeaderLabel = ctk.CTkLabel(appCardapio,
                    text="Buscar Pratos",
                    font=("Pacifico", 25),
                    text_color="#FFFFFF",
                    bg_color="#555555",
                    ).place(x=759,y=144)

nome_do_prato_pesquisadoLabel = ctk.CTkLabel(appCardapio,
                    text="Nome do Prato: ",
                    font=("Modern M", 25),
                    text_color="#FFFFFF",
                    bg_color="#555555",
                    )
nome_do_prato_pesquisadoLabel.place(x=759, y=260)

desc_do_prato_pesquisadoLabel = ctk.CTkLabel(appCardapio,
                    text="Descrição:\n ",
                    font=("Modern M", 20),
                    text_color="#FFFFFF",
                    bg_color="#555555",
                    )
desc_do_prato_pesquisadoLabel.place(x=759, y=313)

categoria_do_prato_pesquisadoLabel = ctk.CTkLabel(appCardapio,
                    text="Categoria: ",
                    font=("Modern M", 25),
                    text_color="#FFFFFF",
                    bg_color="#555555",
                    )
categoria_do_prato_pesquisadoLabel.place(x=759, y=366)

disponibilidade_do_prato_pesquisadoLabel = ctk.CTkLabel(appCardapio,
                    text="Disponibilidade: ",
                    font=("Modern M", 25),
                    text_color="#FFFFFF",
                    bg_color="#555555",
                    )
disponibilidade_do_prato_pesquisadoLabel.place(x=759, y=419)

preco_do_prato_pesquisadoLabel = ctk.CTkLabel(appCardapio,
                    text="Preço: ",
                    font=("Modern M", 25),
                    text_color="#FFFFFF",
                    bg_color="#555555",
                    )
preco_do_prato_pesquisadoLabel.place(x=759, y=472)

serve_prato_pesquisadoLabel = ctk.CTkLabel(appCardapio,
                    text="Serve: ",
                    font=("Modern M", 25),
                    text_color="#FFFFFF",
                    bg_color="#555555",
                    )
serve_prato_pesquisadoLabel.place(x=759, y=525)

img_ilustrativa_prato_pesquisadoLabel = ctk.CTkLabel(appCardapio,
                    text="Imagem Ilustrativa: ",
                    font=("Modern M", 25),
                    text_color="#FFFFFF",
                    bg_color="#555555",
                    )
img_ilustrativa_prato_pesquisadoLabel.place(x=759, y=578)
# Entrys

nome_do_pratoEntry = ctk.CTkEntry(appCardapio,
                                  text_color="#1C1C1C",
                                  placeholder_text='Ex. Batata Frita Média',
                                  placeholder_text_color='#000000',
                                  width=700,
                                  height=30,
                                  corner_radius=15,
                                  bg_color="#555555",
                                  fg_color="#D9D9D9",
                                  border_width=0,
                                  )
nome_do_pratoEntry.place(x=20,y=203)

desc_do_pratoEntry = ctk.CTkEntry(appCardapio,
                                  text_color="#1C1C1C",
                                  placeholder_text='Ex. Batatas cortadas em tiras, fritas em óleo quente, 250 gramas.',
                                  placeholder_text_color='#000000',
                                  width=700,
                                  height=30,
                                  corner_radius=15,
                                  bg_color="#555555",
                                  fg_color="#D9D9D9",
                                  border_width=0,
                                  )
desc_do_pratoEntry.place(x=20,y=299)

categoria_do_pratoMenuOption = ctk.CTkOptionMenu(appCardapio,
                                                 width=350,
                                                 height=30,
                                                 corner_radius=15,
                                                 bg_color="#555555",
                                                 fg_color="#D9D9D9",
                                                 text_color="#242424",
                                                 button_color="#1C1C1C",
                                                 button_hover_color="#5C5C5C",
                                                 values=['Prato Principal', 'Bebida','Acompanhamento', 'Sobremesa', 'Salada', 'Entrada', 'Sobremesa'],
                                                 )
categoria_do_pratoMenuOption.place(x=20,y=398)

disponibilidade_do_pratoMenuOption = ctk.CTkOptionMenu(appCardapio,
                                                 width=350,
                                                 height=30,
                                                 corner_radius=15,
                                                 bg_color="#555555",
                                                 fg_color="#D9D9D9",
                                                 text_color="#242424",
                                                 button_color="#1C1C1C",
                                                 button_hover_color="#5C5C5C",
                                                 values=['Sim', 'Não'],
                                                 )
disponibilidade_do_pratoMenuOption.place(x=370,y=398)

icone_label = ctk.CTkLabel(appCardapio,
                           width=150,
                           height=150,
                           text='',
                           corner_radius=0,
                           fg_color="#555555",
                           bg_color="#555555",
                           )
icone_label.place(x=791, y=633)

preco_do_pratoEntry = ctk.CTkEntry(appCardapio,
                                  placeholder_text='Ex. 29,99',
                                  placeholder_text_color='#000000',
                                  text_color="#1C1C1C",
                                  width=350,
                                  height=30,
                                  corner_radius=15,
                                  bg_color="#555555",
                                  fg_color="#D9D9D9",
                                  border_width=0,
                                  )
preco_do_pratoEntry.place(x=20,y=497)

serve_pratoMenuOption = ctk.CTkOptionMenu(appCardapio,
                                                 width=350,
                                                 height=30,
                                                 corner_radius=15,
                                                 bg_color="#555555",
                                                 fg_color="#D9D9D9",
                                                 text_color="#242424",
                                                 button_color="#1C1C1C",
                                                 button_hover_color="#5C5C5C",
                                                 values=['1 pessoa', '2 pessoas', '3 pessoas', '4 pessoas', '5 pessoas', '6 pessoas', '7 pessoas','8 pessoas'],
                                                 )
serve_pratoMenuOption.place(x=370,y=497)

buscar_prato_menuOption = ctk.CTkOptionMenu(appCardapio,
                                                 width=660,
                                                 height=45,
                                                 corner_radius=50,
                                                 bg_color="#555555",
                                                 fg_color="#D9D9D9",
                                                 text_color="#242424",
                                                 button_color="#1C1C1C",
                                                 button_hover_color="#5C5C5C",
                                                 values=nomes_pratos,
                                                 )
buscar_prato_menuOption.place(x=759,y=188) 

# BTNs

btnUploadIcone = ctk.CTkButton(appCardapio,
                          width=350,
                          height=40,
                          corner_radius=10,
                          font=('Pacifico', 25),
                          text_color="#000000",
                          fg_color="#D9D9D9",
                          bg_color="#555555",
                          text='Carregar Imagem Ilustrativa',
                          hover_color="#828282",
                          command=carregar_imagem,
                          )
btnUploadIcone.place(x=195,y=633)

btnEnviar = ctk.CTkButton(appCardapio,
                          width=175,
                          height=40,
                          corner_radius=10,
                          font=('Pacifico', 25),
                          text_color="#000000",
                          fg_color="#D9D9D9",
                          bg_color="#555555",
                          text='Enviar',
                          hover_color="#828282",
                          command=cadastrar_prato,
                          state="disabled"
                          )
btnEnviar.place(x=282,y=708)

btnBuscar = ctk.CTkButton(appCardapio,
                                   width=78,
                                   height=45,
                                   corner_radius=0,
                                   font=('Russian', 25),
                                   text_color="#D9D9D9",
                                   fg_color="#000000",
                                   bg_color="#555555",
                                   text='IR',
                                   hover_color="#828282",
                                   command=buscar_prato_selecionado,
                                   )
btnBuscar.place(x=1342, y=188)

btnEditar = ctk.CTkButton(appCardapio,
                          width=150,
                          height=40,
                          corner_radius=10,
                          font=('Pacifico', 25),
                          text_color="#000000",
                          fg_color="#D9D9D9",
                          bg_color="#555555",
                          text='Editar',
                          hover_color="#828282",
                          command=editar_prato_selecionado,
                          )
btnEditar.place(x=1231, y=633)

btnExcluir = ctk.CTkButton(appCardapio,
                           width=150,
                           height=40,
                           corner_radius=10,
                           font=('Pacifico', 25),
                           text_color="#000000",
                           fg_color="#D9D9D9",
                           bg_color="#555555",
                           text='Excluir',
                           hover_color="#828282",
                           command=excluir_prato_selecionado,
                           )
btnExcluir.place(x=1231, y=708)

selCampo = ctk.CTkOptionMenu(appCardapio,
                            width=232,
                            height=40,
                            corner_radius=15,
                            bg_color="#555555",
                            fg_color="#D9D9D9",
                            font=("Square", 20),
                            text_color="#1C1C1C",
                            button_color="#1C1C1C",
                            button_hover_color="#0C0C0C",
                            values=nomes_campos,
                            )
selCampo.place(x=970, y=633)

novoValorEntry = ctk.CTkEntry(appCardapio,
                         width=232,
                         height=40,
                         corner_radius=15,
                         bg_color="#555555",
                         fg_color="#D9D9D9",
                         font=("Square", 20),
                         text_color="#1C1C1C",
                         placeholder_text='Ex: Preço 34,99',
                         )
novoValorEntry.place(x=970,y=708)

btnLimpar = ctk.CTkButton(appCardapio,
                           width=78,
                           height=45,
                           corner_radius=0,
                           font=('Russian', 20),
                           text_color="#D9D9D9",
                           fg_color="#000000",
                           bg_color="#555555",
                           text='Limpar',
                           hover_color="#828282",
                           command=limpar_detalhes_prato,
                           )
btnLimpar.place(x=1264, y=188)

appCardapio.mainloop()