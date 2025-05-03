# Database Setup

### bot uses a sqlite3 database

`config.db`
```sql
CREATE TABLE config (
    id INTEGER PRIMARY KEY,
    server TEXT,
    key TEXT,
    value TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    updater TEXT DEFAULT ''
);

CREATE TRIGGER [UPDATE_DT]
    AFTER UPDATE ON config FOR EACH ROW
    WHEN OLD.timestamp = NEW.timestamp OR OLD.timestamp IS NULL
BEGIN
    UPDATE config SET timestamp = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
```
