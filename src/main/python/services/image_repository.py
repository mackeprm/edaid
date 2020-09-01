import sqlite3
from datetime import datetime

init_db_sql_statement = """
CREATE TABLE IF NOT EXISTS images (
id integer PRIMARY KEY,
path text NOT NULL,
image_size text NOT NULL,
file_size text NOT NULL,
phash text NOT NULL);
"""


def to_dict(entry):
    return {
        "id": entry[0],
        "path": entry[1],
        "image_size": entry[2],
        "file_size": entry[3] + " MB",
        "phash": entry[4],
    }


class ImageRepository:

    # TODO init with an already existing connection.
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        cursor = self.connection.cursor()
        cursor.execute(init_db_sql_statement)

    def find_by_path(self, path):
        sql = '''SELECT * from images WHERE path=?'''
        cursor = self.connection.cursor()
        cursor.execute(sql, (path,))
        rows = cursor.fetchall()
        if rows:
            return rows
        else:
            return None

    def update(self, image_info):
        pass

    def save(self, image_info):
        sql = ''' INSERT INTO images(path, image_size, file_size, phash) VALUES(?,?,?,?) '''
        cursor = self.connection.cursor()
        cursor.execute(sql, [image_info['path'],
                             image_info['image_size'],
                             image_info['file_size'],
                             image_info['phash']])
        self.connection.commit()
        return cursor.lastrowid

    def remove_by_id(self, id):
        sql = '''DELETE FROM images WHERE id=?'''
        cursor = self.connection.cursor()
        cursor.execute(sql, (id,))
        self.connection.commit()

    # TODO how to do the "handled" thing?
    # TODO only show hashes whith more than one image
    def get_duplicates(self):
        sql = '''SELECT phash, count(*) as count, count(*) as handled FROM images GROUP BY phash ORDER BY count(*) DESC'''
        cursor = self.connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows

    def get_all_paths(self):
        sql = '''SELECT path FROM images'''
        cursor = self.connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return [row[0] for row in rows]

    def get_duplicates_for_phash(self, phash):
        sql = '''SELECT * FROM images WHERE phash=?'''
        cursor = self.connection.cursor()
        cursor.execute(sql, (phash,))
        rows = cursor.fetchall()
        return map(to_dict, rows)

    def last_update(self):
        return datetime.now()
