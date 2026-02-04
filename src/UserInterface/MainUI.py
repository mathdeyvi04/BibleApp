import customtkinter as ctk
from src.UserInterface.ResponsiveImageButton import ResponsiveImageButton
from pathlib import Path

class MainUI(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("BibleApp")
        self.geometry("600x400")
        self.minsize(400, 300)

        # Layout Principal
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_menu = ctk.CTkFrame(self)
        self.main_menu.grid(row=0, column=0, sticky="nsew")

        # Divide a tela em duas metades EXATAS
        self.main_menu.grid_rowconfigure(0, weight=1)
        self.main_menu.grid_rowconfigure(1, weight=1)
        self.main_menu.grid_columnconfigure(0, weight=1)

        # Botão Superior (Metade de Cima)
        self.btn_top = ResponsiveImageButton(
            master=self.main_menu,
            image_path=Path(__file__).parent / "image_background.jpg",
            position="top",  # <--- Define que é o topo
            text="Adicionar Nota",
            command=lambda: print("Clique Topo")
        )
        # padding 0 para as imagens se tocarem
        self.btn_top.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # Botão Inferior (Metade de Baixo)
        self.btn_bottom = ResponsiveImageButton(
            master=self.main_menu,
            image_path=Path(__file__).parent / "image_background.jpg",
            position="bottom",  # <--- Define que é a base
            text="Apresentar Notas",
            command=lambda: print("Clique Baixo")
        )
        self.btn_bottom.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)



    # def __init__(self):
    #     super().__init__()
    #
    #     # Configurações da Janela
    #     self.title("BibleApp")
    #     self.geometry("600x400")
    #     self.minsize(400, 300)
    #
    #     # Configuração do Grid principal (1 linha, 1 coluna)
    #     # Isso permite empilhar frames um sobre o outro
    #     self.grid_rowconfigure(0, weight=1)
    #     self.grid_columnconfigure(0, weight=1)
    #
    #     # --- Frame do Menu Principal ---
    #     self.main_menu_frame = ctk.CTkFrame(self)
    #     self.main_menu_frame.grid(row=0, column=0, sticky="nsew")
    #
    #     # Configura o grid do menu (2 linhas para dividir a tela)
    #     self.main_menu_frame.grid_rowconfigure(0, weight=1)  # Metade superior
    #     self.main_menu_frame.grid_rowconfigure(1, weight=1)  # Metade inferior
    #     self.main_menu_frame.grid_columnconfigure(0, weight=1)
    #
    #     # Botão Superior
    #     self.btn_top = ResponsiveImageButton(
    #         master=self.main_menu_frame,
    #         image_path=Path(__file__).parent / "image_background.jpg",
    #         text="Adicionar Nota",
    #         font=("Arial", 24, "bold"),
    #         position="top",
    #         text_color="white",
    #         command=lambda: self.show_interface(0)
    #     )
    #     self.btn_top.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
    #
    #     # Botão Inferior
    #     self.btn_bottom = ResponsiveImageButton(
    #         master=self.main_menu_frame,
    #         image_path=Path(__file__).parent / "image_background.jpg",
    #         text="Apresentar Notas",
    #         font=("Arial", 24, "bold"),
    #         position="bottom",
    #         text_color="white",
    #         command=lambda: self.show_interface(1)
    #     )
    #     self.btn_bottom.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
    #
    #     # --- Frame da Nova Interface (Placeholder) ---
    #     self.content_frame = None
    #
    # def show_interface(self, identifier: int) -> None:
    #     # 1. Esconde o menu principal (não destrói, apenas remove do grid)
    #     self.main_menu_frame.grid_forget()
    #
    #     # 2. Cria o frame novo
    #     self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
    #     self.content_frame.grid(row=0, column=0, sticky="nsew")
    #
    #     # Layout interno da nova interface
    #     self.content_frame.grid_columnconfigure(0, weight=1)
    #     self.content_frame.grid_rowconfigure(0, weight=1)
    #
    #     # Painel centralizado
    #     panel = ctk.CTkFrame(self.content_frame)
    #     panel.grid(row=0, column=0)
    #
    #     label = ctk.CTkLabel(panel, text=f"Bem-vindo à {identifier}", font=("Arial", 20))
    #     label.pack(pady=20, padx=20)
    #
    #     btn_back = ctk.CTkButton(panel, text="Voltar", command=self.show_main_menu)
    #     btn_back.pack(pady=10)
    #
    # ##
    # # @brief Retorna ao menu principal.
    # def show_main_menu(self):
    #     if self.content_frame:
    #         self.content_frame.destroy()  # Limpa a interface anterior
    #         self.content_frame = None
    #
    #     # Mostra o menu novamente
    #     self.main_menu_frame.grid(row=0, column=0, sticky="nsew")













