import psycopg2

class pgvector():
    def __init__(self):
        self.db_name = "convolens"
        self.db_user = "postgresql"
        self.db_password = "psql1234"
        self.db_host = "localhost"
        self.db_port = "5432"

    def create_connection(self):
        connection = psycopg2.connect(
            dbname=self.db_name, user=self.db_user, password=self.db_password, host=self.db_host, port=self.db_port
        )
        return connection

    def insert(self, row):
        insert_query = """
            INSERT INTO audios (customer_id, csr_id, customer_satisfied, query_resolved, unprofessional_csr, call_purpose, user_qoi, customer_mood_change, transcript, embedding, audio_path)
            VALUES (%(customer_id)s, %(csr_id)s, %(customer_satisfied)s, %(query_resolved)s, %(unprofessional_csr)s, %(call_purpose)s, %(user_qoi)s, %(customer_mood_change)s, %(transcript)s, %(embedding)s, %(audio_path)s);
        """
        with self.create_connection() as conn, conn.cursor() as cursor:
            cursor.execute(insert_query, row)
            conn.commit()

    def select(self, query, values):
        with self.create_connection() as conn, conn.cursor() as cursor:
            cursor.execute(query, values)
            rows = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]
            rows = [dict(zip(column_names, row)) for row in rows]

        return rows

    
