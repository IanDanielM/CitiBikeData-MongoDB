import numpy as np


def lat_lon_to_radians(df, lat_col, lon_col):
    return np.radians(df[[lat_col, lon_col]])


# Vectorized Haversine function
def haversine_vectorized(start_lats, start_lons, end_lats, end_lons):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert degrees to radians
    start_lats, start_lons, end_lats, end_lons = map(
        np.radians, [start_lats, start_lons, end_lats, end_lons]
    )

    # Differences in coordinates
    dlat = end_lats - start_lats
    dlon = end_lons - start_lons

    # Haversine formula
    a = (np.sin(dlat / 2.0) ** 2 + np.cos(start_lats) * np.cos(end_lats) * np.sin(dlon / 2.0) ** 2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c
    return distance
