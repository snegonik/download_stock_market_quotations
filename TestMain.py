import unittest
import main
import pandas as pd
from pandas.util.testing import assert_frame_equal


class TestMain(unittest.TestCase):

    def setUp(self):
        tic_list = ['AAPL', 'TSLA']
        self.data = main.download_tic(tic_list)

    def test_download_tic(self):
        """ Test that the dataframe read in equals what you expect"""

        foo = pd.read_csv('test_tic.csv')
        foo['Date'] = foo['Date'].astype('datetime64[ns]')
        foo.set_index('Date', inplace=True)

        assert_frame_equal(self.data, foo)

    def test_fail(self):
        with self.assertRaises(SystemExit):
            main.download_tic([1, 2])


if __name__ == "__main__":
    unittest.main()
