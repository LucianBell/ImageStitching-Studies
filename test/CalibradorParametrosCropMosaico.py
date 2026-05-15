import cv2
import os
import re
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class MosaicCalibrator:

    def __init__(self, root):
        self.root = root
        self.root.title("Calibração de Mosaico")
        self.root.geometry("1400x900")

        self.images = {}
        self.mode = tk.StringVar(value="2col")

        # ============================
        # CONTROLES
        # ============================
        ctrl = tk.Frame(root)
        ctrl.pack(side="top", fill="x")

        def add_field(label, default):
            f = tk.Frame(ctrl)
            f.pack(side="left", padx=5)
            tk.Label(f, text=label).pack()
            e = tk.Entry(f, width=8)
            e.insert(0, str(default))
            e.pack()
            return e

        self.entry_passo_x = add_field("PASSO_X", 3000)
        self.entry_passo_y = add_field("PASSO_Y", 1200)
        self.entry_overlap = add_field("Overlap %", 10)

        self.entry_corte_col1 = add_field("Corte Col1", 900)
        self.entry_corte_col2 = add_field("Corte Col2", 900)
        
        #inclusao junior
        #self.entry_corte_h = add_field("Corte Altura", 0)
        self.entry_corte_w = add_field("Corte Largura", 0)
        
        self.entry_corte_topo = add_field("Corte Topo", 0)
        self.entry_corte_base = add_field("Corte Base", 0)
        
        
        # ============================
        # BOTÕES
        # ============================
        tk.Button(ctrl, text="Carregar Pasta", command=self.load_folder).pack(side="left", padx=10)
        tk.Button(ctrl, text="Atualizar Preview", command=self.update_preview).pack(side="left")
        tk.Button(ctrl, text="Salvar Mosaico", command=self.save_mosaic).pack(side="left")

        tk.OptionMenu(ctrl, self.mode, "1col", "2col", "grid").pack(side="left", padx=10)

        # ============================
        # CANVAS
        # ============================
        self.canvas = tk.Canvas(root, bg="black")
        self.canvas.pack(fill="both", expand=True)

        self.preview_img = None
        self.last_mosaic = None

    # ============================
    # LOAD
    # ============================
    def load_folder(self):
        path = filedialog.askdirectory()
        if not path:
            return

        self.images = {}

        print(path)
        for f in os.listdir(path):
            print(f.lower())
            if not f.lower().endswith(".jpg"):
                continue

            m = re.search(r"_r(\d+)_c(\d+)", f)
            if not m:
                continue

            r = int(m.group(1))
            c = int(m.group(2))

            img = cv2.imread(os.path.join(path, f))
            self.images[(r, c)] = img

        print(f"[LOAD] {len(self.images)} imagens")

    # ============================
    # CROP 2 COL
    # ============================
    def crop_2col(self, img, col, corte1, corte2):
        H, W = img.shape[:2]

        if col == 1:
            x1 = 0
            x2 = W - corte1

        elif col == 2:
            x1 = corte2
            x2 = W

        else:
            return img

        x1 = max(0, min(x1, W - 1))
        x2 = max(x1 + 1, min(x2, W))

        cropped = img[:, x1:x2]

        print(f"[CROP] col={col} -> w={cropped.shape[1]}")

        return cropped

    # ============================
    # PREVIEW
    # ============================
    def update_preview(self):

        if not self.images:
            return

        #alteracao junior
        #ch = int(self.entry_corte_h.get())
        
        ct = int(self.entry_corte_topo.get())
        cb = int(self.entry_corte_base.get())
        
        cw = int(self.entry_corte_w.get())
        
        passo_x = int(self.entry_passo_x.get())
        passo_y = int(self.entry_passo_y.get())
        overlap = float(self.entry_overlap.get()) / 100.0

        corte1 = int(self.entry_corte_col1.get())
        corte2 = int(self.entry_corte_col2.get())

        tiles = {}

        # ============================
        # APLICA CROP
        # ============================
        for (r, c), img in self.images.items():
            
            #alteracoa junior
            H, W = img.shape[:2]
            
            #y1, y2 = ch, max(ch + 1, H - ch)
            #x1, x2 = cw, max(cw + 1, W - cw)
            
            y1 = ct
            y2 = max(y1 + 1, H - cb)
            
            x1 = cw
            x2 = max(x1 + 1, W - cw)
            
            img = img[y1:y2, x1:x2]

            if self.mode.get() == "2col":
                img = self.crop_2col(img, c, corte1, corte2)

            tiles[(r, c)] = img

        sample = next(iter(tiles.values()))
        h, w = sample.shape[:2]

        # aplica overlap
        passo_x = int(passo_x * (1 - overlap))
        passo_y = int(passo_y * (1 - overlap))

        rows = max(r for (r, _) in tiles.keys())
        cols = max(c for (_, c) in tiles.keys())

        canvas_h = rows * passo_y + h
        canvas_w = cols * passo_x + w

        print(f"[MOSAIC]")
        print(f"  tile={w}x{h}")
        print(f"  passo={passo_x},{passo_y}")
        print(f"  canvas={canvas_w}x{canvas_h}")

        canvas = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)

        # ============================
        # POSICIONAMENTO
        # ============================
        for (r, c), img in tiles.items():

            y = (r - 1) * passo_y
            x = (c - 1) * passo_x

            hh, ww = img.shape[:2]

            canvas[y:y+hh, x:x+ww] = img

        self.last_mosaic = canvas
        self.show_on_canvas(canvas)

    # ============================
    # SHOW
    # ============================
    def show_on_canvas(self, img):

        self.root.update_idletasks()

        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()

        if canvas_w < 10:
            canvas_w = 1200
            canvas_h = 800

        h, w = img.shape[:2]

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)

        scale = min(canvas_w / w, canvas_h / h, 1.0)

        new_w = int(w * scale)
        new_h = int(h * scale)

        pil_img = pil_img.resize((new_w, new_h), Image.LANCZOS)

        img_tk = ImageTk.PhotoImage(pil_img)

        self.canvas.delete("all")

        x = (canvas_w - new_w) // 2
        y = (canvas_h - new_h) // 2

        self.canvas.create_image(x, y, anchor="nw", image=img_tk)
        self.preview_img = img_tk

    # ============================
    # SAVE
    # ============================
    def save_mosaic(self):

        if self.last_mosaic is None:
            return

        path = filedialog.asksaveasfilename(defaultextension=".jpg")

        if not path:
            return

        cv2.imwrite(path, self.last_mosaic)
        print("[OK] Mosaico salvo:", path)


# ============================
# RUN
# ============================
root = tk.Tk()
app = MosaicCalibrator(root)
root.mainloop()
