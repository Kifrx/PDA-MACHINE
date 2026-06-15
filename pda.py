import json
import urllib.parse
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

def pda_trace(input_string):
    state = "q0"
    stack = ["Z0"]

    print(f"State: {state}, Stack: {stack}")

    for symbol in input_string:

        if symbol == "(":
            stack.append("X")
            print(f"Read: {symbol}, Push X -> {stack}")

        elif symbol == ")":
            if len(stack) > 0 and stack[-1] == "X":
                stack.pop()
                print(f"Read: {symbol}, Pop X -> {stack}")
            else:
                print("REJECT")
                return

        else:
            print("Invalid symbol")
            return

    if stack == ["Z0"]:
        print("Move to qf")
        print("ACCEPT\n")
    else:
        print("REJECT\n")

def pda_trace_json(input_string):
    """
    Menjalankan simulasi PDA dan mengembalikan list of dict (langkah-langkah)
    untuk dirender oleh frontend HTML.
    """
    steps = []
    state = "q0"
    stack = ["Z0"]
    
    # Langkah 0: Inisialisasi
    steps.append({
        "stepIndex": 0,
        "state": "q0",
        "tapeIndex": -1,
        "symbolRead": "ε",
        "stack": list(stack),
        "action": "Start",
        "status": "running",
        "desc": "Mesin berada di State q0 dengan simbol dasar Z0 di dalam Stack.",
        "transitionId": "trans-init",
        "nextState": "q0"
    })
    
    rejected = False
    for i, symbol in enumerate(input_string):
        if rejected:
            break
            
        if symbol == "(":
            stack.append("X")
            steps.append({
                "stepIndex": len(steps),
                "state": "q0",
                "tapeIndex": i,
                "symbolRead": "(",
                "stack": list(stack),
                "action": "Push X",
                "status": "running",
                "desc": "Membaca simbol '(', memasukkan (Push) 'X' ke Stack.",
                "transitionId": "trans-push",
                "nextState": "q0"
            })
        elif symbol == ")":
            if len(stack) > 0 and stack[-1] == "X":
                stack.pop()
                steps.append({
                    "stepIndex": len(steps),
                    "state": "q0",
                    "tapeIndex": i,
                    "symbolRead": ")",
                    "stack": list(stack),
                    "action": "Pop X",
                    "status": "running",
                    "desc": "Membaca simbol ')', mengeluarkan (Pop) 'X' dari Stack.",
                    "transitionId": "trans-pop",
                    "nextState": "q0"
                })
            else:
                rejected = True
                steps.append({
                    "stepIndex": len(steps),
                    "state": "q0",
                    "tapeIndex": i,
                    "symbolRead": ")",
                    "stack": list(stack),
                    "action": "REJECT",
                    "status": "reject",
                    "desc": "Membaca simbol ')' tetapi Top Stack bukan 'X'. Mesin gagal bertransisi dan menolak input!",
                    "transitionId": "",
                    "nextState": "q0"
                })
        else:
            rejected = True
            steps.append({
                "stepIndex": len(steps),
                "state": "q0",
                "tapeIndex": i,
                "symbolRead": symbol,
                "stack": list(stack),
                "action": "REJECT",
                "status": "reject",
                "desc": f"Membaca simbol tidak valid '{symbol}'. Mesin langsung menolak input!",
                "transitionId": "",
                "nextState": "q0"
            })
            
    if not rejected:
        if stack == ["Z0"]:
            steps.append({
                "stepIndex": len(steps),
                "state": "q0",
                "tapeIndex": len(input_string),
                "symbolRead": "ε",
                "stack": list(stack),
                "action": "ACCEPT",
                "status": "accept",
                "desc": "Seluruh input berhasil dibaca, Stack kembali berisi Z0. Mesin berpindah ke State qf. ACCEPT!",
                "transitionId": "trans-accept",
                "nextState": "qf"
            })
        else:
            steps.append({
                "stepIndex": len(steps),
                "state": "q0",
                "tapeIndex": len(input_string),
                "symbolRead": "ε",
                "stack": list(stack),
                "action": "REJECT",
                "status": "reject",
                "desc": "Input habis tetapi Stack tidak kembali berisi Z0 (kelebihan tanda kurung buka '('). REJECT!",
                "transitionId": "",
                "nextState": "q0"
            })
            
    return steps

class PDARequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Mencegah log request yang memenuhi terminal agar output tetap bersih
        pass

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        # API Route: /api/simulate?input=...
        if parsed_path.path == '/api/simulate':
            query = urllib.parse.parse_qs(parsed_path.query)
            input_val = query.get('input', [''])[0]
            
            result = pda_trace_json(input_val)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
            
        # Static Route: Serve pda_simulator.html
        elif parsed_path.path in ('/', '/index.html', '/pda_simulator.html'):
            try:
                # Cari file HTML di direktori yang sama dengan script ini
                html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pda_simulator.html')
                with open(html_path, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Error: File pda_simulator.html tidak ditemukan di direktori kerja.")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Halaman tidak ditemukan.")

def start_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, PDARequestHandler)
    print(f"============================================================")
    print(f"SERVER SIMULATOR PDA BERHASIL DIJALANKAN.")
    print(f"Buka browser Anda dan kunjungi: http://localhost:{port}")
    print(f"============================================================")
    print("Tekan Ctrl+C untuk menghentikan server.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer dihentikan.")
        sys.exit(0)

if __name__ == "__main__":
    # Test case default bawaan pda.py
    test_cases = [
        "()",
        "(())",
        "()()",
        "(()())",
        "(()",
        "())",
        ")(",
        "((((((()))"
    ]

    # Cek parameter input
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "--cli":
            print("--- MENJALANKAN TEST CASES DARI TERMINAL ---")
            for tc in test_cases:
                print(f"Uji string: {tc}")
                pda_trace(tc)
        elif arg == "--help" or arg == "-h":
            print("Penggunaan:")
            print("  python pda.py           : Menjalankan web server simulator (default)")
            print("  python pda.py --cli     : Menjalankan test case CLI bawaan")
            print("  python pda.py [string]  : Menjalankan penelusuran CLI untuk string tertentu")
        else:
            print(f"--- PENELUSURAN CLI UNTUK STRING: '{arg}' ---")
            pda_trace(arg)
    else:
        # Secara default, jalankan web server untuk UI
        start_server(8080)