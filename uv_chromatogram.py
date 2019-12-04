#!/usr/bin/env python
import csv

def load_dlls():
    """Ensure the Thermo DLLs are on the Python import path in here.

    For simplicity, I'll cheat by loading the stored copy in ms_deisotope.
    """
    import ms_deisotope
    from ms_deisotope.data_source.thermo_raw_net import register_dll
    register_dll()


load_dlls()

# Assuming the Thermo DLLs are on the PYTHONPATH/sys.path now, we can tell pythonnet about
# them and load them from Python.
import clr
clr.AddReference('ThermoFisher.CommonCore.RawFileReader')
clr.AddReference('ThermoFisher.CommonCore.Data')
import ThermoFisher.CommonCore.Data.Business as Business
import ThermoFisher.CommonCore.RawFileReader as RawFileReader


def open_raw(path):
    """Create and configure a RawFileReader instance

    Parameters
    ----------
    path : str
        The path to the .raw file to read from

    Returns
    -------
    RawFileReader
    """
    raw_file_reader = RawFileReader.RawFileReaderAdapter.FileFactory(path)
    raw_file_reader.SelectInstrument(Business.Device.MS, 1)
    return raw_file_reader


def load_chromatogram(raw_file_reader):
    """Load the UV chromatogram from the RawFileReader object.

    This function first constructs a configuration object of type
    ChromatogramTraceSettings, sets it up, and then passes it and
    the scan number ranges desired (start to end) to the RawFileReader's
    GetChromatogramData method, which returns the chromatogram. It then
    unwraps the relevant arrays, converting them into Python lists for
    later use.

    Parameters
    ----------
    raw_file_reader : RawFileReader

    Returns
    -------
    time: list[float]
        The time of each observation
    intensity: list[float]
        The signal abundance of each observation
    """
    settings = Business.ChromatogramTraceSettings()
    settings.DelayInMin = 0.0
    # This inscrutable Enum name was deduced from ProteoWizard source
    # https://github.com/ProteoWizard/pwiz/blob/96421c9ae8bd201ceb8f26b069732c78fa4ab47a/pwiz_aux/msrc/utility/vendor_api/thermo/RawFile.h#L341
    settings.Trace = Business.TraceType.ChannelA
    start = 1
    end = raw_file_reader.RunHeaderEx.LastSpectrum
    uv_chromatogram = raw_file_reader.GetChromatogramData([settings], start, end)
    time = list(uv_chromatogram.PositionsArray[0])
    intensity = list(uv_chromatogram.IntensitiesArray[0])
    return time, intensity


def main(raw_file_path, output_path):
    raw_file = open_raw(raw_file_path)
    time, intensity = load_chromatogram(raw_file)
    with open(output_path, 'wb') as fh:
        writer = csv.writer(fh)
        writer.writerow(['time', 'intensity'])
        writer.writerows(zip(time, intensity))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Dump the UV chromatogram from a .raw file to .csv")
    parser.add_argument("raw_file_path", help="The path to the .raw file")
    parser.add_argument("output_path", help="The path to write the output to, as a .csv")

    args = parser.parse_args()

    main(args.raw_file_path, args.output_path)
