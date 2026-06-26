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
                grow_pattern TEXT DEFAULT None,
                water_amount REAL DEFAULT 100,
                fertilizer INEGER DEFAULT None,
                sow_start INTEGER DEFAULT None,
                sow_end INTEGER DEFAULT None,
                harvest_start INTEGER DEFAULT None,
                harvest_end INTEGER DEFAULT None
            )
        """)


# favorite table
def init_fav_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS plants_fav_data(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                scientific_name TEXT,
                temp_max REAL,
                temp_min REAL,
                grow_pattern TEXT,
                water_amount REAL,
                fertilizer INEGER,
                sow_start INTEGER,
                sow_end INTEGER,
                harvest_start INTEGER,
                harvest_end INTEGER
            )
        """)


def save_plants(plants_dict, table="plants_data", database=DB):
    with sqlite3.connect(database) as conn:
        columns = ", ".join(plants_dict.keys())

        placeholders = ", ".join(f":{k}" for k in plants_dict.keys())

        updates = ", ".join(
            f"{k}=excluded.{k}" for k in plants_dict.keys() if k != "name"
        )

        query = f"""
        INSERT INTO {table} ({columns})
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
    fertilizer = input("Fertilizer (int): ")
    sow_start = input("Sowing start month(int): ")
    sow_end = input("Sowing end month(int): ")
    harvest_start = input("When Harvest start(int): ")
    harvest_end = input("When Harvest end(int): ")
    plants_dict = {}
    plants_dict["name"] = name
    plants_dict["scientific_name"] = scientific_name
    plants_dict["temp_max"] = temp_max
    plants_dict["temp_min"] = temp_min
    plants_dict["grow_pattern"] = grow_pattern
    plants_dict["water_amount"] = water_amount
    plants_dict["fertilizer"] = fertilizer
    plants_dict["sow_start"] = sow_start
    plants_dict["sow_end"] = sow_end
    plants_dict["harvest_start"] = harvest_start
    plants_dict["harvest_end"] = harvest_end
    return plants_dict


def get_data(keyword=None, table="plants_data", database=DB):
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()

        if keyword:
            cursor.execute(
                f"""
                SELECT * FROM {table}
                WHERE name LIKE ?
                ORDER BY name
                """,
                (f"%{keyword}%",),
            )
        else:
            cursor.execute(f"""
                SELECT * FROM {table}
                ORDER BY name
                """)

        columns = [d[0] for d in cursor.description]
        rows = cursor.fetchall()

        return rows, columns


def search_data(keyword, table="plants_data", database=DB):
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()

        response = cursor.execute(
            f"""
            SELECT * FROM {table} WHERE name like ?
        """,
            # part match
            (f"%{keyword}%",),
        )

def delete_data(item_name, table="plants_data", database=DB):
    with sqlite3.connect(database) as conn:
        conn.execute(
            f"""
            DELETE FROM {table}
            WHERE name = ?
            """,
            (item_name,),
        )


def add_favorite(name):
    with sqlite3.connect(DB) as conn:
        conn.execute(
            """
            INSERT INTO plants_fav_data
            SELECT *
            FROM plants_data
            WHERE name = ?
            """,
            (name,),
        )


def get_temp_rows(keyword=None, table="plants_data", database=DB):
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()

        if keyword is None:
            cursor.execute(f"""
                SELECT name, temp_min, temp_max
                FROM {table}
                ORDER BY name
            """)
        else:
            cursor.execute(
                f"""
                SELECT name, temp_min, temp_max
                FROM {table}
                WHERE name LIKE ?
                ORDER BY name
                """,
                (f"%{keyword}%",),
            )

        rows = cursor.fetchall()
        return rows


def get_gantt_data(keyword, table="plants_data", database=DB):
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()

        if keyword is None:
            return
        else:
            cursor.execute(
                f"""
                SELECT name, fertilizer, sow_start, sow_end, harvest_start, harvest_end
                FROM {table}
                WHERE name LIKE ?
                """,
                (f"%{keyword}%",),
            )

        rows = cursor.fetchall()
        return rows


if __name__ == "__main__":
    init_db()
