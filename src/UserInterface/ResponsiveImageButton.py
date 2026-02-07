import customtkinter as ctk
from src.UserInterface.ResponsiveImageFrame import ResponsiveImageFrame
from pathlib import Path

class ResponsiveImageButton(ResponsiveImageFrame):
    """
    Versão clicável do ResponsiveImageFrame que atua como um botão customizado.

    Args:
        master: Widget pai.
        image_path: Caminho da imagem de fundo.
        text (str): Texto a ser exibido centralizado sobre a imagem.
        command (callable): Função executada ao clicar no frame ou imagem.
    """

    def __init__(self, master, image_path: str | Path, text='', command=None, **kwargs):
        super().__init__(master, image_path, **kwargs)

        self.command = command

        self.display_label.configure(
            self,
            text=text,
            font=("Arial", 24, "bold"),
            text_color="white",
            compound="center"  # <--- O segredo da transparência
        )
        self.display_label.pack(expand=True, fill="both")

        # Configura interatividade
        self.display_label.configure(cursor="hand2")
        if self.command:
            self.display_label.bind("<Button-1>", lambda e: self.command())

if __name__ == '__main__':
    app = ctk.CTk()
    app.geometry("400x300")
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)

    btn = ResponsiveImageButton(
        app,
        "image_background.jpg",
        text="CLIQUE AQUI",
        command=lambda: print("Botão pressionado!")
    )
    btn.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    app.mainloop()