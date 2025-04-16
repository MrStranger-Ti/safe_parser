import io
import logging
from typing import Any

from lxml import etree

from src.parser.abstract import XMLParser
from src.utils.tqdm import ProductsIterator

log = logging.getLogger(__name__)


class SafeParser(XMLParser):
    CATEGORY_DEPTH = 1

    def _parse(self, xml: bytes) -> Any:
        items_rows = []
        section_depth = 0
        depth_category = {}

        products_iter = etree.iterparse(io.BytesIO(xml), events=("end", "start"))
        for event, element in ProductsIterator(iterparse=products_iter):
            if event == "start":
                if element.tag == "sections":
                    section_depth += 1

                elif element.tag == "section":
                    depth_category[section_depth] = element.find("name").text

            elif event == "end":
                if element.tag == "sections":
                    section_depth -= 1

                elif element.tag == "item":
                    item_data = {
                        item.tag: item.text if item.text else ""
                        for item in element.findall("*")
                    }
                    item_data["category"] = depth_category[self.CATEGORY_DEPTH]
                    formated_row = self.process_formatters(item_data)
                    items_rows.append(formated_row)

                    element.clear()

                    product_name = formated_row.get("name", "Noname")
                    log.info(f"Product {product_name!r} was parsed")

        return items_rows
