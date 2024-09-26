from dataclasses import dataclass
import tkinter as tk
from tkinter import ttk


@dataclass
class ScrollableFrame(ttk.Frame):
   def __init__(self, container, *args, **kwargs):
      super().__init__(container, *args, **kwargs)

      canvas = tk.Canvas(self)
      scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
      self.scroll = ttk.Frame(canvas)

      self.scroll.bind(
         "<Configure>",
         lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
         )
      )

      canvas.create_window((0, 0), window=self.scroll, anchor="nw")

      canvas.configure(yscrollcommand=scrollbar.set)

      canvas.grid(row=0, column=0, sticky="nsew")
      scrollbar.grid(row=0, column=1, sticky="ns")

      self.grid_rowconfigure(0, weight=1)
      self.grid_columnconfigure(0, weight=1)



