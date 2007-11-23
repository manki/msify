#!/usr/bin/env python -t
#
# Part of MSify project (http://code.google.com/p/msify/)
#
# Distributed under GNU GPL version 2.

"""Sify Broadband configuration settings."""

import ConfigParser


CONFIG_FILE = './.sify'
SESSION_FILE = './.session'


class Configuration(object):
    """Configuration settings read from config file."""

    def __init__(self, config_file=CONFIG_FILE):
        """Initializer.

        Arguments:
          config_file -- configuration file name.
        """
        self._config = self._LoadFile(config_file)

    def NetSetting(self, key):
        """Return network setting identified by key."""
        return self._config.get('network', key)

    def AuthenticationSetting(self, key):
        """Return authentication setting identified by key."""
        return self._config.get('authentication', key)

    def _LoadFile(self, fname):
        """Load configuration settings from file.

        Arguments:
          fname: configuration file name.

        Returns:
          ConfigParser object representing the configuration specified
          in file fname.
        """
        config = ConfigParser.ConfigParser()
        config.read(fname)
        return config
