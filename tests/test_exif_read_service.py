import unittest

from core.services.exifs_reader_service import ExifsReaderService


class TestImageService(unittest.TestCase):

    def test_load_image_when_non_existing_file(self):
        none_existing_image = ExifsReaderService(
            **{"image-source": "tests/resources/image-fake.png"}
        )
        self.assertIsNone(
            none_existing_image.get_image_file(),
            "The image file is not None as expected !!!",
        )
        self.assertEqual(
            none_existing_image.get_errors()["user_error"],
            "The image file is not existing.",
            "The message for the user is incorrect.",
        )
        self.assertIn(
            "The image file is not existing - [Errno 2] No such file or directory",
            none_existing_image.get_errors()["technical_error"],
            "The message for the technical team is incorrect.",
        )

    def test_load_image_when_existing_file(self):
        existing_image = ExifsReaderService(
            **{"image-source": "tests/resources/image-without-exifs.png"}
        )
        self.assertIsNotNone(
            existing_image.get_image_file(), "The image file is None !!!"
        )
        self.assertIsNone(
            existing_image.get_errors()["user_error"],
            "The message for the user has a label.",
        )
        self.assertIsNone(
            existing_image.get_errors()["technical_error"],
            "The message for the technical team has a label.",
        )

    def test_exifs_existence_from_image_without_exifs(self):
        image = ExifsReaderService(
            **{"image-source": "tests/resources/image-without-exifs.png"}
        )
        self.assertFalse(image.has_exif()["status"])
        self.assertEqual(
            image.has_exif()["version"],
            "N/A",
            "The version for an image with no exif is incorrect !",
        )

    def test_exifs_existence_from_image_with_exifs(self):
        image = ExifsReaderService(
            **{"image-source": "tests/resources/image-with-exifs.jpg"}
        )
        self.assertTrue(image.has_exif()["status"])
        self.assertNotEqual(
            image.has_exif()["version"],
            "N/A",
            "The version for an image with exifs is incorrect !",
        )
        self.assertIsNotNone(
            image.has_exif()["version"],
            "The version for an image with exifs cant be None !",
        )

    def test_exifs_existence_from_non_existing_image(self):
        image = ExifsReaderService(
            **{"image-source": "tests/resources/image-fake.jpg"}
        )
        self.assertFalse(image.has_exif()["status"])

    def test_exifs_camera_lens_from_image_with_exifs(self):
        image = ExifsReaderService(
            **{"image-source": "tests/resources/image-with-exifs.jpg"}
        )
        result = image.get_camera_lens_exifs()
        self.assertTrue(result["status"])
        self.assertEqual(
            result["camera"]["brand"],
            "Canon",
            "{}".format(dir(image.get_image_file())),
        )
        self.assertEqual(
            result["camera"]["model"],
            "5Ds",
            "{}".format(dir(image.get_image_file())),
        )

    def test_exifs_camera_lens_from_image_without_exifs(self):
        image = ExifsReaderService(
            **{"image-source": "tests/resources/image-without-exifs.jpg"}
        )
        result = image.get_camera_lens_exifs()
        self.assertFalse(result["status"])

    def test_exifs_image_info_from_image_with_exifs(self):
        image = ExifsReaderService(
            **{"image-source": "tests/resources/CZO-presenter-py.jpg"}
        )
        result = image.get_image_exifs()
        self.assertTrue(result["status"], "{}".format(result))

    def test_exifs_gps_info_from_image_without_gps_exifs(self):
        image = ExifsReaderService(
            **{"image-source": "tests/resources/CZO-presenter-py.jpg"}
        )
        result = image.get_gps_exifs()
        self.assertFalse(
            result["status"],
            "The gps info are present in this file => {}".format(result),
        )
