import oracledb
from config.my_keys import ORACLE_CONFIG

class OracleConnector:
    def __init__(self):
        self.conn = None
        self.connect()
    
    def connect(self):
        try:
            self.conn = oracledb.connect(
                user=ORACLE_CONFIG['user'],
                password=ORACLE_CONFIG['password'],
                host=ORACLE_CONFIG['host'],
                port=1521,
                sid='ORCL'
            )
            print("Conectado ao Oracle Database")
        except Exception as e:
            print(f"Erro de conexão: {e}")
            self.conn = None
    
    def execute_query(self, query, params=None):
        if not self.conn:
            return []
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params or {})
                
                if query.strip().upper().startswith('SELECT'):
                    columns = [col[0] for col in cursor.description]
                    results = cursor.fetchall()
                    return [dict(zip(columns, row)) for row in results]
                else:
                    self.conn.commit()
                    return [{"rows_affected": cursor.rowcount}]
                    
        except Exception as e:
            print(f" Erro na query: {e}")
            return []
    
    def close(self):
        if self.conn:
            self.conn.close()