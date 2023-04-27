import os
from abc import ABC
from datetime import datetime
from random import randint
from typing import Optional

import numpy as np


class DataPreparation(ABC):
    """Create cube slices to train model."""

    def __init__(
        self,
        mask_filepath: str,
        dataset_size: int,
        cube_size: int,
        dataset_type: str = 'train',
        threshold_percent: Optional[float] = None,
        threshold_value: Optional[int] = None,
    ):
        self.mask_filepath = mask_filepath
        self.dataset_size = dataset_size
        self.cube_size = cube_size
        self.dataset_type = dataset_type
        assert dataset_type in ['train', 'test', 'eval']
        if threshold_percent is None and threshold_value is None:
            raise TypeError(
                "You should specify threshold_percent or " +
                "threshold_value"
            )
        if threshold_percent <= 0 or threshold_percent >= 1:
            raise TypeError("threshold_percent should be between 0 and 1")
        self.threshold_percent = threshold_percent
        self.threshold_value = self._get_threshold_value(threshold_value)

    def _get_threshold_value(
        self,
        threshold_value: int,
    ) -> int:
        """
        Specify threshold value.

        If we get threshold value then use it.
        If doesn't then we calculate using cube cube_size and threshold_percent
        Args:
            threshold_value: amount of pixel that are fault

        Returns:
            min value of amount of fault pixel in cube
        """
        if threshold_value is None:
            return ((self.cube_size ** 3) * self.threshold_percent)
        return threshold_value

    def _get_slice_coordinates(
        self,
        faultfile,
    ) -> tuple[int, int, int]:
        """Find сoordinates of cube by threshold.
        Get random XYZ point and get cube based on point and cube_size
        Check amount fault pixel and return coordinate if it contains equal or
        higher than threshold
        """
        count = 0
        IL, XL, Z = faultfile['arr_0'].shape
        while True:
            count += 1
            iline = randint(0, IL - self.cube_size)
            xline = randint(0, XL - self.cube_size)
            zline = randint(0, Z - self.cube_size)
            fault_slice = faultfile['arr_0'][
                iline: iline + self.cube_size,
                xline: xline + self.cube_size,
                zline: zline + self.cube_size
            ]
            if fault_slice.sum() > self.threshold_value:
                return iline, xline, zline
            if count >= 25:
                print('Very high density value. Reduce by 10%')
                self.threshold_value = int(0.9 * self.threshold_value)

    def create_dataset(self) -> str:
        """
        Create temp folder with dataset cubes.

        Returns: path to dataset
        """
        base_path = '..\\..\\'
        if not os.path.isdir(base_path + 'data'):
            os.makedirs(base_path + 'data')
        mask_coords_filepath = (
            base_path +
            'data\\' +
            f'masks_{(datetime.now().strftime("%d_%m_%Y_%H_%M"))}.txt'
        )

        with np.load(self.mask_filepath) as maskfile, \
            open(mask_coords_filepath, 'w') as mask_coords_file:
            for i in range(self.dataset_size):
                print(i)
                xline, inline, timeline = self._get_slice_coordinates(maskfile)
                mask_coords_file.write(f'{xline} {inline} {timeline} \n')
            print('Finding end')
        return mask_coords_filepath
