import pandas as pd

from pandas.io.sas.sasreader import SASReader

class XportReader(SASReader):
    def close(self) -> None: ...
    def __next__(self) -> pd.DataFrame: ...
    def read(self, nrows: int | None = None) -> pd.DataFrame:
        """
Read observations from SAS Xport file, returning as data frame.

Parameters
----------
nrows : int
    Number of rows to read from data file; if None, read whole
    file.

Returns
-------
A DataFrame.
        """
        pass
