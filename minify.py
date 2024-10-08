import math
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2._page import PageObject
from pathlib import Path
from tqdm import tqdm
import math

A4_WIDTH, A4_HEIGHT = 595.28, 841.89
A5_WIDTH, A5_HEIGHT = 419.528, 595.276

PAGE_SCALE_MAP = {
  (A4_WIDTH, A4_HEIGHT): 0.25,
  (A5_WIDTH, A5_HEIGHT): 0.25*math.sqrt(2)
}

def minify(input_file: str, output_file: str):
    input_file = Path(input_file)
    output_file = Path(output_file)

    assert input_file.suffix == ".pdf" and input_file.is_file()
    assert output_file.suffix == ".pdf" and not output_file.is_file()

    with input_file.open("rb") as instream:
        reader = PdfFileReader(instream)

        height = float(reader.getPage(0).mediaBox.getHeight())
        width = float(reader.getPage(0).mediaBox.getWidth())

        stack_pages = math.ceil(reader.numPages / 32) * 2

        writer = PdfFileWriter()
        page_scale = PAGE_SCALE_MAP[tuple(sorted([height, width]))]

        for page_number in tqdm(range(stack_pages), "Minfying page"):

            new_page = PageObject.createBlankPage(None, A4_WIDTH, A4_HEIGHT)

            for inpage_pos in range(16):
                inpage_row = inpage_pos // 4
                inpage_col = inpage_pos % 4

                fn = identity if is_even(page_number) else reverse_row

                index = (inpage_row * 4 + fn(inpage_col)) * stack_pages + page_number

                old_page = (
                    reader.getPage(index)
                    if index < reader.numPages
                    else PageObject.createBlankPage(None, width, height)
                )
                tx = inpage_col * A4_WIDTH * 0.25
                ty = reverse_row(inpage_row) * A4_HEIGHT * 0.25

                new_page.mergeScaledTranslatedPage(old_page, scale=page_scale, tx=tx, ty=ty)

            writer.addPage(new_page)

        print("Saving minified document...")

        with output_file.open("wb") as outstream:
            writer.write(outstream)

    print("DONE!")


# helpers


def identity(x: int) -> int:
    return x


def reverse_row(x: int) -> int:
    return 3 - x


def is_even(x: int) -> bool:
    return x % 2 == 0


if __name__ == "__main__":
    minify("input.pdf", "minified.pdf")
