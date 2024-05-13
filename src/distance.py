from math import radians, sin, cos, sqrt, atan2


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0 * 1000

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return round(distance, 2)


def get_station_info(station_name, df):
    station_rows = df[df["Station"] == station_name]
    if not station_rows.empty:
        station_info = {
            "Latitude": station_rows.iloc[0]["Latitude"],
            "Longitude": station_rows.iloc[0]["Longitude"],
            "Lines": set(station_rows["Line"]),
        }
        return station_info
    else:
        return None


def calculate_distance(row, df):
    origin_info = get_station_info(row["Station"], df)
    dest_info = get_station_info(row["Destination"], df)

    if origin_info and dest_info:
        if origin_info["Lines"].intersection(dest_info["Lines"]):
            return haversine_distance(
                origin_info["Latitude"],
                origin_info["Longitude"],
                dest_info["Latitude"],
                dest_info["Longitude"],
            )
    return None
