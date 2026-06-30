import os
import customtkinter as ctk


class DuplicateDialog(ctk.CTkToplevel):

    def __init__(self, parent, pdf1, pdf2, pages, size):

        super().__init__(parent)

        self.title("Possible Duplicate PDFs")

        self.geometry("700x430")

        self.resizable(False, False)

        self.result = "KEEP_BOTH"

        self.apply_all = False

        self.grab_set()

        ########################################################

        title = ctk.CTkLabel(

            self,

            text="Possible Duplicate PDFs",

            font=("Segoe UI", 22, "bold")

        )

        title.pack(pady=15)

        ########################################################

        frame = ctk.CTkFrame(self)

        frame.pack(fill="both", padx=20, pady=10, expand=True)

        left = ctk.CTkFrame(frame)

        left.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        right = ctk.CTkFrame(frame)

        right.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        ########################################################

        ctk.CTkLabel(

            left,

            text=os.path.basename(pdf1),

            font=("Segoe UI",16,"bold")

        ).pack(pady=10)

        ctk.CTkLabel(

            left,

            text=f"Pages : {pages}"

        ).pack()

        ctk.CTkLabel(

            left,

            text=f"Size : {round(size/1024/1024,2)} MB"

        ).pack()

        ########################################################

        ctk.CTkLabel(

            right,

            text=os.path.basename(pdf2),

            font=("Segoe UI",16,"bold")

        ).pack(pady=10)

        ctk.CTkLabel(

            right,

            text=f"Pages : {pages}"

        ).pack()

        ctk.CTkLabel(

            right,

            text=f"Size : {round(size/1024/1024,2)} MB"

        ).pack()

        ########################################################

        self.apply = ctk.BooleanVar(value=False)

        chk = ctk.CTkCheckBox(

            self,

            text="Apply this decision to all remaining duplicates",

            variable=self.apply

        )

        chk.pack(pady=10)

        ########################################################

        btnframe = ctk.CTkFrame(self)

        btnframe.pack(fill="x", padx=20, pady=15)

        b1 = ctk.CTkButton(

            btnframe,

            text="Use First Only",

            command=self.first

        )

        b1.pack(side="left", expand=True, padx=8)

        b2 = ctk.CTkButton(

            btnframe,

            text="Use Second Only",

            command=self.second

        )

        b2.pack(side="left", expand=True, padx=8)

        b3 = ctk.CTkButton(

            btnframe,

            text="Include Both",

            fg_color="#2E8B57",

            hover_color="#256f46",

            command=self.keep

        )

        b3.pack(side="left", expand=True, padx=8)

    ########################################################

    def first(self):

        self.result = "FIRST"

        self.apply_all = self.apply.get()

        self.destroy()

    ########################################################

    def second(self):

        self.result = "SECOND"

        self.apply_all = self.apply.get()

        self.destroy()

    ########################################################

    def keep(self):

        self.result = "KEEP_BOTH"

        self.apply_all = self.apply.get()

        self.destroy()