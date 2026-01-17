textract
========

Simple extraction of text from image (PNG, JPEG, WEBP, GIF) or
text (PDF, DOCX, EPUB) files or web resources.

```
usage: textract [-h] [-o | -c] [--markdown] [-l LANGUAGES] [--gpu]
                [--apikey APIKEY]
                locations [locations ...]

Extract text from image or text files. Version 1.0.1

positional arguments:
  locations             Locations (URL or local filepath) of files.

options:
  -h, --help            show this help message and exit
  -o, --outfiles        Store results in files with same name but '.txt'.
  -c, --clipboard       Copy result to the clipboard.
  --markdown            Extract Markdown instead of plain text from text file.
  -l LANGUAGES, --languages LANGUAGES
                        String containing languages to use for OCR.
  --gpu                 Use GPU if present for OCR.
  --apikey APIKEY       API key to use for URLs.
```

Packages used
-------------
- [EasyOCR](https://pypi.org/project/easyocr/)
- [PyMuPDF](https://pypi.org/project/PyMuPDF/)
- [Pyperclip](https://pypi.org/project/pyperclip/)
- [requests](https://pypi.org/project/requests/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
