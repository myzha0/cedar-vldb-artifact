from ..pipe import (
    InProcessPipeVariant,
    Pipe,
    PipeVariant,
)
from ..context import PipeVariantType
import nvidia.dali as dali
import numpy as np


class ImageDaliDecoderPipe(Pipe):
    """
    Given a FileOpener pipe, yields the decoded tensor
    representation of the images specified in the FileOpener pipe.

    Decodes on either gpu or cpu with DALI,

    Output Format:
    Yields torch.Tensor of shape (image_channels, image_height, image_width).
    The values of the output tensor are dtype=uint8 in [0, 255].
    Ordering of channels is RGB.
    """

    def __init__(
        self, input_pipe: Pipe, use_gpu=True, is_random: bool = False
    ):
        super().__init__("ImageReaderPipe", [input_pipe], is_random=is_random)
        self.use_gpu = use_gpu

    def _to_inprocess(self) -> InProcessPipeVariant:
        if self.input_pipes[0].pipe_variant_type != PipeVariantType.INPROCESS:
            raise NotImplementedError
        return InProcessImageDaliDecoderPipeVariant(
            self.input_pipes[0].pipe_variant, self.use_gpu
        )


class InProcessImageDaliDecoderPipeVariant(InProcessPipeVariant):
    def __init__(self, input_pipe_variant: PipeVariant, use_gpu):
        super().__init__(input_pipe_variant)
        self.use_gpu = use_gpu

    def __iter__(self):
        ex = [
            np.fromfile(image_path, dtype=np.uint8)
            for image_path, _ in self.dp
        ]
        batch_size = len(ex)
        ex = np.array(ex)[np.newaxis, :]

        pipe = self._image_pipeline(ex, self.use_gpu, batch_size)
        pipe.build()
        img = pipe.run()[0]
        img = img.as_cpu() if self.use_gpu else img
        output = [img.at(i) for i in range(batch_size)]

        yield output

    def _image_pipeline(self, ext_source, use_gpu, batch_size):
        device = "mixed" if use_gpu else "cpu"
        pipe = dali.pipeline.Pipeline(
            batch_size=batch_size, num_threads=1, device_id=0
        )
        with pipe:
            img = dali.fn.external_source(
                source=ext_source, dtype=dali.types.UINT8
            )
            img = dali.fn.decoders.image(img, device=device)
            pipe.set_outputs(img)
        return pipe
