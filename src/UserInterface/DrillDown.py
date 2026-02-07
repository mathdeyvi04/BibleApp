import customtkinter as ctk
from pathlib import Path
import pickle


class BibleSelector(ctk.CTkFrame):
    def __init__(self, master, data: dict, **kwargs):
        super().__init__(master, **kwargs)

        # Nossos dados
        self.data = data

        # Estes para montarmos os locais de tela
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=7)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.nav_frame = ctk.CTkScrollableFrame(
            self
        )
        self.nav_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.nav_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        # --- Estado Interno ---
        self.current_book: str | None = None
        self.current_chapter: int | None = None
        self.selected_verses: set = set()

        # Iniciamos a busca
        self._render_books_view()

    def _render_books_view(self):
        # Vamos apresentar a grid dinâmica inicial, contendo apenas os livros

        for idx, book_name in enumerate(self.data):
            btn = ctk.CTkButton(
                self.nav_frame,
                text=book_name,
                fg_color="transparent",
                border_width=1,
                border_color=("gray70", "gray30"),
                text_color=("black", "white"),
                command=lambda b=book_name: self._select_book(b)
            )
            btn.grid(row=idx // 5, column=idx % 5, padx=5, pady=5, sticky="ew")

    def _select_book(self, book_name: str):
        # Devemos criar um novo botão no topo
        # Depois limpar o scrollableframe
        # E preencher ele dnv

        pass





if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("500x400")

    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)

    with open(
        Path(__file__).parent / "bible.pkl",
        "rb"
    ) as f:
        data_from_the_bible = pickle.load(f)

    selector = BibleSelector(app, data_from_the_bible)
    selector.grid(row=0, column=0, sticky="nsew")

    app.mainloop()