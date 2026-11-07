"""
main.py - Menu-driven University Course Prerequisite System.

Graph direction: an edge  A -> B  means "A is a prerequisite of B".
    prerequisites of B     = incoming edges of B
    courses unlocked by A  = outgoing edges of A
"""

from course import Course, CORE, ELECTIVE
from graph import Graph


def build_sample_system():
    courses = {c.courseCode: c for c in [
        Course("CS101", "Programming Fundamentals", 3, CORE, "Introduction to programming concepts.", "Mr. Adam"),
        Course("CS102", "Data Structures", 4, CORE, "Study of data structures and algorithms.", "Ms. Sarah"),
        Course("CS103", "Algorithms", 3, CORE, "Introduction to algorithm design.", "Mr. Daniel"),
        Course("CS104", "Database Systems", 3, ELECTIVE, "Introduction to database management.", "Ms. Emily"),
        Course("CS105", "Software Engineering", 3, CORE, "Software development principles and practices.", "Mr. John"),
        Course("CS106", "Discrete Mathematics", 3, CORE, "Logic, sets, graphs and proofs.", "Dr. Lee"),
        Course("CS107", "Machine Learning", 3, ELECTIVE, "Introduction to learning from data.", "Dr. Tan"),
    ]}
    graph = Graph()
    for code in courses:
        graph.addVertex(code)
    for prerequisite, course in [
        ("CS101", "CS102"), ("CS101", "CS104"), ("CS102", "CS103"),
        ("CS106", "CS103"),                      # Algorithms needs two courses
        ("CS102", "CS105"), ("CS103", "CS107"), ("CS106", "CS107"),
    ]:
        graph.addEdge(prerequisite, course)
    return courses, graph


def ask_course_code(courses, prompt="Enter course code: "):
    """Ask for a course code; return it if it exists, otherwise None."""
    code = input(prompt).strip().upper()
    if code not in courses:
        print("Course not found.")
        return None
    return code


def label(courses, code):
    return f"{code} ({courses[code].courseName})"


# ------------------------------------------------------- mandatory features
def display_courses(courses):
    print("\nAVAILABLE COURSES")
    for course in courses.values():
        print(f"{course.courseCode} - {course.courseName}")


def view_course_details(courses):
    code = ask_course_code(courses)
    if code:
        print()
        courses[code].display_info()


def view_prerequisites(courses, graph):
    code = ask_course_code(courses)
    if not code:
        return
    prerequisites = graph.listIncomingAdjacentVertex(code)
    print(f"\nPREREQUISITES FOR {label(courses, code)}")
    if prerequisites:
        for p in prerequisites:
            print("-", label(courses, p))
    else:
        print("This course has no prerequisites.")


def view_unlocked_courses(courses, graph):
    code = ask_course_code(courses)
    if not code:
        return
    unlocked = graph.listOutgoingAdjacentVertex(code)
    print(f"\nCOURSES UNLOCKED BY {label(courses, code)}")
    if unlocked:
        for u in unlocked:
            print("-", label(courses, u))
    else:
        print("This course does not unlock any other courses.")


# ------------------------------------------------------- advanced features
def add_prerequisite(courses, graph):
    course = ask_course_code(courses, "Enter the course that needs a prerequisite: ")
    if not course:
        return
    prerequisite = ask_course_code(courses, "Enter the prerequisite course code: ")
    if not prerequisite:
        return
    if course == prerequisite:
        print("A course cannot be its own prerequisite.")
    elif graph.hasEdge(prerequisite, course):
        print("This prerequisite already exists.")
    elif graph.hasPath(course, prerequisite):
        # course already (directly or indirectly) leads to prerequisite,
        # so the new edge would create a circular dependency.
        print("Rejected: this would create a circular prerequisite.")
    else:
        graph.addEdge(prerequisite, course)
        print("Prerequisite added successfully!")
        print(f"{courses[prerequisite].courseName} is now a prerequisite for "
              f"{courses[course].courseName}")


def remove_prerequisite(courses, graph):
    course = ask_course_code(courses, "Enter the course to remove a prerequisite from: ")
    if not course:
        return
    prerequisite = ask_course_code(courses, "Enter the prerequisite course code to remove: ")
    if not prerequisite:
        return
    if graph.removeEdge(prerequisite, course):
        print("Prerequisite removed successfully!")
    else:
        print(f"{prerequisite} is not a prerequisite of {course}.")


def add_course(courses, graph):
    code = input("Enter new course code: ").strip().upper()
    if not code:
        print("Course code cannot be empty.")
        return
    if code in courses:
        print("Course code already exists.")
        return
    name = input("Enter course name: ").strip()
    try:
        hours = int(input("Enter credit hours: "))
        if hours <= 0:
            raise ValueError
    except ValueError:
        print("Credit hours must be a positive whole number.")
        return
    level = input("Enter level (Core/Elective): ").strip().capitalize()
    if level not in (CORE, ELECTIVE):
        print("Level must be Core or Elective.")
        return
    description = input("Enter description: ").strip()
    lecturer = input("Enter lecturer: ").strip()

    courses[code] = Course(code, name, hours, level, description, lecturer)
    graph.addVertex(code)
    print(f"Course {code} added successfully!")


def view_profile(courses):
    code = ask_course_code(courses)
    if code:
        print()
        courses[code].display_profile()


# ---------------------------------------------------------------- main menu
def main():
    courses, graph = build_sample_system()
    actions = {
        "1": lambda: display_courses(courses),
        "2": lambda: view_course_details(courses),
        "3": lambda: view_prerequisites(courses, graph),
        "4": lambda: view_unlocked_courses(courses, graph),
        "5": lambda: add_prerequisite(courses, graph),
        "6": lambda: remove_prerequisite(courses, graph),
        "7": lambda: add_course(courses, graph),
        "8": lambda: view_profile(courses),
    }
    while True:
        print("\n===== UNIVERSITY COURSE SYSTEM =====")
        print("1. Display all courses")
        print("2. View course details")
        print("3. View course prerequisites")
        print("4. View courses unlocked")
        print("5. Add prerequisite")
        print("6. Remove prerequisite")
        print("7. Add new course")
        print("8. View course profile (electives hidden)")
        print("9. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "9":
            print("Exiting program. Goodbye!")
            break
        action = actions.get(choice)
        action() if action else print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
