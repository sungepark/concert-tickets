
# ConcertTix - Future Development Tasks

This document outlines potential features and improvements for the ConcertTix concert ticket selling application. Tasks are organized by priority and category.

---

## 🔴 Priority 1: Critical Missing Features

These features are essential to complete the core purchase flow.

### [x] 1.1 Order Placement Implementation
**Description**: Implement actual order creation when "Place Order" is clicked
**Affected Files**: `server.py`, `public/cart-summary.html`
**Details**:
- Create `orders` table in database (order_id, session_id, total_amount, order_date, status)
- Create `order_items` table (order_id, event_id, quantity, price_at_purchase)
- Add `POST /api/orders` endpoint
- Update cart-summary.html to send order data
- Clear cart after successful order placement

### [x] 1.2 Inventory Management
**Description**: Deduct available_tickets when orders are placed
**Affected Files**: `server.py`
**Dependencies**: Task 1.1
**Details**:
- Update `available_tickets` in events table when order is created
- Add transaction handling to ensure atomic updates
- Prevent overselling by checking availability before order confirmation
- Show "Sold Out" badge on event cards when available_tickets = 0

### [x] 1.3 Order Confirmation Page
**Description**: Create confirmation page shown after successful order
**Affected Files**: New `public/order-confirmation.html`, `server.py`
**Dependencies**: Task 1.1
**Details**:
- Display order number, items purchased, total paid
- Show event details and ticket quantities
- Provide printable ticket view
- Add "View Order History" and "Browse More Events" links

### [x] 1.4 Email Notifications
**Description**: Send confirmation emails after purchase
**Affected Files**: `server.py`
**Dependencies**: Task 1.1, requires email collection
**Details**:
- Collect customer email during checkout
- Send HTML email with order details
- Include QR code or ticket barcode
- Setup email service integration (SMTP or service like SendGrid)

---

## 🟡 Priority 2: User Account System

Enable users to create accounts and track their purchases.

### [x] 2.1 User Registration & Login
**Description**: Implement user authentication system
**Affected Files**: `server.py`, new `public/login.html`, `public/register.html`
**Details**:
- Create `users` table (user_id, email, password_hash, name, created_at)
- Add `/api/register` and `/api/login` endpoints
- Implement password hashing (bcrypt or argon2)
- Create login/register pages with forms
- Add JWT or session-based auth
- Update navigation to show login/logout

### [ ] 2.2 User Profile Management
**Description**: Allow users to view and edit their profile
**Affected Files**: New `public/profile.html`, `server.py`
**Dependencies**: Task 2.1
**Details**:
- Create profile page with editable fields
- Display user info (name, email, member since)
- Allow password changes
- Add profile picture upload (optional)
- Create `PUT /api/users/:id` endpoint

### [ ] 2.3 Order History
**Description**: Show users their past orders
**Affected Files**: New `public/order-history.html`, `server.py`
**Dependencies**: Task 1.1, Task 2.1
**Details**:
- Create order history page
- Add `GET /api/orders` endpoint (filtered by user)
- Display list of past orders with dates and totals
- Allow viewing individual order details
- Show ticket downloads/QR codes

### [ ] 2.4 Password Reset
**Description**: Allow users to reset forgotten passwords
**Affected Files**: `server.py`, new `public/reset-password.html`
**Dependencies**: Task 2.1, Task 1.4 (email)
**Details**:
- Create password reset request form
- Generate secure reset tokens
- Send reset link via email
- Create reset password page
- Expire tokens after 24 hours

---

## 🟢 Priority 3: User Experience Enhancements

Improve discoverability and engagement.

### [ ] 3.1 Search Functionality
**Description**: Allow users to search for events
**Affected Files**: `public/index.html`, `server.py`
**Details**:
- Add search bar to events page
- Update `GET /api/events` to accept search query parameter
- Search across artist_name, venue_name, description
- Display search results count
- Highlight search terms in results

### [ ] 3.2 Filtering & Sorting
**Description**: Add filters and sort options to event listing
**Affected Files**: `public/index.html`, `server.py`
**Details**:
- Add filter controls (date range, price range, venue)
- Add sort dropdown (date, price, popularity)
- Update API to support filter/sort parameters
- Persist filters in URL query params
- Add "Clear Filters" button

### [ ] 3.3 Event Categories/Genres
**Description**: Organize events by music genre or category
**Affected Files**: `server.py`, `public/index.html`, database schema
**Details**:
- Add `genre` column to events table
- Create genre filter in UI
- Add genre badges to event cards
- Create dedicated category pages
- Update seed data with genres

### [ ] 3.4 Wishlist/Favorites
**Description**: Allow users to save events they're interested in
**Affected Files**: New `public/wishlist.html`, `server.py`, `public/event.html`
**Dependencies**: Task 2.1
**Details**:
- Create `wishlist` table (user_id, event_id, added_at)
- Add heart/bookmark icon to event cards
- Create wishlist page showing saved events
- Add `POST /api/wishlist` and `DELETE /api/wishlist/:id`
- Show notification when event from wishlist is selling out

### [ ] 3.5 User Reviews & Ratings
**Description**: Let users review events they've attended
**Affected Files**: `server.py`, `public/event.html`, database schema
**Dependencies**: Task 2.1, Task 1.1
**Details**:
- Create `reviews` table (user_id, event_id, rating, comment, created_at)
- Add review form on event page (only for past events)
- Display average rating on event cards
- Show reviews list on event detail page
- Add `POST /api/events/:id/reviews` endpoint

### [ ] 3.6 Social Sharing
**Description**: Enable sharing events on social media
**Affected Files**: `public/event.html`
**Details**:
- Add share buttons (Facebook, Twitter, WhatsApp, email)
- Generate share-friendly URLs
- Create Open Graph meta tags for previews
- Add "Copy Link" button
- Track shares for popularity metrics

---

## 🔵 Priority 4: Admin & Management

Tools for managing the platform.

### [ ] 4.1 Admin Authentication
**Description**: Create admin user role and protected routes
**Affected Files**: `server.py`
**Dependencies**: Task 2.1
**Details**:
- Add `is_admin` column to users table
- Create admin middleware for protected routes
- Add admin login page
- Implement role-based access control
- Secure all admin endpoints

### [ ] 4.2 Admin Dashboard
**Description**: Overview page for site metrics
**Affected Files**: New `public/admin/dashboard.html`, `server.py`
**Dependencies**: Task 4.1
**Details**:
- Show total sales, orders, users
- Display recent orders list
- Show top-selling events
- Revenue charts (daily, weekly, monthly)
- Create `GET /api/admin/stats` endpoint

### [ ] 4.3 Event Management CRUD
**Description**: Allow admins to create, edit, delete events
**Affected Files**: New `public/admin/events.html`, `server.py`
**Dependencies**: Task 4.1
**Details**:
- Create event management interface
- Add form to create new events
- Allow editing existing events
- Implement soft delete for events with orders
- Add image upload for event posters
- Create `POST/PUT/DELETE /api/admin/events` endpoints

### [ ] 4.4 Customer Management
**Description**: View and manage customer accounts
**Affected Files**: New `public/admin/customers.html`, `server.py`
**Dependencies**: Task 4.1, Task 2.1
**Details**:
- List all registered users
- View user details and order history
- Search/filter customers
- Ability to deactivate accounts
- Export customer data (CSV)

### [ ] 4.5 Sales Analytics
**Description**: Detailed reporting on sales performance
**Affected Files**: New `public/admin/analytics.html`, `server.py`
**Dependencies**: Task 4.1, Task 1.1
**Details**:
- Revenue trends over time
- Sales by event, venue, genre
- Conversion funnel (views → cart → purchase)
- Popular events and sell-through rates
- Export reports as PDF/CSV

---

## 🟣 Priority 5: Cart & Checkout Improvements

Enhanced shopping experience.

### [ ] 5.1 Promo Codes / Discount System
**Description**: Apply discount codes at checkout
**Affected Files**: `server.py`, `public/cart-summary.html`, database schema
**Details**:
- Create `promo_codes` table (code, discount_type, discount_value, expires_at)
- Add promo code input field in cart/checkout
- Validate codes server-side
- Apply percentage or fixed-amount discounts
- Show discount line in cost breakdown
- Create `POST /api/validate-promo` endpoint

### [ ] 5.2 Multiple Ticket Types
**Description**: Support different ticket tiers (VIP, General, etc.)
**Affected Files**: `server.py`, `public/event.html`, database schema
**Details**:
- Create `ticket_types` table (event_id, type_name, price, available)
- Update event page to show multiple ticket options
- Modify cart to store ticket type
- Update pricing calculations
- Display ticket type in cart/summary

### [ ] 5.3 Seat Selection Interface
**Description**: Visual seat picker for venues with assigned seating
**Affected Files**: New `public/seat-selection.html`, `server.py`, database schema
**Details**:
- Create `venue_layouts` and `seats` tables
- Build interactive seat map UI
- Mark seats as available/reserved/sold
- Implement seat hold during selection (temporary lock)
- Release seats if not purchased within time limit
- Update cart to include seat numbers

### [ ] 5.4 Cart Expiration Timer
**Description**: Add countdown timer to create urgency
**Affected Files**: `public/cart.html`, `public/cart-summary.html`
**Details**:
- Display countdown timer (e.g., "Complete purchase in 10:00")
- Clear cart or release held items when timer expires
- Show warning when time is running low
- Pause timer on checkout page
- Store expiration time in session

### [ ] 5.5 Gift Cards
**Description**: Allow purchasing and redeeming gift cards
**Affected Files**: `server.py`, `public/cart-summary.html`, database schema
**Details**:
- Create `gift_cards` table (code, balance, created_at, redeemed_by)
- Create gift card purchase page
- Add gift card redemption at checkout
- Send gift card codes via email
- Create `POST /api/gift-cards` and `POST /api/redeem-gift-card`

---

## 🟠 Priority 6: Technical Improvements

Code quality, security, and performance.

### [ ] 6.1 Input Validation & Sanitization
**Description**: Validate all user inputs to prevent injection attacks
**Affected Files**: `server.py`
**Details**:
- Add input validation for all API endpoints
- Sanitize HTML/SQL inputs
- Implement request body schemas
- Add rate limiting per endpoint
- Return proper error messages

### [ ] 6.2 Comprehensive Error Handling
**Description**: Improve error handling across the application
**Affected Files**: `server.py`, all HTML files
**Details**:
- Create consistent error response format
- Add try-catch blocks to all endpoints
- Display user-friendly error messages
- Log errors server-side
- Create error page for 404/500 errors

### [ ] 6.3 Database Indexing
**Description**: Add indexes for frequently queried columns
**Affected Files**: `server.py`
**Details**:
- Add indexes on events (event_date, venue_name)
- Add index on cart_items (session_id)
- Add indexes on orders (user_id, order_date)
- Analyze query performance
- Document index strategy

### [ ] 6.4 Code Refactoring - DRY Utilities
**Description**: Extract duplicate utility functions into shared module
**Affected Files**: All HTML files, new `public/js/utils.js`
**Details**:
- Create shared JavaScript file for common functions
- Move formatPrice, formatDate, showToast, cart functions
- Update all pages to import utilities
- Remove duplicate code
- Add JSDoc comments

### [ ] 6.5 Unit & Integration Tests
**Description**: Add automated test coverage
**Affected Files**: New `tests/` directory, `server.py`
**Details**:
- Set up testing framework (pytest for Python)
- Write API endpoint tests
- Test database operations
- Test edge cases and error conditions
- Add test runner to CI/CD

### [ ] 6.6 HTTPS & SSL
**Description**: Enable secure connections
**Affected Files**: `server.py`, deployment configuration
**Details**:
- Generate SSL certificates
- Configure server for HTTPS
- Redirect HTTP to HTTPS
- Update cookie settings (secure flag)
- Test in production environment

### [ ] 6.7 CSRF Protection
**Description**: Prevent cross-site request forgery attacks
**Affected Files**: `server.py`, all forms
**Details**:
- Implement CSRF token generation
- Add tokens to all forms
- Validate tokens on POST/PUT/DELETE requests
- Set proper CORS headers
- Test with security scanning tools

### [ ] 6.8 API Documentation
**Description**: Document all API endpoints
**Affected Files**: New `API.md`
**Details**:
- Document all endpoints with examples
- Include request/response schemas
- List error codes and meanings
- Add authentication requirements
- Provide cURL examples

---

## 🟣 Priority 7: Payment Integration

Payment processing for completing transactions.

### [ ] 7.1 Payment Integration
**Description**: Integrate payment processor for real transactions
**Affected Files**: `server.py`, `public/cart-summary.html`
**Dependencies**: Task 1.1
**Details**:
- Choose payment provider (Stripe, PayPal, Square)
- Add payment form to checkout
- Create payment processing endpoint
- Handle payment success/failure flows
- Store payment status with orders

---

## 🟤 Priority 8: Nice-to-Have Features

Advanced features for future consideration.

### [ ] 8.1 Multi-Currency Support
**Description**: Display prices in different currencies
**Affected Files**: `server.py`, all HTML files
**Details**:
- Integrate currency conversion API
- Add currency selector in UI
- Store base currency in database
- Convert prices dynamically
- Handle currency in payment processing

### [ ] 8.2 Event Recommendations
**Description**: Suggest events based on user preferences
**Affected Files**: `public/index.html`, `server.py`
**Dependencies**: Task 2.1, Task 1.1
**Details**:
- Analyze user purchase history
- Recommend similar events by genre/venue
- Create "You May Also Like" section
- Use collaborative filtering
- Add `GET /api/recommendations` endpoint

### [ ] 8.3 Calendar Integration
**Description**: Add events to user's calendar
**Affected Files**: `public/event.html`
**Details**:
- Generate .ics files for events
- Add "Add to Calendar" buttons
- Support Google Calendar, Outlook, Apple Calendar
- Include event details in calendar entry
- Send calendar invite with confirmation email

### [ ] 8.4 Mobile App
**Description**: Create native or progressive web app
**Affected Files**: New mobile project
**Details**:
- Convert to Progressive Web App (PWA)
- Add service worker for offline support
- Create app manifest
- Optimize for mobile performance
- Enable push notifications

### [ ] 8.5 Ticket Transfers & Resale
**Description**: Allow users to transfer or resell tickets
**Affected Files**: `server.py`, database schema, new UI pages
**Dependencies**: Task 2.1, Task 1.1
**Details**:
- Create transfer mechanism between users
- Add resale marketplace
- Implement secure transfer verification
- Update ticket ownership in database
- Set resale price limits

### [ ] 8.6 Waitlist for Sold-Out Events
**Description**: Let users join waitlist when events sell out
**Affected Files**: `server.py`, `public/event.html`, database schema
**Dependencies**: Task 1.2, Task 1.4
**Details**:
- Create `waitlist` table
- Show "Join Waitlist" button on sold-out events
- Notify users if tickets become available
- Automatically offer tickets to waitlist members
- Set time limit for waitlist offers

### [ ] 8.7 Live Event Updates
**Description**: Real-time updates for ticket availability
**Affected Files**: All frontend files, `server.py`
**Details**:
- Implement WebSocket connection
- Push real-time ticket count updates
- Show "X people viewing" indicator
- Update prices for dynamic pricing
- Show flash sales notifications

### [ ] 8.8 Accessibility Improvements
**Description**: Make the site WCAG 2.1 AA compliant
**Affected Files**: All HTML files, `styles.css`
**Details**:
- Add ARIA labels to interactive elements
- Improve keyboard navigation
- Ensure sufficient color contrast
- Add alt text to all images
- Test with screen readers
- Create skip navigation links

### [ ] 8.9 Internationalization (i18n)
**Description**: Support multiple languages
**Affected Files**: All HTML files, `server.py`
**Details**:
- Extract all text strings to translation files
- Add language selector
- Translate UI elements
- Support RTL languages
- Localize date/time/currency formats

### [ ] 8.10 Performance Optimization
**Description**: Improve page load times and responsiveness
**Affected Files**: All files
**Details**:
- Implement lazy loading for images
- Minify CSS/JavaScript
- Add caching headers
- Optimize database queries
- Use CDN for static assets
- Implement pagination for event lists

---

## 📊 Task Statistics

- **Priority 1 (Critical)**: 4 tasks
- **Priority 2 (User Accounts)**: 4 tasks
- **Priority 3 (UX Enhancements)**: 6 tasks
- **Priority 4 (Admin)**: 5 tasks
- **Priority 5 (Cart/Checkout)**: 5 tasks
- **Priority 6 (Technical)**: 8 tasks
- **Priority 7 (Payment Integration)**: 1 task
- **Priority 8 (Nice-to-Have)**: 10 tasks

**Total Tasks**: 43

---

## Getting Started

1. Start with **Priority 1** tasks to complete the core purchase flow
2. Consider dependencies when choosing tasks (some require others to be completed first)
3. Mark tasks as complete by changing `[ ]` to `[x]`
4. Feel free to reorder priorities based on your project goals
5. Break down larger tasks into smaller subtasks as needed

---

*Last updated: 2026-02-01*
