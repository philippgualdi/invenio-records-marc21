# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Marc21 datamodel"""

from __future__ import absolute_import, print_function

from .ext import InvenioRecordsMARC21
from .proxies import Marc21, current_marc21record
from .version import __version__

__all__ = ("__version__", "InvenioRecordsMARC21", "Marc21", "current_marc21record")
