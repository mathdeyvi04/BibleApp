import customtkinter as ctk
from pathlib import Path
from PIL import Image, ImageOps
from tkinter import messagebox as msb

class ResponsiveImageButton(ctk.CTkFrame):
    """
    Classe modular que utiliza um único Label com compound="center"
    para garantir que o texto fique sobre a imagem sem fundo opaco.
    """

    def __init__(self, master, image_path, position="top", text="", command=None, **kwargs):
        # Removemos o fg_color do frame para evitar interferências
        super().__init__(master, fg_color="transparent", **kwargs)

        self.command = command
        self.position = position
        self._resize_timer = None

        # Carregamento da imagem original
        try:
            self.pil_image = Image.open(image_path)
        except Exception:
            self.pil_image = Image.new('RGB', (100, 100), color='gray')

        # --- O ÚNICO WIDGET NECESSÁRIO ---
        # Usamos compound="center" para o texto ignorar o fundo e ficar sobre a imagem
        self.display_label = ctk.CTkLabel(
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

        # Vincula o redimensionamento
        self.bind("<Configure>", self._on_resize_event)

    def _on_resize_event(self, event):
        """
        Gerencia o evento de redimensionamento usando Debouncing.
        Cancela execuções pendentes se uma nova for disparada rapidamente.
        """
        # Se já houver um redimensionamento agendado, cancelamos
        if self._resize_timer is not None:
            self.after_cancel(self._resize_timer)

        # Agendamos a execução real para daqui a 100ms
        # Isso garante que, se o usuário estiver arrastando a janela,
        # a imagem só será processada quando ele parar ou fizer uma pausa.
        self._resize_timer = self.after(100, self._perform_render)

    def _perform_render(self):
        """
        Realiza o processamento pesado da imagem de forma isolada.
        """
        width = self.winfo_width()
        height = self.winfo_height()

        if width < 10 or height < 10:
            return

        # 1. Calculamos a altura total teórica (mosaico)
        full_height = height * 2

        # 2. Redimensionamento (usamos BILINEAR que é mais rápido que LANCZOS)
        full_img_resized = ImageOps.fit(
            self.pil_image,
            (width, full_height),
            method=Image.Resampling.BILINEAR,
            centering=(0.5, 0.5)
        )

        # 3. Recorte da fatia
        if self.position == "top":
            slice_img = full_img_resized.crop((0, 0, width, height))
        else:
            slice_img = full_img_resized.crop((0, height, width, full_height))

        # 4. Atualização do widget
        new_image = ctk.CTkImage(
            light_image=slice_img,
            dark_image=slice_img,
            size=(width, height)
        )
        self.display_label.configure(image=new_image)

        # Limpa o timer
        self._resize_timer = None