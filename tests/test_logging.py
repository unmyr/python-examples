"""Test logging with unittest."""
import unittest
import logging


class TestLogging(unittest.TestCase):
    """Test logging module."""

    def test_handler_set_level_none(self):
        """Test the handler instance."""
        with self.assertRaises(TypeError) as context:
            logger = logging.getLogger(__name__)
            handler = logging.StreamHandler()
            handler.setLevel(None)  # NG
            logger.setLevel(logging.DEBUG)
            logger.addHandler(handler)
            logger.propagate = False

            logger.debug("hello world!")

        self.assertEqual(
            "Level not an integer or a valid string: None", str(context.exception)
        )

    def test_logger_set_level_none(self):
        """Test the logger instance."""
        with self.assertRaises(TypeError) as context:
            logger = logging.getLogger(__name__)
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
            logger.setLevel(None)  # NG
            logger.addHandler(handler)
            logger.propagate = False

            logger.debug("hello world!")

        self.assertEqual(
            "Level not an integer or a valid string: None", str(context.exception)
        )

    def test_logging_level_name(self):
        """Test the logging level representation."""
        self.assertEqual(logging.getLevelName("NOTSET"), logging.NOTSET)
        self.assertEqual(logging.getLevelName("DEBUG"), logging.DEBUG)
        self.assertEqual(logging.getLevelName("INFO"), logging.INFO)
        self.assertEqual(logging.getLevelName("WARNING"), logging.WARNING)
        self.assertEqual(logging.getLevelName("ERROR"), logging.ERROR)
        self.assertEqual(logging.getLevelName("CRITICAL"), logging.CRITICAL)
        self.assertEqual(logging.getLevelName("FATAL"), logging.CRITICAL)
        self.assertEqual(logging.getLevelName("Info"), "Level Info")

        self.assertEqual(logging.getLevelName(logging.NOTSET), "NOTSET")
        self.assertEqual(logging.getLevelName(logging.DEBUG), "DEBUG")
        self.assertEqual(logging.getLevelName(logging.INFO), "INFO")
        self.assertEqual(logging.getLevelName(logging.WARNING), "WARNING")
        self.assertEqual(logging.getLevelName(logging.ERROR), "ERROR")
        self.assertEqual(logging.getLevelName(logging.CRITICAL), "CRITICAL")
