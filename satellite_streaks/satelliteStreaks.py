import os
import numpy as np
import pandas as pd
import galsim
from skycatalogs.objects import BaseObject, ObjectCollection
from skycatalogs.utils import normalize_sed
from .utils import object_type_config


__all__ = ["SatelliteStreakCollection", "SatelliteStreakObject"]


class SatelliteStreakObject(BaseObject):
    def __init__(self, params, parent_collection, index):
        super().__init__(params.ra, params.dec, params.obj_id,
                         parent_collection._object_type,
                         parent_collection, index)
        self.params = params

    def get_observer_sed_component(self, component, mjd=None):
        if component != "this_object":
            raise RuntimeError("Unknown SED component: %s", component)
        sed_path = self.params.sed_path
        if not os.path.isfile(sed_path):
            # Try to find this file under $SIMS_SED_LIBRARY_DIR.
            sed_path = os.path.join(os.environ['SIMS_SED_LIBRARY_DIR'],
                                    sed_path)
            if not os.path.isfile(sed_path):
                raise FileNotFoundError(f"SED file {self.params.sed_path} "
                                        "not found.")
        sed = galsim.SED(sed_path, wave_type='nm', flux_type='flambda')
        sed = normalize_sed(sed, params.magnorm)
        return sed

    def get_gsobject_components(self, gsparams=None, rng=None):
        if gsparams is not None:
            gsparams = galsim.GSParams(**gsparams)
        length = float(self.params.length)
        width = float(self.params.width)
        gs_obj = galsim.Box(length, width, gsparams=gsparams)
        position_angle = galsim.Angle(float(self.params.position_angle),
                                      galsim.degrees)
        gs_obj = gs_obj.rotate(position_angle)
        return {'this_object': gs_obj}


class SatelliteStreakCollection(ObjectCollection):
    """
    Collection of satellite streaks, simulated with galsim.Box with an
    SED from an input file with columns wavelength, flambda.  The SED
    normalization is determined from the magnorm column in the catalog
    file.
    """
    def __init__(self, catalog_file, sky_catalog, object_type):
        # Read in the parquet file containing the pandas data frame of
        # parameters for the satellite streaks.
        self.catalog = pd.read_parquet(catalog_file)

        # Fill the private attributes required by the base class.
        self._ra = self.df0['ra'].to_numpy()
        self._dec = self.df0['dec'].to_numpy()
        self._id = self.df0['obj_id'].to_numpy()
        self._sky_catalog = sky_catalog
        self._object_type_unique = object_type
        self._object_class = SatelliteStreakObject
        self._uniform_object_type = True

    @property
    def native_columns(self):
        return ()

    def __getitem__(self, index):
        params = self.catalog.iloc[index]
        return SatelliteStreak(params, self, index)

    def __len__(self):
        return len(self._ra)

    @staticmethod
    def register(sky_catalog, object_type):
        sky_catalog.cat_cxt.register_source_type(
            object_type,
            object_class=SatelliteStreakObject,
            collection_class=SatelliteStreakCollection,
            custom_load=True
        )

    @staticmethod
    def load_collection(region, sky_catalog, mjd=None, exposure=None,
                        object_type=None):
        # Get catalog parameters from config file.
        config = object_type_config(sky_catalog, object_type)
        catalog_file = config['catalog_file']
        return SatelliteStreakCollection(catalog_file, sky_catalog,
                                         object_type)
