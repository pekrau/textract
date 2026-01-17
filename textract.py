"textract: Extract text from various file formats."

from http import HTTPStatus as HTTP
import mimetypes
import os
from pathlib import Path
import sys
import tempfile
import uuid
import urllib.parse

import requests
import pyperclip

VERSION = "1.0.0"

PNG_MIMETYPE = "image/png"
JPEG_MIMETYPE = "image/jpeg"
WEBP_MIMETYPE = "image/webp"
GIF_MIMETYPE = "image/gif"
IMAGE_MIMETYPES = {
    PNG_MIMETYPE,
    JPEG_MIMETYPE,
    WEBP_MIMETYPE,
    GIF_MIMETYPE,
}

PDF_MIMETYPE = "application/pdf"
DOCX_MIMETYPE = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)
EPUB_MIMETYPE = "application/epub+zip"
TEXT_MIMETYPES = {
    PDF_MIMETYPE,
    DOCX_MIMETYPE,
    EPUB_MIMETYPE,
}


def main(locations, outfiles=False, clipboard=True, languages="sv en", gpu=True, apikey=None):
    "Process the content given by the locations (URL of local filepath)."
    clipboard_result = []
    for location in locations:
        try:
            filepath, name, mimetype = get_content_mimetype(location, apikey=apikey)
            if mimetype in IMAGE_MIMETYPES:
                text = extract_text_from_image(filepath, languages=languages.split(), gpu=gpu)
            elif mimetype in TEXT_MIMETYPES:
                text = extract_text_from_textfile(filepath)
        finally:
            filepath.unlink()
        if outfiles:
            Path(name).with_suffix(".txt").write_text(text)
        elif clipboard:
            clipboard_result.append(text)
        else:
            print(text)
    if clipboard_result:
        pyperclip.copy("\n\n".join(clipboard_result))


def get_content_mimetype(location, apikey=None):
    """Fetch the content from URL or local file.
    Return a tuple of (content filepath, name, mimetype).
    """
    parts = urllib.parse.urlparse(location)
    if parts.scheme:
        if apikey:
            headers = dict(apikey=apikey)
        else:
            headers = dict()
        response = requests.get(location, headers=headers)
        if response.status_code in (HTTP.BAD_GATEWAY, HTTP.SERVICE_UNAVAILABLE):
            raise IOError(f"invalid response: {response.status_code=}")
        elif response.status_code != HTTP.OK:
            raise IOError(f"invalid response: {response.status_code=} {response.content=}")
        content = response.content
        name = Path(parts.path).stem
        mimetype = response.headers["Content-Type"]
    else:
        location = Path(location)
        content = location.read_bytes()
        name = location.stem
        mimetype = mimetypes.guess_type(location)[0]

    filename = uuid.uuid4().hex + (mimetypes.guess_extension(mimetype) or ".bin")
    filepath = Path(tempfile.gettempdir()) / filename
    filepath.write_bytes(content)
    return (filepath, name, mimetype)


def extract_text_from_image(filepath, languages, gpu):
    import easyocr
    reader = easyocr.Reader(languages, gpu=gpu)
    text = reader.readtext(str(filepath), detail=0)
    return "\n".join(text)


def extract_text_from_textfile(filepath):
    import pymupdf
    text = []
    doc = pymupdf.open(str(filepath))
    for page in doc:
        text.append(page.get_text())
    doc.close()
    return "\n".join(text)


def extract_markdown_from_textfile(filepath):
    import pymupdf4llm
    return pymupdf4llm.to_markdown(str(filepath))


if __name__ == "__main__":
    import argparse
    import dotenv
    import os

    dotenv.load_dotenv()

    parser = argparse.ArgumentParser(
        prog="textract",
        description=f"Extract text from image or text files. Version {VERSION}")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-o", "--outfiles", action="store_true",
                        help="Store results in files with same name but '.txt'.")
    group.add_argument("-c", "--clipboard", action="store_true",
                        help="Copy result to the clipboard.")
    parser.add_argument("-l", "--languages", default="sv en",
                        help="String containing languages to use.")
    parser.add_argument("-g", "--gpu", action="store_true",
                        help="Use GPU if present.")
    parser.add_argument("-a", "--apikey", default=os.environ.get("APIKEY"),
                        help="API key to use for URLs.")
    parser.add_argument("locations", nargs="+",
                        help="Locations (URL or local filepath) of files.")
    args = parser.parse_args()
    main(**vars(args))
