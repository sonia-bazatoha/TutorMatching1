from django.core.management.base import BaseCommand
from tutoring.models import Programme, AcademicYear, Semester, Subject


class Command(BaseCommand):
    help = 'Populate subjects from Cavendish University timetable'

    def handle(self, *args, **kwargs):

        # Create programmes
        programmes = {
            'BCS': Programme.objects.get_or_create(code='BCS', defaults={'name': 'Bachelor of Computer Science'})[0],
            'BSE': Programme.objects.get_or_create(code='BSE', defaults={'name': 'Bachelor of Software Engineering'})[0],
            'BDS': Programme.objects.get_or_create(code='BDS', defaults={'name': 'Bachelor of Data Science'})[0],
            'BIT': Programme.objects.get_or_create(code='BIT', defaults={'name': 'Bachelor of Information Technology'})[0],
            'DIT': Programme.objects.get_or_create(code='DIT', defaults={'name': 'Diploma in Information Technology'})[0],
        }

        # Create years and semesters
        years = {i: AcademicYear.objects.get_or_create(number=i)[0] for i in range(1, 5)}
        semesters = {i: Semester.objects.get_or_create(number=i)[0] for i in range(1, 3)}

        # Subject data: (code, name, programme_code, year_number, semester_number)
        subjects = [

            # BCS Year 1 Semester 1
            ('BIT111', 'Discrete Mathematics', 'BCS', 1, 1),
            ('BBA116', 'Basic Statistics', 'BCS', 1, 1),
            ('BJC110', 'Communication Skills and Learning Skills for Employability', 'BCS', 1, 1),
            ('COM113', 'Computer Architecture and Organisation', 'BCS', 1, 1),
            ('BIT110', 'Introduction to Information and Communication Technologies', 'BCS', 1, 1),
            ('COM111', 'Mathematics for Computing', 'BCS', 1, 1),

            # BCS Year 1 Semester 2
            ('BIT212', 'Systems Analysis and Design', 'BCS', 1, 2),
            ('BIT122', 'Internet and Web Programming I', 'BCS', 1, 2),
            ('COM122', 'Principles of Programming', 'BCS', 1, 2),
            ('BIT124', 'E-Commerce', 'BCS', 1, 2),
            ('COM123', 'Numerical Analysis and Computation', 'BCS', 1, 2),

            # BCS Year 2 Semester 1
            ('COM321', 'Simulation and Modeling', 'BCS', 2, 1),
            ('COM211', 'Object Oriented Programming', 'BCS', 2, 1),
            ('BIT121', 'Database Development and Management I', 'BCS', 2, 1),
            ('BIT213', 'Internet and Web Programming II', 'BCS', 2, 1),
            ('COM212', 'Data Structures and Algorithms', 'BCS', 2, 1),
            ('BIT214', 'Computer Networks and Data Communications', 'BCS', 2, 1),

            # BCS Year 2 Semester 2
            ('COM221', 'Operating Systems Principles', 'BCS', 2, 2),
            ('COM224', 'Software Engineering Principles', 'BCS', 2, 2),
            ('BIT215', 'Database Development and Management II', 'BCS', 2, 2),
            ('BSE224', 'Python Programming', 'BCS', 2, 2),
            ('BIT222', 'Research Methodology in Computing', 'BCS', 2, 2),
            ('BIS313', 'Business Systems Modeling', 'BCS', 2, 2),
            ('BSE412', 'Embedded Systems Design', 'BCS', 2, 2),

            # BCS Year 3 Semester 1
            ('COM312', 'Artificial Intelligence and Expert Systems', 'BCS', 3, 1),
            ('BIT311', 'ICT Project Planning and Management', 'BCS', 3, 1),
            ('COM323', 'Computer Graphics', 'BCS', 3, 1),
            ('COM311', 'Compiler Design', 'BCS', 3, 1),
            ('BIT312', 'Mobile Application Development', 'BCS', 3, 1),
            ('BIT314', 'Network Configuration and Management', 'BCS', 3, 1),

            # BCS Year 3 Semester 2
            ('BIT321', 'Professional Issues in Computing', 'BCS', 3, 2),
            ('COM324', 'Machine Learning', 'BCS', 3, 2),
            ('BBA214', 'Entrepreneurship and Small Business Management', 'BCS', 3, 2),
            ('BIT225', 'Emerging Trends in Computer Science', 'BCS', 3, 2),
            ('BIT324', 'Network and Information Security', 'BCS', 3, 2),

            # BSE Year 1 Semester 1
            ('BIT111', 'Discrete Mathematics', 'BSE', 1, 1),
            ('BSE111', 'Calculus for Software Engineering', 'BSE', 1, 1),
            ('BIT110', 'Introduction to Information and Communication Technologies', 'BSE', 1, 1),
            ('BJC110', 'Communication Skills and Learning Skills for Employability', 'BSE', 1, 1),
            ('COM113', 'Computer Architecture and Organisation', 'BSE', 1, 1),

            # BSE Year 1 Semester 2
            ('BIT212', 'System Analysis and Design', 'BSE', 1, 2),
            ('BIT122', 'Internet and Web Programming', 'BSE', 1, 2),
            ('BIT121', 'Fundamentals of Database Systems', 'BSE', 1, 2),
            ('COM122', 'Principles of Programming', 'BSE', 1, 2),
            ('COM123', 'Numerical Analysis and Computation', 'BSE', 1, 2),

            # BSE Year 2 Semester 1
            ('COM221', 'Operating Systems Principles', 'BSE', 2, 1),
            ('COM224', 'Principles of Software Engineering', 'BSE', 2, 1),
            ('COM211', 'Object Oriented Programming', 'BSE', 2, 1),
            ('BIT215', 'Advanced Database Systems', 'BSE', 2, 1),
            ('COM212', 'Data Structures and Algorithms', 'BSE', 2, 1),
            ('BIT214', 'Computer Networks and Data Communications', 'BSE', 2, 1),

            # BSE Year 2 Semester 2
            ('BSE222', 'Advanced Object Oriented Programming', 'BSE', 2, 2),
            ('BSE224', 'Python Programming', 'BSE', 2, 2),
            ('COM224', 'Software Requirements Engineering', 'BSE', 2, 2),
            ('BIT213', 'Advanced Internet and Web Programming', 'BSE', 2, 2),
            ('BSE221', 'Formal Methods in Software Engineering', 'BSE', 2, 2),
            ('BIT222', 'Research Methodology in Computing', 'BSE', 2, 2),

            # BSE Year 3 Semester 1
            ('COM312', 'Artificial Intelligence and Expert Systems', 'BSE', 3, 1),
            ('BSE314', 'Internet of Things', 'BSE', 3, 1),
            ('COM311', 'Compiler Design', 'BSE', 3, 1),
            ('BIT124', 'E-Commerce', 'BSE', 3, 1),
            ('BIT312', 'Mobile Applications Development', 'BSE', 3, 1),
            ('BIT314', 'Network Configuration and Management', 'BSE', 3, 1),

            # BSE Year 3 Semester 2
            ('COM321', 'Simulation and Modelling', 'BSE', 3, 2),
            ('COM324', 'Machine Learning', 'BSE', 3, 2),
            ('BSE326', 'Software Evolution', 'BSE', 3, 2),
            ('BSE327', 'Advanced Mobile Applications Development', 'BSE', 3, 2),
            ('BIT323', 'User Interface Design', 'BSE', 3, 2),

            # BSE Year 4 Semester 1
            ('BSE323', 'Software Architecture and Patterns', 'BSE', 4, 1),
            ('BSE321', 'Software Metrics', 'BSE', 4, 1),
            ('BBA214', 'Entrepreneurship and Small Business Management', 'BSE', 4, 1),
            ('BSE411', 'Software Quality Assurance and Testing', 'BSE', 4, 1),
            ('BSE414', 'Computer Games Development', 'BSE', 4, 1),
            ('BSE412', 'Embedded Systems Development', 'BSE', 4, 1),

            # BSE Year 4 Semester 2
            ('BIT311', 'Managing Software Engineering Projects', 'BSE', 4, 2),
            ('BIT321', 'Software Engineering Ethics', 'BSE', 4, 2),
            ('BSE417', 'Network Application Development', 'BSE', 4, 2),
            ('BSE426', 'Software Security', 'BSE', 4, 2),

            # BDS Year 1 Semester 1
            ('DDA1106', 'Digital Electronics', 'BDS', 1, 1),
            ('BIT111', 'Discrete Mathematics', 'BDS', 1, 1),
            ('BSE111', 'Calculus for Software Engineering', 'BDS', 1, 1),
            ('BBA116', 'Basic Statistics', 'BDS', 1, 1),
            ('BJC110', 'Communication Skills and Learning Skills for Employability', 'BDS', 1, 1),
            ('BSE224', 'Python Engineering', 'BDS', 1, 1),
            ('BIT110', 'Introduction to Information and Communication Technologies', 'BDS', 1, 1),

            # BDS Year 1 Semester 2
            ('BDA1201', 'Design Thinking', 'BDS', 1, 2),
            ('COM123', 'Numerical Analysis and Computation', 'BDS', 1, 2),
            ('BIT214', 'Computer Networks and Data Communications', 'BDS', 1, 2),
            ('BDA1202', 'R Programming', 'BDS', 1, 2),
            ('BIT122', 'Internet and Web Programming', 'BDS', 1, 2),
            ('COM211', 'Object Oriented Programming', 'BDS', 1, 2),

            # BDS Year 2 Semester 1
            ('BIT121', 'Data Development and Management', 'BDS', 2, 1),
            ('BDA2101', 'Data Ethics', 'BDS', 2, 1),
            ('COM221', 'Operating Systems', 'BDS', 2, 1),
            ('BSE314', 'Internet of Things', 'BDS', 2, 1),
            ('BDA2102', 'Data Wrangling', 'BDS', 2, 1),
            ('COM212', 'Data Structures and Algorithms', 'BDS', 2, 1),
            ('BDA2104', 'ASP.NET and C#', 'BDS', 2, 1),

            # BDS Year 2 Semester 2
            ('BDA2202', 'Front End Development', 'BDS', 2, 2),
            ('BSE222', 'Advanced Object-Oriented Programming', 'BDS', 2, 2),
            ('BDA2201', 'Microprocessor and Microcontroller', 'BDS', 2, 2),
            ('BIT222', 'Research Methodology in Computing', 'BDS', 2, 2),
            ('COM321', 'Simulation and Modelling', 'BDS', 2, 2),
            ('DDA2201', 'Analysis and Visualization', 'BDS', 2, 2),

            # BIT Year 1 Semester 1
            ('BIT111', 'Discrete Mathematics', 'BIT', 1, 1),
            ('BBA116', 'Basic Statistics', 'BIT', 1, 1),
            ('BJC110', 'Communication Skills and Learning Skills for Employability', 'BIT', 1, 1),
            ('BIT113', 'Fundamentals of Information Systems', 'BIT', 1, 1),
            ('BIT110', 'Introduction to Information and Communication Technologies', 'BIT', 1, 1),

            # BIT Year 1 Semester 2
            ('BIT122', 'Internet Technology and Web Design', 'BIT', 1, 2),
            ('BIT123', 'Computer Applications', 'BIT', 1, 2),
            ('BIT121', 'Database Development and Management I', 'BIT', 1, 2),
            ('COM122', 'Principles of Programming', 'BIT', 1, 2),
            ('BIT125', 'Information Systems Management', 'BIT', 1, 2),
            ('BIT124', 'E-Commerce', 'BIT', 1, 2),

            # BIT Year 2 Semester 1
            ('BIT212', 'Systems Analysis and Design', 'BIT', 2, 1),
            ('COM211', 'Object Oriented Programming', 'BIT', 2, 1),
            ('BIT215', 'Database Development and Management II', 'BIT', 2, 1),
            ('BBA214', 'Entrepreneurship and Small Business Management', 'BIT', 2, 1),
            ('BIT213', 'Web Development and Management', 'BIT', 2, 1),
            ('BIT214', 'Computer Networks and Data Communications', 'BIT', 2, 1),

            # BIT Year 2 Semester 2
            ('COM221', 'Operating Systems Principles', 'BIT', 2, 2),
            ('COM224', 'Software Engineering Principles', 'BIT', 2, 2),
            ('BIT225', 'Emerging Trends in Information Technology', 'BIT', 2, 2),
            ('BIT223', 'Computer Repair and Maintenance', 'BIT', 2, 2),
            ('BIT222', 'Research Methodology in Computing', 'BIT', 2, 2),

            # BIT Year 3 Semester 1
            ('BIT311', 'ICT Project Planning and Management', 'BIT', 3, 1),
            ('BIS313', 'Business Systems Modelling', 'BIT', 3, 1),
            ('BIT315', 'Multimedia Systems', 'BIT', 3, 1),
            ('BIT312', 'Mobile Application Development', 'BIT', 3, 1),
            ('BIT314', 'Network Configuration and Management', 'BIT', 3, 1),

            # BIT Year 3 Semester 2
            ('BIT321', 'Professional Issues in Computing', 'BIT', 3, 2),
            ('BIT325', 'Information Systems Audit', 'BIT', 3, 2),
            ('BIT322', 'Distributed System Development', 'BIT', 3, 2),
            ('BIT324', 'Network and Information Security', 'BIT', 3, 2),
            ('BIT323', 'User Interface Design', 'BIT', 3, 2),

            # DIT Year 1 Semester 1
            ('DCS112', 'Introduction to Operating Systems', 'DIT', 1, 1),
            ('BJC110', 'Communication Skills and Learning Skills for Employability', 'DIT', 1, 1),
            ('BIT113', 'Fundamentals of Information Systems', 'DIT', 1, 1),
            ('BIT110', 'Introduction to Information and Communication Technologies', 'DIT', 1, 1),
            ('DCS111', 'Fundamentals of Mathematics', 'DIT', 1, 1),

            # DIT Year 1 Semester 2
            ('BIT123', 'Computer Applications', 'DIT', 1, 2),
            ('BIT121', 'Introduction to Database Systems', 'DIT', 1, 2),
            ('BIT122', 'Internet Technology and Web Design', 'DIT', 1, 2),
            ('COM113', 'Computer Architecture and Organisation', 'DIT', 1, 2),
            ('COM122', 'Programming Principles', 'DIT', 1, 2),

            # DIT Year 2 Semester 1
            ('BIT212', 'Systems Analysis and Design', 'DIT', 2, 1),
            ('BIT225', 'Emerging Trends in Information Technology', 'DIT', 2, 1),
            ('BIT124', 'E-Commerce', 'DIT', 2, 1),
            ('BIT213', 'Dynamic Website Development', 'DIT', 2, 1),
            ('BIT223', 'Computer Assembly, Repair and Maintenance', 'DIT', 2, 1),

            # DIT Year 2 Semester 2
            ('BIT321', 'Professional Issues in Computing', 'DIT', 2, 2),
            ('BIT215', 'Database Development and Administration', 'DIT', 2, 2),
            ('BIT315', 'Introduction to Multimedia Systems', 'DIT', 2, 2),
            ('BIT214', 'PC Network and Data Communication', 'DIT', 2, 2),
            ('BIT222', 'Research Methodology in Computing', 'DIT', 2, 2),
        ]

        created = 0
        for code, name, prog_code, year_num, sem_num in subjects:
            prog = programmes[prog_code]
            year = years[year_num]
            sem = semesters[sem_num]
            _, was_created = Subject.objects.get_or_create(
                code=code,
                programme=prog,
                year=year,
                semester=sem,
                defaults={'name': name},
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f'Done. {created} subjects created.'))