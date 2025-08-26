import os
import sys
from io import BytesIO

from PIL import Image
import pytest

# Ensure src package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import main  # noqa: E402


class DummyResponse:
    def __init__(self, content: bytes):
        self.content = content

    def raise_for_status(self) -> None:  # pragma: no cover - simple stub
        return None


def test_generate_3d(tmp_path, monkeypatch):
    # Create a simple input image
    input_img = Image.new('RGB', (2, 2), color='white')
    input_path = tmp_path / 'input.png'
    input_img.save(input_path)

    # Create fake depth map bytes
    depth_img = Image.new('L', (2, 2), color=128)
    buf = BytesIO()
    depth_img.save(buf, format='PNG')
    depth_bytes = buf.getvalue()

    def fake_post(url, headers=None, data=None):
        assert 'dummy-model' in url
        return DummyResponse(depth_bytes)

    monkeypatch.setattr(main.requests, 'post', fake_post)

    output_path = tmp_path / 'out.stl'
    os.environ['MODEL_NAME'] = 'dummy-model'
    os.environ['IMAGE_PATH'] = str(input_path)
    os.environ['OUTPUT_PATH'] = str(output_path)
    os.environ['RESOLUTION'] = '2'

    main.generate_3d()

    assert output_path.exists()
    text = output_path.read_text()
    assert 'facet normal' in text
