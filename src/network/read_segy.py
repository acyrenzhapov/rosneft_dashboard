import pathlib
import re
import typing

import numpy as np
import segyio


def get_segy_header(
    filepath: typing.Union[str, pathlib.Path],
) -> dict:
    """Return dictionary header of segy file.

    Args:
        filepath (typing.Union[str, pathlib.Path]): path to segy file

    Returns:
        dict: dictionary with structure C##: some information
    """
    with segyio.open(filepath) as segyfile:
        raw_header = segyio.tools.wrap(segyfile.text[0])
        cut_header = re.split(r'C[0-9 ]+', raw_header)[1::]
        text_header = [re.sub(' +', ' ', x.replace('\n', ' ')) for x in
                       cut_header]
        clean_header = {}
        for index, item in enumerate(text_header):
            key = 'C' + str(index + 1).rjust(2, '0')
            clean_header[key] = item
        return clean_header


def get_trace_id_list(
    segyfile: segyio.SegyFile,
    trace_id: int,
) -> list:
    """Get trace ids in segyfile.

    Args:
        segyfile (segyio.SegyFile): opened segyfile
        trace_id (int): id of trace

    Returns:
        list: List of ids of trace
    """
    trace_id_list: list = []
    for index, item in enumerate(segyfile.attributes(1)):
        if item == trace_id:
            trace_id_list.append(index)
    return trace_id_list


def get_trace_header(
    filepath: typing.Union[str, pathlib.Path],
    trace_id: int = 1,
) -> None:
    """Get header of trace.

    Args:
        filepath (typing.Union[str, pathlib.Path]): filepath to segy file
        trace_id (int, optional): id of trace which header need to get.
        Defaults to 1.

    TODO: Is it really need to do? How should the format look like?
    """
    with segyio.open(filepath) as segyfile:
        headers = segyio.tracefield.keys

        trace_id_list = get_trace_id_list(segyfile, trace_id)
        for k, v in headers.items():
            # print(k, segyfile.attributes(v)[trace_id_list])
            pass


def get_standart_view(
    filepath: typing.Union[str, pathlib.Path],
    xline_id: int = 1,
) -> np.ndarray:
    """Get slice of segy cube by iline.

    Args:
        filepath (typing.Union[str, pathlib.Path]): filepath to segy file
        xline_id (int, optional): xline_id which need to get. Defaults to 1.

    Raises:
        IndexError: Try to get xline_id out of bounds

    Returns:
        np.ndarray: get slice by freezing iline
    """
    with segyio.open(filepath) as segyfile:
        xline_count = len(segyfile.xlines)
        if xline_count < xline_id:
            raise IndexError('Wrong index')
        return segyfile.trace.raw[
           xline_count * xline_id: xline_count * (xline_id + 1)
        ]


def get_side_view(
    filepath: typing.Union[str, pathlib.Path],
    iline_id: int = 0,
) -> np.ndarray:
    """Get slice of segy cube by xline.

    Args:
        filepath (typing.Union[str, pathlib.Path]): filepath to segy file
        iline_id (int): slice_id which need to get. Defaults to 1.

    Returns:
        np.ndarray: get slice by freezing xline
    """
    with segyio.open(filepath) as segyfile:
        xlines_count = len(segyfile.xlines)
        if xlines_count < iline_id:
            raise IndexError('Wrong index')
        return segyfile.trace.raw[iline_id::xlines_count]


def check_file_is_readable(
    filepath: typing.Union[str, pathlib.Path],
) -> bool:
    """Check if it necessary to use ignore_index when call segyio.open.

    Args:
        filepath (typing.Union[str, pathlib.Path]): filepath to segy file

    Returns:
        bool: True - if it can be open without strict and ignore_index flag
              False - otherwise
    """
    if filepath is None:
        return False

    try:
        with segyio.open(filepath) as segyfile:  # noqa: F841 WPS328
            pass  # noqa: WPS420
        return True
    except RuntimeError:
        return False
    except FileNotFoundError:
        return False


def get_min_max_value(  # noqa: WPS210
    filepath: typing.Union[str, pathlib.Path],
) -> typing.Tuple[float, float]:
    """Return min max value of amplitude of segy file.

    Can be very long for a big file
    Approximately 80 sec for 9GB file

    Args:
        filepath (typing.Union[str, pathlib.Path]): filepath to segy file

    Returns:
        typing.Tuple[float, float]: min value and max value
    """
    min_value = np.Inf
    max_value = np.NINF
    with segyio.open(filepath) as segyfile:
        for trace in segyfile.trace:
            min_temp = trace.min()
            max_temp = trace.max()
            if min_value > min_temp:
                min_value = min_temp
            if max_temp > max_value:
                max_value = max_temp
    return (min_value, max_value)


def get_segy_cube_shape(
    filepath: typing.Union[str, pathlib.Path],
) -> typing.Tuple[int, int, int]:
    """Return seg-y cube shape.

    Args:
        filepath (typing.Union[str, pathlib.Path]): Path to seg-y file

    Returns:
        typing.Tuple[int, int, int]: shape with order: xlines, ilinex, time/depth
    """
    with segyio.open(filepath) as segyfile:
        xlines = len(segyfile.xlines)
        ilines = len(segyfile.ilines)
        time_value = segyfile.trace.shape
    return xlines, ilines, time_value


def get_full_data(
    filepath: typing.Union[str, pathlib.Path],
) -> np.ndarray:
    """
    Read full cube.

    Can be danger due to high memory consumption
    Args:
        filepath: path to SEG-Y file

    Returns: full cube data_store
    """
    with segyio.open(filepath) as segyfile:
        full_cube = segyio.tools.cube(segyfile)
    return full_cube


def check_out_of_bounds(
    filepath: typing.Union[str, pathlib.Path],
    xline_id: int = 0,
    iline_id: int = 0,
    timeline_id: int = 0,
    size: int = 64,
) -> bool:
    xlines, ilines, time_value = get_segy_cube_shape(filepath)
    if xline_id + size > xlines:
        return True
    if iline_id + size > ilines:
        return True
    if timeline_id + size > time_value:
        return True
    return False


def get_3d_slice(
    filepath: typing.Union[str, pathlib.Path],
    xline_id: int = 0,
    iline_id: int = 0,
    timeline_id: int = 0,
    size: int = 64,
) -> np.ndarray:
    if check_out_of_bounds(filepath, xline_id, iline_id, timeline_id, size):
        return np.zeros((64, 64, 64))
    inlines = []
    with segyio.open(filepath, "r") as segyfile:
        segyfile.mmap()
        for inline in segyfile.ilines[iline_id: iline_id + size]:
            inlines.append(segyfile.iline[inline][
                xline_id: xline_id + size,
                timeline_id: timeline_id + size,
            ])
    return np.array(inlines)