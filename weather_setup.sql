CREATE TABLE IF NOT EXISTS 'weather' (
    'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    'location' REAL NOT NULL,
    'date' TEXT NOT NULL,
    'temperature' REAL NOT NULL,
    'humidity' REAL NOT NULL,
    'pressure' REAL NOT NULL 
);