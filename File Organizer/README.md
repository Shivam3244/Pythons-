# File Organizer

A Python Flask-based file organization application that scans a selected directory, identifies files by extension, creates category folders, and moves files into the appropriate folders.

## Features

- Organize files automatically by type.
- Supports images, documents, videos, audio, archives, spreadsheets, presentations, and other files.
- Automatically creates category folders.
- Prevents overwriting files with duplicate names.
- Simple web-based interface.
- Displays an organization summary after completion.
- Built with Python and Flask.

## Technologies Used

- Python
- Flask
- HTML
- CSS
- `os`
- `shutil`

## Project Structure

```text
File-Organizer/
├── app.py
├── organizer.py
├── requirements.txt
├── README.md
├── .gitignore
├── LICENSE
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## File Categories

| Category | Examples |
|---|---|
| Images | JPG, PNG, GIF, SVG, WEBP |
| Documents | PDF, DOC, DOCX, TXT |
| Videos | MP4, MKV, AVI, MOV |
| Audio | MP3, WAV, AAC, FLAC |
| Archives | ZIP, RAR, 7Z, TAR |
| Spreadsheets | XLS, XLSX, CSV |
| Presentations | PPT, PPTX, ODP |
| Others | Unsupported file types |

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/File-Organizer.git
cd File-Organizer
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

### 4. Start the application

```bash
python app.py
```

### 5. Open in browser

```text
http://127.0.0.1:5000
```

## How It Works

1. Enter the path of the directory you want to organize.
2. The application scans files in that directory.
3. Each file is classified using its extension.
4. A folder is created for the appropriate category.
5. Files are moved into their category folders.
6. If a file with the same name already exists, a unique filename is generated.
7. The application displays a summary of the files organized.

## Example

Before:

```text
Downloads/
├── photo.jpg
├── resume.pdf
├── movie.mp4
├── song.mp3
└── data.xlsx
```

After:

```text
Downloads/
├── Images/
│   └── photo.jpg
├── Documents/
│   └── resume.pdf
├── Videos/
│   └── movie.mp4
├── Audio/
│   └── song.mp3
└── Spreadsheets/
    └── data.xlsx
```

## Future Improvements

- Add a desktop GUI using Tkinter.
- Add drag-and-drop directory selection.
- Add custom category rules.
- Add undo functionality.
- Add file preview.
- Add logging and activity history.
- Add scheduled automatic organization.

## License

This project is created for educational and internship purposes.
