from torch.nn import Module


class Unet3D(Module):
    """3D implementation of Unet."""

    def __init__(
        self,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
