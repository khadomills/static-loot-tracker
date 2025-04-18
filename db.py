import sqlite3

DB_PATH = "loot.db"


# loot identifiers: 0 - crafted gear, 1 - tome gear, 2 - upgraded tome gear, 3 - raid gear
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
                weapon INTEGER,
                head INTEGER,
                body INTEGER,
                chest INTEGER,
                gloves INTEGER,
                feet INTEGER,
                earring INTEGER,
                neck INTEGER,
                wrist INTEGER,
                ring1 INTEGER,
                ring2 INTEGER
            );
        """)

        conn.commit()

def add_member(
    name,
    job,
    priority=0,
    weapon=None,
    head=None,
    body=None,
    chest=None,
    gloves=None,
    feet=None,
    earring=None,
    neck=None,
    wrist=None,
    ring1=None,
    ring2=None
):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO member (
                name, job, priority,
                weapon, head, body, chest,
                gloves, feet,
                earring, neck, wrist,
                ring1, ring2
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name, job, priority,
            weapon, head, body, chest,
            gloves, feet,
            earring, neck, wrist,
            ring1, ring2
        ))
        conn.commit()