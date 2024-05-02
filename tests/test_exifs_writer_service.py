import time
import unittest

from core.services.exifs_reader_service import ExifsReaderService
from core.services.exifs_writer_service import ExifsWriterService


class TestExifsWriterService(unittest.TestCase):

    def setUp(self) -> None:
        self.service_writer = ExifsWriterService(
            **{
                "image-source": "tests/resources/image-with-exifs.jpg",
                "image-dest": "tests/resources/image-updated-with-exifs.jpg",
            }
        )

    def test_set_gps_position(self):
        self.service_writer.update_exifs_gps_position(
            latitude=(37.0, 14.0, 3.6),
            lat_ref="N",
            longitude=(115.0, 48.0, 23.99),
            lg_ref="W",
        )

    def test_set_description(self):
        self.service_writer.set_exifs_description(
            "This is a description for an image"
        )
        self.service_writer.save_image_file()

        image = ExifsReaderService(
            **{"image-source": "tests/resources/image-updated-with-exifs.jpg"}
        )
        result = image.get_image_exifs()
        self.assertEqual(
            result["image"]["description"],
            "This is a description for an image",
            "The description is not correctly set => {}".format(result),
        )

    def test_set_copyright(self):
        self.service_writer.set_exifs_copyright("Copyright actionphotopassion")
        self.service_writer.save_image_file()

        image = ExifsReaderService(
            **{"image-source": "tests/resources/image-updated-with-exifs.jpg"}
        )
        result = image.get_image_exifs()
        self.assertEqual(
            result["image"]["copyright"],
            "Copyright actionphotopassion",
            "The copyright is not correctly set => {}".format(result),
        )

    def test_set_fstop(self):
        self.service_writer.set_exifs_fstop(5.6)
        self.service_writer.save_image_file()

        image = ExifsReaderService(
            **{"image-source": "tests/resources/image-updated-with-exifs.jpg"}
        )
        result = image.get_image_exifs()
        self.assertEqual(
            result["image"]["fstop"],
            5.6,
            "The f-stop is not correctly set => {}".format(result),
        )

    def test_set_shutter_speed(self):
        self.service_writer.set_exifs_shutter_speed(0.5)
        self.service_writer.save_image_file()

        image = ExifsReaderService(
            **{"image-source": "tests/resources/image-updated-with-exifs.jpg"}
        )
        result = image.get_image_exifs()
        self.assertEqual(
            result["image"]["shutter-speed"],
            0.5,
            "The shutter speed is not correctly set => {}".format(result),
        )

    def test_set_iso(self):
        self.service_writer.set_exifs_iso(500)

        self.service_writer.save_image_file()

        image = ExifsReaderService(
            **{"image-source": "tests/resources/image-updated-with-exifs.jpg"}
        )
        result = image.get_image_exifs()
        self.assertEqual(
            result["image"]["iso"],
            500,
            "The iso speed is not correctly set => {}".format(result),
        )
