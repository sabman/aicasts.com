import geopandas as gp
import numpy as np
import pyproj
from python_ags4 import AGS4
from shapely.geometry import Point
from shapely.ops import transform
from sqlalchemy import MetaData, Table, create_engine, inspect, select
from sqlalchemy.sql.expression import func


def _is_epsg(epsg):
    return str(epsg) in pyproj.database.get_codes("EPSG", pyproj.enums.PJType("CRS"))

def _transform_point_list(points, transformer):
    new_points = []
    for point in points:
        new_point = transform(transformer.transform, point)
        new_points.append(new_point)
    return new_points

def ags_to_postgis(filepath,
                   username,
                   password,
                   target_epsg,
                   schema,
                   data_type,
                   source_epsg=None,
                   campaign_id=None,
                   db_name="corp_ta_si",
                   host="ow-postgre.postgres.database.azure.com"
                   ):
    """ags_to_postgis
    Function to parse and upload an .AGS file to the internal OW PostGIS Spatial Database.

    Parameters
    ----------
    filepath : str
       Filepath of the .AGS file to upload.
    username : str
        OW PostgreSQL/PostGIS Username.
    password : str
        OW PostgreSQL/PostGIS Password.
    target_epsg : int
        EPSG code of the CRS used to upload the "LOCA" X/Y coordinates to PostGIS. Mut be the same
        as the CRS of any existing "loca" table already in the target schema. If a "loca" table does
        not exist, it will be created with this CRS. Any subsequent imports will have to match this
        CRS.
    schema : str
        Destination schema within the database.
    data_type : str
        Select 'cpt', 'bh' or 'lab' for the type of data. Adds this as table prefixed when creating
        from scratch.
    source_epsg : int | None
        EPSG code of the CRS of the X/Y coordinate in "LOCA". If None, assumes it is the same as
        the target_epsg and carries out no transformations. If different to target_epsg, a
        transformation will be applied from the source_epsg to target_epsg in the "geom" column. By
        default None. 
    campaign_id : int | None
        Campaign id. Used to manually set the campaign id number for the .AGS file. If None, the
        campaign_id parameter will be determined automatically from the existing data in the
        database by incrementing the highest existing campaign_id by 1. By default None.
    db_name : str, optional
        Name of the databse within the OW cluster, by default "corp_ta_si".
    host : str, optional
        Host URL of the database, by default "ow-postgre.postgres.database.azure.com" for OW's
        database.
    
    Raises
    ------
    ValueError
        If source_espg or target_epsg are not valid EPSG CRS codes, or if data_type is invalid.
    """
    if not _is_epsg(source_epsg) and source_epsg is not None:
        raise ValueError(f"{source_epsg=} not a valid EPSG code.")
    elif not _is_epsg(target_epsg):
        raise ValueError(f"{target_epsg=} not a valid EPSG code.")
    
    if data_type.lower() not in ["cpt", "bh", "lab"]:
        raise ValueError(f"Invalid value for {data_type=}. Must be one of 'bh', 'cpt', or 'lab'.")
    
    reproject = False
    
    if (source_epsg is not None) and not (source_epsg == target_epsg):
        reproject = True
        source_crs = pyproj.CRS("EPSG:" + str(source_epsg))
        target_crs = pyproj.CRS("EPSG:" + str(target_epsg))
        crs_transformer = pyproj.Transformer.from_crs(source_crs, target_crs, always_xy=True)
        
    tables, _ = AGS4.AGS4_to_dataframe(filepath)
    
    db_string = f"postgresql://{username}:{password}@{host}/{db_name}"
    engine = create_engine(db_string)
    metadata = MetaData(schema=schema)
    
    insp = inspect(engine)
    if campaign_id is not None:
        pass
    elif (not insp.has_table(f"{data_type.lower()}_loca", schema=schema)):
        campaign_id = 1
    else:
        table = Table(
        f"{data_type}_loca",
        metadata,
        autoload=True,
        autoload_with=engine
        )
        stmt = select([func.max(table.columns.campaign_id)])
        with engine.connect() as connection:
            results = connection.execute(stmt).fetchall()
        
        campaign_id = results[0][0] + 1

    for key in tables.keys():
        df = AGS4.convert_to_numeric(tables[key])
        df.columns = [x.lower() for x in df.columns]
        df["campaign_id"] = campaign_id
        if key == "LOCA":
            points = []
            for point in np.array(df[["loca_locx", "loca_locy"]]):
                points.append(Point(point[0], point[1] + 10000))
                
            if reproject:
                points = _transform_point_list(points, crs_transformer)
            
            df = gp.GeoDataFrame(df).set_geometry(points, crs=f"EPSG:{target_epsg}")
            df.rename_geometry("geom", inplace=True)
            df.to_postgis(f"{data_type}_{key.lower()}", con=engine, schema=schema, if_exists="append", index=False)
        else:
            df.to_sql(f"{data_type}_{key.lower()}", con=engine, schema=schema, if_exists="append", index=False)