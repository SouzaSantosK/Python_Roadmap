import psycopg2
import os
from collections import namedtuple
from dotenv import load_dotenv  # Remova se não for usar o .env

ArticleData = namedtuple("ArticleData", ["id", "title", "content", "date"])

load_dotenv()  # Remova se não for usar o .env


class ArticleModel:
    def __init__(self):

        # Substitua se não for usar o .env
        self.conn_params = {
            "dbname": os.getenv("DBNAME"),
            "user": os.getenv("DBUSER"),
            "password": os.getenv("DBPASSWORD"),
            "host": os.getenv("DBHOST"),
            "port": os.getenv("DBPORT"),
        }

    def _get_connection(self):
        return psycopg2.connect(**self.conn_params)

    def get_all(self):
        conn = self._get_connection()
        cur = conn.cursor()

        query = "SELECT article_id, article_title, article_content, article_date FROM articles ORDER BY article_date DESC"

        cur.execute(query)
        rows = cur.fetchall()

        articles = [ArticleData(*row) for row in rows]

        cur.close()
        conn.close()
        return articles

    def get_by_id(self, article_id):
        conn = self._get_connection()
        cur = conn.cursor()

        query = "SELECT article_id, article_title, article_content, article_date FROM articles WHERE article_id = %s"

        cur.execute(query, (article_id,))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row:
            return ArticleData(*row)
        return None

    def create(self, title, content, date):
        conn = self._get_connection()
        cur = conn.cursor()

        query = """
            INSERT INTO articles (article_title, article_content, article_date)
            VALUES (%s, %s, %s);
        """

        try:
            cur.execute(query, (title, content, date))
            conn.commit()
        except Exception as e:
            print(f"Erro ao inserir: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

    def delete(self, article_id):
        conn = self._get_connection()
        cur = conn.cursor()

        query = "DELETE FROM articles WHERE article_id = %s"

        try:
            cur.execute(query, (article_id,))
            conn.commit()
        except Exception as e:
            print(f"Erro ao deletar: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

    def update(self, article_id, article_title, article_content, article_date):
        conn = self._get_connection()
        cur = conn.cursor()

        query = """
            UPDATE articles
            SET article_title = %s, article_content = %s, article_date = %s
            WHERE article_id = %s;
        """

        try:
            cur.execute(
                query, (article_title, article_content, article_date, article_id)
            )
            conn.commit()
        except Exception as e:
            print(f"Erro no update: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()
