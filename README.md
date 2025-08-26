# Art Tactile Transform

This project turns a flat picture into a simple 3D model that can be 3D printed. It uses a depth‑estimation model from Hugging Face to create a height map and saves the result as an STL file.

## Step 1 – Install Python

1. Visit <https://www.python.org/downloads/windows/>.
2. Download the Windows installer for **Python&nbsp;3.12 LTS** (64‑bit).
3. Run the installer and check **Add Python to PATH**.

An interpreter is a program that reads your instructions one line at a time and runs them immediately. Unlike older languages such as COBOL or FORTRAN, you do not compile the code before running it.

## Step 2 – Get the project files

Open **Command Prompt** and run:

```
git clone <repository-url>
cd art-tactile-transform
```

If you do not have Git, download the repository as a ZIP file from its web page and unzip it.

## Step 3 – Install the required libraries

```
python -m pip install -r requirements.txt
```

## Step 4 – Configure the program

```
copy .env.example .env
```

Edit the new `.env` file in Notepad and set:

- `MODEL_NAME` – Hugging Face model to use (e.g. `Intel/dpt-large`).
- `IMAGE_PATH` – Path to the input image file (PNG or JPG).
- `OUTPUT_PATH` – Where to save the generated STL file.
- `RESOLUTION` – Optional resize value (e.g. `64`).
- `HF_API_TOKEN` – Optional Hugging Face access token for private models.

## Step 5 – Run the transformation

```
python src\main.py
```

The STL file is written to the location specified by `OUTPUT_PATH`.

## Optional: run tests

To verify everything is set up correctly:

```
python -m pytest
```

