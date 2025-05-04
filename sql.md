# Database Setup

### bot uses a sqlite3 database

`config.db`
```sql
CREATE TABLE config (
    id INTEGER PRIMARY KEY,
    server INTEGER,
    key TEXT,
    value TEXT,
    single INTEGER DEFAULT 0,
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

config keys used:
(roles and channels are IDs)
(emotes are also IDs unless they are standard emoji)
| key | description |
| --- | --- |
| moderator_role | moderator roles |
| caps_prot_immune_channels | channels where caps aren't checked |
| caps_prot_immune_role | roles who don't have caps checked |
| caps_prot_message | message to users who use too many caps |
| caps_prot_percent | percentage of message that has to be caps to catch |
| country_flag | all country flags for banning from no_flag_channel |
| no_flag_channel | channels to not allow country flag reactions |
| banned_emote | emotes to automatically remove |
| full_react_channel | forum channels where new threads should get all forum reacts |
| full_react_emote | emotes to react to new threads in full_react_channels |
| half_react_channel | forum channels to receive half forum reacts |
| half_react_emote | emotes to react to new thread in half_react_channels |
