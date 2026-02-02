# ConcertTix API Reference

Base URL: `http://localhost:3000`

All endpoints return JSON responses unless otherwise noted.

---

## Events

### List All Events

**Endpoint:** `GET /api/events`

**Description:** Returns all events including sold-out ones, ordered by event date.

**Auth Required:** No

**Query Parameters:** None

**Success Response:**
```json
[
  {
    "id": 1,
    "artist_name": "Neon Pulse",
    "venue_name": "The Electric Garden",
    "event_date": "2026-03-15",
    "ticket_price": 75.0,
    "image_url": "https://picsum.photos/seed/neonpulse/800/400",
    "available_tickets": 150
  },
  {
    "id": 2,
    "artist_name": "Midnight Wanderers",
    "venue_name": "Starlight Arena",
    "event_date": "2026-03-22",
    "ticket_price": 95.0,
    "image_url": "https://picsum.photos/seed/midnight/800/400",
    "available_tickets": 0
  }
]
```

---

### Get Single Event

**Endpoint:** `GET /api/events/:id`

**Description:** Returns details for a specific event.

**Auth Required:** No

**URL Parameters:**
- `id` (integer) - Event ID

**Success Response:**
```json
{
  "id": 1,
  "artist_name": "Neon Pulse",
  "venue_name": "The Electric Garden",
  "event_date": "2026-03-15",
  "ticket_price": 75.0,
  "description": "Experience the electrifying synth-wave sounds...",
  "image_url": "https://picsum.photos/seed/neonpulse/800/400",
  "available_tickets": 150
}
```

**Error Response:**
```json
{
  "error": "Event not found"
}
```
Status: `404 Not Found`

---

## Shopping Cart

### Get Cart

**Endpoint:** `GET /api/cart`

**Description:** Returns all items in the current session's cart with calculated total.

**Auth Required:** No (uses session cookie)

**Success Response:**
```json
{
  "items": [
    {
      "cart_id": 1,
      "quantity": 2,
      "event_id": 1,
      "artist_name": "Neon Pulse",
      "venue_name": "The Electric Garden",
      "event_date": "2026-03-15",
      "ticket_price": 75.0,
      "image_url": "https://picsum.photos/seed/neonpulse/800/400"
    }
  ],
  "total": 150.0
}
```

**Empty Cart Response:**
```json
{
  "items": [],
  "total": 0
}
```

---

### Add to Cart

**Endpoint:** `POST /api/cart`

**Description:** Adds an event to the cart with specified quantity. Creates a new session if needed.

**Auth Required:** No (creates session cookie if needed)

**Request Body:**
```json
{
  "eventId": 1,
  "quantity": 2
}
```

**Success Response:**
```json
{
  "success": true,
  "message": "Added to cart"
}
```

**Cookies Set:**
- `sessionId` - Session identifier (7 day expiration)
- `cartCount` - Total quantity of items in cart

**Error Responses:**

Event not found:
```json
{
  "error": "Event not found"
}
```
Status: `404 Not Found`

Not enough tickets:
```json
{
  "error": "Not enough tickets available"
}
```
Status: `400 Bad Request`

---

### Update Cart Item

**Endpoint:** `PUT /api/cart/:id`

**Description:** Updates the quantity of a cart item. Deletes the item if quantity is 0 or less.

**Auth Required:** Yes (session cookie)

**URL Parameters:**
- `id` (integer) - Cart item ID

**Request Body:**
```json
{
  "quantity": 3
}
```

**Success Response:**
```json
{
  "success": true
}
```

**Cookies Updated:**
- `cartCount` - Updated total quantity

**Error Response:**
```json
{
  "error": "No session"
}
```
Status: `401 Unauthorized`

---

### Remove Cart Item

**Endpoint:** `DELETE /api/cart/:id`

**Description:** Removes a specific item from the cart.

**Auth Required:** Yes (session cookie)

**URL Parameters:**
- `id` (integer) - Cart item ID

**Success Response:**
```json
{
  "success": true
}
```

**Cookies Updated:**
- `cartCount` - Updated total quantity

**Error Response:**
```json
{
  "error": "No session"
}
```
Status: `401 Unauthorized`

---

### Clear Cart

**Endpoint:** `DELETE /api/cart`

**Description:** Removes all items from the cart.

**Auth Required:** Yes (session cookie)

**Success Response:**
```json
{
  "success": true
}
```

**Cookies Updated:**
- `cartCount` - Set to `0`

**Error Response:**
```json
{
  "error": "No session"
}
```
Status: `401 Unauthorized`

---

## Orders

### Place Order

**Endpoint:** `POST /api/orders`

**Description:** Creates an order from the current cart items. Automatically decrements inventory, clears the cart, and validates ticket availability.

**Auth Required:** Yes (session cookie)

**Request Body:**
```json
{
  "totalAmount": 187.91
}
```

**Success Response:**
```json
{
  "success": true,
  "orderId": 1,
  "message": "Order placed successfully"
}
```

**Cookies Updated:**
- `cartCount` - Set to `0`

**Error Responses:**

No session:
```json
{
  "error": "No session"
}
```
Status: `401 Unauthorized`

Missing total amount:
```json
{
  "error": "Total amount is required"
}
```
Status: `400 Bad Request`

Empty cart:
```json
{
  "error": "Cart is empty"
}
```
Status: `400 Bad Request`

Insufficient inventory:
```json
{
  "error": "Not enough tickets available for event ID 1"
}
```
Status: `400 Bad Request`

**Side Effects:**
- Creates record in `orders` table
- Creates records in `order_items` table for each cart item
- Decrements `available_tickets` for purchased events
- Clears all cart items for the session
- All operations are atomic (wrapped in transaction)

---

## Session Management

Sessions are managed via HTTP cookies:

- **`sessionId`**: Unique session identifier
  - Created automatically on first cart action
  - Expires after 7 days
  - Used to associate cart items and orders

- **`cartCount`**: Total quantity of items in cart
  - Updated on all cart operations
  - Used for display in navigation badge
  - Expires after 7 days

**Note:** All cart and order operations require a valid session cookie. The session is created automatically when adding the first item to cart.

---

## Error Handling

All errors follow a consistent format:

```json
{
  "error": "Error message description"
}
```

### HTTP Status Codes

- `200 OK` - Successful request
- `400 Bad Request` - Invalid request data or business logic error
- `401 Unauthorized` - Missing or invalid session
- `404 Not Found` - Resource not found

---

## Database Schema

### Tables

**events**
- `id` (INTEGER, PRIMARY KEY)
- `artist_name` (TEXT, NOT NULL)
- `venue_name` (TEXT, NOT NULL)
- `event_date` (TEXT, NOT NULL)
- `ticket_price` (REAL, NOT NULL)
- `description` (TEXT)
- `image_url` (TEXT)
- `available_tickets` (INTEGER, DEFAULT 100)

**cart_items**
- `id` (INTEGER, PRIMARY KEY)
- `session_id` (TEXT, NOT NULL)
- `event_id` (INTEGER, NOT NULL, FOREIGN KEY)
- `quantity` (INTEGER, DEFAULT 1)
- `added_at` (TEXT, DEFAULT CURRENT_TIMESTAMP)

**orders**
- `id` (INTEGER, PRIMARY KEY)
- `session_id` (TEXT, NOT NULL)
- `total_amount` (REAL, NOT NULL)
- `order_date` (TEXT, DEFAULT CURRENT_TIMESTAMP)
- `status` (TEXT, DEFAULT 'pending')

**order_items**
- `id` (INTEGER, PRIMARY KEY)
- `order_id` (INTEGER, NOT NULL, FOREIGN KEY)
- `event_id` (INTEGER, NOT NULL, FOREIGN KEY)
- `quantity` (INTEGER, NOT NULL)
- `price_at_purchase` (REAL, NOT NULL)

---

## Examples

### Complete Purchase Flow

1. **Browse Events**
   ```bash
   curl http://localhost:3000/api/events
   ```

2. **Add to Cart**
   ```bash
   curl -c cookies.txt -X POST http://localhost:3000/api/cart \
     -H "Content-Type: application/json" \
     -d '{"eventId": 1, "quantity": 2}'
   ```

3. **View Cart**
   ```bash
   curl -b cookies.txt http://localhost:3000/api/cart
   ```

4. **Place Order**
   ```bash
   curl -b cookies.txt -X POST http://localhost:3000/api/orders \
     -H "Content-Type: application/json" \
     -d '{"totalAmount": 187.91}'
   ```

### Update Cart Quantity

```bash
curl -b cookies.txt -X PUT http://localhost:3000/api/cart/1 \
  -H "Content-Type: application/json" \
  -d '{"quantity": 3}'
```

### Clear Cart

```bash
curl -b cookies.txt -X DELETE http://localhost:3000/api/cart
```

---

*Last updated: 2026-02-01*
