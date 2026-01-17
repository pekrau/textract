textract
========

Simple extraction of text from image (PNG, JPEG, WEBP, GIF) or
text (PDF, DOCX, EPUB) files or web resources.

```
usage: textract [-h] [-o | -c] [-l LANGUAGES] [-g] [-a APIKEY] locations [locations ...]

Extract text from image or text files.

positional arguments:
  locations             Locations (URL or local filepath) of files.

options:
  -h, --help            show this help message and exit
  -o, --outfiles        Store results in files with same name but '.txt'.
  -c, --clipboard       Copy result to the clipboard.
  -l LANGUAGES, --languages LANGUAGES
                        String containing languages to use.
  -g, --gpu             Use GPU if present.
  -a APIKEY, --apikey APIKEY
                        API key to use for URLs.
```

Packages used
-------------
- [EasyOCR](https://pypi.org/project/easyocr/)
- [PyMuPDF](https://pypi.org/project/PyMuPDF/)
- [Pyperclip](https://pypi.org/project/pyperclip/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
