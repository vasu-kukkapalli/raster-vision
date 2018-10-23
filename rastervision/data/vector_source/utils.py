from subprocess import Popen, PIPE, check_output
from os.path import join, dirname
import json
import logging

from rastervision.utils.files import download_if_needed
from rastervision.rv_config import RVConfig

log = logging.getLogger(__name__)


def mbtiles_to_geojson(uri, crs_transformer, extent):
    map_extent = extent.reproject(lambda point: crs_transformer.pixel_to_map(point))

    with RVConfig.get_tmp_dir() as tmp_dir:
        log.info('Converting MBTiles to GeoJSON...')

        # This code is adapted from https://github.com/developmentseed/label-maker
        local_uri = download_if_needed(uri, tmp_dir)
        ps = Popen(['tippecanoe-decode', '-c', '-f', local_uri], stdout=PIPE)
        stream_filter_path = join(dirname(__file__), 'stream_filter.py')
        filtered_geojson = check_output(
            ['python', stream_filter_path, json.dumps(map_extent.shapely_format())],
            stdin=ps.stdout).decode('utf-8')

    # Each line has a feature. The last line is empty so discard.
    features = [json.loads(feature) for feature in filtered_geojson.split('\n')[:-1]]
    geojson = {
        'type': 'FeatureCollection',
        'features': features
    }

    return geojson
