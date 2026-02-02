# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ConcertTix is a concert ticket selling prototype built with vanilla technologies and no external dependencies.

## Tech Stack

- **Backend**: Python 3 with built-in `http.server` and `sqlite3`
- **Frontend**: Vanilla HTML, CSS, and JavaScript (ES6+)
- **Database**: SQLite (`concerts.db`)

## Running the Server

```bash
python3 server.py
```

Server runs at http://localhost:3000

## Architecture

### Backend (`server.py`)

Single-file HTTP server handling:
- Static file serving from `public/`
- REST API endpoints for events and cart management
- Session management via cookies
- SQLite database operations

**API Endpoints:**
- `GET /api/events` - List all events
- `GET /api/events/:id` - Get single event
- `GET /api/cart` - Get cart items
- `POST /api/cart` - Add item to cart
- `PUT /api/cart/:id` - Update cart item quantity
- `DELETE /api/cart/:id` - Remove cart item
- `DELETE /api/cart` - Clear entire cart

**URL Routing:** Explicit routes exist for `/`, `/cart`, `/cart-summary`, and `/event/:id`. New pages require adding routes in `do_GET()`.

### Frontend (`public/`)

- `index.html` - Events listing page
- `event.html` - Event detail page with ticket selection
- `cart.html` - Shopping cart with quantity controls
- `cart-summary.html` - Order summary with cost breakdown (fees, taxes)
- `styles.css` - Global styles (dark theme, glassmorphic design)

### Design System

- **Primary color**: #e94560 (pink/red)
- **Accent color**: #4ecca3 (green) for prices
- **Background**: Dark gradient (#1a1a2e to #16213e)
- **Cards**: Glassmorphic with `rgba(255, 255, 255, 0.05)` backgrounds

### Utility Functions (in each HTML file)

- `formatPrice(price)` - Returns `$X.XX` format
- `formatDate(dateStr)` - Formats dates for display
- `showToast(message)` - Shows notification toast
- `getCartCount()` / `updateCartCountDisplay()` - Cart badge management

## Git Workflow
When completing tasks from TASKS.md:
1. Create a new branch named `feature/<task-number>-<brief-description>` before starting work
2. Make atomic commits with conventional commit messages:
    - feat: for new features
    - fix: for bug fixes
    - docs: for documentation
    - test: for tests
    - refactor: for refactoring
3. After completing a task, create a pull request with:
    - A descriptive title matching the task
    - A summary of changes made
    - Any testing notes or considerations
4. Update the task checkbox in TASKS.md to mark it complete

## Testing Requirements
Before marking any task as complete:
1. Write unit tests for new functionality
2. Run the full test suite with: `npm test`
3. If tests fail:
    - Analyze the failure output
    - Fix the code (no the tests, unless tests are incorrect)
    - Re-run tests until all pass
