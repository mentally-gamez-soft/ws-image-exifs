from functools import wraps

from exif import Image

from core.services.gps_coordinates_formater import (
    dms_coordinates_to_dd_coordinates,
)


class ExifsReaderService:
    service_error_user_message: str = None
    service_error_tech_message: str = None
    __image_file: Image = None

    def is_valid_image(origin_function):
        @wraps(origin_function)
        def wrapper(*args, **kwargs):
            if args[0].__image_file is None:
                return {"status": False}
            return origin_function(*args, **kwargs)

        return wrapper

    def get_errors(self) -> dict:
        return dict(
            user_error=self.service_error_user_message,
            technical_error=self.service_error_tech_message,
        )

    def get_image_file(self):
        return self.__image_file

    def __open_image(self, file_name: str = ""):
        try:
            with open(file_name, "rb") as file:
                self.__image_file = Image(file)
        except FileNotFoundError as exc:
            self.service_error_user_message = "The image file is not existing."
            self.service_error_tech_message = (
                "The image file is not existing - {}".format(exc)
            )
        except Exception as exc:
            self.service_error_user_message = "The image file is not existing."
            self.service_error_tech_message = (
                "Unknown error when reading the file image - {}".format(exc)
            )

    def __init__(self, **payload):
        self.__open_image(payload.get("image-source"))

    @is_valid_image
    def has_exif(self) -> dict:
        return (
            {"status": True, "version": self.__image_file.exif_version}
            if self.__image_file.has_exif
            else {"status": False, "version": "N/A"}
        )

    @is_valid_image
    def get_camera_lens_exifs(self) -> dict:
        if self.has_exif()["status"]:
            return {
                "status": True,
                "camera": {
                    "brand": self.__image_file.make,
                    "model": self.__image_file.model,
                    "serial": self.__get_body_serial_number(),
                },
                "lens": {
                    "brand": self.__image_file.get("lens_make", "unknown"),
                    "model": self.__image_file.get("lens_model", "unknown"),
                },
                "exif-version": self.__image_file.exif_version,
            }

    def __get_body_serial_number(self):
        return (
            self.__image_file.body_serial_number
            if "body_serial_number" in dir(self.__image_file)
            else "unknown"
        )

    def __get_orientation(self):
        return (
            self.__image_file.orientation
            if "orientation" in dir(self.__image_file)
            else "unknown"
        )

    def __get_date_shot(self):
        return (
            self.__image_file.datetime_original
            if "datetime_original" in dir(self.__image_file)
            else "unknown"
        )

    def __get_width(self):
        return (
            self.__image_file.x_resolution
            if "x_resolution" in dir(self.__image_file)
            else "unknown"
        )

    def __get_height(self):
        return (
            self.__image_file.y_resolution
            if "y_resolution" in dir(self.__image_file)
            else "unknown"
        )

    def __get_focal_length(self):
        return (
            self.__image_file.focal_length
            if "focal_length" in dir(self.__image_file)
            else "unknown"
        )

    def __get_fstop(self):
        return (
            self.__image_file.f_number
            if "f_number" in dir(self.__image_file)
            else "unknown"
        )

    def __get_shutter_speed(self):
        return (
            self.__image_file.exposure_time
            if "exposure_time" in dir(self.__image_file)
            else "unknown"
        )

    def __get_iso_speed(self):
        return (
            self.__image_file.iso_speed
            if "iso_speed" in dir(self.__image_file)
            else "unknown"
        )

    def __get_copyright(self):
        return (
            self.__image_file.copyright
            if "copyright" in dir(self.__image_file)
            else "unknown"
        )

    def __get_description(self):
        return (
            self.__image_file.image_description
            if "image_description" in dir(self.__image_file)
            else "unknown"
        )

    def __get_latitude_info(self):
        result = {}
        result["status"] = True

        if "gps_latitude" in dir(
            self.__image_file
        ) and "gps_latitude_ref" in dir(self.__image_file):
            result["decimal"] = dms_coordinates_to_dd_coordinates(
                self.__image_file.gps_latitude
            )
            result["referential"] = self.__image_file.gps_latitude_ref
        else:
            result["status"] = False
        return result

    def __get_longitude_info(self):
        result = {}
        result["status"] = True

        if "gps_longitude" in dir(
            self.__image_file
        ) and "gps_longitude_ref" in dir(self.__image_file):
            result["decimal"] = dms_coordinates_to_dd_coordinates(
                self.__image_file.gps_longitude
            )
            result["referential"] = self.__image_file.gps_longitude_ref
        else:
            result["status"] = False
        return result

    def __get_altitude_info(self):
        result = {}
        result["status"] = True

        if "gps_altitude" in dir(
            self.__image_file
        ) and "gps_altitude_ref" in dir(self.__image_file):
            result["decimal"] = dms_coordinates_to_dd_coordinates(
                self.__image_file.gps_altitude
            )
            result["referential"] = self.__image_file.gps_altitude_ref
        else:
            result["status"] = False
        return result

    @is_valid_image
    def get_image_exifs(self) -> dict:
        if self.has_exif()["status"]:
            return {
                "status": True,
                "image": {
                    "copyright": self.__get_copyright(),
                    "description": self.__get_description(),
                    "orientation": self.__get_orientation(),
                    "date": self.__get_date_shot(),
                    "width": self.__get_width(),
                    "height": self.__get_height(),
                    "focal-length": self.__get_focal_length(),
                    "fstop": self.__get_fstop(),
                    "shutter-speed": self.__get_shutter_speed(),
                    "iso": self.__get_iso_speed(),
                    "exif-version": self.__image_file.exif_version,
                },
            }

    @is_valid_image
    def get_gps_exifs(self) -> dict:
        result = {}
        result["status"] = False
        if self.has_exif()["status"]:
            latitude_info = self.__get_latitude_info()
            longitude_info = self.__get_longitude_info()
            altitude_info = self.__get_altitude_info()

            if latitude_info["status"] and longitude_info["status"]:
                result["gps"]["latitude"] = latitude_info
                result["gps"]["longitude"] = longitude_info
                result["status"] = True

            if altitude_info["status"]:
                result["gps"]["altitude"] = altitude_info

            return result
