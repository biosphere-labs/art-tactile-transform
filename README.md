# Art Tactile Transform

This project converts a flat picture into a simple 3D model that can be 3D printed. It uses a Hugging Face depth-estimation model to create a height map and saves the result as an STL file.

## Prerequisites

1. **Install Python**
   - Download and install Python 3.10 or later from [python.org/downloads](https://www.python.org/downloads/).
   - During installation on Windows, check "Add Python to PATH".

2. **Clone this repository**
   ```bash
   git clone <repository-url>
   cd art-tactile-transform
   ```

3. **Create a virtual environment (recommended)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configure

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` in a text editor and set:
   - `MODEL_NAME` – Hugging Face model to use (e.g. `Intel/dpt-large`).
   - `IMAGE_PATH` – Path to the input image file (PNG or JPG).
   - `OUTPUT_PATH` – Where to save the generated STL file.
   - `RESOLUTION` – Optional resize value (e.g. `64`).
   - `HF_API_TOKEN` – Optional Hugging Face access token for private models.

## Run

After configuration, run the transformation:
```bash
python src/main.py
```
The STL file will be written to the location specified by `OUTPUT_PATH`.

## Tests

Run the automated tests with:
```bash
pytest
```
