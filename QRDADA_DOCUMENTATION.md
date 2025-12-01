# QRDADA - Complete System Documentation

## Document Information
- **Project Name:** QRDADA (QR Code Generation and Analytics Platform)
- **Version:** 1.0
- **Last Updated:** November 2025
- **Platform:** Flask (Python) Web Application
- **Database:** PostgreSQL
- **Payment Gateway:** Razorpay

---

# Table of Contents

1. [Overview](#1-overview)
2. [System Architecture](#2-system-architecture)
3. [Functional Documentation](#3-functional-documentation)
4. [Technical Documentation](#4-technical-documentation)
5. [API Routes Reference](#5-api-routes-reference)
6. [Database Schema](#6-database-schema)
7. [Requirements Specification (SRS)](#7-requirements-specification-srs)
8. [Deployment and Configuration](#8-deployment-and-configuration)
9. [Workflow Diagrams](#9-workflow-diagrams)

---

# 1. Overview

## 1.1 What is QRDADA?

**QRDADA** is a comprehensive QR Code generation and analytics platform built with Flask that enables users to:
- Generate customized QR codes with various styling options
- Create both static and dynamic QR codes
- Track QR code scans with detailed analytics
- Manage subscription-based access to premium features
- Process payments through Razorpay integration
- Export QR codes in multiple formats (PNG, SVG, PDF)

## 1.2 Key Goals and Purpose

### Primary Objectives:
1. **QR Code Generation:** Provide users with professional-grade QR code creation tools
2. **Analytics Tracking:** Enable detailed scan analytics for dynamic QR codes
3. **Subscription Management:** Implement tiered subscription plans with usage limits
4. **Payment Processing:** Secure payment processing via Razorpay
5. **User Management:** Complete authentication, authorization, and profile management

### Target Users:
- Businesses requiring branded QR codes
- Marketing professionals tracking campaign performance
- Event organizers needing attendance tracking
- Restaurants and retail businesses
- Digital marketers and SEO professionals

## 1.3 Platform Architecture Overview

### Frontend:
- **Template Engine:** Jinja2
- **CSS Framework:** Tailwind CSS
- **JavaScript:** Vanilla JS with AJAX for dynamic interactions
- **UI Components:** Custom responsive design

### Backend:
- **Framework:** Flask 3.0.0
- **Language:** Python 3.x
- **ORM:** SQLAlchemy 2.0.31
- **Authentication:** Flask-Login 0.6.3
- **Email:** Flask-Mail with OAuth2 support (Gmail)
- **Caching:** Flask-Caching

### Database:
- **Primary Database:** PostgreSQL
- **ORM:** SQLAlchemy with Alembic migrations
- **Connection Pooling:** Managed via SQLAlchemy engine options

### External Services:
- **Payment Gateway:** Razorpay (Test and Live modes)
- **Email Service:** Gmail SMTP with app-specific passwords
- **QR Code Library:** python-qrcode with Pillow for image processing
- **Scheduler:** APScheduler for automated tasks

---

# 2. System Architecture

## 2.1 Application Structure

```
QRDADA/
│
├── app.py                      # Main Flask application
├── app_config.py              # Application configuration
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
│
├── models/                    # Database models
│   ├── __init__.py
│   ├── database.py           # Database initialization
│   ├── user.py               # User and EmailLog models
│   ├── qr_models.py          # QR Code related models
│   ├── subscription.py       # Subscription and SubscribedUser models
│   ├── payment.py            # Payment and InvoiceAddress models
│   ├── contact.py            # Contact form submissions
│   ├── admin.py              # Admin and WebsiteSettings models
│   └── usage_log.py          # Usage tracking
│
├── templates/                 # HTML templates
│   ├── base.html             # Base template
│   ├── index.html            # Landing page
│   ├── login.html            # User login
│   ├── signup.html           # User registration
│   ├── dashboard.html        # User dashboard
│   ├── profile.html          # User profile
│   ├── create_qr.html        # QR code creation
│   ├── analytics.html        # QR analytics
│   ├── pricing.html          # Subscription plans
│   ├── admin/                # Admin templates
│   │   ├── dashboard.html
│   │   ├── users.html
│   │   ├── subscriptions.html
│   │   └── payments.html
│   ├── services/             # QR type-specific templates
│   └── user/                 # User-specific templates
│
├── static/                    # Static files
│   ├── css/                  # Stylesheets
│   ├── js/                   # JavaScript files
│   ├── images/               # Images and icons
│   └── uploads/              # User-uploaded files
│       ├── logos/            # QR code logos
│       ├── temp/             # Temporary files
│       └── vcard/            # vCard files
│
├── utils/                     # Utility modules
│   ├── email_service.py      # Email sending utilities
│   ├── pdf_generator.py      # PDF generation for invoices
│   └── analytics_helper.py   # Analytics calculations
│
├── migrations/                # Database migrations
│   └── versions/             # Migration scripts
│
└── scheduler.py              # Background task scheduler
```

## 2.2 Technology Stack

### Backend Technologies:
- **Flask 3.0.0:** Web framework
- **SQLAlchemy 2.0.31:** ORM for database operations
- **Flask-Login 0.6.3:** User session management
- **Flask-Mail:** Email functionality
- **Flask-Migrate:** Database migrations
- **Flask-WTF:** Form handling and CSRF protection
- **Flask-Caching:** Response caching
- **Razorpay SDK:** Payment processing
- **APScheduler 3.10.4:** Task scheduling
- **Pillow 10.1.0:** Image processing
- **qrcode:** QR code generation
- **pytz:** Timezone handling
- **python-dotenv:** Environment variable management

### Frontend Technologies:
- **Tailwind CSS:** Utility-first CSS framework
- **Jinja2:** Template engine
- **JavaScript (ES6+):** Client-side interactivity
- **AJAX/Fetch API:** Asynchronous requests

### Database:
- **PostgreSQL:** Production database
- **SQLite:** Development/testing database

### Authentication & Security:
- **Werkzeug Security:** Password hashing
- **itsdangerous:** Token generation for email verification
- **Flask-WTF CSRF:** CSRF protection
- **Secure sessions:** HTTPOnly, Secure, SameSite cookies

---

# 3. Functional Documentation

## 3.1 User Authentication and Authorization

### 3.1.1 User Registration (Signup)

**Feature:** New user account creation with email verification

**User Flow:**
1. User navigates to `/signup` or `/register`
2. User fills out registration form:
   - Full Name (minimum 2 characters)
   - Company Email (unique, valid email format)
   - Password (minimum 8 characters with complexity requirements)
   - Confirm Password
3. System validates input:
   - Email uniqueness (case-insensitive)
   - Password complexity (uppercase, lowercase, number, special character)
   - Password confirmation match
4. System creates user account with `email_confirmed=False`
5. System sends verification email via OAuth2
6. User redirected to verification pending page

**Backend Processing:**
- Route: `/signup` (GET, POST)
- Endpoint: `app.py:800-872`
- Email normalization to lowercase
- Password hashing with Werkzeug
- Token generation with URLSafeTimedSerializer
- Email logged in `email_logs` table

**Data Inputs:**
- name: String (2-100 characters)
- companyEmail: String (valid email format)
- password: String (8+ chars, complexity)
- retypePassword: String (must match password)

**Data Outputs:**
- User record created in `user` table
- Verification email sent
- Email log entry created
- Flash message displayed

### 3.1.2 Email Verification

**Feature:** Confirm user email address before allowing login

**User Flow:**
1. User receives verification email
2. User clicks verification link with token
3. System validates token (24-hour expiry)
4. System updates `email_confirmed=True`
5. User redirected to login page

**Backend Processing:**
- Route: `/verify_email/<token>` (GET)
- Endpoint: `app.py:930-943`
- Token verification with 24-hour expiry
- Database update to confirm email
- Token cleared from database

**Security Features:**
- Unique token per user
- Time-limited validity (24 hours)
- Token stored in database for verification
- Token invalidated after use

### 3.1.3 User Login

**Feature:** Secure user authentication with session management

**User Flow:**
1. User navigates to `/login`
2. User enters email and password
3. System validates credentials
4. System checks email verification status
5. System creates secure session
6. User redirected to dashboard

**Backend Processing:**
- Route: `/login` (GET, POST)
- Endpoint: `app.py:719-791`
- Case-insensitive email lookup
- Password verification with bcrypt
- Flask-Login session creation
- Session data storage

**Validation Checks:**
1. Email exists in database
2. Email is verified
3. Password is correct
4. User account is active

**Session Data Stored:**
- user_id: User primary key
- user_name: User's full name
- email_id: User's email
- user_role: User's role (if applicable)
- user_permissions: User's permissions list

### 3.1.4 Password Reset

**Feature:** Secure password recovery via email

**User Flow:**
1. User clicks "Forgot Password" on login page
2. User enters registered email
3. System sends reset email with token
4. User clicks reset link
5. User enters new password (twice)
6. System validates and updates password

**Backend Processing:**
- Request Route: `/reset_password` (GET, POST) - `app.py:970-984`
- Token Route: `/reset_password/<token>` (GET, POST) - `app.py:986-1028`
- Token validity: 30 minutes
- Password complexity validation
- Password hash update

### 3.1.5 User Logout

**Feature:** Secure session termination

**User Flow:**
1. User clicks logout button
2. System clears session data
3. User redirected to homepage

**Backend Processing:**
- Route: `/logout` (GET)
- Endpoint: `app.py:1030-1036`
- Flask-Login logout
- Session cleared
- Flash message displayed

---

## 3.2 QR Code Generation

### 3.2.1 QR Code Types Supported

QRDADA supports 9 different QR code types:

#### 1. **URL/Link QR Code**
- **Purpose:** Direct users to a website
- **Model:** `QRLink`
- **Data:** URL (up to 2000 characters)
- **Dynamic:** Yes (trackable redirects)
- **Service Page:** `/services/qr-code-for-url`

#### 2. **Email QR Code**
- **Purpose:** Pre-fill email client
- **Model:** `QREmail`
- **Data:** Email address, subject, body
- **Dynamic:** No
- **Service Page:** `/services/qr-code-for-email`

#### 3. **vCard (Contact) QR Code**
- **Purpose:** Share contact information
- **Model:** `QRVCard`
- **Data:** Name, phone, email, company, title, address, website, logo, social media
- **Dynamic:** Yes (landing page with "Add to Contacts")
- **Service Page:** `/services/qr-code-for-vcard`
- **Features:**
  - Custom logo upload
  - Primary/secondary color customization
  - Social media links (JSON format)
  - Professional landing page

#### 4. **WiFi QR Code**
- **Purpose:** Auto-connect to WiFi network
- **Model:** `QRWifi`
- **Data:** SSID, password, encryption type (WPA/WEP/None)
- **Dynamic:** Yes
- **Service Page:** `/services/qr-code-for-wifi`

#### 5. **SMS QR Code**
- **Purpose:** Pre-fill SMS message
- **Model:** `QRSms`
- **Data:** Phone number, message text
- **Dynamic:** No
- **Service Page:** `/services/qr-code-for-sms`

#### 6. **Phone Call QR Code**
- **Purpose:** Initiate phone call
- **Model:** `QRPhone`
- **Data:** Phone number
- **Dynamic:** No
- **Service Page:** `/services/qr-code-for-call`

#### 7. **WhatsApp QR Code**
- **Purpose:** Open WhatsApp chat
- **Model:** `QRWhatsApp`
- **Data:** Phone number, pre-filled message
- **Dynamic:** No
- **Service Page:** `/services/qr-code-for-whatsapp`

#### 8. **Event/Calendar QR Code**
- **Purpose:** Add event to calendar
- **Model:** `QREvent`
- **Data:** Title, location, start/end time, description, organizer
- **Dynamic:** Yes
- **Service Page:** `/services/qr-code-for-event`
- **Format:** iCalendar (.ics)

#### 9. **Plain Text QR Code**
- **Purpose:** Display text content
- **Model:** `QRText`
- **Data:** Text content
- **Dynamic:** No
- **Service Page:** `/services/qr-code-for-text`

### 3.2.2 QR Code Creation Process

**User Flow:**
1. User navigates to `/create` (requires login)
2. User selects QR code type
3. User fills out type-specific form
4. User customizes QR code appearance:
   - **Basic Styling:**
     - Shape: square, rounded, circle, vertical_bars, horizontal_bars, gapped_square
     - Color: Solid color or gradient
     - Background color
     - Logo upload (optional)
   - **Advanced Styling (Premium):**
     - Custom eye patterns (inner/outer)
     - Eye colors
     - Module size and quiet zone
     - Error correction level
     - Frame type and text
     - Gradient options (linear, radial)
     - Template selection (modern, corporate, playful, minimal, high_contrast)
5. User previews QR code
6. User saves QR code

**Backend Processing:**
- Route: `/create` (GET, POST)
- Endpoint: `app.py:1510-2120`
- Subscription validation for premium features
- QR code generation with qrcode library
- Style application with Pillow
- Database storage with unique_id
- File system storage (if logo included)

**Subscription Checks:**
- QR code count limit
- Design access (template-based styling)
- Dynamic QR code access

### 3.2.3 QR Code Customization Options

#### Basic Customization (All Users):
- **Shape:** Square, Rounded, Circle
- **Colors:** Foreground and background colors
- **Logo:** Upload custom logo (20MB max)
- **Export Format:** PNG, SVG

#### Premium Customization (Subscription Required):
- **Templates:** Pre-designed styles (modern, corporate, playful, minimal, high_contrast)
- **Custom Eyes:** Different patterns for positioning markers
- **Gradients:** Linear and radial color gradients
- **Frames:** Add frames with custom text
- **Advanced Shapes:** Vertical bars, horizontal bars, gapped squares
- **Module Size Control:** Fine-tune QR density
- **Error Correction:** L, M, Q, H levels

#### QR Code Templates:

**1. Modern Template**
```python
{
    "shape": "rounded",
    "color": "#2c5282",
    "background_color": "#FFFFFF",
    "custom_eyes": True,
    "inner_eye_style": "circle",
    "outer_eye_style": "rounded",
    "export_type": "png"
}
```

**2. Corporate Template**
```python
{
    "shape": "square",
    "color": "#000000",
    "background_color": "#FFFFFF",
    "frame_type": "square",
    "frame_color": "#000000",
    "frame_text": "SCAN ME",
    "custom_eyes": True,
    "export_type": "png"
}
```

**3. Playful Template**
```python
{
    "shape": "circle",
    "gradient": True,
    "gradient_start": "#f97316",
    "gradient_end": "#fbbf24",
    "gradient_type": "linear",
    "gradient_direction": "to-right",
    "custom_eyes": True
}
```

### 3.2.4 Dynamic vs Static QR Codes

**Static QR Codes:**
- Content encoded directly in QR code
- Cannot be edited after creation
- No scan tracking
- Types: Email, SMS, Phone, WhatsApp, Text

**Dynamic QR Codes:**
- Content stored in database
- Redirect through `/r/<qr_id>` route
- Full scan analytics
- Editable content
- Types: URL, vCard, WiFi, Event

---

## 3.3 QR Code Management

### 3.3.1 Dashboard

**Feature:** Central hub for user's QR codes and statistics

**User Flow:**
1. User logs in
2. Automatically redirected to `/dashboard`
3. User sees:
   - QR code count (current subscription period)
   - Subscription status
   - Today's QR codes created
   - Analytics usage
   - Grid of QR codes with thumbnails

**Backend Processing:**
- Route: `/dashboard` (GET)
- Endpoint: `app.py:1134-1256`
- Subscription data loading
- QR code count for current period only
- Usage statistics calculation
- Analytics data aggregation

**Displayed Data:**
- Total QR codes (subscription period)
- QR codes remaining
- QR codes created today
- Subscription plan name
- Subscription expiry date
- Days remaining
- Analytics used/remaining
- List of QR codes with preview

### 3.3.2 View QR Code

**Feature:** View individual QR code details

**User Flow:**
1. User clicks on QR code from dashboard
2. System displays QR code details page
3. User sees:
   - QR code image
   - QR code name and type
   - Creation/update dates
   - Content details
   - Download options
   - Edit/Delete buttons (if applicable)

**Backend Processing:**
- Route: `/qr/<qr_id>` (GET)
- Endpoint: `app.py:2525-2561`
- Ownership validation
- QR code retrieval
- Related data loading (email, vcard, etc.)

### 3.3.3 Edit QR Code

**Feature:** Modify dynamic QR code content and styling

**User Flow:**
1. User clicks "Edit" on QR code detail page
2. System loads edit form with current data
3. User modifies content or styling
4. User saves changes
5. QR code image regenerated (if styling changed)

**Backend Processing:**
- Route: `/qr/<qr_id>/edit` (GET, POST)
- Endpoint: `app.py:2562-2795`
- Dynamic QR check
- Ownership validation
- Content update
- Style update
- Image regeneration

**Limitations:**
- Only dynamic QR codes can be edited
- Cannot change QR type after creation
- Subscription limits apply to premium features

### 3.3.4 Delete QR Code

**Feature:** Permanently remove QR code

**User Flow:**
1. User clicks "Delete" button
2. System shows confirmation modal
3. User confirms deletion
4. QR code and related data deleted

**Backend Processing:**
- Route: `/qr/<qr_id>/delete` (POST)
- Endpoint: `app.py:2796-2848`
- Ownership validation
- Cascade delete of related records
- File cleanup (logos, images)
- Analytics data archived

### 3.3.5 Download QR Code

**Feature:** Export QR code in various formats

**User Flow:**
1. User clicks download button
2. User selects format (PNG, SVG, PDF)
3. System generates file
4. Browser downloads file

**Backend Processing:**
- Route: `/qr/<qr_id>/download` (GET)
- Endpoint: `app.py:2849-2928`
- Format parameter handling
- Image generation
- File serving with correct MIME type

**Export Formats:**
- **PNG:** Standard raster image (default)
- **SVG:** Vector format (scalable)
- **PDF:** Document format with metadata

---

## 3.4 Analytics and Tracking

### 3.4.1 QR Code Analytics

**Feature:** Detailed scan tracking for dynamic QR codes

**User Flow:**
1. User navigates to QR code details
2. User clicks "Analytics" tab
3. System displays:
   - Total scans
   - Scans over time (chart)
   - Geographic data
   - Device/OS breakdown
   - Browser information
   - Recent scan list

**Backend Processing:**
- Route: `/qr/<qr_id>/analytics` (GET)
- Endpoint: `app.py:2946-3072`
- Scan data aggregation
- Time-series data for charts
- Geographic grouping
- Device categorization

**Tracked Data per Scan:**
- Timestamp (UTC)
- IP address
- User agent string
- Operating system
- Device type
- Location (derived from IP)

**Subscription Limits:**
- Analytics operations counted against subscription limit
- Each analytics page view = 1 operation
- Limit enforced via `@subscription_required` decorator

### 3.4.2 User-Level Analytics

**Feature:** Aggregate analytics across all user's QR codes

**User Flow:**
1. User navigates to `/user/analytics`
2. System displays:
   - Total scans across all QR codes
   - Top performing QR codes
   - Scan trends over time
   - Geographic distribution
   - Device/browser statistics

**Backend Processing:**
- Route: `/user/analytics` (GET)
- Endpoint: `app.py:3073-3236`
- Subscription required
- Analytics usage increment
- Aggregate scan queries
- Data visualization preparation

**Analytics Calculations:**
- Dynamic QR codes only
- Scan aggregation by QR code
- Time-series grouping (daily, weekly, monthly)
- Geographic grouping by country/city
- Device categorization

### 3.4.3 Scan Recording

**Feature:** Automatic scan tracking for dynamic QR codes

**User Flow:**
1. End-user scans QR code
2. QR code redirects to `/r/<qr_id>`
3. System records scan data
4. System redirects to target URL/displays content

**Backend Processing:**
- Route: `/r/<qr_id>` (GET)
- Endpoint: `app.py:3281-3505`
- QR code lookup
- Scan record creation
- Subscription scan limit check
- Redirect or content display

**Data Captured:**
```python
{
    'qr_code_id': QR code ID,
    'timestamp': Current UTC time,
    'ip_address': Request IP,
    'user_agent': Browser user agent,
    'os': Detected OS,
    'location': IP geolocation
}
```

---

## 3.5 Subscription Management

### 3.5.1 Subscription Plans

**Feature:** Tiered subscription plans with different limits

**Plan Structure:**
- **Tier System:** Numeric tier (0, 1, 2, 3, etc.)
- **Features:**
  - QR code generation limit
  - Analytics operations limit
  - Scan limit
  - Design access (templates)
  - Plan duration (days)
  - Auto-renewal option

**Backend Processing:**
- Model: `Subscription` (`models/subscription.py`)
- Fields:
  - S_ID: Primary key
  - plan: Plan name (e.g., "Basic", "Professional", "Enterprise")
  - price: Plan price (INR)
  - days: Duration in days
  - tier: Tier level
  - qr_count: QR code limit
  - analytics: Analytics operations limit
  - scan_limit: Maximum scans allowed
  - design: Comma-separated design list
  - features: JSON-encoded features
  - plan_type: Normal/Special
  - is_active: Active status

### 3.5.2 Subscribing to a Plan

**User Flow:**
1. User navigates to `/pricing`
2. User views available plans
3. User clicks "Subscribe" on desired plan
4. System redirects to checkout
5. User enters billing information
6. User completes Razorpay payment
7. System creates subscription
8. User receives confirmation email

**Backend Processing:**
- Pricing Route: `/pricing` (GET) - `app.py:7102-7109`
- Checkout Route: `/subscription/checkout` (GET, POST)
- Payment Creation: Razorpay Order API
- Subscription Creation: `SubscribedUser` model

**Payment Flow:**
1. Create Razorpay order
2. Display Razorpay checkout
3. Handle payment callback
4. Verify payment signature
5. Create subscription record
6. Send confirmation email
7. Generate invoice

### 3.5.3 Subscription Status

**Feature:** View current subscription details

**User Flow:**
1. User navigates to `/subscription/details`
2. System displays:
   - Current plan name
   - Subscription start/end dates
   - Days remaining
   - Usage statistics (QR, Analytics, Scans)
   - Auto-renewal status
   - Upgrade/downgrade options

**Backend Processing:**
- Route: `/subscription/details` (GET)
- Subscription lookup for current user
- Usage calculation
- Remaining time calculation
- Next billing date (if auto-renew)

**Usage Tracking:**
```python
subscription = {
    'qr_generated': Count of QR codes created,
    'qr_limit': Subscription QR limit,
    'qr_remaining': qr_limit - qr_generated,
    'analytics_used': Analytics operations used,
    'analytics_limit': Subscription analytics limit,
    'analytics_remaining': analytics_limit - analytics_used,
    'scans_used': Total scans recorded,
    'scan_limit': Subscription scan limit,
    'scans_remaining': scan_limit - scans_used
}
```

### 3.5.4 Change Subscription

**Feature:** Upgrade, downgrade, or cancel subscription

**User Flow:**
1. User navigates to subscription management
2. User selects new plan or cancellation
3. System calculates prorated credit (if applicable)
4. User confirms change
5. System processes change
6. System sends confirmation email

**Backend Processing:**
- Route: `/subscription/change` (GET, POST)
- Proration calculation
- Credit application for upgrades
- Immediate downgrade or end-of-period
- Subscription record update

**Proration Logic:**
```python
remaining_value = (days_remaining / total_days) * subscription.price
credit_applied = remaining_value (if upgrading)
final_amount = new_plan.price - credit_applied
```

### 3.5.5 Cancel Subscription

**Feature:** Terminate subscription

**User Flow:**
1. User clicks "Cancel Subscription"
2. System shows retention offer (optional)
3. User confirms cancellation
4. System sets auto-renew to False
5. Subscription expires at end of period

**Backend Processing:**
- Route: `/subscription/cancel` (POST)
- Auto-renewal flag update
- Cancellation email sent
- Subscription remains active until end_date

---

## 3.6 Payment Processing

### 3.6.1 Payment Gateway Integration

**Payment Provider:** Razorpay
**Supported Modes:**
- Test Mode: For development/testing
- Live Mode: For production

**Payment Methods Supported:**
- Credit/Debit Cards
- Net Banking
- UPI
- Wallets (Paytm, PhonePe, etc.)

### 3.6.2 Payment Creation

**User Flow:**
1. User selects subscription plan
2. User clicks "Subscribe Now"
3. System creates Razorpay order
4. System displays checkout modal
5. User completes payment
6. Razorpay redirects to success/failure page

**Backend Processing:**
- Order Creation: Razorpay API call
- Order Storage: `Payment` model
- Invoice Generation: Automatic invoice number
- GST Calculation: 18% GST on base amount

**Payment Record Fields:**
```python
{
    'invoice_number': 'INV-YYYYMMDD-XXXXXX',
    'razorpay_order_id': 'order_XXXXX',
    'razorpay_payment_id': 'pay_XXXXX',
    'base_amount': Subscription price,
    'gst_rate': 0.18,
    'gst_amount': base_amount * 0.18,
    'total_amount': base_amount + gst_amount,
    'status': 'created|completed|failed',
    'payment_type': 'new|upgrade|renewal'
}
```

### 3.6.3 Payment Verification

**Feature:** Verify Razorpay payment signature

**Backend Processing:**
- Webhook Route: `/subscription/payment-callback` (POST)
- Signature Verification: HMAC SHA256
- Payment Update: Status update to 'completed'
- Subscription Activation: Create SubscribedUser record
- Email Notification: Send confirmation email

**Security:**
- HMAC signature verification
- Order ID validation
- Amount verification
- Idempotency check (prevent duplicate processing)

### 3.6.4 Invoice Generation

**Feature:** Automatic invoice PDF generation

**User Flow:**
1. Payment completed
2. System generates invoice PDF
3. System sends invoice via email
4. User can download from profile

**Backend Processing:**
- PDF Generation: ReportLab library
- Invoice Template: Professional layout
- Company Details: Configurable
- GST Breakdown: Detailed tax calculation

**Invoice Contents:**
- Invoice number and date
- Customer details (from invoice_address)
- Subscription plan details
- Base amount
- GST breakdown (CGST/SGST or IGST)
- Total amount
- Payment method
- Transaction ID

### 3.6.5 Payment History

**Feature:** View past payments and invoices

**User Flow:**
1. User navigates to profile
2. User clicks "Activity" tab
3. System displays payment history
4. User can download invoices

**Backend Processing:**
- Route: `/profile` (GET) - Activity tab
- Endpoint: `app.py:1261-1377`
- Payment query filtered by user_id
- Ordered by created_at DESC
- Invoice download links

---

## 3.7 User Profile Management

### 3.7.1 View Profile

**Feature:** Display user account information

**User Flow:**
1. User navigates to `/profile`
2. System displays:
   - Account information (name, email)
   - Subscription status
   - Usage statistics
   - Payment history
   - Security settings

**Backend Processing:**
- Route: `/profile` (GET)
- Endpoint: `app.py:1261-1377`
- User data retrieval
- Subscription data loading
- Payment history query
- Analytics calculation

**Profile Tabs:**
1. **Account:** Personal information
2. **Subscription:** Current plan details
3. **Activity:** Payment history
4. **Security:** Password change

### 3.7.2 Update Profile

**Feature:** Modify account information

**User Flow:**
1. User edits profile fields
2. User clicks "Save Changes"
3. System validates input
4. System updates database
5. System shows success message

**Backend Processing:**
- Route: `/update_profile` (POST)
- Endpoint: `app.py:1378-1457`
- Field validation
- Database update
- Session update

**Editable Fields:**
- Name (minimum 2 characters)
- (Email change requires re-verification - feature pending)

### 3.7.3 Change Password

**Feature:** Update account password

**User Flow:**
1. User navigates to Security tab
2. User enters current password
3. User enters new password (twice)
4. System validates password strength
5. System updates password hash

**Backend Processing:**
- Route: `/update_profile` (POST) with update_type='security'
- Endpoint: `app.py:1401-1453`
- Current password verification
- New password validation
- Password hash update
- Security log entry

**Password Requirements:**
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

---

## 3.8 Admin Panel

### 3.8.1 Admin Dashboard

**Feature:** Administrative overview and management

**Access:** Admin users only (is_admin=True)

**User Flow:**
1. Admin logs in
2. Admin navigates to `/admin/dashboard`
3. System displays:
   - User statistics
   - Subscription statistics
   - Revenue metrics
   - Recent activity
   - System health

**Backend Processing:**
- Route: `/admin/dashboard` (GET)
- Model: `models/admin.py`
- Admin authentication required
- Aggregate data queries

### 3.8.2 User Management

**Feature:** Manage user accounts

**Admin Capabilities:**
1. View all users
2. Search users
3. View user details
4. Edit user subscriptions
5. Grant extra usage limits
6. Deactivate/reactivate accounts

**Backend Processing:**
- Route: `/admin/users` (GET)
- User listing with pagination
- Search functionality
- Bulk actions support

### 3.8.3 Subscription Management

**Feature:** Manage subscription plans

**Admin Capabilities:**
1. Create new plans
2. Edit existing plans
3. Archive plans
4. Set pricing
5. Configure limits
6. Manage plan features

**Backend Processing:**
- Route: `/admin/subscriptions` (GET, POST)
- CRUD operations on Subscription model
- Plan activation/deactivation

### 3.8.4 Payment Management

**Feature:** View and manage payments

**Admin Capabilities:**
1. View all payments
2. Filter by status
3. View invoice details
4. Issue refunds (manual process)
5. Export payment data

**Backend Processing:**
- Route: `/admin/payments` (GET)
- Payment listing with filters
- Invoice viewing

### 3.8.5 Website Settings

**Feature:** Configure site-wide settings

**Admin Capabilities:**
1. Update website name
2. Change website icon
3. Upload logo
4. Set tagline
5. Configure email templates

**Backend Processing:**
- Route: `/admin/website-settings` (GET, POST)
- Model: `WebsiteSettings`
- Settings storage as key-value pairs

---

## 3.9 Email System

### 3.9.1 Email Configuration

**Email Service:** Gmail SMTP with OAuth2 support

**Email Accounts:**
1. **payment@qrdada.com:** Payment confirmations and invoices
2. **support@qrdada.com:** Verification, password reset, contact form

**Backend Processing:**
- Service: `utils/email_service.py`
- Authentication: App-specific passwords
- SMTP Server: smtp.gmail.com:587
- TLS: Enabled

### 3.9.2 Email Types

#### 1. Verification Email
- **Trigger:** User registration
- **Sender:** support@qrdada.com
- **Template:** Plain text with verification link
- **Token Expiry:** 24 hours

#### 2. Password Reset Email
- **Trigger:** Password reset request
- **Sender:** support@qrdada.com
- **Template:** Plain text with reset link
- **Token Expiry:** 30 minutes

#### 3. Payment Confirmation Email
- **Trigger:** Successful payment
- **Sender:** payment@qrdada.com
- **Template:** HTML with invoice details
- **Attachments:** Invoice PDF

#### 4. Subscription Expiry Notification
- **Trigger:** 7 days, 3 days, 1 day before expiry
- **Sender:** support@qrdada.com
- **Template:** Renewal reminder
- **Scheduler:** APScheduler automated task

#### 5. Contact Form Submission
- **Trigger:** Contact form submission
- **Sender:** support@qrdada.com
- **Recipients:** Admin, user (confirmation)

### 3.9.3 Email Logging

**Feature:** Track all email sending attempts

**Backend Processing:**
- Model: `EmailLog` (`models/user.py:106-208`)
- Log created for every email attempt
- Status tracking: sent, failed, bounced

**Logged Data:**
- Recipient email and name
- Email type
- Subject
- Status
- Timestamp
- Error message (if failed)
- IP address and user agent
- Metadata (JSON)

---

## 3.10 Contact and Support

### 3.10.1 Contact Form

**Feature:** User contact form for support requests

**User Flow:**
1. User navigates to `/contact`
2. User fills out form:
   - Name
   - Email
   - Subject
   - Message
3. User submits form
4. System sends email to admin
5. System sends confirmation to user

**Backend Processing:**
- Route: `/contact` (GET, POST)
- Endpoint: `app.py:6921-6994`
- Model: `ContactSubmission`
- Email notification to admin
- Confirmation email to user

### 3.10.2 Help Center

**Feature:** FAQ and documentation

**User Flow:**
1. User navigates to `/help`
2. System displays help topics
3. User finds answers or contacts support

**Backend Processing:**
- Route: `/help` (GET)
- Endpoint: `app.py:3583-3587`
- Static content rendering

---

# 4. Technical Documentation

## 4.1 Database Models

### 4.1.1 User Model

**Table:** `user`

**Purpose:** Store user account information

**Fields:**
```python
id: Integer, Primary Key
name: String(100), Not Null
company_email: String(100), Unique, Not Null
password_hash: String(200), Not Null
is_admin: Boolean, Default=False
email_confirmed: Boolean, Default=False
email_confirm_token: String(500), Nullable
email_token_created_at: DateTime, Nullable
created_at: DateTime, Default=UTC Now
```

**Relationships:**
- qr_codes: One-to-Many with QRCode
- subscriptions: One-to-Many with SubscribedUser
- payments: One-to-Many with Payment
- email_logs: One-to-Many with EmailLog

**Methods:**
- `set_password(password)`: Hash and store password
- `check_password(password)`: Verify password
- `get_reset_token()`: Generate password reset token
- `verify_reset_token(token)`: Verify reset token
- `get_email_confirm_token()`: Generate email verification token
- `verify_email_token(token)`: Verify email token

**File:** `models/user.py:13-105`

### 4.1.2 QRCode Model

**Table:** `qr_code`

**Purpose:** Store QR code metadata and styling

**Fields:**
```python
id: Integer, Primary Key
unique_id: String(36), Unique, Not Null (UUID)
name: String(100), Not Null
qr_type: String(50), Not Null (url, email, vcard, etc.)
is_dynamic: Boolean, Default=False
content: Text, Not Null
created_at: DateTime, Default=UTC Now
updated_at: DateTime, Default=UTC Now, OnUpdate=UTC Now

# Basic Styling
color: String(20), Default='#000000'
background_color: String(20), Default='#FFFFFF'
logo_path: String(200), Nullable
frame_type: String(50), Nullable
shape: String(50), Default='square'

# Advanced Styling
template: String(50), Nullable
custom_eyes: Boolean, Default=False
inner_eye_style: String(50), Nullable
outer_eye_style: String(50), Nullable
inner_eye_color: String(20), Nullable
outer_eye_color: String(20), Nullable
module_size: Integer, Default=10
quiet_zone: Integer, Default=4
error_correction: String(1), Default='H'

# Gradient Options
gradient: Boolean, Default=False
gradient_start: String(20), Nullable
gradient_end: String(20), Nullable
gradient_type: String(20), Nullable
gradient_direction: String(20), Nullable

# Frame Options
frame_color: String(20), Nullable
frame_text: String(100), Nullable

# Export Options
export_type: String(20), Default='png'
watermark_text: String(100), Nullable
logo_size_percentage: Integer, Default=25
round_logo: Boolean, Default=False

# Ownership
user_id: Integer, ForeignKey('user.id'), Not Null
```

**Relationships:**
- owner: Many-to-One with User
- scans: One-to-Many with Scan
- email_detail: One-to-One with QREmail
- phone_detail: One-to-One with QRPhone
- sms_detail: One-to-One with QRSms
- whatsapp_detail: One-to-One with QRWhatsApp
- vcard_detail: One-to-One with QRVCard
- event_detail: One-to-One with QREvent
- wifi_detail: One-to-One with QRWifi
- text_detail: One-to-One with QRText
- link_detail: One-to-One with QRLink

**File:** `models/qr_models.py:5-52`

### 4.1.3 Subscription Model

**Table:** `subscriptions`

**Purpose:** Define subscription plan templates

**Fields:**
```python
S_ID: Integer, Primary Key
plan: String(100), Not Null (Plan name)
price: Float, Not Null (Price in INR)
days: Integer, Not Null (Duration)
tier: Integer, Not Null (Tier level)
features: Text, Nullable (JSON features)
is_active: Boolean, Default=True
archived_at: DateTime, Nullable
plan_type: String(50), Default='Normal'
design: Text, Nullable (Comma-separated designs)
analytics: Integer, Default=0 (Analytics limit)
qr_count: Integer, Default=0 (QR code limit)
scan_limit: Integer, Default=0 (Scan limit)
```

**Relationships:**
- subscribed_users: One-to-Many with SubscribedUser
- payments: One-to-Many with Payment

**Methods:**
- `get_designs()`: Return list of allowed designs
- `is_design_allowed(design_name)`: Check design access

**File:** `models/subscription.py:36-88`

### 4.1.4 SubscribedUser Model

**Table:** `subscribed_users`

**Purpose:** Track user subscription instances

**Fields:**
```python
id: Integer, Primary Key
U_ID: Integer, ForeignKey('user.id'), Not Null
S_ID: Integer, ForeignKey('subscriptions.S_ID'), Not Null
start_date: DateTime, Default=UTC Now
end_date: DateTime, Not Null
current_usage: Integer, Default=0 (Legacy)
last_usage_reset: DateTime, Default=UTC Now
is_auto_renew: Boolean, Default=True
_is_active: Boolean, Default=True

# Usage Tracking
analytics_used: Integer, Default=0
qr_generated: Integer, Default=0
scans_used: Integer, Default=0

# User-Specific Limits (Overrides)
user_analytics_limit: Integer, Nullable
user_qr_limit: Integer, Nullable
user_scan_limit: Integer, Nullable
```

**Relationships:**
- user: Many-to-One with User
- subscription: Many-to-One with Subscription

**Computed Properties:**
- `effective_analytics_limit`: User limit or subscription default
- `effective_qr_limit`: User limit or subscription default
- `effective_scan_limit`: User limit or subscription default
- `analytics_percent`: Usage percentage
- `qr_percent`: Usage percentage
- `scan_percent`: Usage percentage
- `days_remaining`: Calculate remaining days
- `is_active`: Check if subscription is active

**Methods:**
- `increment_analytics()`: Increment analytics usage
- `increment_qr()`: Increment QR usage
- `increment_scan()`: Increment scan usage
- `get_qr_remaining()`: Get remaining QR codes
- `get_analytics_remaining()`: Get remaining analytics
- `get_scans_remaining()`: Get remaining scans
- `remaining_value()`: Calculate proration value

**File:** `models/subscription.py:90-300`

### 4.1.5 Payment Model

**Table:** `payments`

**Purpose:** Track payment transactions

**Fields:**
```python
iid: Integer, Primary Key
user_id: Integer, ForeignKey('user.id'), Not Null
subscription_id: Integer, ForeignKey('subscriptions.S_ID'), Not Null
razorpay_order_id: String(100), Not Null
razorpay_payment_id: String(100), Nullable

# Invoice Details
invoice_number: String(50), Unique, Not Null
invoice_date: DateTime, Default=UTC Now
order_number: String(50), Nullable
customer_number: String(50), Nullable
purchase_order: String(50), Nullable
payment_terms: String(100), Default='Credit Card'

# Amounts
base_amount: Float, Not Null
gst_rate: Float, Default=0.18
gst_amount: Float, Not Null
total_amount: Float, Not Null

# Tax Info
hsn_code: String(20), Nullable
cin_number: String(50), Nullable

# Payment Info
currency: String(10), Default='INR'
status: String(20), Default='created'
created_at: DateTime, Default=UTC Now
payment_type: String(20), Default='new'
previous_subscription_id: Integer, ForeignKey('subscriptions.S_ID'), Nullable
credit_applied: Float, Default=0.0
notes: Text, Nullable
```

**Relationships:**
- user: Many-to-One with User
- subscription: Many-to-One with Subscription
- previous_subscription: Many-to-One with Subscription
- invoice_address: One-to-One with InvoiceAddress

**Methods:**
- `_generate_invoice_details()`: Generate invoice number
- `_calculate_total_amount()`: Calculate GST and total
- `get_invoice_summary()`: Return invoice data

**File:** `models/payment.py:7-132`

### 4.1.6 Scan Model

**Table:** `scan`

**Purpose:** Track QR code scans for analytics

**Fields:**
```python
id: Integer, Primary Key
qr_code_id: Integer, ForeignKey('qr_code.id'), Not Null
timestamp: DateTime, Default=UTC Now
ip_address: String(50), Nullable
user_agent: String(200), Nullable
location: String(100), Nullable
os: String(50), Nullable
```

**Relationships:**
- qr_code: Many-to-One with QRCode

**File:** `models/qr_models.py:152-159`

### 4.1.7 Type-Specific QR Models

All type-specific models follow similar pattern:

**QREmail:** email, subject, body
**QRPhone:** phone
**QRSms:** phone, message
**QRWhatsApp:** phone, message
**QRVCard:** name, phone, email, company, title, address, website, logo_path, primary_color, secondary_color, social_media
**QREvent:** title, location, start_date, end_time, description, organizer
**QRWifi:** ssid, password, encryption
**QRText:** text
**QRLink:** url

**File:** `models/qr_models.py:55-151`

### 4.1.8 EmailLog Model

**Table:** `email_logs`

**Purpose:** Track all email sending attempts

**Fields:**
```python
id: Integer, Primary Key
recipient_email: String(255), Not Null, Indexed
recipient_name: String(100), Nullable
user_id: Integer, ForeignKey('user.id'), Nullable, Indexed
email_type: String(50), Not Null, Indexed
subject: String(255), Not Null
status: String(20), Default='sent'
email_metadata: Text, Nullable (JSON)
sent_at: DateTime, Default=UTC Now
error_message: Text, Nullable
ip_address: String(45), Nullable
user_agent: String(500), Nullable
```

**Relationships:**
- user: Many-to-One with User

**Methods:**
- `log_email()`: Static method to create log entry
- `formatted_sent_time`: Property for display formatting

**File:** `models/user.py:106-208`

### 4.1.9 ContactSubmission Model

**Table:** `contact_submissions`

**Purpose:** Store contact form submissions

**Fields:**
```python
id: Integer, Primary Key
name: String(100), Not Null
email: String(255), Not Null
subject: String(255), Not Null
message: Text, Not Null
submitted_at: DateTime, Default=UTC Now
status: String(20), Default='new'
admin_notes: Text, Nullable
```

**File:** `models/contact.py`

### 4.1.10 WebsiteSettings Model

**Table:** `website_settings`

**Purpose:** Store site-wide configuration

**Fields:**
```python
id: Integer, Primary Key
key: String(100), Unique, Not Null
value: Text, Nullable
updated_at: DateTime, Default=UTC Now, OnUpdate=UTC Now
```

**Methods:**
- `get_setting(key, default)`: Retrieve setting value
- `set_setting(key, value)`: Update setting value

**File:** `models/admin.py`

---

## 4.2 Backend Architecture

### 4.2.1 Application Entry Point

**File:** `app.py`

**Main Components:**
1. **Flask App Initialization:** Lines 75-88
2. **Configuration Loading:** Lines 96-280
3. **Database Initialization:** Lines 127-132
4. **Blueprint Registration:** Lines 135-136
5. **Email Service:** Lines 259-263
6. **Scheduler:** Lines 274-280

### 4.2.2 Configuration Management

**Configuration Source:** Environment variables via `.env` file

**Key Configuration Groups:**

1. **Flask Core:**
   - SECRET_KEY
   - FLASK_ENV
   - FLASK_DEBUG
   - FLASK_HOST
   - FLASK_PORT

2. **Database:**
   - SQLALCHEMY_DATABASE_URI
   - SQLALCHEMY_TRACK_MODIFICATIONS

3. **Security:**
   - WTF_CSRF_ENABLED
   - WTF_CSRF_SECRET_KEY
   - SESSION_COOKIE_SECURE
   - SESSION_COOKIE_HTTPONLY
   - SESSION_COOKIE_SAMESITE

4. **File Upload:**
   - UPLOAD_FOLDER
   - MAX_CONTENT_LENGTH (20MB)

5. **Payment (Razorpay):**
   - RAZORPAY_KEY_ID
   - RAZORPAY_KEY_SECRET
   - RAZORPAY_WEBHOOK_SECRET

6. **Email:**
   - MAIL_SERVER
   - MAIL_PORT
   - MAIL_USE_TLS
   - PAYMENT_EMAIL_PASSWORD
   - SUPPORT_EMAIL_PASSWORD

7. **Logging:**
   - LOG_LEVEL
   - LOG_FILE

**File:** `.env`

### 4.2.3 Database Connection

**Database Engine:** PostgreSQL (Production), SQLite (Development)

**Connection URI Format:**
```
postgresql://username:password@host:port/database
```

**SQLAlchemy Configuration:**
```python
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

**Migrations:**
- **Tool:** Flask-Migrate (Alembic)
- **Directory:** `migrations/`
- **Commands:**
  - `flask db init`: Initialize migrations
  - `flask db migrate -m "message"`: Create migration
  - `flask db upgrade`: Apply migrations
  - `flask db downgrade`: Revert migrations

### 4.2.4 Authentication System

**Authentication Library:** Flask-Login

**Login Manager Configuration:**
```python
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'You need to log in to access this page.'
login_manager.login_message_category = 'info'
```

**User Loader:**
```python
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

**Session Management:**
- Session data stored in secure cookies
- HTTPOnly flag enabled
- Secure flag enabled (HTTPS)
- SameSite=Lax

**Password Hashing:**
- Library: Werkzeug Security
- Algorithm: bcrypt (via generate_password_hash)
- Salt: Automatic per password

### 4.2.5 Email Service

**Implementation:** Custom OAuth2-based email service

**Email Accounts:**
1. **payment@qrdada.com**
   - Purpose: Payment confirmations, invoices
   - Password: App-specific password (PAYMENT_EMAIL_PASSWORD)

2. **support@qrdada.com**
   - Purpose: Verification, password reset, support
   - Password: App-specific password (SUPPORT_EMAIL_PASSWORD)

**Service Class:**
```python
class EmailService:
    def send_payment_email(to, subject, body, attachments=None)
    def send_support_email(to, subject, body)
```

**File:** `utils/email_service.py`

### 4.2.6 QR Code Generation

**Library:** python-qrcode with Pillow

**Generation Process:**
1. Create QRCode instance with parameters
2. Add data to QR code
3. Apply module drawer (shape)
4. Apply color/gradient
5. Draw custom eyes (if enabled)
6. Add logo (if provided)
7. Add frame (if selected)
8. Save to BytesIO or file

**Module Drawers:**
- SquareModuleDrawer: Standard square modules
- RoundedModuleDrawer: Rounded corners
- CircleModuleDrawer: Circular modules
- VerticalBarsDrawer: Vertical bar patterns
- HorizontalBarsDrawer: Horizontal bar patterns
- GappedSquareModuleDrawer: Squares with gaps
- DiamondModuleDrawer: Custom diamond shape
- CrossModuleDrawer: Custom X pattern

**File:** `app.py:411-472`

### 4.2.7 Payment Processing

**Gateway:** Razorpay

**Order Creation:**
```python
razorpay_client.order.create({
    'amount': amount_in_paise,
    'currency': 'INR',
    'payment_capture': 1
})
```

**Payment Verification:**
```python
params_dict = {
    'razorpay_order_id': order_id,
    'razorpay_payment_id': payment_id,
    'razorpay_signature': signature
}
razorpay_client.utility.verify_payment_signature(params_dict)
```

**Webhook Handling:**
- Signature verification with HMAC SHA256
- Idempotency checks
- Status updates
- Subscription activation

**File:** `models/subscription.py` (Blueprint routes)

### 4.2.8 Caching Strategy

**Cache Type:** Simple (in-memory) or Redis

**Cached Data:**
- Website settings
- Subscription plans
- User subscription status

**Cache Configuration:**
```python
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # 5 minutes
```

**Usage Example:**
```python
@cache.cached(timeout=300, key_prefix='all_subscriptions')
def get_all_subscriptions():
    return Subscription.query.filter_by(is_active=True).all()
```

### 4.2.9 Scheduler System

**Library:** APScheduler 3.10.4

**Purpose:** Automated background tasks

**Tasks:**
1. **Subscription Expiry Notifications**
   - 7 days before expiry
   - 3 days before expiry
   - 1 day before expiry
   - On expiry day

2. **Subscription Cleanup**
   - Deactivate expired subscriptions
   - Archive old data

**Configuration:**
```python
scheduler = BackgroundScheduler()
scheduler.add_job(
    func=send_expiry_notifications,
    trigger='cron',
    hour=9,  # 9 AM daily
    minute=0
)
scheduler.start()
```

**File:** `scheduler.py`

---

# 5. API Routes Reference

## 5.1 Public Routes (No Authentication Required)

### Landing and Info Pages
| Route | Method | Purpose | File Reference |
|-------|--------|---------|----------------|
| `/` | GET | Homepage/landing page | `app.py:714-717` |
| `/about` | GET | About page | `app.py:7001-7003` |
| `/pricing` | GET | Subscription plans | `app.py:7102-7109` |
| `/contact` | GET, POST | Contact form | `app.py:6921-6994` |
| `/privacy` | GET | Privacy policy | `app.py:6995-6997` |
| `/terms` | GET | Terms of service | `app.py:6998-7000` |
| `/cookie-policy` | GET | Cookie policy | `app.py:7004-7006` |
| `/help` | GET | Help center | `app.py:3583-3587` |

### Authentication Routes
| Route | Method | Purpose | File Reference |
|-------|--------|---------|----------------|
| `/login` | GET, POST | User login | `app.py:719-791` |
| `/signup` | GET, POST | User registration | `app.py:800-872` |
| `/register` | GET, POST | Alias for signup | `app.py:793-798` |
| `/verify_email/<token>` | GET | Email verification | `app.py:930-943` |
| `/verify_account` | GET | Verification pending page | `app.py:925-928` |
| `/resend_verification` | GET, POST | Resend verification email | `app.py:945-968` |
| `/reset_password` | GET, POST | Password reset request | `app.py:970-984` |
| `/reset_password/<token>` | GET, POST | Password reset form | `app.py:986-1028` |
| `/check-email-availability` | POST | AJAX email check | `app.py:874-912` |

### Service Pages (Public)
| Route | Method | Purpose | File Reference |
|-------|--------|---------|----------------|
| `/services/qr-code-for-url` | GET | URL QR info | `app.py:3589-3592` |
| `/services/qr-code-for-email` | GET | Email QR info | `app.py:3594-3597` |
| `/services/qr-code-for-wifi` | GET | WiFi QR info | `app.py:3599-3602` |
| `/services/qr-code-for-sms` | GET | SMS QR info | `app.py:3604-3607` |
| `/services/qr-code-for-event` | GET | Event QR info | `app.py:3609-3612` |
| `/services/qr-code-for-call` | GET | Call QR info | `app.py:3614-3617` |
| `/services/qr-code-for-whatsapp` | GET | WhatsApp QR info | `app.py:3619-3622` |
| `/services/qr-code-for-vcard` | GET | vCard QR info | `app.py:3624-3627` |
| `/services/qr-code-for-text` | GET | Text QR info | `app.py:3629-3632` |

### QR Code Scanning (Public)
| Route | Method | Purpose | File Reference |
|-------|--------|---------|----------------|
| `/r/<qr_id>` | GET | QR code redirect/scan | `app.py:3281-3505` |
| `/text_display/<qr_id>` | GET | Text QR display |  |
| `/vcard_display/<qr_id>` | GET | vCard display page |  |
| `/wifi_display/<qr_id>` | GET | WiFi display page |  |
| `/event_display/<qr_id>` | GET | Event display page |  |

## 5.2 Protected Routes (Login Required)

### User Dashboard and Profile
| Route | Method | Purpose | File Reference |
|-------|--------|---------|----------------|
| `/dashboard` | GET | User dashboard | `app.py:1134-1256` |
| `/profile` | GET | User profile page | `app.py:1261-1377` |
| `/update_profile` | POST | Update profile data | `app.py:1378-1457` |
| `/logout` | GET | User logout | `app.py:1030-1036` |
| `/check_password` | POST | Verify current password | `app.py:914-923` |

### QR Code Management
| Route | Method | Purpose | File Reference |
|-------|--------|---------|----------------|
| `/create` | GET, POST | Create new QR code | `app.py:1510-2120` |
| `/preview-qr` | GET, POST | Preview QR code | `app.py:2120-2524` |
| `/qr/<qr_id>` | GET | View QR code details | `app.py:2525-2561` |
| `/qr/<qr_id>/edit` | GET, POST | Edit QR code | `app.py:2562-2795` |
| `/qr/<qr_id>/delete` | POST | Delete QR code | `app.py:2796-2848` |
| `/qr/<qr_id>/download` | GET | Download QR code | `app.py:2849-2928` |
| `/qr/<qr_id>/export/<format>` | GET | Export QR (PNG/SVG/PDF) | `app.py:3237-3280` |
| `/batch-export` | POST | Export multiple QR codes | `app.py:3506-3582` |

### Analytics
| Route | Method | Purpose | File Reference |
|-------|--------|---------|----------------|
| `/qr/<qr_id>/analytics` | GET | QR code analytics | `app.py:2946-3072` |
| `/user/analytics` | GET | User-level analytics | `app.py:3073-3236` |

### Subscription and Payments
| Route | Method | Purpose | File Reference |
|-------|--------|---------|----------------|
| `/subscription/checkout` | GET, POST | Subscription checkout | Subscription blueprint |
| `/subscription/details` | GET | View subscription | Subscription blueprint |
| `/subscription/change` | GET, POST | Change subscription | Subscription blueprint |
| `/subscription/cancel` | POST | Cancel subscription | Subscription blueprint |
| `/receipt/<payment_id>` | GET | Download receipt | `app.py:1460-1472` |

## 5.3 Admin Routes (Admin Only)

### Admin Panel
| Route | Method | Purpose | File Reference |
|-------|--------|---------|----------------|
| `/admin/login` | GET, POST | Admin login | Admin blueprint |
| `/admin/dashboard` | GET | Admin dashboard | Admin blueprint |
| `/admin/users` | GET | User management | Admin blueprint |
| `/admin/user_details/<user_id>` | GET | User details | Admin blueprint |
| `/admin/subscriptions` | GET | Subscription management | Admin blueprint |
| `/admin/subscribed_users` | GET | Active subscriptions | Admin blueprint |
| `/admin/payments` | GET | Payment management | Admin blueprint |
| `/admin/payment_details/<payment_id>` | GET | Payment details | Admin blueprint |
| `/admin/contact_submissions` | GET | Contact form submissions | Admin blueprint |
| `/admin/email_logs` | GET | Email log viewer | Admin blueprint |
| `/admin/website_settings` | GET, POST | Site settings | Admin blueprint |
| `/admin/sync-subscription-data` | GET | Sync subscription data | `app.py:7110-end` |

## 5.4 API Endpoints (AJAX)

### AJAX Routes
| Route | Method | Purpose | File Reference |
|-------|--------|---------|----------------|
| `/check-email-availability` | POST | Check email uniqueness | `app.py:874-912` |
| `/check_password` | POST | Verify password | `app.py:914-923` |
| `/set_timezone` | POST | Set user timezone | `app.py:5541-end` |

## 5.5 Subscription Blueprint Routes

**Prefix:** `/subscription`

| Route | Method | Purpose |
|-------|--------|---------|
| `/checkout` | GET, POST | Subscription checkout and payment |
| `/payment-callback` | POST | Razorpay payment webhook |
| `/verify-payment` | POST | Verify payment status |
| `/details` | GET | View subscription details |
| `/change` | GET, POST | Change subscription plan |
| `/cancel` | POST | Cancel auto-renewal |
| `/upgrade` | POST | Upgrade subscription |
| `/downgrade` | POST | Downgrade subscription |
| `/renew` | POST | Renew expired subscription |
| `/invoice/<payment_id>` | GET | Download invoice PDF |

**File:** `models/subscription.py`

## 5.6 Admin Blueprint Routes

**Prefix:** `/admin`

| Route | Method | Purpose |
|-------|--------|---------|
| `/login` | GET, POST | Admin authentication |
| `/dashboard` | GET | Admin overview |
| `/users` | GET | List all users |
| `/users/<user_id>` | GET | User details |
| `/users/<user_id>/edit` | POST | Edit user |
| `/users/<user_id>/delete` | POST | Delete user |
| `/subscriptions` | GET | Manage plans |
| `/subscriptions/new` | GET, POST | Create plan |
| `/subscriptions/<id>/edit` | GET, POST | Edit plan |
| `/subscriptions/<id>/archive` | POST | Archive plan |
| `/subscribed_users` | GET | Active subscribers |
| `/subscribed_users/<id>` | GET | Subscription details |
| `/subscribed_users/<id>/edit` | POST | Edit user subscription |
| `/payments` | GET | Payment history |
| `/payments/<id>` | GET | Payment details |
| `/contact_submissions` | GET | Contact form inbox |
| `/contact_submissions/<id>` | GET | Submission details |
| `/email_logs` | GET | Email delivery logs |
| `/website_settings` | GET, POST | Configure site |

**File:** `models/admin.py`

---

# 6. Database Schema

## 6.1 Entity Relationship Diagram (ERD)

```
┌─────────────────────┐
│       User          │
├─────────────────────┤
│ id (PK)             │
│ name                │
│ company_email       │
│ password_hash       │
│ is_admin            │
│ email_confirmed     │
│ created_at          │
└──────────┬──────────┘
           │
           │ 1:N
           │
           ├──────────────────────────────┐
           │                              │
           │                              │
    ┌──────▼──────────┐          ┌───────▼────────┐
    │    QRCode       │          │ SubscribedUser │
    ├─────────────────┤          ├────────────────┤
    │ id (PK)         │          │ id (PK)        │
    │ user_id (FK)    │          │ U_ID (FK)      │
    │ unique_id       │          │ S_ID (FK)      │
    │ name            │          │ start_date     │
    │ qr_type         │          │ end_date       │
    │ is_dynamic      │          │ qr_generated   │
    │ content         │          │ analytics_used │
    │ color           │          │ scans_used     │
    │ ... (styling)   │          └────────┬───────┘
    └────────┬────────┘                   │
             │                            │ N:1
             │ 1:N                        │
             │                     ┌──────▼─────────┐
      ┌──────▼─────┐               │  Subscription  │
      │    Scan    │               ├────────────────┤
      ├────────────┤               │ S_ID (PK)      │
      │ id (PK)    │               │ plan           │
      │ qr_code_id │               │ price          │
      │ timestamp  │               │ days           │
      │ ip_address │               │ qr_count       │
      │ user_agent │               │ analytics      │
      │ location   │               │ scan_limit     │
      │ os         │               │ tier           │
      └────────────┘               └────────────────┘
                                           │
                                           │ 1:N
                                           │
                                    ┌──────▼────────┐
                                    │    Payment    │
                                    ├───────────────┤
                                    │ iid (PK)      │
                                    │ user_id (FK)  │
                                    │ subscription_id│
                                    │ invoice_number│
                                    │ base_amount   │
                                    │ gst_amount    │
                                    │ total_amount  │
                                    │ status        │
                                    └───────────────┘
```

## 6.2 Table Relationships

### Primary Relationships:
1. **User → QRCode:** One-to-Many (user owns multiple QR codes)
2. **User → SubscribedUser:** One-to-Many (user can have multiple subscriptions over time)
3. **User → Payment:** One-to-Many (user makes multiple payments)
4. **User → EmailLog:** One-to-Many (user receives multiple emails)
5. **Subscription → SubscribedUser:** One-to-Many (plan has multiple subscribers)
6. **Subscription → Payment:** One-to-Many (plan has multiple payments)
7. **QRCode → Scan:** One-to-Many (QR code has multiple scans)
8. **QRCode → QREmail/QRVCard/etc.:** One-to-One (type-specific data)
9. **Payment → InvoiceAddress:** One-to-One (payment has billing address)

## 6.3 Indexes

### User Table:
- Primary Key: `id`
- Unique Index: `company_email`

### QRCode Table:
- Primary Key: `id`
- Unique Index: `unique_id`
- Foreign Key Index: `user_id`

### SubscribedUser Table:
- Primary Key: `id`
- Foreign Key Indexes: `U_ID`, `S_ID`
- Composite Index: `(U_ID, end_date, _is_active)` for active subscription queries

### Payment Table:
- Primary Key: `iid`
- Unique Index: `invoice_number`
- Foreign Key Indexes: `user_id`, `subscription_id`

### Scan Table:
- Primary Key: `id`
- Foreign Key Index: `qr_code_id`
- Index: `timestamp` (for time-based queries)

### EmailLog Table:
- Primary Key: `id`
- Indexes: `recipient_email`, `user_id`, `email_type`

---

# 7. Requirements Specification (SRS)

## 7.1 Functional Requirements

### FR1: User Management
- **FR1.1:** System shall allow new users to register with email and password
- **FR1.2:** System shall send email verification link to new registrants
- **FR1.3:** System shall enforce password complexity requirements
- **FR1.4:** System shall allow users to reset forgotten passwords
- **FR1.5:** System shall maintain user profile information
- **FR1.6:** System shall allow users to update their name
- **FR1.7:** System shall allow users to change their password
- **FR1.8:** System shall provide secure logout functionality

### FR2: QR Code Generation
- **FR2.1:** System shall support 9 QR code types: URL, Email, vCard, WiFi, SMS, Phone, WhatsApp, Event, Text
- **FR2.2:** System shall allow customization of QR code color and background
- **FR2.3:** System shall support logo upload for QR codes (max 20MB)
- **FR2.4:** System shall provide template-based styling (5 templates)
- **FR2.5:** System shall support gradient colors (linear and radial)
- **FR2.6:** System shall allow custom eye patterns for QR codes
- **FR2.7:** System shall support different module shapes (6 shapes)
- **FR2.8:** System shall generate both static and dynamic QR codes
- **FR2.9:** System shall assign unique identifier to each QR code

### FR3: QR Code Management
- **FR3.1:** System shall display all user QR codes on dashboard
- **FR3.2:** System shall allow users to view QR code details
- **FR3.3:** System shall allow editing of dynamic QR codes
- **FR3.4:** System shall allow deletion of QR codes
- **FR3.5:** System shall support QR code download in PNG, SVG, PDF formats
- **FR3.6:** System shall support batch export of multiple QR codes
- **FR3.7:** System shall display QR code creation and update timestamps

### FR4: Analytics and Tracking
- **FR4.1:** System shall track scans of dynamic QR codes
- **FR4.2:** System shall record scan timestamp, IP, user agent, OS, location
- **FR4.3:** System shall display scan analytics for individual QR codes
- **FR4.4:** System shall provide user-level analytics dashboard
- **FR4.5:** System shall generate scan trend charts
- **FR4.6:** System shall categorize scans by device and browser
- **FR4.7:** System shall count analytics operations against subscription limit
- **FR4.8:** System shall prevent analytics access when limit exceeded

### FR5: Subscription Management
- **FR5.1:** System shall support multiple subscription tiers
- **FR5.2:** System shall enforce QR code generation limits per subscription
- **FR5.3:** System shall enforce analytics operation limits per subscription
- **FR5.4:** System shall enforce scan limits per subscription
- **FR5.5:** System shall track subscription start and end dates
- **FR5.6:** System shall calculate days remaining in subscription
- **FR5.7:** System shall allow subscription upgrade with proration
- **FR5.8:** System shall allow subscription downgrade
- **FR5.9:** System shall support auto-renewal of subscriptions
- **FR5.10:** System shall allow users to cancel auto-renewal
- **FR5.11:** System shall send expiry notifications (7, 3, 1 day before)

### FR6: Payment Processing
- **FR6.1:** System shall integrate with Razorpay payment gateway
- **FR6.2:** System shall generate unique invoice numbers
- **FR6.3:** System shall calculate GST (18%) on subscription price
- **FR6.4:** System shall verify payment signatures from Razorpay
- **FR6.5:** System shall generate PDF invoices
- **FR6.6:** System shall send payment confirmation emails
- **FR6.7:** System shall store billing address information
- **FR6.8:** System shall display payment history to users
- **FR6.9:** System shall support credit application for upgrades

### FR7: Email Communications
- **FR7.1:** System shall send verification emails to new users
- **FR7.2:** System shall send password reset emails
- **FR7.3:** System shall send payment confirmation emails with invoices
- **FR7.4:** System shall send subscription expiry notifications
- **FR7.5:** System shall send contact form confirmations
- **FR7.6:** System shall log all email sending attempts
- **FR7.7:** System shall use separate email accounts for payment and support
- **FR7.8:** System shall track email delivery status

### FR8: Admin Panel
- **FR8.1:** System shall provide admin dashboard with statistics
- **FR8.2:** System shall allow admins to view all users
- **FR8.3:** System shall allow admins to manage subscription plans
- **FR8.4:** System shall allow admins to view all payments
- **FR8.5:** System shall allow admins to edit user subscriptions
- **FR8.6:** System shall allow admins to grant extra usage limits
- **FR8.7:** System shall allow admins to view contact submissions
- **FR8.8:** System shall allow admins to view email logs
- **FR8.9:** System shall allow admins to configure website settings

### FR9: Contact and Support
- **FR9.1:** System shall provide contact form on public page
- **FR9.2:** System shall store contact form submissions
- **FR9.3:** System shall email contact submissions to admin
- **FR9.4:** System shall send confirmation to user on contact form submission
- **FR9.5:** System shall provide help center with FAQs

## 7.2 Non-Functional Requirements

### NFR1: Performance
- **NFR1.1:** System shall generate QR codes within 2 seconds
- **NFR1.2:** System shall load dashboard within 3 seconds
- **NFR1.3:** System shall handle 100 concurrent users
- **NFR1.4:** System shall respond to API requests within 1 second
- **NFR1.5:** System shall cache frequently accessed data

### NFR2: Security
- **NFR2.1:** System shall hash passwords using bcrypt algorithm
- **NFR2.2:** System shall use HTTPS for all communications
- **NFR2.3:** System shall implement CSRF protection for forms
- **NFR2.4:** System shall use secure session cookies (HTTPOnly, Secure, SameSite)
- **NFR2.5:** System shall validate all user inputs
- **NFR2.6:** System shall prevent SQL injection attacks
- **NFR2.7:** System shall verify Razorpay payment signatures
- **NFR2.8:** System shall expire password reset tokens after 30 minutes
- **NFR2.9:** System shall expire email verification tokens after 24 hours
- **NFR2.10:** System shall rate-limit login attempts

### NFR3: Usability
- **NFR3.1:** System shall provide responsive design for mobile devices
- **NFR3.2:** System shall display clear error messages
- **NFR3.3:** System shall provide success confirmations
- **NFR3.4:** System shall use consistent UI across all pages
- **NFR3.5:** System shall provide QR code previews before saving
- **NFR3.6:** System shall display usage statistics prominently

### NFR4: Reliability
- **NFR4.1:** System shall have 99.5% uptime
- **NFR4.2:** System shall handle database connection failures gracefully
- **NFR4.3:** System shall log all errors for debugging
- **NFR4.4:** System shall provide database backups
- **NFR4.5:** System shall validate payment status before activating subscriptions

### NFR5: Scalability
- **NFR5.1:** System shall support horizontal scaling
- **NFR5.2:** System shall use database connection pooling
- **NFR5.3:** System shall support CDN for static files
- **NFR5.4:** System shall implement caching for expensive queries

### NFR6: Maintainability
- **NFR6.1:** System shall use modular architecture
- **NFR6.2:** System shall follow PEP 8 coding standards
- **NFR6.3:** System shall use database migrations for schema changes
- **NFR6.4:** System shall log application events
- **NFR6.5:** System shall provide admin tools for troubleshooting

### NFR7: Compatibility
- **NFR7.1:** System shall support modern browsers (Chrome, Firefox, Safari, Edge)
- **NFR7.2:** System shall work on desktop and mobile devices
- **NFR7.3:** System shall support PostgreSQL database
- **NFR7.4:** System shall be deployable on cloud platforms (AWS, DigitalOcean, Heroku)

### NFR8: Data Integrity
- **NFR8.1:** System shall enforce foreign key constraints
- **NFR8.2:** System shall use transactions for payment processing
- **NFR8.3:** System shall validate data before saving to database
- **NFR8.4:** System shall maintain audit trails for critical operations
- **NFR8.5:** System shall prevent duplicate QR code unique_ids

## 7.3 Use Case Specifications

### UC1: User Registration
**Actor:** New User
**Precondition:** User has valid email address
**Flow:**
1. User navigates to signup page
2. User enters name, email, password
3. System validates inputs
4. System creates account
5. System sends verification email
6. User clicks verification link
7. System activates account

**Postcondition:** User account created and verified

### UC2: Create Dynamic QR Code
**Actor:** Authenticated User with Active Subscription
**Precondition:** User has available QR codes in subscription
**Flow:**
1. User navigates to create page
2. User selects QR type (e.g., URL)
3. User enters content (URL)
4. User customizes styling
5. User previews QR code
6. User saves QR code
7. System generates unique ID
8. System stores QR code
9. System increments usage counter

**Postcondition:** Dynamic QR code created and accessible

### UC3: View QR Code Analytics
**Actor:** Authenticated User with Active Subscription
**Precondition:** User has dynamic QR code with scans
**Flow:**
1. User navigates to QR code details
2. User clicks Analytics tab
3. System checks analytics limit
4. System retrieves scan data
5. System displays analytics dashboard
6. System increments analytics usage

**Postcondition:** Analytics displayed, usage incremented

### UC4: Subscribe to Plan
**Actor:** Authenticated User
**Precondition:** User does not have active subscription
**Flow:**
1. User navigates to pricing page
2. User selects plan
3. User enters billing details
4. User completes Razorpay checkout
5. Razorpay processes payment
6. System verifies payment
7. System creates subscription
8. System sends confirmation email
9. System generates invoice

**Postcondition:** User has active subscription

### UC5: Admin Edits User Subscription
**Actor:** Admin
**Precondition:** Admin is logged in
**Flow:**
1. Admin navigates to subscribed users
2. Admin selects user
3. Admin clicks Edit
4. Admin modifies limits or end date
5. Admin saves changes
6. System updates subscription
7. System sends notification to user

**Postcondition:** User subscription updated

---

# 8. Deployment and Configuration

## 8.1 Environment Setup

### Development Environment
1. Clone repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env`
6. Configure environment variables
7. Initialize database: `flask db upgrade`
8. Create super admin: `python app.py` (auto-creates)
9. Run: `flask run`

### Production Environment
1. Set up PostgreSQL database
2. Configure `.env` with production values
3. Set `FLASK_ENV=production`
4. Set `FLASK_DEBUG=False`
5. Enable CSRF: `WTF_CSRF_ENABLED=True`
6. Use production Razorpay keys
7. Configure Gunicorn: `gunicorn -w 4 -b 0.0.0.0:5000 app:application`
8. Set up Nginx reverse proxy
9. Configure SSL/TLS certificates
10. Set up automatic backups

## 8.2 Environment Variables

### Required Variables:
```bash
SECRET_KEY=your-secret-key
SQLALCHEMY_DATABASE_URI=postgresql://user:pass@host:port/db
RAZORPAY_KEY_ID=rzp_test_xxxxx
RAZORPAY_KEY_SECRET=secret_key
PAYMENT_EMAIL_PASSWORD=app_password
SUPPORT_EMAIL_PASSWORD=app_password
```

### Optional Variables:
```bash
FLASK_ENV=development
FLASK_DEBUG=True
LOG_LEVEL=INFO
CACHE_TYPE=simple
DEFAULT_TIMEZONE=Asia/Calcutta
```

## 8.3 Database Migration

### Create Migration:
```bash
flask db migrate -m "Description of changes"
```

### Apply Migration:
```bash
flask db upgrade
```

### Rollback Migration:
```bash
flask db downgrade
```

## 8.4 Gunicorn Configuration

**File:** `gunicorn.conf.py` (create if needed)

```python
workers = 4
bind = "0.0.0.0:5000"
worker_class = "sync"
timeout = 120
keepalive = 5
errorlog = "logs/gunicorn-error.log"
accesslog = "logs/gunicorn-access.log"
loglevel = "info"
```

**Run Command:**
```bash
gunicorn -c gunicorn.conf.py app:application
```

## 8.5 Nginx Configuration

**File:** `/etc/nginx/sites-available/qrdada`

```nginx
server {
    listen 80;
    server_name qrdada.com www.qrdada.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/qrdada/static;
        expires 30d;
    }
}
```

## 8.6 Systemd Service

**File:** `/etc/systemd/system/qrdada.service`

```ini
[Unit]
Description=QRDADA Flask Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/qrdada
Environment="PATH=/path/to/qrdada/venv/bin"
ExecStart=/path/to/qrdada/venv/bin/gunicorn -c gunicorn.conf.py app:application

[Install]
WantedBy=multi-user.target
```

**Commands:**
```bash
sudo systemctl enable qrdada
sudo systemctl start qrdada
sudo systemctl status qrdada
```

---

# 9. Workflow Diagrams

## 9.1 User Registration Flow

```
┌─────────────┐
│   Start     │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│ Fill Signup Form │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐      ┌─────────────┐
│  Validate Input  ├─────►│ Show Errors │
└──────┬───────────┘      └─────────────┘
       │ Valid
       ▼
┌──────────────────┐
│ Create User      │
│ (email_confirmed │
│  = False)        │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Generate Token   │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Send Email       │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ User Clicks Link │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Verify Token     │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Set email_       │
│ confirmed = True │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Redirect to Login│
└──────┬───────────┘
       │
       ▼
┌─────────────┐
│     End     │
└─────────────┘
```

## 9.2 QR Code Creation Flow

```
┌─────────────┐
│   Start     │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│ Check Login      │
└──────┬───────────┘
       │ Logged in
       ▼
┌──────────────────┐
│ Check Subscription│
└──────┬───────────┘
       │ Has active subscription
       ▼
┌──────────────────┐
│ Check QR Limit   │
└──────┬───────────┘
       │ Within limit
       ▼
┌──────────────────┐
│ Select QR Type   │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Enter Content    │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Customize Style  │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐      ┌─────────────┐
│ Check Design     ├─────►│ Show Error  │
│ Access           │      │ (Premium    │
└──────┬───────────┘      │  Required)  │
       │ Allowed          └─────────────┘
       ▼
┌──────────────────┐
│ Preview QR       │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Generate UUID    │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Create QR Code   │
│ (qrcode library) │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Apply Styling    │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Save to DB       │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Increment Usage  │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Display Success  │
└──────┬───────────┘
       │
       ▼
┌─────────────┐
│     End     │
└─────────────┘
```

## 9.3 Payment and Subscription Flow

```
┌─────────────┐
│   Start     │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│ Select Plan      │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Enter Billing    │
│ Information      │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Calculate GST    │
│ (18%)            │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Create Razorpay  │
│ Order            │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Save Payment     │
│ (status=created) │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Show Razorpay    │
│ Checkout         │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ User Pays        │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Razorpay Callback│
└──────┬───────────┘
       │
       ▼
┌──────────────────┐      ┌─────────────┐
│ Verify Signature ├─────►│ Payment     │
└──────┬───────────┘      │ Failed      │
       │ Valid            └─────────────┘
       ▼
┌──────────────────┐
│ Update Payment   │
│ (status=completed│
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Create           │
│ SubscribedUser   │
│ Record           │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Generate Invoice │
│ PDF              │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Send Confirmation│
│ Email with Invoice│
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Log Email        │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Redirect to      │
│ Success Page     │
└──────┬───────────┘
       │
       ▼
┌─────────────┐
│     End     │
└─────────────┘
```

## 9.4 QR Code Scan Flow (Dynamic)

```
┌─────────────┐
│   Start     │
│  (User scans│
│   QR code)  │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│ Redirect to      │
│ /r/<qr_id>       │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐      ┌─────────────┐
│ Lookup QR Code   ├─────►│ 404 Error   │
└──────┬───────────┘      └─────────────┘
       │ Found
       ▼
┌──────────────────┐
│ Check Scan Limit │
└──────┬───────────┘
       │ Within limit
       ▼
┌──────────────────┐
│ Capture Scan Data│
│ (IP, UA, OS,     │
│  Location)       │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Create Scan      │
│ Record           │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Increment        │
│ scans_used       │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Get QR Type      │
└──────┬───────────┘
       │
       ├─── URL ────►┌──────────────┐
       │             │ Redirect to  │
       │             │ Target URL   │
       │             └──────────────┘
       │
       ├─ vCard ────►┌──────────────┐
       │             │ Display vCard│
       │             │ Landing Page │
       │             └──────────────┘
       │
       ├─ WiFi ─────►┌──────────────┐
       │             │ Display WiFi │
       │             │ Credentials  │
       │             └──────────────┘
       │
       └─ Event ────►┌──────────────┐
                     │ Display Event│
                     │ Details      │
                     └──────────────┘
```

## 9.5 Analytics Access Flow

```
┌─────────────┐
│   Start     │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│ Check Login      │
└──────┬───────────┘
       │ Logged in
       ▼
┌──────────────────┐
│ Check Subscription│
└──────┬───────────┘
       │ Active
       ▼
┌──────────────────┐      ┌─────────────┐
│ Check Analytics  ├─────►│ Show Limit  │
│ Limit            │      │ Reached Msg │
└──────┬───────────┘      └─────────────┘
       │ Within limit
       ▼
┌──────────────────┐
│ Retrieve Scan    │
│ Data for QR      │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Aggregate Data   │
│ (by time, device,│
│  location)       │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Generate Charts  │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Display Analytics│
│ Dashboard        │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Increment        │
│ analytics_used   │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Log Usage        │
└──────┬───────────┘
       │
       ▼
┌─────────────┐
│     End     │
└─────────────┘
```

---

# 10. Conclusion

## 10.1 Project Summary

QRDADA is a full-featured QR code generation and analytics platform built on Flask, providing users with:
- Professional QR code generation with extensive customization
- Dynamic QR codes with scan tracking and analytics
- Subscription-based access control with usage limits
- Secure payment processing via Razorpay
- Comprehensive admin panel for platform management
- Automated email communications
- Professional invoicing and billing

## 10.2 Key Technologies

- **Backend:** Flask 3.0.0, Python 3.x
- **Database:** PostgreSQL with SQLAlchemy ORM
- **Frontend:** Jinja2, Tailwind CSS, JavaScript
- **Payment:** Razorpay API
- **QR Generation:** python-qrcode, Pillow
- **Email:** Gmail SMTP with OAuth2
- **Scheduling:** APScheduler
- **Deployment:** Gunicorn, Nginx

## 10.3 Future Enhancements

Potential areas for expansion:
1. **Advanced Analytics:** Heatmaps, conversion tracking, A/B testing
2. **API Access:** RESTful API for programmatic QR creation
3. **Bulk Operations:** CSV import/export, bulk QR generation
4. **White Labeling:** Custom branding for enterprise clients
5. **Mobile App:** Native iOS/Android apps
6. **Social Sharing:** Direct sharing to social media platforms
7. **QR Code Templates:** Expanded template library
8. **Multi-language Support:** Internationalization (i18n)
9. **Advanced Security:** Two-factor authentication (2FA)
10. **Integration Hub:** Zapier, Webhooks, Slack integration

---

# Appendix A: Code Examples

## A.1 QR Code Generation Example

```python
# Basic QR Code Generation
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
qr.add_data(content)
qr.make(fit=True)

# Apply module drawer for shape
module_drawer = get_module_drawer(shape)
img = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=module_drawer,
    color_mask=SolidFillColorMask(color=color)
)
```

## A.2 Subscription Check Decorator

```python
def subscription_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        subscription = SubscribedUser.query.filter(
            SubscribedUser.U_ID == user_id,
            SubscribedUser.end_date > datetime.now(UTC),
            SubscribedUser._is_active == True
        ).first()

        if not subscription:
            flash('Active subscription required', 'warning')
            return redirect(url_for('pricing'))

        return f(*args, **kwargs)
    return decorated_function
```

## A.3 Payment Verification

```python
# Verify Razorpay signature
params_dict = {
    'razorpay_order_id': order_id,
    'razorpay_payment_id': payment_id,
    'razorpay_signature': signature
}

try:
    razorpay_client.utility.verify_payment_signature(params_dict)
    # Signature valid - process payment
except:
    # Signature invalid - reject payment
```

---

# Appendix B: Database Schema SQL

## B.1 User Table

```sql
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    company_email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(200) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    email_confirmed BOOLEAN DEFAULT FALSE,
    email_confirm_token VARCHAR(500),
    email_token_created_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## B.2 QRCode Table

```sql
CREATE TABLE qr_code (
    id SERIAL PRIMARY KEY,
    unique_id VARCHAR(36) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    qr_type VARCHAR(50) NOT NULL,
    is_dynamic BOOLEAN DEFAULT FALSE,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    color VARCHAR(20) DEFAULT '#000000',
    background_color VARCHAR(20) DEFAULT '#FFFFFF',
    logo_path VARCHAR(200),
    frame_type VARCHAR(50),
    shape VARCHAR(50) DEFAULT 'square',
    template VARCHAR(50),
    custom_eyes BOOLEAN DEFAULT FALSE,
    inner_eye_style VARCHAR(50),
    outer_eye_style VARCHAR(50),
    inner_eye_color VARCHAR(20),
    outer_eye_color VARCHAR(20),
    module_size INTEGER DEFAULT 10,
    quiet_zone INTEGER DEFAULT 4,
    error_correction VARCHAR(1) DEFAULT 'H',
    gradient BOOLEAN DEFAULT FALSE,
    gradient_start VARCHAR(20),
    gradient_end VARCHAR(20),
    export_type VARCHAR(20) DEFAULT 'png',
    watermark_text VARCHAR(100),
    logo_size_percentage INTEGER DEFAULT 25,
    round_logo BOOLEAN DEFAULT FALSE,
    frame_text VARCHAR(100),
    gradient_type VARCHAR(20),
    gradient_direction VARCHAR(20),
    frame_color VARCHAR(20),
    user_id INTEGER NOT NULL REFERENCES "user"(id)
);
```

## B.3 Subscription Tables

```sql
CREATE TABLE subscriptions (
    "S_ID" SERIAL PRIMARY KEY,
    plan VARCHAR(100) NOT NULL,
    price FLOAT NOT NULL,
    days INTEGER NOT NULL,
    tier INTEGER NOT NULL,
    features TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    archived_at TIMESTAMP,
    plan_type VARCHAR(50) DEFAULT 'Normal',
    design TEXT,
    analytics INTEGER DEFAULT 0,
    qr_count INTEGER DEFAULT 0,
    scan_limit INTEGER DEFAULT 0
);

CREATE TABLE subscribed_users (
    id SERIAL PRIMARY KEY,
    "U_ID" INTEGER NOT NULL REFERENCES "user"(id),
    "S_ID" INTEGER NOT NULL REFERENCES subscriptions("S_ID"),
    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_date TIMESTAMP NOT NULL,
    current_usage INTEGER DEFAULT 0,
    last_usage_reset TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_auto_renew BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE,
    analytics_used INTEGER DEFAULT 0,
    qr_generated INTEGER DEFAULT 0,
    scans_used INTEGER DEFAULT 0,
    user_analytics_limit INTEGER,
    user_qr_limit INTEGER,
    user_scan_limit INTEGER
);
```

---

**End of Documentation**

---

**Document Control:**
- **Created:** November 2025
- **Author:** Senior Technical Writer & System Analyst
- **Review Status:** Complete
- **Next Review:** Upon major version update

For questions or clarifications, please contact the development team or refer to the inline code documentation.
