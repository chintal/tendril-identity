#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) 2019 Chintalagiri Shashank
#
# This file is part of tendril.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import importlib
from tendril.utils.fsutils import get_namespace_package_names
from tendril.utils import log
logger = log.get_logger(__name__, log.DEBUG)


class IdentityBase(object):
    pass


class IdentityManager(object):
    def __init__(self, prefix):
        self._prefix = prefix
        self._modules = {}
        self._identities_loaded = []
        self._load_modules()
        self._load_identities()

    def _load_identities(self):
        pass

    def _load_modules(self):
        logger.debug("Loading identity modules from {0}".format(self._prefix))
        modules = list(get_namespace_package_names(self._prefix))
        for m_name in modules:
            self._modules[m_name] = importlib.import_module(m_name)
