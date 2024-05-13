import csv


def identify_stations_with_multiple_lines(filename):
    stations = {}
    with open(filename, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            station_name = row["Station"]
            line_name = row["Line"]
            if station_name in stations:
                stations[station_name].append(line_name)
            else:
                stations[station_name] = [line_name]
    return {station: lines for station, lines in stations.items() if len(lines) > 1}


def update_csv(filename, stations_to_update):
    updated_rows = []
    with open(filename, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["Station"] in stations_to_update:
                row["Point Color"] = "#FFFFFF"
            updated_rows.append(row)

    with open(filename, "w", encoding="utf-8", newline="") as csvfile:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)


filename = "Metro_Madrid_2021.csv"

stations_to_update = identify_stations_with_multiple_lines(filename)

update_csv(filename, stations_to_update)

print(
    "As cores das estações que estão em mais de uma linha de metrô foram definidas como branco no arquivo CSV."
)
