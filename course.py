"""course.py - Entity class for one university course."""

CORE = "Core"
ELECTIVE = "Elective"


class Course:
    """
    courseCode  : str - unique code, e.g. "CS101"
    courseName  : str - course title
    creditHours : int - credit hours
    level       : str - "Core" or "Elective"
    description : str - short description
    lecturer    : str - lecturer's name
    """

    def __init__(self, courseCode, courseName, creditHours, level, description, lecturer):
        if level not in (CORE, ELECTIVE):
            raise ValueError("Level must be 'Core' or 'Elective'.")
        self.courseCode = courseCode
        self.courseName = courseName
        self.creditHours = creditHours
        self.level = level
        self.description = description
        self.lecturer = lecturer

    def display_info(self):
        """Full details, ignoring the level (mandatory feature)."""
        print("Course Code:", self.courseCode)
        print("Course Name:", self.courseName)
        print("Credit Hours:", self.creditHours)
        print("Level:", self.level)
        print("Description:", self.description)
        print("Lecturer:", self.lecturer)

    def display_profile(self):
        """Public profile (advanced feature): electives show only the name,
        core courses show everything."""
        if self.level == CORE:
            self.display_info()
        else:
            print("Course Name:", self.courseName)
            print("(Elective course - other details are hidden)")
