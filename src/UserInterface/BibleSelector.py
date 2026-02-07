import customtkinter as ctk
from typing import Callable

# --- MOCK DATA (Simulação da estrutura da Bíblia) ---
# Em produção, você carregaria isso de um JSON
BIBLE_STRUCTURE = {
    "Gênesis": 50,  # Nome: Total de Capítulos
    "Êxodo": 40,
    "Levítico": 27,
    "Salmos": 150,
    "João": 21,
    "Apocalipse": 22
}
# Para simplificar o exemplo, assumimos 30 versículos por capítulo.
# Na realidade, precisaria de um dicionário {Livro: {Cap1: 31, Cap2: 25...}}
DEFAULT_VERSES_COUNT = 30


class BibleSelector(ctk.CTkFrame):
    """
    Widget hierárquico para seleção de referências bíblicas (Livro -> Capítulo -> Versículos).

    Permite navegação "drill-down" e seleção múltipla de versículos.
    Gerencia o estado interno e fornece callback com os dados finais.
    """

    def __init__(self, master, on_confirm: Callable | None, **kwargs):
        """
        Inicializa o seletor.

        Args:
            master: Widget pai.
            on_confirm (Callable): Função callback chamada quando o usuário finaliza a seleção.
                                   Recebe um dict: {'book': str, 'chapter': int, 'verses': list[int]}
            **kwargs: Argumentos padrão do CTkFrame.
        """
        super().__init__(master, **kwargs)

        self.on_confirm_callback = on_confirm

        # --- Estado Interno ---
        self.current_book: str | None = None
        self.current_chapter: int | None = None
        self.selected_verses: set = set()  # Usamos set para evitar duplicatas e busca rápida O(1)

        # --- Configuração do Layout ---
        self.grid_rowconfigure(1, weight=1)  # O conteúdo (linha 1) expande
        self.grid_columnconfigure(0, weight=1)

        # 1. Barra de Navegação (Breadcrumbs)
        self.nav_frame = ctk.CTkFrame(self, height=40, fg_color="transparent")
        self.nav_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(5, 0))

        # 2. Área de Conteúdo (Scrollable)
        self.content_frame = ctk.CTkScrollableFrame(self)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # 3. Botão de Ação (Confirmar)
        self.action_btn = ctk.CTkButton(
            self,
            text="Selecione um Livro",
            state="disabled",
            command=self._finish_selection
        )
        self.action_btn.grid(row=2, column=0, sticky="ew", padx=20, pady=10)

        # Inicia na visualização de livros
        self._render_books_view()

    # -------------------------------------------------------------------------
    # MÉTODOS DE RENDERIZAÇÃO (VIEWS)
    # -------------------------------------------------------------------------

    def _render_books_view(self):
        """Renderiza a grade de botões com os nomes dos Livros."""
        self._clear_content()
        self._update_breadcrumbs(step=0)
        self.action_btn.configure(text="Aguardando Seleção...", state="disabled")

        # Configura grid dinâmica (3 colunas)
        columns = 3
        for i in range(columns):
            self.content_frame.grid_columnconfigure(i, weight=1)

        # Cria os botões
        for idx, book_name in enumerate(BIBLE_STRUCTURE.keys()):
            btn = ctk.CTkButton(
                self.content_frame,
                text=book_name,
                fg_color="transparent",
                border_width=1,
                border_color=("gray70", "gray30"),
                text_color=("black", "white"),
                command=lambda b=book_name: self._select_book(b)
            )
            btn.grid(row=idx // columns, column=idx % columns, padx=5, pady=5, sticky="ew")

    def _render_chapters_view(self):
        """Renderiza a grade numérica de Capítulos baseada no livro selecionado."""
        self._clear_content()
        self._update_breadcrumbs(step=1)
        self.action_btn.configure(text="Selecione o Capítulo", state="disabled")

        total_caps = BIBLE_STRUCTURE.get(self.current_book, 0)
        columns = 5  # Mais colunas para números

        for i in range(columns):
            self.content_frame.grid_columnconfigure(i, weight=1)

        for i in range(1, total_caps + 1):
            btn = ctk.CTkButton(
                self.content_frame,
                text=str(i),
                width=40,
                command=lambda c=i: self._select_chapter(c)
            )
            btn.grid(row=(i - 1) // columns, column=(i - 1) % columns, padx=3, pady=3)

    def _render_verses_view(self):
        """Renderiza a grade de Versículos com suporte a seleção múltipla (Toggle)."""
        self._clear_content()
        self._update_breadcrumbs(step=2)
        self._update_confirm_button()  # Atualiza texto do botão

        # Simulação de total de versículos (numa app real, viria do JSON)
        total_verses = DEFAULT_VERSES_COUNT
        columns = 5

        for i in range(columns):
            self.content_frame.grid_columnconfigure(i, weight=1)

        for i in range(1, total_verses + 1):
            # Verifica se já estava selecionado (persistência visual)
            is_selected = i in self.selected_verses
            btn_color = "green" if is_selected else ["#3B8ED0", "#1F6AA5"]  # Cor padrão do CTk

            btn = ctk.CTkButton(
                self.content_frame,
                text=str(i),
                width=40,
                fg_color=btn_color,
                # Passamos o próprio ID do versículo para o comando
                command=lambda v=i: self._toggle_verse(v)
            )
            # Guardamos referência do botão no atributo do widget para mudar cor depois?
            # Truque: Vamos reconstruir a cor baseada no clique, passando o objeto 'btn'
            # Mas como lambda captura variáveis, vamos usar uma função helper.
            btn.configure(command=lambda b=btn, v=i: self._toggle_verse_visual(b, v))

            btn.grid(row=(i - 1) // columns, column=(i - 1) % columns, padx=3, pady=3)

    # -------------------------------------------------------------------------
    # LÓGICA DE NAVEGAÇÃO E ESTADO
    # -------------------------------------------------------------------------

    def _select_book(self, book_name: str):
        """Define o livro atual e avança para capítulos."""
        self.current_book = book_name
        self.current_chapter = None
        self.selected_verses.clear()
        self._render_chapters_view()

    def _select_chapter(self, chapter_num: int):
        """Define o capítulo atual e avança para versículos."""
        self.current_chapter = chapter_num
        self.selected_verses.clear()  # Limpa versículos ao mudar de capítulo
        self._render_verses_view()

    def _toggle_verse_visual(self, btn_widget: ctk.CTkButton, verse_num: int):
        """
        Alterna o estado de seleção de um versículo e atualiza a cor do botão imediatamente.
        """
        if verse_num in self.selected_verses:
            self.selected_verses.remove(verse_num)
            # Volta para a cor padrão (Default theme color)
            btn_widget.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        else:
            self.selected_verses.add(verse_num)
            # Define cor de destaque (ex: Verde ou Laranja)
            btn_widget.configure(fg_color="green")

        self._update_confirm_button()

    def _finish_selection(self):
        """Empacota os dados e chama o callback de sucesso."""
        if not self.selected_verses:
            return

        result_data = {
            "book": self.current_book,
            "chapter": self.current_chapter,
            "verses": sorted(list(self.selected_verses))  # Ordena para ficar bonito (1, 2, 3)
        }
        self.on_confirm_callback(result_data)

    # -------------------------------------------------------------------------
    # MÉTODOS AUXILIARES DE UI
    # -------------------------------------------------------------------------

    def _clear_content(self):
        """Remove todos os widgets da área de scroll."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def _update_breadcrumbs(self, step: int):
        """
        Recria a barra de navegação superior.
        step 0: Apenas [INÍCIO]
        step 1: [INÍCIO] > [LIVRO]
        step 2: [INÍCIO] > [LIVRO] > [CAPÍTULO]
        """
        for w in self.nav_frame.winfo_children():
            w.destroy()

        # Botão Home (Sempre visível)
        btn_home = ctk.CTkButton(self.nav_frame, text="BÍBLIA", width=60,
                                 fg_color="transparent", border_width=1,
                                 command=self._render_books_view)
        btn_home.pack(side="left", padx=2)

        if step >= 1:
            lbl_arrow1 = ctk.CTkLabel(self.nav_frame, text=">", width=10)
            lbl_arrow1.pack(side="left")

            # Botão do Livro (Permite voltar para escolher capítulo)
            # Note que ao clicar aqui, voltamos para a visão de capítulos DO livro atual
            btn_book = ctk.CTkButton(self.nav_frame, text=self.current_book, width=80,
                                     fg_color="transparent", border_width=1,
                                     command=self._render_chapters_view)
            btn_book.pack(side="left", padx=2)

        if step >= 2:
            lbl_arrow2 = ctk.CTkLabel(self.nav_frame, text=">", width=10)
            lbl_arrow2.pack(side="left")

            lbl_chap = ctk.CTkLabel(self.nav_frame, text=f"Cap {self.current_chapter}", font=("Arial", 12, "bold"))
            lbl_chap.pack(side="left", padx=5)

    def _update_confirm_button(self):
        """Habilita ou desabilita o botão de confirmação baseado na seleção."""
        count = len(self.selected_verses)
        if count > 0:
            self.action_btn.configure(state="normal", text=f"Confirmar {count} versículo(s)")
        else:
            self.action_btn.configure(state="disabled", text="Selecione versículos")


# --- BLOCO DE TESTE ---
if __name__ == "__main__":
    def receiver(data):
        print("\n--- DADOS RECEBIDOS ---")
        print(f"Livro: {data['book']}")
        print(f"Capítulo: {data['chapter']}")
        print(f"Versículos: {data['verses']}")
        print("-----------------------")


    app = ctk.CTk()
    app.geometry("500x600")

    selector = BibleSelector(app, on_confirm=receiver)
    selector.pack(expand=True, fill="both", padx=20, pady=20)

    app.mainloop()