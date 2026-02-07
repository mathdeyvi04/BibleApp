import customtkinter as ctk
from PIL import Image, ImageOps
from pathlib import Path
from tkinter import messagebox as msb

class ResponsiveImageFrame(ctk.CTkFrame):
    """
    Um CTkFrame personalizado que suporta uma imagem de fundo responsiva.

    A imagem preenche todz o espaço do frame automaticamente (estilo 'cover'),
    utilizando um timer para evitar processamento excessivo durante o redimensionamento.

    Args:
        master: O widget pai.
        image_path (str | Path): Caminho para o arquivo de imagem.
        **kwargs: Argumentos padrão do ctk.CTkFrame.
    """

    def __init__(self, master, image_path: str | Path, position: tuple[int, int, int] = None, **kwargs):
        super().__init__(master, **kwargs)

        self.position = position if position else (1, 1, 1)
        self.image_path = image_path
        self._resize_timer = None

        # Configura o grid para que widgets filhos possam ser empilhados sobre a imagem
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Carregamento inicial da imagem
        try:
            self.pil_image = Image.open(image_path)
        except Exception as e:
            msb.showerror("Erro na Imagem", "Imagem não encontrada.")
            self.pil_image = Image.new('RGB', (100, 100), color='gray')

        # Label que servirá de fundo.
        # Ele fica na célula (0,0) e se expande para todas as direções.
        self.display_label = ctk.CTkLabel(self, text="", image=None)
        self.display_label.grid(row=0, column=0, sticky="nsew")
        self.bg_image = None # Para usarmos mais tarde

        # Vincula o evento de redimensionamento
        self.bind("<Configure>", lambda event: self._handle_resize())

    def _handle_resize(self):
        """
        Gerencia o redimensionamento com debouncing para evitar sobrecarga.
        """
        if self._resize_timer is not None:
            self.after_cancel(self._resize_timer)

        self._resize_timer = self.after(100, self._update_background)

    def _update_background(self):
        """
        Realiza o processamento da imagem usando a lógica de grid (subplot).
        self.position = (total_linhas, total_colunas, indice)
        Ex: (2, 1, 1) -> Primeiro de dois botões verticais.
        Ex: (2, 2, 2) -> Segundo botão (topo direita) de uma grade 2x2.
        """
        width = self.winfo_width()
        height = self.winfo_height()

        if width < 10 or height < 10:
            return

        # 1. Extraímos os dados da posição (Subplot style)
        rows, cols, idx = self.position

        # 2. Calculamos o tamanho "VIRTUAL" total da imagem
        # Se o botão tem 100px e há 3 colunas, a imagem mestre deve ter 300px de largura
        virtual_width = width * cols
        virtual_height = height * rows

        # 3. Redimensionamento 'Cover' para a área total da grade
        # Isso garante que a imagem preencha o mosaico sem distorção
        full_img_resized = ImageOps.fit(
            self.pil_image,
            (virtual_width, virtual_height),
            method=Image.Resampling.BILINEAR,
            centering=(0.5, 0.5)
        )

        # 4. Cálculo de Coordenadas do Quadrante (Lógica de Matriz)
        # Convertemos o índice linear (1, 2, 3...) em coordenadas (linha, coluna)
        current_row = (idx - 1) // cols
        current_col = (idx - 1) % cols

        # Definimos os pontos de corte baseados no quadrante
        left = current_col * width
        top = current_row * height
        right = left + width
        bottom = top + height

        # 5. Recorte e Atualização
        slice_img = full_img_resized.crop((left, top, right, bottom))

        self.bg_image = ctk.CTkImage(
            light_image=slice_img,
            dark_image=slice_img,
            size=(width, height)
        )

        self.display_label.configure(image=self.bg_image)
        self._resize_timer = None

if __name__ == '__main__':
    # 0. Vamos realizar um teste
    app = ctk.CTk()
    app.geometry("600x400")

    # 1. Configura a janela principal para o frame poder expandir
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)

    # 2. Instancia o frame
    frame = ResponsiveImageFrame(app, "image_background.jpg", position=(1, 2, 1))

    # 3. EXIBE o frame (O "pulo do gato")
    frame.grid(row=0, column=0, sticky="nsew")

    app.mainloop()