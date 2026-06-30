import os
import shutil
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox

from natsort import natsorted
from pypdf import PdfWriter, PdfReader


class ZipPDFMerger:

    def __init__(self, root):

        self.root = root
        self.root.title("ZIP to PDF Merger")
        self.root.geometry("650x350")
        self.root.resizable(False, False)

        self.folder = tk.StringVar()

        tk.Label(root, text="Main Folder", font=("Segoe UI", 10, "bold")).pack(pady=(20, 5))

        frame = tk.Frame(root)
        frame.pack(fill="x", padx=15)

        tk.Entry(frame, textvariable=self.folder).pack(side="left", fill="x", expand=True)

        tk.Button(frame,
                  text="Browse",
                  command=self.browse).pack(side="left", padx=5)

        self.status = tk.Label(root,
                               text="Ready",
                               anchor="w",
                               justify="left",
                               font=("Segoe UI", 10))

        self.status.pack(fill="x", padx=15, pady=20)

        tk.Button(root,
                  text="Start",
                  width=20,
                  height=2,
                  command=self.start).pack()

    def browse(self):

        folder = filedialog.askdirectory()

        if folder:
            self.folder.set(folder)

    def update_status(self, text):

        self.status.config(text=text)
        self.root.update()

    def merge_pdfs(self, folder, output):

        pdfs = []

        for root_dir, _, files in os.walk(folder):
            for f in files:
                if f.lower().endswith(".pdf"):
                    pdfs.append(os.path.join(root_dir, f))

        pdfs = natsorted(pdfs)

        if not pdfs:
            return False

        writer = PdfWriter()

        for pdf in pdfs:

            try:
                reader = PdfReader(pdf)

                for page in reader.pages:
                    writer.add_page(page)

            except Exception:
                print(f"Skipping invalid PDF: {pdf}")

        if len(writer.pages) == 0:
            return False

        with open(output, "wb") as fp:
            writer.write(fp)

        return True

    def start(self):

        main_folder = self.folder.get()

        if not os.path.isdir(main_folder):
            messagebox.showerror("Error", "Select a valid folder.")
            return

        zips = [
            f for f in os.listdir(main_folder)
            if f.lower().endswith(".zip")
        ]

        if not zips:
            messagebox.showinfo("Done", "No ZIP files found.")
            return

        success = 0

        for zip_name in zips:

            zip_path = os.path.join(main_folder, zip_name)

            folder_name = os.path.splitext(zip_name)[0]

            extract_folder = os.path.join(main_folder, folder_name)

            output_pdf = os.path.join(main_folder, folder_name + ".pdf")

            self.update_status(f"Extracting:\n{zip_name}")

            try:

                if os.path.exists(extract_folder):
                    shutil.rmtree(extract_folder)

                with zipfile.ZipFile(zip_path, "r") as z:
                    z.extractall(extract_folder)

            except Exception as e:
                print(e)
                continue

            self.update_status(f"Merging:\n{folder_name}")

            try:

                merged = self.merge_pdfs(extract_folder, output_pdf)

                if merged:
                    success += 1

            except Exception as e:
                print(e)

            try:
                shutil.rmtree(extract_folder)
            except Exception:
                pass

        self.update_status("Finished.")

        messagebox.showinfo(
            "Completed",
            f"{success} PDF(s) created successfully."
        )


if __name__ == "__main__":

    root = tk.Tk()

    app = ZipPDFMerger(root)

    root.mainloop()