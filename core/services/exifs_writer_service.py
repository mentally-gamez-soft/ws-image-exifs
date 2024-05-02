from exif import Image


class ExifsWriterService:
    service_error_user_message: str = None
    service_error_tech_message: str = None
    __image_source_file: Image = None
    __image_dest_file_name: str = None
    __image_dest_file: Image = None

    def __open_image(self, file_name: str = ""):
        try:
            with open(file_name, "rb") as file:
                self.__image_source_file = Image(file)
        except FileNotFoundError as exc:
            self.service_error_user_message = (
                "The image source file is not existing."
            )
            self.service_error_tech_message = (
                "The image source file is not existing - {}".format(exc)
            )
        except Exception as exc:
            self.service_error_user_message = "The image file is not existing."
            self.service_error_tech_message = (
                "Unknown error when reading the source file image - {}".format(
                    exc
                )
            )

    def __init__(self, **payload):
        self.__open_image(payload.get("image-source"))
        self.__image_dest_file_name = payload.get("image-dest")

    def get_image_source_file(self):
        return self.__image_source_file

    def get_image_destination_file(self):
        return self.__image_dest_file

    def save_image_file(self):
        with open(self.__image_dest_file_name, "wb") as updated_image_file:
            updated_image_file.write(self.__image_source_file.get_file())
            self.__image_dest_file = updated_image_file

    def set_exifs_copyright(self, copyright: str):
        self.__image_source_file.copyright = copyright

    def set_exifs_description(self, description: str):
        self.__image_source_file.image_description = description

    def set_exifs_fstop(self, fstop: float):
        self.__image_source_file.f_number = fstop

    def set_exifs_shutter_speed(self, exposure_time: float):
        self.__image_source_file.exposure_time = exposure_time

    def set_exifs_iso(self, iso: int):
        self.__image_source_file.iso_speed = iso
        self.__image_source_file.photographic_sensitivity = iso

    def set_exifs_focal_length(self, focal_length: float):
        self.__image_source_file.focal_length = focal_length

    def __has_gps_exifs(self) -> bool:
        return "gps_latitude" in dir(
            self.__image_source_file
        ) and "gps_longitude" in dir(self.__image_source_file)

    def update_exifs_gps_position(
        self,
        latitude: tuple,
        lat_ref: str,
        longitude: tuple,
        lg_ref: str,
        altitude: tuple = None,
        alt_ref: str = None,
    ):
        if self.__has_gps_exifs():
            if (
                latitude
                and longitude
                and lat_ref in ("N", "S")
                and lg_ref in ("E", "W")
            ):
                self.__image_source_file.gps_latitude = latitude
                self.__image_source_file.gps_latitude_ref = lat_ref
                self.__image_source_file.gps_longitude = longitude
                self.__image_source_file.gps_longitude_ref = lg_ref

            if altitude and alt_ref in (-1, 0):
                self.__image_source_file.gps_altitude = altitude
                self.__image_source_file.gps_altitude_ref = alt_ref
