from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger
import os

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Yhdistäjä – nopea")
        self.root.geometry("600x450")
        self.root.configure(bg='white')

        self.pdf_files = []

        self.label = tk.Label(root, text="Pudota tai valitse PDF-tiedostoja", bg='white', font=("Arial", 12))
        self.label.pack(pady=10)

        self.file_listbox = tk.Listbox(root, height=15)
        self.file_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.button_frame = tk.Frame(root, bg='white')
        self.button_frame.pack(pady=10)

        self.add_button = tk.Button(self.button_frame, text="Lisää PDF-tiedostoja", command=self.open_file_dialog)
        self.add_button.grid(row=0, column=0, padx=5)

        self.merge_button = tk.Button(self.button_frame, text="Yhdistä PDF:t", command=self.merge_pdfs)
        self.merge_button.grid(row=0, column=1, padx=5)

        self.clear_button = tk.Button(self.button_frame, text="Tyhjennä tiedostot", command=self.clear_files)
        self.clear_button.grid(row=0, column=2, padx=5)

        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.handle_drop)

    def open_file_dialog(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        self.handle_files(files)

    def handle_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        self.handle_files(files)

    def handle_files(self, files):
        for file in files:
            if file.lower().endswith(".pdf") and file not in self.pdf_files:
                self.pdf_files.append(file)
                self.file_listbox.insert(tk.END, os.path.basename(file))

    def clear_files(self):
        self.pdf_files.clear()
        self.file_listbox.delete(0, tk.END)

    def merge_pdfs(self):
        if not self.pdf_files:
            messagebox.showwarning("Ei tiedostoja", "Valitse tai pudota ensin PDF-tiedostoja.")
            return

        last_dir = os.path.dirname(self.pdf_files[-1])
        output_path = os.path.join(last_dir, "yhdistettyPDF.pdf")

        merger = PdfMerger()
        try:
            for pdf in self.pdf_files:
                merger.append(pdf)
            merger.write(output_path)
            merger.close()
            messagebox.showinfo("Valmis", f"PDF:t yhdistetty tiedostoksi:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Virhe", f"Virhe yhdistettäessä PDF:iä:\n{e}")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
