from src import config
from src.parser.parser import SafeParser
from src.excel.manager import ExcelManager


def main() -> None:
    parser = SafeParser(url=config.URL)
    rows = parser.get_data()

    with ExcelManager(rows=rows) as manager:
        manager.insert_rows()


if __name__ == "__main__":
    main()
