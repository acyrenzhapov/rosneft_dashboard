from abc import ABC


class SegyToNumpy(ABC):
    """Class to transform from .segy to npz file"""
    def __init__(
        self,
        segy_filepath: str,
        mask_filepath: str,
    ):
        pass
