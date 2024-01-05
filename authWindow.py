import sqlite3
import customtkinter as ctk
from PIL import Image

authApp = ctk.CTk()

authApp.title('Login - Restaurante')
authApp.resizable(False, False)
authApp.geometry('500x200')

# Funcs

mostrar_mensagem = ''

def fazer_login(matricula, senha):
    # Conectar ao banco de dados
    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()

    # Verificar as credenciais no banco de dados
    cursor.execute("SELECT * FROM usuarios WHERE matriculaUsuario = ? AND senhaUsuario = ?", (matricula, senha))
    resultado = cursor.fetchone()

    # Fechar a conexão com o banco de dados
    conexao.close()

    # Verificar se as credenciais são válidas
    if resultado:
        mostrar_mensagem("Login bem-sucedido!")
    else:
        mostrar_mensagem("Matrícula ou senha incorretas")

# Frames

restaurantLogoIMG = ctk.CTkImage(dark_image=Image.open(r"assets\loginIMG.jpg"),
                                 size=(250,200))
ctk.CTkLabel(authApp, 
            text=None,
            image=restaurantLogoIMG,
            bg_color="#F69EE3",
            fg_color="#242424",
            corner_radius=0
            ).place(x=0, y=0)

rightPinkFrame = ctk.CTkFrame(authApp,
                              width=250,
                              height=200,
                              bg_color="#FFA1DF",
                              fg_color="#FFA1DF",
                              corner_radius=0,
                              ).place(x=250,y=0)

# Labels

userLabel = ctk.CTkLabel(authApp,
                    text="Usuário",
                    font=("Pacifico", 12),
                    text_color="#D63BB3",
                    bg_color="#FFA1DF",
                    ).place(x=270,y=34)

userPwLabel = ctk.CTkLabel(authApp,
                    text="Senha",
                    font=("Pacifico", 12),
                    text_color="#D63BB3",
                    bg_color="#FFA1DF",
                    ).place(x=270,y=90)

# Entrys

userEntry = ctk.CTkEntry(authApp,
                         width=230,
                         height=20,
                         corner_radius=10,
                         bg_color="#FFA1DF",
                         fg_color="#FFBFF1",
                         border_width=1,
                         border_color="#D63BB3",
                         )
userEntry.place(x=261, y=60)

userPwEntry = ctk.CTkEntry(authApp,
                           width=230,
                           height=20,
                           corner_radius=10,
                           bg_color="#FFA1DF",
                           fg_color="#FFBFF1",
                           border_width=1,
                           border_color="#D63BB3",
                           )
userPwEntry.place(x=261, y=116)

# Botão Entrar

def tentar_login():
    matricula = userEntry.get()
    senha = userPwEntry.get()
    fazer_login(matricula, senha)

btnEntrar = ctk.CTkButton(authApp,
                          width=115,
                          height=30,
                          font=("Pacifico", 12),
                          text="Entrar",
                          text_color='white',
                          corner_radius=10,
                          bg_color="#F69EE3",
                          fg_color="#DE63C2",
                          border_color="#D63BB3",
                          border_width=1,
                          hover_color="#D63BB3",
                          command=tentar_login,
                          ).place(x=318,y=153)

authApp.mainloop()