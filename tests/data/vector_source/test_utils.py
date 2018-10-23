import unittest

from rastervision.data.vector_source.utils import mbtiles_to_geojson
from rastervision.core.box import Box
from rastervision.data.crs_transformer import IdentityCRSTransformer
from tests import data_file_path


class TestUtils(unittest.TestCase):
    def test_mbtiles_to_geojson(self):
        # This test file was copied from https://github.com/developmentseed/label-maker
        mbtiles_path = data_file_path('portugal-z17.mbtiles')
        crs_transformer = IdentityCRSTransformer()

        # Extent covers subset of shapes.
        extent = Box.make_square(38.85, -10.0, 1.0)
        geojson = mbtiles_to_geojson(mbtiles_path, crs_transformer, extent)
        self.assertEqual(len(geojson['features']), 352)

        # Extent covers whole set of shapes.
        extent = Box.make_square(38.0, -10.0, 1.0)
        geojson = mbtiles_to_geojson(mbtiles_path, crs_transformer, extent)
        self.assertEqual(len(geojson['features']), 554)


if __name__ == '__main__':
    unittest.main()
