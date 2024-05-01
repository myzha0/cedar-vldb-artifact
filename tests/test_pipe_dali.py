import numpy as np
import pathlib
from typing import List
import pytest

from ember.config import EmberContext
from ember.config import DALI_AVAILABLE
from ember.compose import Feature
from ember.pipes import (
    FileOpenerPipe,
    Pipe,
)
from ember.sources import LocalFSSource


@pytest.mark.skipif(not DALI_AVAILABLE, reason="DALI is not available.")
def test_image_dali_decoder_pipe():
    from ember.pipes.dali import ImageDaliDecoderPipe

    class TestFeature(Feature):
        def _compose(self, source_pipes: List[Pipe]) -> Pipe:
            fp = source_pipes[0]
            fp = FileOpenerPipe(fp)
            fp = ImageDaliDecoderPipe(fp, True)  # True GPU, False CPU
            return fp

    test_dir = pathlib.Path(__file__).resolve().parents[0]
    test_file = pathlib.Path(test_dir) / "data/example_image.jpeg"
    pipe = TestFeature()
    pipe.apply(LocalFSSource(str(test_file)))
    res = pipe.load(EmberContext())
    out = []
    for x in res:
        out.append(x)

    expected_output = [
        [[167, 174, 168], [141, 148, 142], [101, 118, 60], [108, 125, 67]],
        [[85, 92, 86], [139, 146, 140], [156, 173, 115], [159, 176, 118]],
        [[58, 36, 87], [144, 122, 173], [167, 177, 130], [152, 162, 115]],
        [[35, 13, 64], [102, 80, 131], [129, 139, 92], [147, 157, 110]],
    ]
    expected_output = np.asarray(expected_output, dtype=np.uint8)
    comparison = np.abs(out - expected_output) <= 1
    assert comparison.all()
