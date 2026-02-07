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
            position=(2, 1, 1),
            text="Adicionar Nota",
            command=lambda: print("Clique Topo")
        )
        # padding 0 para as imagens se tocarem
        self.btn_top.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # Botão Inferior (Metade de Baixo)
        self.btn_bottom = ResponsiveImageButton(
            master=self.main_menu,
            image_path=Path(__file__).parent / "image_background.jpg",
            position=(2, 1, 2),
            text="Apresentar Notas",
            command=lambda: print("Clique Baixo")
        )
        self.btn_bottom.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)




















