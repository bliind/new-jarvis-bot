import aiosqlite

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
async def add_config(key: str, value: str) -> bool:
    query = 'INSERT INTO config (key, value) VALUES (?, ?)'
    bind = (key, value)

    return await sql_query(query, bind)

# read entries with specified key
async def get_config(key: str, make_int=False, single=False):
    query = 'SELECT value FROM config WHERE key = ?'
    bind = (key,)
    rows = await sql_query(query, bind)

    if make_int:
        out = [int(r[0]) for r in rows]
    else:
        out = [r[0] for r in rows]

    if single:
        return out[0]

    return out


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
