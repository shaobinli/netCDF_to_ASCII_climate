'''
Created on April 20, 2019

The objective of this script is to be used for converting netCDF to raster and then raster to ASCII files for a specific geography (northern high plain).
The created ASCII files can be further used in a USGS software "Soil Water Balance" to estimate the irrigation data and recharge data under different climate conditions.
The groundwater recharge data can be further used as inputs to MODFLOW to predict future ground water depletions.

@author: Shaobin Li, sli2@huskers.unl.edu | leeshbin@gmail.com
'''

import time
start = time.time()
import os
import arcpy
from arcpy import env
# Import everything from the spatial analyst library
from arcpy.sa import *

# Set some environment variables
arcpy.env.workspace = r"C:\Users\sli48\Box Sync\netCDF_to_ASCII_climate\netCDF_climate.gdb"
arcpy.env.scratchWorkspace = r"C:\Users\sli48\Box Sync\netCDF_to_ASCII_climate\netCDF_climate.gdb"
arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")

# Step 1: convert netCDF file into raster
##inNetCDF = r"C:\Users\sli48\Box Sync\NRES898_project_SL\netCDF_climate.gdb\BCCAv1.nc4"
## 'BCAAv1.nc4' is
inNetCDF = r"C:\Users\sli48\Box Sync\netCDF_to_ASCII_climate\netCDF_climate.gdb\BCCAv1.nc4"
variable = "pr"
XDimension = "longitude"
YDimension = "latitude"
outRasterLayer = "rainfall"
bandDimmension = ""
valueSelectionMethod = "BY_VALUE"
project_system = arcpy.SpatialReference('USA Contiguous Albers Equal Area Conic')
geographic_transform = 'NAD_1983_To_WGS_1984_1'

## Check netCDF file properties and how many days of data are contained in the netCDF file
nc_FP = arcpy.NetCDFFileProperties(inNetCDF)
print "nc_FP:", nc_FP
nc_Dim = nc_FP.getDimensions()
print "nc_Dim:", nc_Dim

## Create rasters for all days. 1 raster represent rainfall in a day. 
## In this case, 3653 rasters are created to present 3653 days from 20160101 to 20251231
for dimension in nc_Dim:
    print "dimension:", dimension
    if dimension == "time":
        top = nc_FP.getDimensionSize(dimension)
        print "top:", top
        for i in range(0, 30):
            dimension_values = nc_FP.getDimensionValue(dimension, i)
#             print "dimension_values", dimension_values
            nowFile = str(dimension_values)
#             print "nowFile:", nowFile
            dimension_values = 'time ' + "'" + dimension_values + "'"
            output_raster = arcpy.MakeNetCDFRasterLayer_md(inNetCDF, variable, XDimension, YDimension, outRasterLayer,
                                           bandDimmension, dimension_values, valueSelectionMethod)
 
## Step 2: reproject the converted file from Step 1 as Albers Equal Area Conic projection (NAD 83) in meter. Scripts exported from model builder 
            #Name the reprojected raster by date in netCDF file
            date = nowFile.split(' ')[0].split(r'/')
            pr_raster_repro = 'ppt_' +  date[2] + '_' + date[0] + '_' + date[1]
            #Reproject
            arcpy.ProjectRaster_management(output_raster, pr_raster_repro,  project_system, "BILINEAR", 1000, geographic_transform)
 
## Step 3: clip the reprojected raster from Step 2 into the boundary of northern high plain aquifer
            arcpy.Clip_management(pr_raster_repro, "-810000 148213.739399999 -14998.3845999986 713214.887499999",
                                  'clip_' + pr_raster_repro,
                                  r"C:\Users\sli48\Box Sync\netCDF_to_ASCII_climate\netCDF_climate.gdb\NHP_modflow_grid_reproject_meter.shp",
                                  "-9999", "NONE", "MAINTAIN_EXTENT")
            
## Step 4: Convert the unit of precipitation from "inch" to "mm" by multiplying "0.0393701" and save it
            pr_raster_repro_mm = Raster('clip_' + pr_raster_repro) * 0.0393701
            pr_raster_repro_mm.save(os.path.join(arcpy.env.workspace, pr_raster_repro + "_mm"))
            
## Step 5: Convert clipped raster from step 4 into ASCII format.
            output_path = r'C:\Users\sli48\Box Sync\NRES898_project_SL\ASCII_results'
            arcpy.RasterToASCII_conversion(pr_raster_repro_mm, os.path.join(output_path, pr_raster_repro + '.asc'))
            
## Post-processing: Delete intermediate rasters created for exporting to ASCII format
            # Delete pr_raster_repro that is the output raster after reprojection and resample
            arcpy.Delete_management(pr_raster_repro)
            # Delete 'clip_' + pr_raster_repro  that is the output raster after clipping with Northern high plain aquifer
            arcpy.Delete_management('clip_' + pr_raster_repro)
            # Delete pr_raster_repro + "_mm"  that is the output raster after converting unit of precipitation from inch to mm
            arcpy.Delete_management(pr_raster_repro + "_mm")
            
## Post-processing: calculate processing time
print "Done processing"
end = time.time()
print "Processing time is ", end-start
