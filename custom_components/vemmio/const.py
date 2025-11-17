"""Constants for the Vemmio integration."""

from datetime import timedelta
import logging

DOMAIN = "vemmio"
SCAN_INTERVAL = timedelta(seconds=60)  # in seconds
LOGGER = logging.getLogger("homeassistant.components.vemmio")
