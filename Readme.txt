The objective of this project is to be used for converting netCDF to raster and then raster to ASCII files for a specific geography (northern high plain) in arcpy.
The created ASCII files can be further used in a USGS software "Soil Water Balance" to estimate the irrigation data and recharge data under different climate conditions. The geography boundary of interest can be easily adapted to any geography boundary.

Coordinate system: USA_Contiguous_Albers_Equal_Area_Conic in meter

root directory
	|
	|-> ppt_2009_12_31.asc			- An example of ASCII file containg precipitation data for northern high plain aquifer 
	|-> ASCII_results			- An example of precipitation data in ASCII format for the northern high plain geography.
	|-> netCDF_to_raster_to_ASCII.py	- Python scripts for this project
	|-> netCDF_to_raster_to_ascii.mxd	- ArcMap document file for visualizing climate data, shapefile of northern high plain aquifer, etc.
	|-> netCDF_climate.gdb (unabloaded to push due to file size limit, can be downloaded via this link: https://unl.box.com/s/2z71n0oahao4oop9x9l9fwcraf4g8gpj)
		|-> BCCAv1.nc4			- BCCAv2_0.125deg_pr_day_CSIRO-Mk3-6-0_rcp26_r10i1p1_20160101-202512313 downloaded from ftp://gdo-dcp.ucllnl.org/pub/dcp/archive/cmip5/
		|-> NHP_modflow 		- Shapefile of northern high plain aquifer
		|-> NHP_modflow_grid_reproject_meter - Shapefile of northern high plain aquifer consisted of 795 columns and 565 rows in 1000 meter cell size.
		|-> pr_Layer_ProjectRaster	- GeoDatabase Raster Dataset converted from netCDF: preciptation data of the contiguous US on January 1st, 2016
		|-> pr_raster_repro_clip	- GeoDatabase Raster Dataset clipped with NHP_modflow_grid_reproject_meter