# ConcertTix

A concert ticket selling prototype built with vanilla technologies and no external dependencies.

## Tech Stack

- **Backend**: Python 3 with built-in `http.server` and `sqlite3`
- **Frontend**: Vanilla HTML, CSS, and JavaScript (ES6+)
- **Database**: SQLite (auto-created on first run)

## Quick Start

### Prerequisites

- Python 3.8 or higher

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sungepark/concert-tickets.git
   cd concert-tickets
   ```

2. Start the server:
   ```bash
   python3 server.py
   ```

3. Open your browser to http://localhost:3000

That's it! No dependencies to install.

## Database Setup

The SQLite database (`concerts.db`) is automatically created on first run with:
- Schema for events, cart items, orders, and order items
- Sample event data (8 concerts)

To reset the database, simply delete `concerts.db` and restart the server.

## Environment Variables

None required. The application runs with sensible defaults:

| Variable | Default | Description |
|----------|---------|-------------|
| PORT | 3000 | Server port (hardcoded in `server.py`) |
| DB_PATH | `./concerts.db` | SQLite database file location |

To change the port, edit `PORT` constant in `server.py` (line 17).

## Available Scripts

Since this uses vanilla technologies, there are no build scripts. Just run:

```bash
python3 server.py
```

## Project Structure

```
concert-tickets/
├── server.py           # HTTP server and API endpoints
├── concerts.db         # SQLite database (auto-created)
├── public/             # Frontend files
│   ├── index.html      # Events listing
│   ├── event.html      # Event detail page
│   ├── cart.html       # Shopping cart
│   ├── cart-summary.html # Checkout page
│   └── styles.css      # Global styles
└── docs/
    └── api.md          # API documentation
```

## Features

- ✅ Browse concert events
- ✅ Add tickets to cart with quantity selection
- ✅ Shopping cart management (add, update, remove)
- ✅ Order placement with fee and tax calculations
- ✅ Inventory management (prevents overselling)
- ✅ Sold-out event display with badges
- ✅ Session-based cart persistence (7 days)

## API Documentation

See [/docs/api.md](/docs/api.md) for complete API reference with:
- All 8 endpoints (events, cart, orders)
- Request/response examples
- cURL command examples

## Development

### Making Changes

1. Edit files in `public/` for frontend changes
2. Edit `server.py` for backend/API changes
3. Refresh browser (no build step needed)
4. Server restart required only for `server.py` changes

### Database Schema

```sql
-- Events table
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artist_name TEXT NOT NULL,
    venue_name TEXT NOT NULL,
    event_date TEXT NOT NULL,
    ticket_price REAL NOT NULL,
    description TEXT,
    image_url TEXT,
    available_tickets INTEGER DEFAULT 100
);

-- Orders and cart tables
-- See server.py lines 29-73 for complete schema
```

## Testing the Application

1. Browse events at http://localhost:3000
2. Click an event to view details
3. Add tickets to cart
4. View cart at http://localhost:3000/cart
5. Proceed to checkout at http://localhost:3000/cart-summary
6. Place order (inventory automatically decrements)

## Troubleshooting

**Port already in use:**
```bash
# Find and kill the process
lsof -ti:3000 | xargs kill -9

# Or change the port in server.py (line 17)
```

**Database issues:**
```bash
# Reset database
rm concerts.db
python3 server.py
```

**Browser cache issues:**
- Hard refresh: Ctrl+Shift+R (Linux/Windows) or Cmd+Shift+R (Mac)

## Contributing

1. Create a feature branch: `feature/<task-number>-<description>`
2. Make atomic commits with conventional messages (feat/fix/docs/etc)
3. Create a pull request with summary and test notes
4. See [CLAUDE.md](/CLAUDE.md) for detailed workflow

## License

MIT

## Support

For issues or questions, please open a GitHub issue.

---

Built with ❤️ using vanilla technologies
