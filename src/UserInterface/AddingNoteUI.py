import customtkinter as ctk
from src.UserInterface.ResponsiveImageFrame import ResponsiveImageFrame

class AddingNoteUI(ResponsiveImageFrame):
    def __init__(self, master: ctk.CTk, **kwargs):
        super().__init__(master, **kwargs, fg_color="transparent")

        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        # Apresentando os botões!
        btn_left = ctk.CTkButton(
            self,
            text="Voltar",
            font=("Arial", 15, "bold"),
            width=90, # Forçamos a sempre ocupar o menor espaço possível
            corner_radius=0,
            fg_color="#332D30",
            command=lambda: master.MainMenu.tkraise() if hasattr(master, "MainMenu") else None
        )
        # sticky="nw" = gruda no norte (topo) e oeste (esquerda)
        btn_left.configure(cursor="hand2")
        btn_left.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        btn_right = ctk.CTkButton(
            self,
            text="Confirmar",
            font=("Arial", 15, "bold"),
            width=90, # Forçamos a sempre ocupar o menor espaço possível
            corner_radius=0,
            fg_color="#A6845D",
            command=lambda: print("Confirmando")
        )
        # sticky="ne" = gruda no norte (topo) e leste (direita)
        btn_right.configure(cursor="hand2")
        btn_right.grid(row=0, column=4, padx=10, pady=10, sticky="ne")
















