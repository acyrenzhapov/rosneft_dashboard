from typing import Optional
from linecache import getline
import numpy as np
import torch
from torch.utils.data import Dataset


class SegyDataset(Dataset):
    """Dataset with 3D slice of seg-y file"""

    def __init__(
        self,
        segy_filepath: str,
        fault_filepath: str,
        fault_coords_filepath: str,
        cube_size: int = 64,
    ):
        """
        Create dataset for seg-y file
        Args:
            segy_filepath: path to seismic data (.npz format)
            fault_filepath: path to file with mask (.npz format)
            fault_coords_filepath: path to file with mask coords (.txt format),
            cube_size: cube_size of cube
        """
        self.cube_size = cube_size
        self.segy_filepath = segy_filepath
        self.fault_filepath = fault_filepath
        self.fault_coords_filepath = fault_coords_filepath
        self.length = self._get_dataset_length()

    def _get_dataset_length(self):
        with open(self.fault_coords_filepath) as fault_file:
            length = 0
            for _ in fault_file:
                length += 1
        return length

    def __len__(self):
        return self.length

    def _get_coords(self, index) -> list[int, int, int]:
        line = getline(self.fault_coords_filepath, index)
        result = []
        for item in line.split(' '):
            if item.isdigit():
                result.append(int(item))
        return result

    def __getitem__(self, idx):
        with np.load(self.fault_filepath) as fault_data, \
            np.load(self.segy_filepath) as segy_data:
            iline, xline, zline = self._get_coords(idx)
            fault_slice = fault_data['arr_0'][
                iline: iline + self.cube_size,
                xline: xline + self.cube_size,
                zline: zline + self.cube_size,
            ]
            segy_slice = segy_data['arr_0'][
                iline: iline + self.cube_size,
                xline: xline + self.cube_size,
                zline: zline + self.cube_size,
            ]
            X = torch.Tensor(segy_slice)
            Y = torch.Tensor(fault_slice)
            return X[None, :], Y[None, :]
