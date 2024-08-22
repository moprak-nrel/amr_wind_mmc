### This is a helper script to read MMC forcing data from ABL stats file
### and convert it into a tendency forcing input file

import numpy as np
import netCDF4 as nc

## Read the relevant fields from ABL Stats
data = {}
abl_stats = nc.Dataset("./post_processing/abl_statistics00000.nc", "r")
data["times"] = abl_stats.variables["time"][:]
data["tflux"] = abl_stats.variables["Q"][:]
mean_profiles = abl_stats["mean_profiles"]
data["heights"] = mean_profiles.variables["h"][:]
data["momentum_u"] = mean_profiles.variables["abl_meso_forcing_mom_x"][:].flatten()
data["momentum_v"] = mean_profiles.variables["abl_meso_forcing_mom_y"][:].flatten()
data["temperature"] = mean_profiles.variables["abl_meso_forcing_theta"][:].flatten()
abl_stats.close()


## Create a tendency forcing netcdf file
tf = nc.Dataset("tendency_forcing.nc", "w")
tf.createDimension("ntime", len(data["times"]))
tf.createDimension("nheight", len(data["heights"]))
tf.createDimension("datasize", len(data["heights"])*len(data["times"]))

for var in ["momentum_u", "momentum_v", "temperature"]:
    temp_var = tf.createVariable(var, "double", ("datasize",))
    temp_var[:] = data[var]
for var in ["tflux", "times"]:
    temp_var = tf.createVariable(var, "double", ("ntime",))
    temp_var[:] = data[var]
for var in ["heights"]:
    temp_var = tf.createVariable(var, "double", ("nheight",))
    temp_var[:] = data[var]
tf.setncattr("coordinates", "heights")
tf.close()
