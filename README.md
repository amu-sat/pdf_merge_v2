# ZIP PDF Merger

A lightweight Windows application that automatically converts ZIP archives of PDFs into merged PDF documents.

## Features

- Browse for a main folder
- Detect all ZIP files
- Extract each ZIP into a temporary folder
- Recursively locate every PDF
- Merge PDFs in natural filename order
- Save merged PDF as the ZIP filename
- Automatically delete extracted folders after processing
- Continue processing if one ZIP fails

## Example

Input:

```
Books/
    Physics.zip
    Chemistry.zip
    Maths.zip
```

Output:

```
Books/
    Physics.zip
    Chemistry.zip
    Maths.zip

    Physics.pdf
    Chemistry.pdf
    Maths.pdf
```

## Build

```
pip install -r requirements.txt
build.bat
```

or

```
pyinstaller --onefile --windowed app.py
```