from tensorboard.program import TensorBoard

from src.settings import Settings


class SegmentationTask(object):
    """Pipeline to train model."""

    def __init__(self):
        self._tensorboard = None

    def launch(self):
        """Start pipeline to train model."""
        self._tensorboard = TensorBoard()
        self._tensorboard.configure(
            argv=[  # noqa:WPS317
                None,
                '--logdir', str('/logs/'),
                '--port', str(Settings.TENSORBOARD_PORT),
            ],
        )
        self._tensorboard.launch()
