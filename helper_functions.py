from pathlib import Path
from numpy import arange
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
import json
from openpyxl.drawing.image import Image
import os
import sys
import re


def apply_replacements(sql, brand=None, season=None, category=None, currency=None) -> str:
    replacements = {
        "{brand}": brand,
        "{season}": season,
        "{category}": category,
        "{currency}": currency,
    }

    for key, value in replacements.items():
        if value is not None:
            sql = sql.replace(key, value)

    return sql


def resize_image(image, new_width=None, new_height=None) -> Image:

    if new_width and not new_height:
        aspect_ratio = image.height / image.width
        new_height = int(new_width * aspect_ratio)

    elif new_height and not new_width:
        aspect_ratio = image.width / image.height
        new_width = int(new_height * aspect_ratio)

    image.width = new_width
    image.height = new_height

    return image


def get_sql_dataframe(sql: str):

    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    config_path = os.path.join(base_path, "config.json")

    with open(config_path) as config_file:
        config = json.load(config_file)

    try:
        DRIVER_NAME = "SQL SERVER"
        SERVER_NAME = "WHServer"
        DATABASE_NAME = "Warehouse"
        USERNAME = config["db_user"]
        PASSWORD = config["db_password"]

        connection_string = f"""
        DRIVER={{{DRIVER_NAME}}};
        SERVER={SERVER_NAME};
        DATABASE={DATABASE_NAME};
        UID={USERNAME};
        PWD={PASSWORD};
        """
        params = quote_plus(connection_string)

        engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
        with engine.connect() as conn:
            df = pd.read_sql_query(sql, conn)

        return df, None

    except SQLAlchemyError as e:
        error_message = f"SQLAlchemy Error: {str(e)}"
        return None, error_message
    except Exception as e:
        error_message = f"Error: {str(e)}"
        return None, error_message


def get_size_order(size_cat: str, use_size: str) -> list[str]:

    f0_sizes_in = [f"{x:.0f}" for x in arange(1.0, 1001.0, 1.0)]
    f1_sizes_in = [f"{x:.1f}" for x in arange(1.0, 100.1, 0.1)]
    f2_sizes_in = [f"{x:.2f}" for x in arange(1.0, 100.01, 0.01)]
    f3_sizes_in = [f"{x:.3f}" for x in arange(1.0, 100.001, 0.001)]

    in_sizes = f0_sizes_in + f1_sizes_in + f2_sizes_in + f3_sizes_in

    f0_sizes_mm = [f"{x:.0f}" for x in arange(1.0, 2001.0, 1.0)]
    f1_sizes_mm = [f"{x:.1f}" for x in arange(1.0, 2000.1, 0.1)]
    f2_sizes_mm = [f"{x:.2f}" for x in arange(1.0, 2000.01, 0.01)]
    f3_sizes_mm = [f"{x:.3f}" for x in arange(1.0, 2000.001, 0.001)]

    fractions_mm = [
        "1/8",
        "1/4",
        "1/2",
        "5/8",
        "3/4",
        "7/8",
        "1 1/8",
        "1 1/4",
        "1 3/8",
        "1 1/2",
    ]

    in_sizes = sorted(f0_sizes_in + f1_sizes_in + f2_sizes_in + f3_sizes_in, key=lambda x: float(x))

    mm_sizes = sorted(f0_sizes_mm + f1_sizes_mm + f2_sizes_mm + f3_sizes_mm, key=lambda x: float(x))

    mm_sizes = fractions_mm + mm_sizes

    adult_footwear_sizes = [
        "3",
        "3.5",
        "4",
        "4.5",
        "5",
        "5.5",
        "6",
        "6.5",
        "7",
        "7.5",
        "8",
        "8.5",
        "9",
        "9.5",
        "10",
        "10.5",
        "11",
        "11.5",
        "12",
        "12.5",
        "13",
        "13.5",
    ]
    youth_footwear_sizes = [
        "10",
        "10.5",
        "11",
        "11.5",
        "12",
        "12.5",
        "13",
        "13.5",
        "1",
        "2",
        "3",
        "4",
        "5",
    ]

    size_cat_order = {
        "Accessory": ["O/S", "OS", "OSFA", "4-7", "8-11", ""],
        "Pants": [
            "25/28",
            "25/30",
            "26/30",
            "26/32",
            "27/30",
            "27/32",
            "28/30",
            "28/32",
            "29/30",
            "29/32",
            "30/32",
            "31/32",
            "32/32",
            "33/32",
            "34/32",
            "34/34",
            "36/32",
            "36/34",
        ],
        "Women": ["4", "6", "8", "10", "12", "14", "16", "18", "20", "22", "24", "26"],
        "Adult": ["XXXS", "XXS", "XS", "S", "M", "L", "XL", "XXL", "XXXL", "XXXXL"],
        "Youth": ["4-6", "6-8", "8-10", "10-12", "12-14", "14-16"],
        "Waist": ["26", "28", "30", "32", "34", "36", "38", "40"],
        "Adult /": ["XXS/XS", "XS/S", "S/M", "M/L", "L/XL", "XL/XXL", "XXL/XXXL"],
        "Footwear": adult_footwear_sizes,
        "Yth Footwear": youth_footwear_sizes,
        "Heelys": adult_footwear_sizes,
        "Yth Heelys": youth_footwear_sizes,
        "SWS": adult_footwear_sizes,
        "Yth SWS": youth_footwear_sizes,
        "Rollerskates": adult_footwear_sizes,
        "Yth Rollerskates": youth_footwear_sizes,
        "IN": in_sizes,
        "MM": mm_sizes,
        "CM": mm_sizes,
    }

    yth_eu_footwear = [
        "28",
        "28.5",
        "29",
        "29.5",
        "30",
        "30.5",
        "31",
        "31.5",
        "32",
        "32.5",
        "33",
        "33.5",
        "34",
        "34.5",
        "35",
        "35.5",
        "36",
        "36.5",
        "37",
        "37.5",
        "38",
        "38.5",
        "39",
        "39.5",
        "40",
    ]

    adult_eu_footwear = [
        "36",
        "36.5",
        "37",
        "37.5",
        "38",
        "38.5",
        "39",
        "39.5",
        "40",
        "40.5",
        "41",
        "41.5",
        "42",
        "42.5",
        "43",
        "43.5",
        "44",
        "44.5",
        "45",
        "45.5",
        "46",
        "46.5",
        "47",
        "47.5",
        "48",
        "48.5",
        "49",
        "49.5",
        "50",
    ]

    yth_us_rollerskates = [
        "1M/2W",
        "1.5M/2.5W",
        "2M/3W",
        "2.5M/3.5W",
        "3M/4W",
        "3.5M/4.5W",
        "4M/5W",
        "4.5M/5.5W",
        "5M/6W",
        "5.5M/6.5W",
        "6M/7W",
    ]

    adult_us_rollerskates = [
        "1M/2W",
        "1.5M/2.5W",
        "2M/3W",
        "2.5M/3.5W",
        "3M/4W",
        "3.5M/4.5W",
        "4M/5W",
        "4.5M/5.5W",
        "5M/6W",
        "5.5M/6.5W",
        "6M/7W",
        "6.5M/7.5W",
        "7M/8W",
        "7.5M/8.5W",
        "8M/9W",
        "8.5M/9.5W",
        "9M/10W",
        "9.5M/10.5W",
        "10M/11W",
        "10.5M/11.5W",
        "11M/12W",
        "11.5M/12.5W",
        "12M/13W",
        "12.5M/13.5W",
        "13M/14W",
        "13.5M/14.5W",
        "14M/15W",
    ]

    if use_size == "EU":

        size_cat_order["Yth Footwear"] = adult_eu_footwear + adult_footwear_sizes
        size_cat_order["Yth Footwear"] = yth_eu_footwear + youth_footwear_sizes
        size_cat_order["Heelys"] = adult_eu_footwear + adult_footwear_sizes
        size_cat_order["Yth Heelys"] = yth_eu_footwear + youth_footwear_sizes
        size_cat_order["SWS"] = adult_eu_footwear + adult_footwear_sizes
        size_cat_order["Yth SWS"] = yth_eu_footwear + youth_footwear_sizes
        size_cat_order["Rollerskates"] = adult_eu_footwear + adult_footwear_sizes
        size_cat_order["Yth Rollerskates"] = yth_eu_footwear + youth_footwear_sizes

    if use_size == "US":
        size_cat_order["Rollerskates"] = adult_us_rollerskates + adult_footwear_sizes
        size_cat_order["Yth Rollerskates"] = yth_us_rollerskates + youth_footwear_sizes

    return size_cat_order.get(size_cat, [])


def get_brand_image(brand: str) -> Path:

    brand_images = {
        "Arbor": "Arbor_MainLogo 2000px.jpg",
        "Arbor Apparel": "Arbor_MainLogo 2000px.jpg",
        "Birdhouse": "Birdhouse_sticker.jpg",
        "Feiyue": "Feiyue_MainLogo 2000px.jpg",
        "Heelys": "Heelys_MainLogo 2000px.jpg",
        "Independent Apparel": "IN_Span_Logo_Black 2000px.jpg",
        "Bronson Speed Co.": "Bronson Speed Co Round Logo.jpg",
        "Bullet Safety Gear": "Bullet Safety Gear Logo - Black.jpg",
        "Bullet": "Bullet Safety Gear Logo - Black.jpg",
        "Creature": "Creature-Green.jpg",
        "Krux": "Krux Logo Blue on Trans.png",
        "MOB": "MOB Grip Black on White.jpg",
        "OJ Wheels": "OJ.jpg",
        "Ricta": "ricta_Logo.jpg",
        "Addict": "Addict Simple Logo.jpg",
        "Blazer Pro": "BlazerPro-2016-black.jpg",
        "Chopsticks Scooter Wheel": "Chopsticks Logo.jpg",
        "Clouds Urethane": "Clouds-2016.png",
        "Eagle Supply": "Eagle Supply - W_Eagle5.jpg",
        "Rookie": "Rookie Logo.jpg",
        "Santa Cruz Apparel": "SC_ClassicDot_Logo 1000px.jpg",
        "Santa Cruz": "SC_ClassicDot_Logo 1000px.jpg",
        "187": "187-Logo.jpg",
        "Anti Hero": "AntiHero.Eagle.jpg",
        "D-street": "D Street - black.jpg",
        "Jessup": "Jessup.Red.jpg",
        "Krooked": "Krooked.Black.jpg",
        "Pro-Tec": "Pro-Tec-2017-Logo-Wordmark-Black-on-White.jpg",
        "Real": "Real.jpg",
        "Spitfire": "Spitfire-Bighead-Logo.jpg",
        "Thunder": "TH-Charged-Logo-2019.jpg",
        "Thrasher": "Thrasher-Classic-Logo-black-on-white.jpg",
        "Tony Hawk": "Tony-Hawk-Signature-Series-Red-on-White.jpg",
    }

    if brand in brand_images:
        return Path(brand_images[brand])
    else:
        return Path("SHINER_LOGO_BLK_GEN.png")


def validate_file_name_and_path(file_name: str, error_file_name: str, folder_path: str) -> tuple[bool, str]:

    invalid_file_name_pattern = r'[<>:"/\\|?*]'

    if not os.path.isdir(folder_path):
        return False, "The specified folder path does not exist."

    if re.search(invalid_file_name_pattern, file_name):
        return False, "The file name contains invalid characters."

    if re.search(invalid_file_name_pattern, error_file_name):
        return False, "The error file name contains invalid characters."

    if not file_name.strip():
        return False, "The file name cannot be empty."

    if not error_file_name.strip():
        return False, "The error file name cannot be empty."

    return True, ""
