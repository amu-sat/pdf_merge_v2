import os
import shutil
import tempfile
import zipfile

from natsort import natsorted

from merger import merge_pdfs
from duplicate_checker import check_duplicates


def process_folder(folder, ui):

    zip_files = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith(".zip")
    ]

    zip_files = natsorted(zip_files)

    total = len(zip_files)

    if total == 0:
        ui.write_log("No ZIP files found.")
        return

    processed = 0
    merged = 0
    failed = 0

    ui.write_log(f"{total} ZIP file(s) found.\n")

    for zip_path in zip_files:

        if ui.stop_requested:
            ui.write_log("\nProcessing stopped by user.")
            break

        zip_name = os.path.splitext(os.path.basename(zip_path))[0]

        ui.set_current_zip(zip_name)

        ui.write_log(f"\nProcessing : {zip_name}")

        extract_folder = os.path.join(folder, zip_name)

        try:

            if os.path.exists(extract_folder):
                shutil.rmtree(extract_folder)

            os.makedirs(extract_folder)

            with zipfile.ZipFile(zip_path, "r") as z:

                z.extractall(extract_folder)

            ui.write_log("Extraction complete.")

        except Exception as e:

            ui.write_log(f"Extraction failed : {e}")

            failed += 1

            processed += 1

            ui.update_overall(processed / total)

            continue

        pdfs = []

        for root, dirs, files in os.walk(extract_folder):

            for file in files:

                if file.lower().endswith(".pdf"):

                    pdfs.append(os.path.join(root, file))

        pdfs = natsorted(pdfs)

        if len(pdfs) == 0:

            ui.write_log("No PDFs found.")

            shutil.rmtree(extract_folder)

            processed += 1

            ui.update_overall(processed / total)

            continue

        ui.write_log(f"{len(pdfs)} PDFs found.")

        # Update folder progress while scanning

        cleaned = []

        total_pdf = len(pdfs)

        for i, pdf in enumerate(pdfs):

            if ui.stop_requested:
                break

            ui.update_folder((i + 1) / total_pdf)

            cleaned.append(pdf)

        try:

            cleaned = check_duplicates(cleaned, ui)

        except Exception as e:

            ui.write_log(f"Duplicate check failed : {e}")

        output_pdf = os.path.join(folder, zip_name + ".pdf")

        try:

            merge_pdfs(

                cleaned,

                output_pdf,

                ui

            )

            merged += 1

            ui.write_log("Merged successfully.")

        except Exception as e:

            failed += 1

            ui.write_log(f"Merge failed : {e}")

        try:

            shutil.rmtree(extract_folder)

            ui.write_log("Temporary folder removed.")

        except Exception:

            pass

        processed += 1

        ui.update_overall(processed / total)

        ui.update_folder(0)

    ui.set_current_zip("Completed")

    ui.write_log("\n----------------------------")

    ui.write_log("Processing Complete")

    ui.write_log(f"ZIPs Processed : {processed}")

    ui.write_log(f"Merged PDFs    : {merged}")

    ui.write_log(f"Failed         : {failed}")

    ui.write_log("----------------------------")