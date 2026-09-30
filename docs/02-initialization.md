# Initialize the July 2022 heatwave case

Guide 2 of 3 | LIU Zhuo | The Hong Kong University of Science and Technology

Compile both cores using Guide 1 first. This guide prepares geographic fields, initial conditions and surface updates for a global Hong Kong-refined mesh.

## Step 1 | Prepare the mesh and ERA5 inputs

The teaching period is 2022-07-19 00:00 UTC to 2022-07-30 06:00 UTC. Follow the [mesh-generation repository cited by Cao et al.](https://github.com/caomoyu/MPAS-A-mesh-generation) for the global variable-resolution mesh, refined to about 500 m around Hong Kong and coarsening to about 30 km. The inspected case mesh contains 746,053 cells; a newly generated mesh can differ.

Prepare a model-ready spherical MPAS mesh and its matching, unpartitioned graph. Complete the mesh conversion/scaling steps in the mesh workflow; a raw unit-sphere mesh is not the final Earth-sized input. Keep the cell ordering identical between mesh and graph.

Prepare two separate inputs from ERA5 [pressure-level](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-pressure-levels) and [single-level](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels) data:

- Initial conditions: one complete intermediate file, `ERA5:2022-07-19_00`, containing the required atmospheric, surface and soil fields.
- Surface updates: SST and sea-ice fields every 3 hours from 19 July 00:00 to 30 July 06:00 UTC, prepared with the separate prefix `SST`. The inspected case surface file has 3-hourly records.

This is a global simulation: no time series of atmospheric lateral-boundary forcing is needed. Do not download complete atmospheric and soil fields for every later time just to update SST.

For WPS preparation, follow the [official WRF/WPS guide](https://www2.mmm.ucar.edu/wrf/site/documentation/users_guide/wps.html) and the [MPAS real-data tutorial](https://www2.mmm.ucar.edu/projects/mpas/tutorial/StAndrews2025/). Use the ERA5-compatible Vtable and inspect the resulting intermediate records. MPAS reads these files directly; WRF `met_em` files are not used here.

This repository does not distribute a ready mesh or ERA5 archive. After preparation, place the inputs under this layout (the names on the left are the tutorial's local names):

```text
$HOME/MPAS/DATA/heatwave2022/
|-- heatwave2022.grid.nc
|-- heatwave2022.graph.info
|-- ERA5:2022-07-19_00
|-- SST:2022-07-19_00
|-- SST:2022-07-19_03
|-- ...
`-- SST:2022-07-30_06
```

## Step 2 | Prepare static geographic data

Download the standard geographic archive and the HKUST urban land-cover dataset:

```bash
export MPAS_ROOT="$HOME/MPAS"
mkdir -p "$MPAS_ROOT/DATA"
cd "$MPAS_ROOT/DATA"
curl -fL -O \
  https://www2.mmm.ucar.edu/projects/mpas/mpas_static.tar.bz2
tar -xjf mpas_static.tar.bz2
cd "$MPAS_ROOT/DATA/mpas_static"
curl -fL -O \
  https://github.com/HKUST-MPAS/HKUST-MPAS/releases/download/LCZ_dataset_for_MPAS_Urban/mpas_cglc_lcz.tar.gz
tar -xzf mpas_cglc_lcz.tar.gz
```

The geographic directory must contain the dataset folders, not an extra nested `mpas_static` folder. Check the two indexes below and retain all tile files in the downloaded datasets:

```bash
test -s "$MPAS_ROOT/DATA/mpas_static/landuse_30s/index"
test -s "$MPAS_ROOT/DATA/mpas_static/mpas_cglc_lcz/index"
```

`landuse_30s` is needed for native-mesh gravity-wave-drag fields, even when the surface land cover is CGLC/LCZ. The reference settings use GMTED2010 terrain and MODIS vegetation fraction, albedo and maximum snow albedo. Land cover comes from the [HKUST LCZ release](https://github.com/HKUST-MPAS/HKUST-MPAS/releases/tag/LCZ_dataset_for_MPAS_Urban).

### Soil data

[Dy and Fung (2016)](https://doi.org/10.1002/2015JD024558) describe an updated WRF soil map built by updating the default map with BNU data. Contact the authors for that dataset and its processing details if it is needed for your experiment. The official MPAS BNU dataset is related, but is not identical to that updated WRF product.

The main workflow here uses the default STATSGO soil-category input supported by HKUST-MPAS v8.2.2. Optional BNU soil data require MPAS v8.3 or later; the HKUST-MPAS version used in this tutorial does not support the `config_soilcat_data` option. Do not add it to this version's namelist.

For a separate setup using MPAS v8.3 or later, download BNU as follows:

```bash
cd "$MPAS_ROOT/DATA/mpas_static"
curl -fL -O \
  https://www2.mmm.ucar.edu/projects/mpas/bnu_soiltype_top.tar.bz2
tar -xjf bnu_soiltype_top.tar.bz2
test -s bnu_soiltype_top/index
```

In that version only, set `config_soilcat_data = 'BNU'` under `&data_sources` when generating the static file. Changing soil input requires generating a new static file. This optional choice does not change the source version used in the main tutorial.

## Step 3 | Create the case directory

Set the paths. Repeat these exports when starting a new shell:

```bash
export MPAS_ROOT="$HOME/MPAS"
export MPAS_BUILD="$MPAS_ROOT/HKUST-MPAS"
export TUTORIAL="$MPAS_ROOT/MPAS-Urban-Tutorial"
export INPUT="$MPAS_ROOT/DATA/heatwave2022"
export CASE="$MPAS_ROOT/CASES/heatwave2022"
mkdir -p "$CASE"
cd "$CASE"
```

Link the executable, mesh and vertical-level definition:

```bash
ln -sf "$MPAS_BUILD/init_atmosphere_model" .
ln -sf "$INPUT/heatwave2022.grid.nc" .
ln -sf "$INPUT/heatwave2022.graph.info" .
ln -sf "$MPAS_BUILD/vertical_levels" .
test -s "$INPUT/ERA5:2022-07-19_00"
ln -sf "$INPUT/ERA5:2022-07-19_00" .
```

## Step 4 | Partition the mesh

Use METIS `gpmetis` on the graph that belongs to your mesh. Here 192 is the number of MPI tasks, matching the reference case; use the resources allocated by your machine.

```bash
export NPROCS=192
gpmetis heatwave2022.graph.info "$NPROCS"
ls -lh "heatwave2022.graph.info.part.$NPROCS"
```

### Optional | Change the number of CPU tasks

For example, to use 112 tasks instead, make a new partition from the unpartitioned graph:

```bash
export NPROCS=112
gpmetis heatwave2022.graph.info "$NPROCS"
```

The following commands use `NPROCS` for the task count. Keep the same value in Guide 3. Do not rename `.part.192` to `.part.112`; it contains a different decomposition. The namelist prefix stays `heatwave2022.graph.info.part.`.

## Step 5 | Generate the static file

```bash
cp "$TUTORIAL/config/namelist.init_atmosphere" .
cp "$TUTORIAL/config/streams.init_atmosphere" .
nano namelist.init_atmosphere
```

Change `config_geog_data_path` to the full path of your `DATA/mpas_static` directory, ending in `/`. Fortran namelists do not expand `$HOME`. The supplied file marks this one path with `CHANGE_ME`.

These two files start with the static-stage settings. Keep editing the same local files in Steps 6 and 7; do not copy the originals again. In `streams.init_atmosphere`, the `input` stream reads `heatwave2022.grid.nc` and the `output` stream writes `heatwave2022.static.nc`.

The static stage has these six switches:

```fortran
&preproc_stages
 config_static_interp = true
 config_native_gwd_static = true
 config_vertical_grid = false
 config_met_interp = false
 config_input_sst = false
 config_frac_seaice = false
/
```

The first two create geographic and native-mesh gravity-wave-drag fields. This stage does not interpolate ERA5 or build the vertical grid.

Run in an allocated compute session:

```bash
mpiexec -n "$NPROCS" ./init_atmosphere_model
cp log.init_atmosphere.0000.out log.static.out
ls -lh heatwave2022.static.nc
tail -n 20 log.static.out
```

Expect a non-empty static file and a normal completion in the log. Static interpolation on this large global mesh can take hours, depending on CPUs, storage and data resolution. This is a planning estimate, not a measured duration for this new setup. While waiting, you can explore plotting the mesh using the official MPAS tutorial.

## Step 6 | Generate the initial conditions

```bash
nano namelist.init_atmosphere
nano streams.init_atmosphere
```

Check the start/stop time is `2022-07-19_00:00:00`, prefix is `ERA5`, and vertical levels are 55 with `vertical_levels/urban_ZR_75.txt`. This file has 56 interfaces, from the surface to 30 km.

The reference uses 38 meteorological levels (37 ERA5 pressure levels plus a surface level) and four soil levels. Set `config_nfglevels` to match your actual WPS intermediate input. `config_use_spechumd = false` expects relative humidity; use `true` only if you prepared specific humidity instead.

```fortran
&preproc_stages
 config_static_interp = false
 config_native_gwd_static = false
 config_vertical_grid = true
 config_met_interp = true
 config_input_sst = false
 config_frac_seaice = true
/
```

This stage reads the existing static file, builds the vertical grid and interpolates ERA5 at the initial time. It does not remake geographic fields.

In `streams.init_atmosphere`, change the two `filename_template` values:

- `input`: `heatwave2022.grid.nc` to `heatwave2022.static.nc`.
- `output`: `heatwave2022.static.nc` to `heatwave2022.init.nc`.

Keep the other stream settings unchanged.

```bash
mpiexec -n "$NPROCS" ./init_atmosphere_model
cp log.init_atmosphere.0000.out log.initial.out
ls -lh heatwave2022.init.nc
tail -n 20 log.initial.out
```

Allow tens of minutes to hours as a broad planning range; actual time depends on the machine and input. Check the log rather than assuming a quiet terminal means the job has stopped.

## Step 7 | Generate surface updates

The run uses evolving SST. Use the 3-hourly SST and sea-ice intermediate files prepared in Step 1. These are surface-only inputs, separate from the single complete ERA5 initialization file.

```bash
test -s "$INPUT/SST:2022-07-19_00"
test -s "$INPUT/SST:2022-07-30_06"
ln -sf "$INPUT"/SST:* .
nano namelist.init_atmosphere
```

In `&nhyd_model`, set:

```fortran
 config_init_case = 8
 config_start_time = '2022-07-19_00:00:00'
 config_stop_time = '2022-07-30_06:00:00'
```

In `&data_sources`, retain `config_sfc_prefix = 'SST'` and `config_fg_interval = 10800` (3 hours). Set the six stage switches to:

```fortran
&preproc_stages
 config_static_interp = false
 config_native_gwd_static = false
 config_vertical_grid = false
 config_met_interp = false
 config_input_sst = true
 config_frac_seaice = true
/
```

Keep `streams.init_atmosphere` as it was after Step 6. Its `input` reads `heatwave2022.static.nc`; the `surface` stream already writes `heatwave2022.sfc_update.nc` with `output_interval="10800"`. Case 8 uses this surface output, not the initial-condition output.

```bash
mpiexec -n "$NPROCS" ./init_atmosphere_model
cp log.init_atmosphere.0000.out log.surface.out
ls -lh heatwave2022.sfc_update.nc
ncdump -v xtime heatwave2022.sfc_update.nc
```

Check that `xtime` contains records every 3 hours, covering 19 July 00:00 through 30 July 06:00 UTC. The original atmosphere configuration's hourly surface-stream read interval is retained; it is not a requirement for hourly ERA5 input records.

You now have the three generated inputs: `heatwave2022.static.nc`, `heatwave2022.init.nc` and `heatwave2022.sfc_update.nc`. Continue with Guide 3.
