#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2023-present Hydrogram <https://hydrogram.org>
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of Pyrofork.
#
#  Pyrofork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrofork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrofork.  If not, see <http://www.gnu.org/licenses/>.

import sys

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

# Add the current directory to the path, so we can import the compiler.
sys.path.insert(0, ".")


class CustomHook(BuildHookInterface):
    """A custom build hook for pyrofork."""

    def initialize(self, version, build_data):
        """Initialize the hook."""
        if self.target_name not in ["wheel", "install"]:
            return

        from compiler.api.compiler import start as compile_api
        from compiler.errors.compiler import start as compile_errors

        compile_api()
        compile_errors()
