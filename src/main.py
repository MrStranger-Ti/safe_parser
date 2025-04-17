import sys


def main() -> None:
    from src.parser.parser import SafeParser
    from src.excel.manager import ExcelManager
    from src import config

    parser = SafeParser(url=config.URL)
    rows = parser.get_data()

    with ExcelManager(rows=rows) as manager:
        manager.insert_rows()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Error: {exc}")
        input("Press Enter to close console...")
        sys.exit(1)
