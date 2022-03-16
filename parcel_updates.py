# Import system modules
import os, arcpy

###### Local variables######

FolderName = input("Type todays date to create a new folder here: T:\Data\Downloads\Parcels\....")
os.mkdir("T:\\Data\\Downloads\\Parcels\\" + FolderName)

#Pause so you can copy parcels from ftp site to new folder.
input("Press Enter once you have copied parcels to newly created folder")

#Parcel feature class in SDE
ParcelSDE = "T:\\Data\\SDE\\GISSQL_RosemountEGDB-osa.sde\\RosemountEGDB.DBO.Cadastral\\RosemountEGDB.DBO.parcels"

#Location of new parcels copied from ftp site
NewParcels = "T:\\Data\\Downloads\\Parcels\\" +FolderName+ "\\parcels.shp"
ClippedParcels = "T:\\Data\\Downloads\\Parcels\\" +FolderName+ "\\parcels_clipped.shp"

#City Boundary Layer to clip parcel layer
CityBoundary = "T:\\Data\\SDE\\GISSQL_RosemountEGDB-osa.sde\\RosemountEGDB.DBO.ReferenceData\\RosemountEGDB.DBO.City_Boundary"

#LFID Table and intermediate parcel FC to join to
LFID_Table = "T:\\Data\\SDE\\GISSQL_RosemountEGDB-osa.sde\\RosemountEGDB.DBO.Parcels_LFID"
ParcelIntermediate = "T:\\Project\\Automation\\ToolOutputs.gdb\\ParcelsForTool"

######Run Tool######

# Clip parcels to city boundary
arcpy.Clip_analysis(NewParcels, CityBoundary, ClippedParcels)
print("Clip to city boundary done")

#Remove existing features from  intermediate Parcel Layer
arcpy.management.TruncateTable(ParcelIntermediate)
print("Truncate table done for intermediate layer")

#Take the clipped parcels and load into the parcel feature class in Intermediate Layer
arcpy.management.Append(ClippedParcels, ParcelIntermediate, "NO_TEST")
print("Clipped features loaded into intermediate layer")

#Join Tables and calculate field in intermediate parcel layer
arcpy.management.JoinField(ParcelIntermediate, "OLDPIN", LFID_Table, "PIN_String")
print("LFID table joined to intermediate layer")
arcpy.management.CalculateField(ParcelIntermediate, "LFID", "!LFID_1!", "PYTHON3")
arcpy.management.CalculateField(ParcelIntermediate, "PADDRESS", "!ADDRESS!", "PYTHON3")
print("LFID and PADDRESS fields calculated on intermediate parcel layer")

#Delete fields from join
arcpy.management.DeleteField(ParcelIntermediate, ["PIN_1", "LFID_1", "ADDRESS", "PIN_STRING"])
print("Joined fields deleted from intermediate layer")

#Remove existing features from parcel feature class in SDE
arcpy.management.TruncateTable(ParcelSDE)
print("Truncate table done for SDE parcel Layer")

#Take the intermediate parcel layer and load into the parcel feature class into the sde parcel layer
arcpy.management.Append(ParcelIntermediate, ParcelSDE, "NO_TEST")
print("Clipped features loaded into SDE layer")

