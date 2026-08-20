from flask import Flask, render_template, request
from organizer import organize_directory
import os

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    error = None
    summary = None

    if request.method == "POST":
        directory = request.form.get("directory", "").strip()

        if not directory:
            error = "Please enter a directory path."
        elif not os.path.isdir(directory):
            error = "The specified directory does not exist."
        else:
            try:
                summary = organize_directory(directory)
                message = "Files organized successfully."
            except PermissionError:
                error = "Permission denied. Please choose a directory you can modify."
            except Exception as exc:
                error = f"An error occurred: {exc}"

    return render_template(
        "index.html",
        message=message,
        error=error,
        summary=summary
    )


if __name__ == "__main__":
    app.run(debug=True)
