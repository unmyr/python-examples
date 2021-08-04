"""Test logging with unittest."""
import unittest
import logging


class TestLogging(unittest.TestCase):
    """Test logging module."""

    def test_handler_set_level_none(self):
        """Test dict."""
        with self.assertRaises(TypeError) as context:
            logger = logging.getLogger(__name__)
            handler = logging.StreamHandler()
            handler.setLevel(None)  # NG
            logger.setLevel(logging.DEBUG)
            logger.addHandler(handler)
            logger.propagate = False

            logger.debug("hello world!")

        self.assertEqual(
            "Level not an integer or a valid string: None",
            str(context.exception)
        )

    def test_logger_set_level_none(self):
        """Test dict."""
        with self.assertRaises(TypeError) as context:
            logger = logging.getLogger(__name__)
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
            logger.setLevel(None)  # NG
            logger.addHandler(handler)
            logger.propagate = False

            logger.debug("hello world!")

        self.assertEqual(
            "Level not an integer or a valid string: None",
            str(context.exception)
        )
