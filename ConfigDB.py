import aiosqlite

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

database_file = 'config.db'
async def sql_query(query, bind=()):
    try:
        async with aiosqlite.connect(database_file) as db:
            cursor = await db.execute(query, bind)
            if query.lower().startswith('select'):
                rows = await cursor.fetchall()
                await cursor.close()
                return rows
            else:
                await db.commit()
                return True
    except Exception as e:
        print('sql query failed:')
        print(e)
        print('query', query)
        print('bind', bind)
        return False

# create new entry
async def add_config(server: int, key: str, value: str) -> bool:
    query = 'INSERT INTO config (server, key, value) VALUES (?, ?)'
    bind = (server, key, value)

    return await sql_query(query, bind)

# read entries with specified key
async def get_config(server: int, key: str, make_int=False, single=False):
    query = 'SELECT value FROM config WHERE key = ? AND server = ?'
    bind = (key, server)
    rows = await sql_query(query, bind)

    if make_int:
        out = [int(r[0]) for r in rows]
    else:
        out = [r[0] for r in rows]

    if single:
        return out[0]

    return out

async def get_configs(server: int, keys: list) -> dotdict:
    keys_in = ','.join(['?' for key in keys])
    query = f'SELECT key, value FROM config WHERE key IN ({keys_in}) AND server = ?'
    rows = await sql_query(query, [*keys, server])
    out = {}
    for row in rows:
        if row[0] not in out:
            # if not plural key name, make single entry
            if not row[0].endswith('s'):
                try: out[row[0]] = int(row[1])
                except: out[row[0]] = row[1]
                continue

            out[row[0]] = []

        # try to make it int
        try: out[row[0]].append(int(row[1]))
        except: out[row[0]].append(row[1])

    # fill any missing keys with an empty list
    for key in keys:
        if key not in out:
            out[key] = []

    return dotdict(out)

# update a specific entry
async def update_config(id: int, value: str) -> bool:
    query = 'UPDATE config SET value = ? WHERE id = ?'
    bind = (value, id)

    return await sql_query(query, bind)

# delete a specific entry
async def delete_config(id: int) -> bool:
    query = 'DELETE FROM config WHERE id = ?'
    bind = (id,)

    return await sql_query(query, bind)
