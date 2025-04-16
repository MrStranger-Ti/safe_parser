from xml.etree.ElementTree import Element

from lxml.etree import iterparse as ip
from tqdm import tqdm

PRODUCTS_PARSING_CONFIG = dict(
    bar_format="{postfix[0]}: {postfix[value]}",
    postfix={0: "Products parsed", "value": 0},
    leave=False,
)

CREATING_EXCEL_CONFIG = dict(
    bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}",
    ncols=100,
    desc="Inserting products into the excel file",
)


class ProductsIterator:
    def __init__(self, iterparse: ip):
        self.iterparse: ip = iterparse
        self.t = tqdm(**PRODUCTS_PARSING_CONFIG)

    def __iter__(self) -> "XMLTreeProductsIterator":
        return self

    def __next__(self) -> tuple[str, Element]:
        event, element = next(self.iterparse)
        if event == "end" and element.tag == "item":
            self.t.postfix["value"] += 1
            self.t.update()

        return event, element
