import os

import numpy as np
import pytest

# Ensure src package is importable
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import main  # noqa: E402


class DummyResponse:
    def __init__(self, content: bytes = b'data'):
        self.content = content

    def raise_for_status(self) -> None:  # pragma: no cover - simple stub
        return None


def test_query_hf_api_uses_token(monkeypatch):
    captured = {}

    def fake_post(url, headers=None, data=None):
        captured['url'] = url
        captured['headers'] = headers
        captured['data'] = data
        return DummyResponse(b'depth')

    monkeypatch.setattr(main.requests, 'post', fake_post)
    result = main.query_hf_api(b'img', 'the-model', api_token='token123')

    assert captured['url'].endswith('/the-model')
    assert captured['headers']['Authorization'] == 'Bearer token123'
    assert captured['data'] == b'img'
    assert result == b'depth'


def test_heightmap_to_stl(tmp_path):
    heightmap = np.array([[0.0, 1.0], [0.5, 0.25]])
    output = tmp_path / 'out.stl'

    main.heightmap_to_stl(heightmap, str(output))

    text = output.read_text().strip().splitlines()
    assert text[0] == 'solid model'
    assert text[-1] == 'endsolid model'
    assert any('vertex 0 1 1.0' in line for line in text)


def test_generate_3d_missing_env(monkeypatch):
    monkeypatch.delenv('MODEL_NAME', raising=False)
    monkeypatch.delenv('IMAGE_PATH', raising=False)
    monkeypatch.delenv('OUTPUT_PATH', raising=False)

    with pytest.raises(ValueError):
        main.generate_3d()
