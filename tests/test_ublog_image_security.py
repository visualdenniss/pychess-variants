"""Security properties of the legacy blog image proxy."""

import unittest

from views.ublog import _is_safe_image_content_type


class UblogImageSecurityTests(unittest.TestCase):
    def test_rejects_active_content(self):
        for content_type in (
            "image/svg+xml",
            "image/svg+xml; charset=utf-8",
            "text/html",
            "application/javascript",
        ):
            with self.subTest(content_type=content_type):
                self.assertFalse(_is_safe_image_content_type(content_type))

    def test_keeps_bitmap_images(self):
        for content_type in ("image/png", "image/jpeg", "image/gif", "image/webp", "image/avif"):
            with self.subTest(content_type=content_type):
                self.assertTrue(_is_safe_image_content_type(content_type))
