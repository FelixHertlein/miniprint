import math
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2._page import PageObject
from pathlib import Path
from tqdm import tqdm


def read_num_pages(input_file: Path) -> int:
    assert input_file.suffix == ".pdf" and input_file.is_file()

    with input_file.open("rb") as instream:
        reader = PdfFileReader(instream)
        return reader.numPages


def create_rearrangement(num_pages: int) -> list[int]:
    def identity(x):
        return x

    def reverse_row(x):
        return 3 - x

    def is_even(x):
        return x % 2 == 0

    rearranged_indicies = []
    stack_pages = math.ceil(num_pages / 16)

    for i in range(stack_pages * 16):
        page_no = i // 16
        inpage_pos = i % 16
        inpage_row = inpage_pos // 4
        inpage_col = inpage_pos % 4

        fn = identity if is_even(page_no) else reverse_row

        index = (inpage_row * 4 + fn(inpage_col)) * stack_pages + page_no

        rearranged_indicies.append(index)

    assert set(rearranged_indicies) == set(range(stack_pages * 16))

    return rearranged_indicies


def create_minfied(input_file: Path, output_file: Path, rearranged_indicies: list[int]):
    assert input_file.suffix == ".pdf" and input_file.is_file()
    assert output_file.suffix == ".pdf"

    with input_file.open("rb") as instream:
        reader = PdfFileReader(instream)

        height = float(reader.getPage(0).mediaBox.getHeight())
        width = float(reader.getPage(0).mediaBox.getWidth())

        writer = PdfFileWriter()
        scale = 0.25

        for i, j in enumerate(tqdm(rearranged_indicies, "Minfying page")):
            if i % 16 == 0:
                new_page = PageObject.createBlankPage(None, width, height)

            inpage_pos = i % 16
            inpage_row = inpage_pos // 4
            inpage_col = inpage_pos % 4

            old_page = (
                reader.getPage(j)
                if j < reader.numPages
                else PageObject.createBlankPage(None, width, height)
            )
            tx = inpage_col * width * scale
            ty = (3 - inpage_row) * height * scale

            new_page.mergeScaledTranslatedPage(old_page, scale=scale, tx=tx, ty=ty)

            if i % 16 == 0:
                writer.addPage(new_page)

        print("Saving minified document...")

        with output_file.open("wb") as outstream:
            writer.write(outstream)


def minify(input_file: str, output_file: str):
    input_file = Path(input_file)
    output_file = Path(output_file)

    num_pages = read_num_pages(input_file=input_file)
    rearranged_indicies = create_rearrangement(num_pages)
    create_minfied(
        input_file=input_file,
        output_file=output_file,
        rearranged_indicies=rearranged_indicies,
    )

    print("DONE!")


if __name__ == "__main__":
    minify("input.pdf", "minified.pdf")
