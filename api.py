from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3
import json
import pandas as pd
from urllib.parse import urlparse, parse_qs

class RequestHandler(BaseHTTPRequestHandler):
    # Funzione per eseguire query SQL e restituire il risultato come JSON
    def execute_query(self, query, params=()):
        conn = sqlite3.connect('pesca.db')
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df.to_dict(orient='records')
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_components = parse_qs(parsed_path.query)
        da_anno = int(query_components.get('da_anno', [2000])[0])
        a_anno = int(query_components.get('a_anno', [2024])[0])
        
        if parsed_path.path == '/api/economia':
            query = '''
            SELECT * FROM Economia_Pesca WHERE anno BETWEEN ? AND ?
            '''
            params = (da_anno, a_anno)
            data = self.execute_query(query, params)
            self.respond(data)
        
        elif parsed_path.path == '/api/occupazione':
            query = '''
            SELECT * FROM Occupazione_Pesca WHERE anno BETWEEN ? AND ?
            '''
            params = (da_anno, a_anno)
            data = self.execute_query(query, params)
            self.respond(data)
        
        elif parsed_path.path == '/api/produttivita':
            query = '''
            SELECT * FROM Produttivita_Pesca WHERE anno BETWEEN ? AND ?
            '''
            params = (da_anno, a_anno)
            data = self.execute_query(query, params)
            self.respond(data)
        
        elif parsed_path.path == '/api/serie_calcolate':
            query = '''
            SELECT * FROM Serie_Calcolate WHERE anno BETWEEN ? AND ?
            '''
            params = (da_anno, a_anno)
            data = self.execute_query(query, params)
            self.respond(data)
        
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Not Found'}).encode())
    
    def respond(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=4).encode())

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
