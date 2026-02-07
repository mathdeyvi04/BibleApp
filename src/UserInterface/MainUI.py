import customtkinter as ctk
from src.UserInterface.ResponsiveImageButton import ResponsiveImageButton
from src.UserInterface.AddingNoteUI import AddingNoteUI
from src.UserInterface.ApresentingNotesUI import ApresentingNotesUI
from pathlib import Path
from PIL import Image

class MainUI(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("BibleApp")
        self.wallpaper = Image.open(Path(__file__).parent / "image_background.jpg")
        self.geometry("700x600")

        # Layout Principal
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.MainMenu = ctk.CTkFrame(self)
        self.MainMenu.grid(row=0, column=0, sticky="nsew")

        # Divide a tela em duas metades EXATAS
        self.MainMenu.grid_rowconfigure(0, weight=1)
        self.MainMenu.grid_rowconfigure(1, weight=1)
        self.MainMenu.grid_columnconfigure(0, weight=1)

        # Criamos as novas interfaces
        self.AddingNote = AddingNoteUI(self, image=self.wallpaper)
        self.AddingNote.grid(row=0, column=0, sticky="nsew")
        self.ApresentingNotes = ApresentingNotesUI(self, image=self.wallpaper)
        self.ApresentingNotes.grid(row=0, column=0, sticky="nsew")
        self.MainMenu.tkraise()

        # Botão Superior (Metade de Cima)
        self.btn_top = ResponsiveImageButton(
            master=self.MainMenu,
            image=self.wallpaper,
            position=(2, 1, 1),
            text="Adicionar Nota",
            command=lambda: self.AddingNote.tkraise()
        )
        # padding 0 para as imagens se tocarem
        self.btn_top.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # Botão Inferior (Metade de Baixo)
        self.btn_bottom = ResponsiveImageButton(
            master=self.MainMenu,
            image=self.wallpaper,
            position=(2, 1, 2),
            text="Apresentar Notas",
            command=lambda: self.ApresentingNotes.tkraise()
        )
        self.btn_bottom.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

        self.bind("<Configure>", lambda event: self.minsize(700, 600))
