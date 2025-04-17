import re

import bs4

from src.parser.format.base import BaseFormatter
from src.utils.format import clear_html_entity


class DefaultFieldsFormatter(BaseFormatter):
    def format(self, data: dict[str, str]) -> dict[str, str]:
        return {
            "vat": "20",
            "available": "под заказ",
            "unit_measurement": "Шт",
        }


class SimpleFieldsFormatter(BaseFormatter):
    SIMPLE_FIELDS = [
        "id",
        "name",
        "manufacturer",
        "price22",
        "vat",
        "category",
        "images",
        "warranty",
        "country",
        "unit_measurement",
        "available",
        "weight",
        "outer_depth",
        "outer_width",
        "outer_height",
    ]

    def format(self, data: dict[str, str]) -> dict[str, str]:
        simple_data = {
            name: value.strip("-")
            for name, value in data.items()
            if name in self.SIMPLE_FIELDS
        }

        if simple_data.get("warranty"):
            simple_data["warranty"] = "Да"
        else:
            simple_data.update({"warranty": "Нет"})

        if id_ := simple_data.get("id"):
            simple_data["id"] = id_ + "S"

        return simple_data


class DescriptionFormatter(BaseFormatter):
    DESCRIPTION_FIELDS = [
        "preview_text",
        "detail_text",
    ]

    VALID_HTML_TAGS = ["p", "h2", "ul", "ol", "li", "br"]

    def format(self, data: dict[str, str]) -> dict[str, str]:
        for descr_field in self.DESCRIPTION_FIELDS:
            descr = data.get(descr_field)
            if descr:
                return {"description": self.clear(descr)}

        return {}

    def clear(self, text: str) -> str:
        cleared_text_from_entity = clear_html_entity(text)
        soup = bs4.BeautifulSoup(cleared_text_from_entity, "lxml")
        for tag in soup.find_all(True):
            if tag.name not in self.VALID_HTML_TAGS:
                tag.unwrap()

        return str(soup)


class CharacteristicsFormatter(BaseFormatter):
    CHARACTERISTICS_MAPPINGS = {
        "bacterial_effectiv": "Бактериальная эффективность, %",
        "volume_keys": "Вместимость (количество ключей, шт)",
        "volume_box": "Вместимость, количество папок Корона (75мм)",
        "outer_height": "Внешняя высота",
        "outer_depth": "Внешняя глубина",
        "outer_width": "Внешняя ширина",
        "in_compartments": "Внутренние размеры отделений (ВхШхГ), мм",
        "volume_cell": "Внутренние размеры ячеек, мм (ВхШхГ)",
        "inside_sizes": "Внутренние размеры ящика, мм (ВхШхГ)",
        "inner_height": "Внутренняя высота",
        "inner_depth": "Внутренняя глубина",
        "inner_width": "Внутренняя ширина",
        "mount": "Возможность крепления",
        "height_on_floor": "Высота от пола до лежака",
        "seat_height": "Высота сиденья (min-max), мм",
        "size_heel": "Габаритные размеры с учетом подпятников, мм (ВхШхГ)",
        "dimensions_of_upper_section": "Габариты верхней секции (ВхШхГ), мм",
        "dimensions_of_lower_section": "Габариты нижней секции",
        "lock_warranty": "Гарантия на замок",
        "seat_size": "Глубина и ширина сиденья, мм",
        "permissible_static_load": "Допустимая нагрузка",
        "volume_deposit": "Емкость депозитной кассеты",
        "frame": "Каркас",
        "crack_resistance_class": "Класс взломостойкости",
        "fire_resistance_class": "Класс огнестойкости",
        "class_of_weapon_safes": "Класс оружейных сейфов",
        "num_door": "Количество дверей",
        "number_locks": "Количество замков",
        "number_lamps": "Количество ламп",
        "shelves_number": "Количество полок",
        "num_sections": "Количество секций",
        "num_wells": "Количество скважин на ячейку",
        "number_of_barrels": "Количество стволов",
        "number_storage": "Количество ярусов хранения",
        "num_cell": "Количество ячеек",
        "num_box": "Количество ящиков",
        "cross": "Крестовина",
        "height_of_barrel": "Максимальная высота ствола, мм",
        "max_load": "Максимальная нагрузка",
        "max_load_shelf": "Максимальная нагрузка на полку, кг",
        "maximum_load_on_the_rack": "Максимальная нагрузка на стеллаж, кг",
        "max_load_shelf_kg": "Максимальная нагрузка на ящик, кг",
        "master_lock": "Мастер-ключ",
        "material": "Материал",
        "mechanism": "Механизм",
        "power_lamp": "Мощность одной лампы, Вт",
        "table_top_load": "Нагрузка на столешницу",
        "nalichie_spinki": "Наличие спинки",
        "nds_not_apply": "Не облагается НДС",
        "load_on_bed": "Номинальная нагрузка на ложе",
        "upholstery": "Обивка",
        "volume": "Объём, л",
        "cartridge": "Патронное отделение (трейзер)",
        "armrest": "Подлокотники",
        "runners": "Полозья",
        "programm_open": "Программируемая задержка открывания",
        "productivity": "Производительность, м3/час",
        "dimensions_of_adjustable_sections": "Размеры регулируемых секций",
        "treyzer_size": "Размеры трейзера, мм (ВхШхГ)",
        "dimension_case": "Размеры ячейки, мм (ВхШхГ)",
        "consumption_energy": "Расход электроэнергии за сутки, кВт*час/сутки (при Т окружающей среды +25°С)",
        "recom_room_volume": "Рекомендуемый объем помещения, м3",
        "temperature": "Температурный интервал, °С",
        "lock_type": "Тип замка",
        "cover_type": "Тип покрытия",
        "section_type": "Тип секции",
        "angles_of_the_sections": "Углы наклона секций",
        "angle": "Угол наклона подголовника",
        "noise": "Уровень шумов",
        "sealing": "Устройство для опечатывания",
        "format_doc": "Формат документов",
        "color": "Цвет",
        "color_frame": "Цвет каркаса",
        "color_upholstery": "Цвет обивки",
        "color_tabletop": "Цвет столешницы",
        "power_supply": "Электропитание, В/Гц",
    }

    def format(self, data: dict[str, str]) -> dict[str, str]:
        characteristics = [
            f"{self.CHARACTERISTICS_MAPPINGS[name]}|{value};"
            for name, value in data.items()
            if name in self.CHARACTERISTICS_MAPPINGS
        ]
        return {"characteristics": "".join(characteristics)}


class ImagesFormatter(BaseFormatter):
    IMAGES_FIELDS = [
        "preview_picture",
        "detail_picture",
        "additional_photo",
    ]

    def format(self, data: dict[str, str]) -> dict[str, str]:
        images = [
            value
            for name, value in data.items()
            if name in self.IMAGES_FIELDS and value
        ][:10]
        return {"images": ",".join(images)}
