# URL Shortener

A simple Python Flask web application that converts long URLs into short, shareable links.

## Features

- Enter and validate a long URL.
- Generate a unique 6-character short code.
- Store URL mappings in SQLite.
- Redirect short URLs to the original URL.
- Reuse an existing short link for the same URL.
- Simple responsive user interface.
- 404 handling for invalid short URLs.

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- Git/GitHub

## Project Structure

```text
URL-Shortener/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/URL-Shortener.git
cd URL-Shortener
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

### 5. Open in your browser

```text
http://127.0.0.1:5000
```

## How It Works

1. The user enters a long URL.
2. The application validates the URL.
3. A unique short code is generated.
4. The original URL and short code are stored in SQLite.
5. The short URL is displayed to the user.
6. When the short URL is opened, Flask looks up the original URL and redirects the user.

## Future Improvements

- User accounts and authentication.
- URL click analytics.
- Custom short URLs.
- QR code generation.
- URL expiration.
- REST API support.

## License

This project is created for educational and internship purposes.
