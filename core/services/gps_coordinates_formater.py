def format_dms_coordinates(coordinates: tuple) -> str:
    return "{} deg {}' {}\"".format(
        coordinates[0], coordinates[1], coordinates[2]
    )


def dms_coordinates_to_dd_coordinates(
    coordinates: tuple, coordinates_ref: str
) -> float:
    decimal_degrees = (
        coordinates[0] + coordinates[1] / 60 + coordinates[2] / 3600
    )

    if coordinates_ref == "S" or coordinates_ref == "W":
        decimal_degrees = -decimal_degrees

    return decimal_degrees
