from database.DB_connect import DBConnect
from model.album import Album


class DAO:
    @staticmethod
    def get_album_durata(durata_minima):
        # return : lista di oggetti album con la durata maggiore della durata_minima inserita
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT a.id, a.title, a.artist_id, SUM(t.milliseconds)/60000 AS duration
                FROM album a, track t
                WHERE a.id = t.album_id
                GROUP BY a.id, a.title, a.artist_id
                HAVING duration > %s"""

        cursor.execute(query,(durata_minima,))

        for row in cursor:
            result.append(Album(row["id"],row["title"],row["artist_id"],row["duration"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_album_connessi():
        #return : lista di tuple con album connessi
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct t1.album_id as a1, t2.album_id as a2
from track t1,track t2, playlist_track pt1, playlist_track pt2
where t1.album_id <> t2.album_id and t1.album_id< t2.album_id and t1.id=pt1.track_id and  t2.id=pt2.track_id and pt1.playlist_id = pt2.playlist_id"""

        cursor.execute(query)

        for row in cursor:
            result.append((row["a1"],row["a2"]))

        cursor.close()
        conn.close()
        return result

