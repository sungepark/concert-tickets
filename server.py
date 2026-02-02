#!/usr/bin/env python3
"""
Concert Tickets - A simple ticket selling prototype
Uses Python's built-in http.server and sqlite3 (no external dependencies)
"""

import http.server
import json
import os
import sqlite3
import uuid
from http.cookies import SimpleCookie
from urllib.parse import urlparse, parse_qs
from pathlib import Path

# Configuration
PORT = 3000
DB_PATH = Path(__file__).parent / 'concerts.db'
PUBLIC_DIR = Path(__file__).parent / 'public'


def init_database():
    """Initialize the SQLite database with schema and sample data."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist_name TEXT NOT NULL,
            venue_name TEXT NOT NULL,
            event_date TEXT NOT NULL,
            ticket_price REAL NOT NULL,
            description TEXT,
            image_url TEXT,
            available_tickets INTEGER DEFAULT 100
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            event_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1,
            added_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (event_id) REFERENCES events(id)
        )
    ''')

    # Check if we need to seed data
    cursor.execute('SELECT COUNT(*) as count FROM events')
    if cursor.fetchone()['count'] == 0:
        events = [
            ('Neon Pulse', 'The Electric Garden', '2026-03-15', 75.00,
             'Experience the electrifying synth-wave sounds of Neon Pulse in an intimate garden setting. Known for their immersive light shows and pulsating beats.',
             'https://picsum.photos/seed/neonpulse/800/400', 150),
            ('Midnight Wanderers', 'Starlight Arena', '2026-03-22', 95.00,
             'The indie folk sensation Midnight Wanderers bring their acoustic magic to the grand Starlight Arena. A night of storytelling through song.',
             'https://picsum.photos/seed/midnight/800/400', 500),
            ('Crystal Thunder', 'The Underground', '2026-04-05', 45.00,
             'Raw energy meets technical precision. Crystal Thunder delivers a metal experience that will leave your ears ringing for days.',
             'https://picsum.photos/seed/crystal/800/400', 200),
            ('Luna Eclipse', 'Riverside Amphitheater', '2026-04-12', 120.00,
             'Grammy-nominated artist Luna Eclipse performs her greatest hits under the stars. VIP packages include meet-and-greet opportunities.',
             'https://picsum.photos/seed/luna/800/400', 1000),
            ('The Velvet Frequencies', 'Jazz Corner Club', '2026-04-18', 55.00,
             'Smooth jazz meets electronic experimentation. The Velvet Frequencies create soundscapes that transport you to another dimension.',
             'https://picsum.photos/seed/velvet/800/400', 80),
            ('Solar Flare', 'Metro Stadium', '2026-05-01', 150.00,
             'The world tour stops here! Solar Flare brings their spectacular production with pyrotechnics, aerial performers, and non-stop hits.',
             'https://picsum.photos/seed/solar/800/400', 5000),
            ('Echo Chamber', 'The Warehouse District', '2026-05-10', 35.00,
             'Underground techno collective Echo Chamber hosts an all-night rave. Multiple DJs, immersive visuals, and dancing until dawn.',
             'https://picsum.photos/seed/echo/800/400', 300),
            ('Autumn Leaves', 'Heritage Hall', '2026-05-20', 85.00,
             'Classical meets contemporary as Autumn Leaves performs with a full orchestra. An evening of sophisticated musical fusion.',
             'https://picsum.photos/seed/autumn/800/400', 400),
        ]

        cursor.executemany('''
            INSERT INTO events (artist_name, venue_name, event_date, ticket_price, description, image_url, available_tickets)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', events)
        print('Database seeded with sample events')

    conn.commit()
    conn.close()


def get_db():
    """Get a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def row_to_dict(row):
    """Convert a sqlite3.Row to a dictionary."""
    if row is None:
        return None
    return dict(row)


def rows_to_list(rows):
    """Convert a list of sqlite3.Row to a list of dictionaries."""
    return [dict(row) for row in rows]


class ConcertHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler for the concert tickets application."""

    def get_session_id(self):
        """Get or create a session ID from cookies."""
        cookie = SimpleCookie(self.headers.get('Cookie', ''))
        if 'sessionId' in cookie:
            return cookie['sessionId'].value
        return None

    def set_cookies(self, cookies_dict):
        """Set cookies in the response."""
        for name, value in cookies_dict.items():
            self.send_header('Set-Cookie', f'{name}={value}; Path=/; Max-Age=604800')

    def send_json(self, data, status=200, cookies=None):
        """Send a JSON response."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        if cookies:
            self.set_cookies(cookies)
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def send_file(self, filepath):
        """Send a static file."""
        content_types = {
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.json': 'application/json',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
        }

        ext = os.path.splitext(filepath)[1].lower()
        content_type = content_types.get(ext, 'application/octet-stream')

        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404)

    def get_request_body(self):
        """Read and parse the request body as JSON."""
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            body = self.rfile.read(content_length)
            return json.loads(body.decode())
        return {}

    def get_cart_count(self, session_id):
        """Get the total number of items in the cart."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT COALESCE(SUM(quantity), 0) as count FROM cart_items WHERE session_id = ?',
            (session_id,)
        )
        count = cursor.fetchone()['count']
        conn.close()
        return count

    def do_GET(self):
        """Handle GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path

        # API routes
        if path == '/api/events':
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, artist_name, venue_name, event_date, ticket_price, image_url, available_tickets
                FROM events
                ORDER BY event_date ASC
            ''')
            events = rows_to_list(cursor.fetchall())
            conn.close()
            self.send_json(events)
            return

        if path.startswith('/api/events/'):
            event_id = path.split('/')[-1]
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM events WHERE id = ?', (event_id,))
            event = row_to_dict(cursor.fetchone())
            conn.close()
            if event:
                self.send_json(event)
            else:
                self.send_json({'error': 'Event not found'}, 404)
            return

        if path == '/api/cart':
            session_id = self.get_session_id()
            if not session_id:
                self.send_json({'items': [], 'total': 0})
                return

            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT
                    cart_items.id as cart_id,
                    cart_items.quantity,
                    events.id as event_id,
                    events.artist_name,
                    events.venue_name,
                    events.event_date,
                    events.ticket_price,
                    events.image_url
                FROM cart_items
                JOIN events ON cart_items.event_id = events.id
                WHERE cart_items.session_id = ?
            ''', (session_id,))
            items = rows_to_list(cursor.fetchall())
            conn.close()

            total = sum(item['ticket_price'] * item['quantity'] for item in items)
            self.send_json({'items': items, 'total': total})
            return

        # Static files and HTML pages
        if path == '/':
            self.send_file(PUBLIC_DIR / 'index.html')
            return

        if path.startswith('/event/'):
            self.send_file(PUBLIC_DIR / 'event.html')
            return

        if path == '/cart':
            self.send_file(PUBLIC_DIR / 'cart.html')
            return

        if path == '/cart-summary':
            self.send_file(PUBLIC_DIR / 'cart-summary.html')
            return

        # Try to serve static file
        filepath = PUBLIC_DIR / path.lstrip('/')
        if filepath.exists() and filepath.is_file():
            self.send_file(filepath)
            return

        self.send_error(404)

    def do_POST(self):
        """Handle POST requests."""
        parsed = urlparse(self.path)
        path = parsed.path

        if path == '/api/cart':
            session_id = self.get_session_id()
            cookies = {}

            if not session_id:
                session_id = str(uuid.uuid4())
                cookies['sessionId'] = session_id

            body = self.get_request_body()
            event_id = body.get('eventId')
            quantity = body.get('quantity', 1)

            conn = get_db()
            cursor = conn.cursor()

            # Check if event exists
            cursor.execute('SELECT * FROM events WHERE id = ?', (event_id,))
            event = row_to_dict(cursor.fetchone())
            if not event:
                conn.close()
                self.send_json({'error': 'Event not found'}, 404)
                return

            if event['available_tickets'] < quantity:
                conn.close()
                self.send_json({'error': 'Not enough tickets available'}, 400)
                return

            # Check if item already in cart
            cursor.execute(
                'SELECT * FROM cart_items WHERE session_id = ? AND event_id = ?',
                (session_id, event_id)
            )
            existing = row_to_dict(cursor.fetchone())

            if existing:
                cursor.execute(
                    'UPDATE cart_items SET quantity = quantity + ? WHERE id = ?',
                    (quantity, existing['id'])
                )
            else:
                cursor.execute(
                    'INSERT INTO cart_items (session_id, event_id, quantity) VALUES (?, ?, ?)',
                    (session_id, event_id, quantity)
                )

            conn.commit()

            # Update cart count cookie
            cart_count = self.get_cart_count(session_id)
            cookies['cartCount'] = str(cart_count)

            conn.close()
            self.send_json({'success': True, 'message': 'Added to cart'}, cookies=cookies)
            return

        self.send_error(404)

    def do_PUT(self):
        """Handle PUT requests."""
        parsed = urlparse(self.path)
        path = parsed.path

        if path.startswith('/api/cart/'):
            cart_id = path.split('/')[-1]
            session_id = self.get_session_id()

            if not session_id:
                self.send_json({'error': 'No session'}, 401)
                return

            body = self.get_request_body()
            quantity = body.get('quantity', 0)

            conn = get_db()
            cursor = conn.cursor()

            if quantity <= 0:
                cursor.execute(
                    'DELETE FROM cart_items WHERE id = ? AND session_id = ?',
                    (cart_id, session_id)
                )
            else:
                cursor.execute(
                    'UPDATE cart_items SET quantity = ? WHERE id = ? AND session_id = ?',
                    (quantity, cart_id, session_id)
                )

            conn.commit()

            cart_count = self.get_cart_count(session_id)
            conn.close()

            self.send_json({'success': True}, cookies={'cartCount': str(cart_count)})
            return

        self.send_error(404)

    def do_DELETE(self):
        """Handle DELETE requests."""
        parsed = urlparse(self.path)
        path = parsed.path

        session_id = self.get_session_id()
        if not session_id:
            self.send_json({'error': 'No session'}, 401)
            return

        conn = get_db()
        cursor = conn.cursor()

        if path == '/api/cart':
            # Clear entire cart
            cursor.execute('DELETE FROM cart_items WHERE session_id = ?', (session_id,))
            conn.commit()
            conn.close()
            self.send_json({'success': True}, cookies={'cartCount': '0'})
            return

        if path.startswith('/api/cart/'):
            # Delete specific item
            cart_id = path.split('/')[-1]
            cursor.execute(
                'DELETE FROM cart_items WHERE id = ? AND session_id = ?',
                (cart_id, session_id)
            )
            conn.commit()

            cart_count = self.get_cart_count(session_id)
            conn.close()

            self.send_json({'success': True}, cookies={'cartCount': str(cart_count)})
            return

        conn.close()
        self.send_error(404)

    def log_message(self, format, *args):
        """Custom log format."""
        print(f"[{self.log_date_time_string()}] {args[0]}")


def main():
    """Start the server."""
    init_database()

    server = http.server.HTTPServer(('', PORT), ConcertHandler)
    print(f'\n  Concert Tickets server running at http://localhost:{PORT}\n')
    print('  Press Ctrl+C to stop the server\n')

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n  Server stopped.')
        server.server_close()


if __name__ == '__main__':
    main()
