import sqlite3

DB_PATH = "loot.db"


# loot identifiers: 0 - crafted gear, 1 - tome gear, 2 - normal raid gear, 3 - upgraded tome gear, 4 - raid gear, 5 - trial gear
# priority identifiers 1 - Carry dps 1, 2 - Carry dps 2, 3 - group 1 second dps, 4 - group 2 second dps, 5 - Group 1 tank, 6 - Group 2 tank, 7 - Group 1 healer, 8- Group 2 healer
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS member (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                job TEXT NOT NULL,
                priority INTEGER DEFAULT 0,
                curr_weapon INTEGER,
                bis_weapon INTEGER,
                curr_head INTEGER,
                bis_head INTEGER,
                curr_body INTEGER,
                bis_body INTEGER,
                curr_gloves INTEGER,
                bis_gloves INTEGER,
                curr_feet INTEGER,
                bis_feet INTEGER,
                curr_earring INTEGER,
                bis_earring INTEGER,
                curr_neck INTEGER,
                bis_neck INTEGER,
                curr_wrist INTEGER,
                bis_wrist INTEGER,
                curr_ring1 INTEGER,
                bis_ring1 INTEGER,
                curr_ring2 INTEGER,
                bis_ring2 INTEGER
            );
        """)

        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS settings (
                        static_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        setup_complete BOOLEAN NOT NULL,
                        static_type INTEGER NOT NULL
                    );
                """)

        conn.commit()


def add_member(
    name,
    job,
    priority,
    curr_weapon,
    bis_weapon,
    curr_head,
    bis_head,
    curr_body,
    bis_body,
    curr_gloves,
    bis_gloves,
    curr_feet,
    bis_feet,
    curr_earring,
    bis_earring,
    curr_neck,
    bis_neck,
    curr_wrist,
    bis_wrist,
    curr_ring1,
    bis_ring1,
    curr_ring2,
    bis_ring2
):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO member (
                name, job, priority,
                curr_weapon, bis_weapon,
                curr_head, bis_head,
                curr_body, bis_body,
                curr_gloves, bis_gloves,
                curr_feet, bis_feet,
                curr_earring, bis_earring,
                curr_neck, bis_neck,
                curr_wrist, bis_wrist,
                curr_ring1, bis_ring1,
                curr_ring2, bis_ring2
            ) VALUES (?, ?, ?,
                      ?, ?,
                      ?, ?,
                      ?, ?,
                      ?, ?,
                      ?, ?,
                      ?, ?,
                      ?, ?,
                      ?, ?,
                      ?, ?,
                      ?, ?)
        """, (
            name, job, priority,
            curr_weapon, bis_weapon,
            curr_head, bis_head,
            curr_body, bis_body,
            curr_gloves, bis_gloves,
            curr_feet, bis_feet,
            curr_earring, bis_earring,
            curr_neck, bis_neck,
            curr_wrist, bis_wrist,
            curr_ring1, bis_ring1,
            curr_ring2, bis_ring2
        ))
        conn.commit()

def set_type(static_type):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
               INSERT INTO settings (setup_complete, static_type
               ) VALUES (?,?)
        """, (False, static_type
              ))
        conn.commit()
        if static_type == 1:
            print("Static type set to Regular")
        else:
            print("Static type set to Splits")


def check_type():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT static_type FROM settings")
        for row in cursor:
            return row[0]
