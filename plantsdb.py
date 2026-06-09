import sqlite3

DB = "plants.db"
DEFAULT_INPUT = {"temp_max": 40.0, "temp_min": 0.0, "water_amount": 100}


def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS plants_data(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                scientific_name TEXT DEFAULT "",
                temp_max REAL DEFAULT 40.0,
                temp_min REAL DEFAULT 0.0,
                grow_pattern TEXT,
                water_amount REAL DEFAULT 100,
                fertilizer TEXT,
                plant TEXT,
                harvest TEXT
            )
        """)


def save_plants(plants_dict):
    with sqlite3.connect(DB) as conn:
        columns = ", ".join(plants_dict.keys())

        placeholders = ", ".join(f":{k}" for k in plants_dict.keys())

        updates = ", ".join(
            f"{k}=excluded.{k}" for k in plants_dict.keys() if k != "name"
        )

        query = f"""
        INSERT INTO plants_data ({columns})
        VALUES ({placeholders})
        ON CONFLICT(name)
        DO UPDATE SET {updates}
        """

        conn.execute(query, plants_dict)


def check_input(input_data):
    if input_data == "":
        return False
    return True


def Input_plants_data():
    name = input("Input name (*text): ")
    scientific_name = input("Scientific_name (text): ")
    temp_max = input("Temperture Max (float): ")
    if check_input(temp_max):
        temp_max = float(temp_max)
    else:
        temp_max = DEFAULT_INPUT["temp_max"]
    temp_min = input("Temperture min (float): ")
    if check_input(temp_min):
        temp_min = float(temp_min)
    else:
        temp_min = DEFAULT_INPUT["temp_min"]
    grow_pattern = input("Growing pattern (text):")
    water_amount = input("Watering amount (float): ")
    if check_input(water_amount):
        water_amount = float(water_amount)
    else:
        water_amount = DEFAULT_INPUT["water_amount"]
    fertilizer = input("Fertilizer (text): ")
    plant = input("When Plants (text): ")
    harvest = input("When Harvest (text): ")

    plants_dict = {}
    plants_dict["name"] = name
    plants_dict["scientific_name"] = scientific_name
    plants_dict["temp_max"] = temp_max
    plants_dict["temp_min"] = temp_min
    plants_dict["grow_pattern"] = grow_pattern
    plants_dict["water_amount"] = water_amount
    plants_dict["fertilizer"] = fertilizer
    plants_dict["plant"] = plant
    plants_dict["harvest"] = harvest
    return plants_dict


def show_data(keyword=None):
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()

        if keyword == None:
            cursor.execute("""
                SELECT * FROM plants_data ORDER BY name
            """)
        else:
            cursor.execute(
                """
                SELECT * FROM plants_data WHERE name like ?
            """,
                # part match
                (f"%{keyword}%",),
            )
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        if not rows:
            print("No data found.")
            return
        # max width for each column
        col_widths = [
            max(len(str(row[i])) for row in rows + [columns])
            for i in range(len(columns))
        ]

        # header
        header = " | ".join(
            f"{col:<{width}}" for col, width in zip(columns, col_widths)
        )
        print(header)
        print("-" * len(header))

        # data rows
        for row in rows:
            print(
                " | ".join(
                    f"{str(item):<{width}}" for item, width in zip(row, col_widths)
                )
            )


def search_data(keyword):
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()

        response = cursor.execute(
            """
            SELECT * FROM plants_data WHERE name like ?
        """,
            # part match
            (f"%{keyword}%",),
        )
        result = response.fetchone()
    print(result)


def delete_data(item_name):
    with sqlite3.connect(DB) as conn:
        conn.execute(
            """
            DELETE FROM plants_data
            WHERE name = ?
            """,
            (item_name,),
        )
    print("Deleted data successfully")


if __name__ == "__main__":
    init_db()
    show_data()
