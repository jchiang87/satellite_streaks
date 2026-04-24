## Setting up the package
If you have `imSim` and `skyCatalogs` set up in the usual way, i.e., alongside an installation of `lsst_distrib`, then to set up this package just do
```
$ setup -r <path/to/satellite_streaks> -j
```

## Running the example code
To run the example in the [examples](examples) folder, you'll need to have the `SIMS_SED_LIBRARY_DIR` environment variable pointing to
the usual installation of those SED data.
While in the `examples` folder, generate the example catalog:
```
$ python make_catalog.py
```
Then run the simulation with
```
$ galsim -v 2 imsim-skycat.yaml
```
The resulting eimage and centroid files will be written to the `output` folder.
