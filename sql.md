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

---

config keys used:
(roles and channels are IDs)
(emotes are also IDs unless they are standard emoji)
| key | description | used by | single (no unless marked) |
| --- | --- | --- | --- |
| moderator_role | moderator roles | MiscCog |
| caps_prot_immune_channel | channels where caps aren't checked | MiscCog |
| caps_prot_immune_role | roles who don't have caps checked | MiscCog |
| caps_prot_message | message to users who use too many caps | MiscCog | y |
| caps_prot_percent | percentage of message that has to be caps to catch | MiscCog | y |
| country_flag | all country flags for banning from no_flag_channel | ReactionsCog |
| no_flag_channel | channels to not allow country flag reactions | ReactionsCog |
| banned_emote | emotes to automatically remove | ReactionsCog |
| full_react_channel | forum channels where new threads should get all forum reacts | ReactionsCog |
| full_react_emote | emotes to react to new threads in full_react_channels | ReactionsCog |
| half_react_channel | forum channels to receive half forum reacts | ReactionsCog |
| half_react_emote | emotes to react to new thread in half_react_channels | ReactionsCog |
| reaction_role_users | users who can grant a role with a reaction | ReactionsCog |
| reaction_role_reaction | the reaction to trigger off of | ReactionsCog | y |
| reaction_role_role | the role to grant | ReactionsCog | y |
| new_account_role | a role to give fresh discord accounts | MembersCog | y |
| new_account_days | how many days old is no longer "fresh" | MembersCog | y |
| member_role | a role granted to members after member_hours hours on the server | MembersCog | y |
| member_hours | how long after join to grant users member_role | MembersCog | y |
| auto_publish_channel | channels to auto publish every message | MiscCog |
