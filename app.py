import customtkinter as ctk
from ui import NHDCBatchBidExtractorUI


def main():

    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")

    app = NHDCBatchBidExtractorUI()

    app.mainloop()


if __name__ == "__main__":
    main()