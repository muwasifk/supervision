"""
Driver code to solve the main problem.

Copyright (C) 2023 Karan Chawla, Muhammad Wasif Kamran, Eric Sui 

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import random


class Teacher:
    def __init__(self, schedule: list[list[str]]) -> None:
        self.schedule = schedule
        self.schedule[0] = [
            random.choice(["TAKEN", "SPARE"]),
            random.choice(["TAKEN", "SPARE"]),
            random.choice(["TAKEN", "SPARE"]),
            random.choice(["TAKEN", "SPARE"]),
        ]

        self.schedule[1] = [
            random.choice(["TAKEN", "SPARE"]),
            random.choice(["TAKEN", "SPARE"]),
            random.choice(["TAKEN", "SPARE"]),
            random.choice(["TAKEN", "SPARE"]),
        ]
        self.schedule[2] = [
            self.schedule[0][1],
            self.schedule[0][0],
            self.schedule[0][3],
            self.schedule[0][2],
        ]
        self.schedule[3] = [
            self.schedule[1][1],
            self.schedule[1][0],
            self.schedule[1][3],
            self.schedule[1][2],
        ]