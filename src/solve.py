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
    def __init__(self, name: str, schedule: list[list[str]]) -> None:
        self.name = name
        self.schedule = schedule
        self.dor: int = 0
        self.potential: list[int] = []
        if len(schedule[0]) == 0:
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


teachers: list[Teacher] = []
for i in range(75):
    cur = Teacher("TEACH" + str(i), [[], [], [], []])
    teachers.append(cur)
    if cur.schedule == ["TAKEN", "TAKEN", "TAKEN", "TAKEN"]:
        print(cur.schedule)

teachers.append(
    Teacher(
        "TEACH75",
        [
            ["TAKEN", "TAKEN", "TAKEN", "TAKEN"],
            ["TAKEN", "TAKEN", "TAKEN", "TAKEN"],
            ["TAKEN", "TAKEN", "TAKEN", "TAKEN"],
            ["TAKEN", "TAKEN", "TAKEN", "TAKEN"],
        ],
    )
)
teachers.append(
    Teacher(
        "TEACH76",
        [
            ["SPARE", "TAKEN", "TAKEN", "TAKEN"],
            ["TAKEN", "TAKEN", "TAKEN", "TAKEN"],
            ["TAKEN", "SPARE", "TAKEN", "TAKEN"],
            ["TAKEN", "TAKEN", "TAKEN", "TAKEN"],
        ],
    )
)

candidates: list[list[str]] = [[], [], [], [], [], [], [], [], [], [], [], []]

for teacher in teachers:
    for day in range(0, 4):
        if teacher.schedule[day][1] == "SPARE" or teacher.schedule[day][2] == "SPARE":
            candidates[day].append(teacher.name)

            candidates[day + 4].append(teacher.name)

            candidates[day + 8].append(teacher.name)

            teacher.potential.append(day)
            teacher.potential.append(day + 4)
            teacher.potential.append(day + 8)

dors: list[int] = []
for i in range(len(teachers)):
    dors.append(0)

for teacher in teachers:
    for cur_day in candidates:
        if teacher.name in cur_day:
            dors[int(teacher.name[5:])] += 1

for teacher in teachers:
    teacher.dor = dors[int(teacher.name[5:])]

sorted_teachers = sorted(teachers, key=lambda x: x.dor)

construction: list[list[str]] = [[], [], [], [], [], [], [], [], [], [], [], []]

for teacher in sorted_teachers:
    if teacher.dor == 0 or len(teacher.potential) == 0:
        continue

    choice = random.choice(teacher.potential)
    while len(construction[choice]) == 6:
        choice = random.choice(teacher.potential)

    construction[choice].append(teacher.name)

    if len(construction[choice]) == 6:
        for alt_teacher in sorted_teachers:
            if choice in alt_teacher.potential:
                alt_teacher.potential.remove(choice)

print(construction)
