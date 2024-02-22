# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from __future__ import annotations

import os
from typing import Any, ClassVar
from urllib.parse import urlsplit

import attr


@attr.define()
class Dataset(os.PathLike):
    """A Dataset is used for marking data dependencies between workflows."""

    uri: str = attr.field(validator=[attr.validators.min_len(1), attr.validators.max_len(3000)])
    extra: dict[str, Any] | None = None

    __version__: ClassVar[int] = 1

    @uri.validator
    def _check_uri(self, attr, uri: str):
        if uri.isspace():
            raise ValueError(f"{attr.name} cannot be just whitespace")
        try:
            uri.encode("ascii")
        except UnicodeEncodeError:
            raise ValueError(f"{attr.name!r} must be ascii")
        parsed = urlsplit(uri)
        if parsed.scheme and parsed.scheme.lower() == "airflow":
            raise ValueError(f"{attr.name!r} scheme `airflow` is reserved")

    def __fspath__(self):
        return self.uri

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.uri == other.uri
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.uri)
