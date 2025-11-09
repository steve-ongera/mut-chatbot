"""
Django management command to seed the database with Murang'a University data
Place this file in: your_app/management/commands/seed_data.py
Run with: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
import uuid

from mut_chatgpt.models import (
    KnowledgeCategory, KnowledgeBase, FinancialInformation, BankAccount,
    ExamInformation, AcademicYear, Discontinuation, UniversityOfficial,
    OfficeLocation, FAQ, Announcement, SystemSettings
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with Murang\'a University data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            self.clear_data()

        self.stdout.write(self.style.SUCCESS('Starting data seeding...'))
        
        # Seed in order of dependencies
        self.seed_system_settings()
        self.seed_users()
        self.seed_knowledge_categories()
        self.seed_bank_accounts()
        self.seed_financial_information()
        self.seed_academic_years()
        self.seed_exam_information()
        self.seed_discontinuation()
        self.seed_university_officials()
        self.seed_office_locations()
        self.seed_knowledge_base()
        self.seed_faqs()
        self.seed_announcements()
        
        self.stdout.write(self.style.SUCCESS('✅ Database seeding completed successfully!'))

    def clear_data(self):
        """Clear existing data"""
        models = [
            Announcement, FAQ, KnowledgeBase, OfficeLocation, UniversityOfficial,
            Discontinuation, ExamInformation, AcademicYear, FinancialInformation,
            BankAccount, KnowledgeCategory, SystemSettings
        ]
        
        for model in models:
            count = model.objects.count()
            model.objects.all().delete()
            self.stdout.write(f'  Deleted {count} {model.__name__} records')

    def seed_system_settings(self):
        """Seed system settings"""
        self.stdout.write('Seeding system settings...')
        
        settings = [
            {
                'key': 'ANTHROPIC_API_KEY',
                'value': 'your-api-key-here',
                'description': 'Anthropic Claude API key for AI responses'
            },
            {
                'key': 'UNIVERSITY_NAME',
                'value': 'Murang\'a University of Technology',
                'description': 'Official university name'
            },
            {
                'key': 'UNIVERSITY_ACRONYM',
                'value': 'MUT',
                'description': 'University acronym'
            },
            {
                'key': 'SUPPORT_EMAIL',
                'value': 'support@mut.ac.ke',
                'description': 'Support email address'
            },
            {
                'key': 'SUPPORT_PHONE',
                'value': '+254 712 345 678',
                'description': 'Support phone number'
            },
        ]
        
        for setting_data in settings:
            SystemSettings.objects.update_or_create(
                key=setting_data['key'],
                defaults=setting_data
            )
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {len(settings)} system settings'))

    def seed_users(self):
        """Seed test users"""
        self.stdout.write('Seeding users...')
        
        users_data = [
            {
                'username': 'admin',
                'email': 'admin@mut.ac.ke',
                'password': 'admin123',
                'user_type': 'admin',
                'is_staff': True,
                'is_superuser': True
            },
            {
                'username': 'john.doe',
                'email': 'john.doe@student.mut.ac.ke',
                'password': 'student123',
                'user_type': 'student',
                'student_id': 'MUT/01/2021/001',
                'department': 'Computer Science',
                'year_of_study': 3,
                'phone_number': '+254 712 345 001'
            },
            {
                'username': 'jane.smith',
                'email': 'jane.smith@student.mut.ac.ke',
                'password': 'student123',
                'user_type': 'student',
                'student_id': 'MUT/01/2022/002',
                'department': 'Business IT',
                'year_of_study': 2,
                'phone_number': '+254 712 345 002'
            },
            {
                'username': 'staff.member',
                'email': 'staff@mut.ac.ke',
                'password': 'staff123',
                'user_type': 'staff',
                'department': 'ICT Department',
                'phone_number': '+254 712 345 100'
            },
        ]
        
        created_count = 0
        for user_data in users_data:
            password = user_data.pop('password')
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(**user_data)
                user.set_password(password)
                user.save()
                created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {created_count} users'))

    def seed_knowledge_categories(self):
        """Seed knowledge categories"""
        self.stdout.write('Seeding knowledge categories...')
        
        categories = [
            {'name': 'Admissions', 'slug': 'admissions', 'icon': 'fa-graduation-cap', 'order': 1},
            {'name': 'Fees & Payments', 'slug': 'fees-payments', 'icon': 'fa-money-bill-wave', 'order': 2},
            {'name': 'Academic Information', 'slug': 'academic', 'icon': 'fa-book', 'order': 3},
            {'name': 'Examinations', 'slug': 'examinations', 'icon': 'fa-file-alt', 'order': 4},
            {'name': 'Student Services', 'slug': 'student-services', 'icon': 'fa-users', 'order': 5},
            {'name': 'Campus Life', 'slug': 'campus-life', 'icon': 'fa-home', 'order': 6},
            {'name': 'Library', 'slug': 'library', 'icon': 'fa-book-open', 'order': 7},
            {'name': 'IT Services', 'slug': 'it-services', 'icon': 'fa-laptop', 'order': 8},
            {'name': 'Administration', 'slug': 'administration', 'icon': 'fa-building', 'order': 9},
            {'name': 'General Information', 'slug': 'general', 'icon': 'fa-info-circle', 'order': 10},
        ]
        
        for cat_data in categories:
            KnowledgeCategory.objects.update_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {len(categories)} categories'))

    def seed_bank_accounts(self):
        """Seed bank account information"""
        self.stdout.write('Seeding bank accounts...')
        
        accounts = [
            {
                'account_type': 'fees',
                'bank_name': 'Equity Bank',
                'account_name': 'Murang\'a University of Technology',
                'account_number': '0360291234567',
                'branch': 'Murang\'a Branch',
                'swift_code': 'EQBLKENA',
                'paybill_number': '247247',
                'account_reference': 'Student ID',
                'notes': 'Use your Student ID as the account number when paying via M-Pesa'
            },
            {
                'account_type': 'accommodation',
                'bank_name': 'Co-operative Bank',
                'account_name': 'MUT Accommodation Account',
                'account_number': '01129123456789',
                'branch': 'Murang\'a Branch',
                'swift_code': 'KCOOKENA',
                'paybill_number': '400200',
                'account_reference': 'Student ID + HOSTEL',
                'notes': 'For hostel and accommodation payments'
            },
            {
                'account_type': 'main',
                'bank_name': 'KCB Bank',
                'account_name': 'Murang\'a University of Technology',
                'account_number': '1234567890',
                'branch': 'Murang\'a Branch',
                'swift_code': 'KCBLKENX',
                'paybill_number': '',
                'account_reference': '',
                'notes': 'Main university account for general payments'
            },
        ]
        
        for acc_data in accounts:
            BankAccount.objects.update_or_create(
                account_number=acc_data['account_number'],
                defaults=acc_data
            )
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {len(accounts)} bank accounts'))

    def seed_financial_information(self):
        """Seed fee structure information"""
        self.stdout.write('Seeding financial information...')
        
        fees = [
            {
                'payment_type': 'tuition',
                'program': 'Bachelor of Science in Computer Science',
                'year_of_study': 1,
                'amount': 52000.00,
                'currency': 'KES',
                'description': 'Tuition fee per semester for Computer Science Year 1',
                'academic_year': '2024/2025'
            },
            {
                'payment_type': 'tuition',
                'program': 'Bachelor of Science in Computer Science',
                'year_of_study': 2,
                'amount': 52000.00,
                'currency': 'KES',
                'description': 'Tuition fee per semester for Computer Science Year 2',
                'academic_year': '2024/2025'
            },
            {
                'payment_type': 'tuition',
                'program': 'Bachelor of Business Information Technology',
                'year_of_study': 1,
                'amount': 48000.00,
                'currency': 'KES',
                'description': 'Tuition fee per semester for Business IT Year 1',
                'academic_year': '2024/2025'
            },
            {
                'payment_type': 'registration',
                'program': 'All Programs',
                'year_of_study': None,
                'amount': 5000.00,
                'currency': 'KES',
                'description': 'Annual registration fee for all programs',
                'academic_year': '2024/2025'
            },
            {
                'payment_type': 'exam',
                'program': 'All Programs',
                'year_of_study': None,
                'amount': 3000.00,
                'currency': 'KES',
                'description': 'Examination fee per semester',
                'academic_year': '2024/2025'
            },
            {
                'payment_type': 'accommodation',
                'program': 'All Programs',
                'year_of_study': None,
                'amount': 12000.00,
                'currency': 'KES',
                'description': 'Hostel accommodation per semester',
                'academic_year': '2024/2025'
            },
            {
                'payment_type': 'other',
                'program': 'All Programs',
                'year_of_study': None,
                'amount': 2000.00,
                'currency': 'KES',
                'description': 'Student ID card and other administrative charges',
                'academic_year': '2024/2025'
            },
        ]
        
        for fee_data in fees:
            FinancialInformation.objects.create(**fee_data)
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {len(fees)} fee structures'))

    def seed_academic_years(self):
        """Seed academic year information"""
        self.stdout.write('Seeding academic years...')
        
        current_year = datetime.now().year
        
        years = [
            {
                'year': f'{current_year}/{current_year + 1}',
                'start_date': datetime(current_year, 9, 1).date(),
                'end_date': datetime(current_year + 1, 8, 31).date(),
                'status': 'current',
                'registration_start': datetime(current_year, 8, 15).date(),
                'registration_end': datetime(current_year, 9, 15).date(),
                'semester_1_start': datetime(current_year, 9, 1).date(),
                'semester_1_end': datetime(current_year, 12, 20).date(),
                'semester_2_start': datetime(current_year + 1, 1, 10).date(),
                'semester_2_end': datetime(current_year + 1, 5, 15).date(),
            },
            {
                'year': f'{current_year + 1}/{current_year + 2}',
                'start_date': datetime(current_year + 1, 9, 1).date(),
                'end_date': datetime(current_year + 2, 8, 31).date(),
                'status': 'upcoming',
                'registration_start': datetime(current_year + 1, 8, 15).date(),
                'registration_end': datetime(current_year + 1, 9, 15).date(),
                'semester_1_start': datetime(current_year + 1, 9, 1).date(),
                'semester_1_end': datetime(current_year + 1, 12, 20).date(),
                'semester_2_start': datetime(current_year + 2, 1, 10).date(),
                'semester_2_end': datetime(current_year + 2, 5, 15).date(),
            },
        ]
        
        for year_data in years:
            AcademicYear.objects.update_or_create(
                year=year_data['year'],
                defaults=year_data
            )
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {len(years)} academic years'))

    def seed_exam_information(self):
        """Seed examination information"""
        self.stdout.write('Seeding exam information...')
        
        current_year = datetime.now().year
        
        exams = [
            {
                'exam_type': 'supplementary',
                'title': 'Supplementary Examinations - Semester 1',
                'description': 'Supplementary examinations for students who failed or missed regular exams',
                'academic_year': f'{current_year}/{current_year + 1}',
                'semester': 'Semester 1',
                'application_start_date': datetime(current_year, 1, 15).date(),
                'application_deadline': datetime(current_year, 2, 15).date(),
                'exam_start_date': datetime(current_year, 3, 1).date(),
                'exam_end_date': datetime(current_year, 3, 15).date(),
                'application_fee': 1500.00,
                'requirements': '''1. Must have sat for the regular examination
2. Valid student ID
3. Clear fee balance or payment plan
4. Duly filled supplementary exam application form''',
                'application_process': '''1. Log into the student portal
2. Navigate to Examinations > Supplementary Exams
3. Select the units you wish to sit for
4. Pay the application fee via M-Pesa or bank
5. Submit the application
6. Download your exam card from the portal
7. Attend the exam on scheduled date'''
            },
            {
                'exam_type': 'supplementary',
                'title': 'Supplementary Examinations - Semester 2',
                'description': 'Supplementary examinations for students who failed or missed regular exams',
                'academic_year': f'{current_year}/{current_year + 1}',
                'semester': 'Semester 2',
                'application_start_date': datetime(current_year, 8, 15).date(),
                'application_deadline': datetime(current_year, 9, 15).date(),
                'exam_start_date': datetime(current_year, 10, 1).date(),
                'exam_end_date': datetime(current_year, 10, 15).date(),
                'application_fee': 1500.00,
                'requirements': '''1. Must have sat for the regular examination
2. Valid student ID
3. Clear fee balance or payment plan
4. Duly filled supplementary exam application form''',
                'application_process': '''1. Log into the student portal
2. Navigate to Examinations > Supplementary Exams
3. Select the units you wish to sit for
4. Pay the application fee via M-Pesa or bank
5. Submit the application
6. Download your exam card from the portal
7. Attend the exam on scheduled date'''
            },
            {
                'exam_type': 'regular',
                'title': 'End of Semester Examinations - Semester 1',
                'description': 'Regular end of semester examinations for all students',
                'academic_year': f'{current_year}/{current_year + 1}',
                'semester': 'Semester 1',
                'application_start_date': None,
                'application_deadline': None,
                'exam_start_date': datetime(current_year, 12, 1).date(),
                'exam_end_date': datetime(current_year, 12, 20).date(),
                'application_fee': None,
                'requirements': '''1. Must be a registered student
2. Must have paid at least 60% of tuition fees
3. Valid student ID
4. Attendance of at least 75% of lectures''',
                'application_process': '''Regular exams are automatic for all registered students. 
Download your exam card from the student portal 2 weeks before exams begin.'''
            },
        ]
        
        for exam_data in exams:
            ExamInformation.objects.create(**exam_data)
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {len(exams)} exam records'))

    def seed_discontinuation(self):
        """Seed discontinuation information"""
        self.stdout.write('Seeding discontinuation information...')
        
        discontinuation = {
            'title': 'Student Discontinuation Procedures',
            'reason_types': '''Valid reasons for discontinuation include:
- Financial constraints
- Health issues
- Transfer to another institution
- Personal reasons
- Academic challenges
- Employment opportunities''',
            'process_steps': '''1. Download discontinuation form from student portal
2. Fill the form completely with all required details
3. Attach supporting documents (if applicable)
4. Get approval from:
   - Head of Department
   - Dean of School
   - Finance Department (fee clearance)
5. Submit to Academic Registrar's office
6. Collect discontinuation letter (processing takes 7-14 days)
7. Return student ID card and library books
8. Collect clearance certificate''',
            'required_documents': '''- Completed discontinuation form
- Copy of student ID
- Fee statement from Finance office
- Letter stating reasons for discontinuation
- Medical reports (if health-related)
- Acceptance letter from new institution (if transferring)
- Clearance form from library
- Clearance form from hostel (if applicable)''',
            'contact_office': 'Academic Registrar\'s Office',
            'contact_email': 'registrar@mut.ac.ke',
            'contact_phone': '+254 712 345 600',
            'fees_refund_policy': '''Refund Policy:
- Discontinuation before semester starts: 90% refund
- Discontinuation within first 4 weeks: 50% refund
- Discontinuation after 4 weeks: No refund
- Registration and exam fees are non-refundable
- Accommodation fees refunded on pro-rata basis
- Processing fee of KES 500 applies

Note: Refunds are processed within 60-90 days''',
            'timeline': '''Expected processing timeline:
- Form submission and verification: 2-3 days
- Departmental approval: 3-5 days
- Finance clearance: 3-7 days
- Final approval: 2-3 days
- Letter issuance: 1-2 days

Total estimated time: 7-14 working days''',
            'important_notes': '''Important things to note:
- Discontinuation is not the same as deferment
- You may reapply for admission in the future
- Transcripts can be requested after discontinuation
- Outstanding fees must be cleared or a payment plan established
- All university property must be returned
- Discontinuation does not affect your academic records
- You will need a clearance certificate for future applications'''
        }
        
        Discontinuation.objects.update_or_create(
            title=discontinuation['title'],
            defaults=discontinuation
        )
        
        self.stdout.write(self.style.SUCCESS('  ✓ Created discontinuation information'))

    def seed_university_officials(self):
        """Seed university officials"""
        self.stdout.write('Seeding university officials...')
        
        officials = [
            {
                'position': 'vc',
                'position_title': 'Vice Chancellor',
                'full_name': 'Prof. James Kinyua Mwaura',
                'department': 'Administration',
                'email': 'vc@mut.ac.ke',
                'phone': '+254 712 345 500',
                'office_location': 'Administration Block, 3rd Floor',
                'bio': 'Prof. Mwaura is an accomplished academician with over 20 years of experience in higher education. He holds a PhD in Engineering and has published extensively in international journals.',
                'order': 1
            },
            {
                'position': 'dvc_academic',
                'position_title': 'Deputy Vice Chancellor - Academic Affairs',
                'full_name': 'Prof. Mary Wanjiku Kamau',
                'department': 'Academic Affairs',
                'email': 'dvc.academic@mut.ac.ke',
                'phone': '+254 712 345 510',
                'office_location': 'Administration Block, 2nd Floor',
                'bio': 'Prof. Kamau oversees all academic programs and curriculum development at MUT.',
                'order': 2
            },
            {
                'position': 'dvc_admin',
                'position_title': 'Deputy Vice Chancellor - Administration & Finance',
                'full_name': 'Prof. David Kimani Njoroge',
                'department': 'Administration',
                'email': 'dvc.admin@mut.ac.ke',
                'phone': '+254 712 345 520',
                'office_location': 'Administration Block, 2nd Floor',
                'bio': 'Prof. Njoroge manages the administrative and financial operations of the university.',
                'order': 3
            },
            {
                'position': 'registrar',
                'position_title': 'Academic Registrar',
                'full_name': 'Dr. Sarah Muthoni Githinji',
                'department': 'Academic Registry',
                'email': 'registrar@mut.ac.ke',
                'phone': '+254 712 345 600',
                'office_location': 'Academic Block, Ground Floor',
                'bio': 'Dr. Githinji oversees student records, admissions, and academic administration.',
                'order': 4
            },
            {
                'position': 'dean',
                'position_title': 'Dean - School of Computing & IT',
                'full_name': 'Dr. Peter Kariuki Mwangi',
                'department': 'Computing & IT',
                'email': 'dean.computing@mut.ac.ke',
                'phone': '+254 712 345 700',
                'office_location': 'ICT Block, 1st Floor',
                'bio': 'Dr. Mwangi leads the School of Computing and IT with expertise in software engineering.',
                'order': 5
            },
            {
                'position': 'dean',
                'position_title': 'Dean - School of Business & Economics',
                'full_name': 'Dr. Agnes Nyambura Ndung\'u',
                'department': 'Business & Economics',
                'email': 'dean.business@mut.ac.ke',
                'phone': '+254 712 345 710',
                'office_location': 'Business Block, 2nd Floor',
                'bio': 'Dr. Ndung\'u oversees business and economics programs at MUT.',
                'order': 6
            },
            {
                'position': 'director',
                'position_title': 'Director - Student Affairs',
                'full_name': 'Mr. John Kamau Kiarie',
                'department': 'Student Affairs',
                'email': 'student.affairs@mut.ac.ke',
                'phone': '+254 712 345 800',
                'office_location': 'Student Center, Ground Floor',
                'bio': 'Mr. Kiarie manages student welfare, clubs, and co-curricular activities.',
                'order': 7
            },
            {
                'position': 'director',
                'position_title': 'Director - Finance',
                'full_name': 'Ms. Lucy Wanjiru Kimemia',
                'department': 'Finance',
                'email': 'finance@mut.ac.ke',
                'phone': '+254 712 345 650',
                'office_location': 'Administration Block, Ground Floor',
                'bio': 'Ms. Kimemia oversees all financial operations and student fee matters.',
                'order': 8
            },
        ]
        
        for official_data in officials:
            UniversityOfficial.objects.update_or_create(
                email=official_data['email'],
                defaults=official_data
            )
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {len(officials)} university officials'))

    def seed_office_locations(self):
        """Seed office locations"""
        self.stdout.write('Seeding office locations...')
        
        offices = [
            {
                'name': 'Finance Office',
                'office_type': 'financial',
                'building': 'Administration Block',
                'floor': 'Ground Floor',
                'room_number': 'A-G-12',
                'description': 'Handles all financial matters including fee payments, refunds, and financial statements',
                'services_offered': 'Fee payment processing, Fee statements, Payment plans, Refund processing, Financial clearance',
                'contact_person': 'Ms. Lucy Kimemia',
                'email': 'finance@mut.ac.ke',
                'phone': '+254 712 345 650',
                'opening_hours': 'Monday - Friday: 8:00 AM - 5:00 PM\nSaturday: 9:00 AM - 1:00 PM\nSunday & Public Holidays: Closed'
            },
            {
                'name': 'Academic Registrar\'s Office',
                'office_type': 'academic',
                'building': 'Academic Block',
                'floor': 'Ground Floor',
                'room_number': 'AC-G-01',
                'description': 'Handles student registration, transcripts, certificates, and academic records',
                'services_offered': 'Student registration, Transcripts, Certificates, Academic records, ID cards, Discontinuation',
                'contact_person': 'Dr. Sarah Githinji',
                'email': 'registrar@mut.ac.ke',
                'phone': '+254 712 345 600',
                'opening_hours': 'Monday - Friday: 8:00 AM - 5:00 PM\nLunch Break: 1:00 PM - 2:00 PM\nWeekends: Closed'
            },
            {
                'name': 'Examination Office',
                'office_type': 'academic',
                'building': 'Academic Block',
                'floor': 'Ground Floor',
                'room_number': 'AC-G-05',
                'description': 'Manages examination schedules, results, and supplementary exams',
                'services_offered': 'Exam registration, Exam cards, Supplementary exam applications, Results processing, Special exams',
                'contact_person': 'Mr. Thomas Ochieng',
                'email': 'exams@mut.ac.ke',
                'phone': '+254 712 345 620',
                'opening_hours': 'Monday - Friday: 8:00 AM - 5:00 PM\nWeekends: Closed'
            },
            {
                'name': 'Student Affairs Office',
                'office_type': 'student_services',
                'building': 'Student Center',
                'floor': 'Ground Floor',
                'room_number': 'SC-G-01',
                'description': 'Handles student welfare, clubs, sports, and co-curricular activities',
                'services_offered': 'Student welfare, Club registration, Sports activities, Counseling referrals, Event approvals',
                'contact_person': 'Mr. John Kiarie',
                'email': 'student.affairs@mut.ac.ke',
                'phone': '+254 712 345 800',
                'opening_hours': 'Monday - Friday: 8:00 AM - 5:00 PM\nSaturday: 9:00 AM - 1:00 PM'
            },
            {
                'name': 'ICT Support Desk',
                'office_type': 'it',
                'building': 'ICT Block',
                'floor': 'Ground Floor',
                'room_number': 'ICT-G-10',
                'description': 'Provides IT support for students and staff',
                'services_offered': 'Student portal issues, Email setup, Wi-Fi access, Computer lab support, Password resets',
                'contact_person': 'Mr. Kevin Mwangi',
                'email': 'ict.support@mut.ac.ke',
                'phone': '+254 712 345 900',
                'opening_hours': 'Monday - Friday: 7:30 AM - 7:00 PM\nSaturday: 8:00 AM - 4:00 PM\nSunday: Closed'
            },
            {
                'name': 'University Library',
                'office_type': 'library',
                'building': 'Library Building',
                'floor': 'All Floors',
                'room_number': 'LIB',
                'description': 'Main university library with extensive book collections and study spaces',
                'services_offered': 'Book borrowing, Research materials, Study spaces, Computer access, Printing services, Digital library',
                'contact_person': 'Ms. Grace Wambui',
                'email': 'library@mut.ac.ke',
                'phone': '+254 712 345 950',
                'opening_hours': 'Monday - Friday: 7:00 AM - 10:00 PM\nSaturday: 8:00 AM - 8:00 PM\nSunday: 10:00 AM - 6:00 PM'
            },
            {
                'name': 'Health Services',
                'office_type': 'health',
                'building': 'Medical Center',
                'floor': 'Ground Floor',
                'room_number': 'MC-G-01',
                'description': 'University health center providing basic medical services to students',
                'services_offered': 'First aid, Medical consultations, Prescriptions, Health insurance, Medical reports, Counseling',
                'contact_person': 'Dr. Elizabeth Njeri',
                'email': 'health@mut.ac.ke',
                'phone': '+254 712 345 850',
                'opening_hours': 'Monday - Friday: 8:00 AM - 5:00 PM\nEmergencies: 24/7\nWeekends: 9:00 AM - 1:00 PM'
            },
            {
                'name': 'Admissions Office',
                'office_type': 'academic',
                'building': 'Administration Block',
                'floor': '1st Floor',
                'room_number': 'A-1-15',
                'description': 'Handles new student admissions and application inquiries',
                'services_offered': 'Application processing, Admission letters, Course information, Entry requirements, Transfer applications',
                'contact_person': 'Mrs. Anne Wangari',
                'email': 'admissions@mut.ac.ke',
                'phone': '+254 712 345 550',
                'opening_hours': 'Monday - Friday: 8:00 AM - 5:00 PM\nWeekends: Closed'
            },
            {
                'name': 'Accommodation Office',
                'office_type': 'student_services',
                'building': 'Student Center',
                'floor': 'Ground Floor',
                'room_number': 'SC-G-08',
                'description': 'Manages student hostel allocation and accommodation matters',
                'services_offered': 'Hostel booking, Room allocation, Accommodation payments, Hostel transfers, Clearance',
                'contact_person': 'Mr. Patrick Omondi',
                'email': 'accommodation@mut.ac.ke',
                'phone': '+254 712 345 820',
                'opening_hours': 'Monday - Friday: 8:00 AM - 5:00 PM\nSaturday: 9:00 AM - 1:00 PM'
            },
            {
                'name': 'Career Services Office',
                'office_type': 'student_services',
                'building': 'Student Center',
                'floor': '1st Floor',
                'room_number': 'SC-1-10',
                'description': 'Provides career guidance, internship placement, and job opportunities',
                'services_offered': 'Career counseling, Internship placements, Job listings, CV writing workshops, Interview preparation',
                'contact_person': 'Ms. Betty Akinyi',
                'email': 'careers@mut.ac.ke',
                'phone': '+254 712 345 880',
                'opening_hours': 'Monday - Friday: 8:00 AM - 5:00 PM\nWeekends: Closed'
            },
        ]
        
        for office_data in offices:
            OfficeLocation.objects.update_or_create(
                name=office_data['name'],
                defaults=office_data
            )
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {len(offices)} office locations'))

    def seed_knowledge_base(self):
        """Seed knowledge base entries"""
        self.stdout.write('Seeding knowledge base...')
        
        # Get categories
        fees_cat = KnowledgeCategory.objects.get(slug='fees-payments')
        academic_cat = KnowledgeCategory.objects.get(slug='academic')
        exams_cat = KnowledgeCategory.objects.get(slug='examinations')
        services_cat = KnowledgeCategory.objects.get(slug='student-services')
        general_cat = KnowledgeCategory.objects.get(slug='general')
        
        knowledge_entries = [
            {
                'category': fees_cat,
                'title': 'How to Pay School Fees',
                'question': 'How do I pay my school fees?',
                'answer': '''You can pay your school fees through the following methods:

1. M-PESA:
   - Go to M-PESA menu
   - Select Lipa na M-PESA
   - Select Paybill
   - Enter Paybill Number: 247247
   - Account Number: Your Student ID
   - Enter Amount
   - Enter PIN and confirm

2. Bank Deposit:
   - Visit any Equity Bank branch
   - Deposit to Account: 0360291234567
   - Account Name: Murang'a University of Technology
   - Indicate your Student ID as reference

3. Online Banking:
   - Log into your bank's online platform
   - Select "Pay to Paybill"
   - Use the details above

4. Student Portal:
   - Log into the student portal
   - Navigate to Finance > Make Payment
   - Follow the instructions

Note: Always keep your payment receipts and allow 24-48 hours for payment confirmation.''',
                'keywords': 'pay fees, school fees, payment, mpesa, paybill, bank deposit',
                'priority': 100
            },
            {
                'category': fees_cat,
                'title': 'Fee Structure',
                'question': 'What are the fee structures for different programs?',
                'answer': '''Fee structures vary by program and year of study:

TUITION FEES PER SEMESTER:
- Computer Science: KES 52,000
- Business IT: KES 48,000
- Engineering Programs: KES 55,000
- Business Programs: KES 45,000

ADDITIONAL FEES:
- Registration Fee (Annual): KES 5,000
- Examination Fee (Per Semester): KES 3,000
- Student ID & Admin Charges: KES 2,000
- Accommodation (Per Semester): KES 12,000

PAYMENT TERMS:
- At least 60% of tuition must be paid before exams
- Payment plans available through Finance Office
- Fees are payable at the beginning of each semester

For detailed fee structure for your specific program, visit the Finance Office or check the student portal.''',
                'keywords': 'fee structure, tuition fees, cost, amount, how much',
                'priority': 95
            },
            {
                'category': exams_cat,
                'title': 'Supplementary Examinations',
                'question': 'How do I apply for supplementary exams?',
                'answer': '''To apply for supplementary examinations:

ELIGIBILITY:
- Must have sat for the regular exam
- Valid student ID
- Clear fee balance or approved payment plan

APPLICATION PROCESS:
1. Log into student portal
2. Go to Examinations > Supplementary Exams
3. Select units you want to retake
4. Pay application fee (KES 1,500 per unit)
5. Submit application
6. Download exam card

TIMELINE:
- Semester 1 Supplementary: March
- Semester 2 Supplementary: October
- Application opens 1 month before exams

PAYMENT:
- M-PESA Paybill: 247247
- Account: Your Student ID + SUP
- Amount: KES 1,500 per unit

Contact: exams@mut.ac.ke or visit Examination Office''',
                'keywords': 'supplementary exams, sup exams, retake, failed exam, special exam',
                'priority': 90
            },
            {
                'category': academic_cat,
                'title': 'Course Registration',
                'question': 'How do I register for courses?',
                'answer': '''Course registration is done online through the student portal:

STEPS:
1. Log into student portal using your credentials
2. Ensure fees are paid (at least 60%)
3. Navigate to Academic > Course Registration
4. Select your semester and year
5. Choose courses from the list
6. Verify course units (normal load: 15-18 units)
7. Submit registration
8. Download and print course registration form
9. Get HOD approval (if required)

REGISTRATION PERIOD:
- Opens 2 weeks before semester starts
- Closes 2 weeks after semester begins
- Late registration attracts penalty fee

IMPORTANT:
- Minimum units: 12
- Maximum units: 21 (requires Dean's approval)
- Prerequisites must be met
- Check timetable for course scheduling

Need help? Visit Academic Registrar's Office''',
                'keywords': 'course registration, register units, add courses, semester registration',
                'priority': 85
            },
            {
                'category': academic_cat,
                'title': 'Student Portal Access',
                'question': 'How do I access the student portal?',
                'answer': '''To access the MUT Student Portal:

PORTAL URL: portal.mut.ac.ke

LOGIN CREDENTIALS:
- Username: Your Student ID (e.g., MUT/01/2021/001)
- Password: Default is your ID number

FIRST TIME LOGIN:
1. Go to portal.mut.ac.ke
2. Enter your Student ID as username
3. Enter your ID number as password
4. You will be prompted to change password
5. Create a strong password
6. Set up security questions

FORGOT PASSWORD:
1. Click "Forgot Password" on login page
2. Enter Student ID and email
3. Check email for reset link
4. Follow instructions to reset

PORTAL FEATURES:
- Course registration
- Exam results
- Fee statements
- Exam cards
- Academic transcripts
- Timetables

ISSUES?
Contact ICT Support: ict.support@mut.ac.ke or +254 712 345 900''',
                'keywords': 'student portal, login, access portal, password, portal.mut.ac.ke',
                'priority': 88
            },
            {
                'category': services_cat,
                'title': 'Student ID Card',
                'question': 'How do I get my student ID card?',
                'answer': '''To obtain your student ID card:

NEW STUDENTS:
1. Complete registration process
2. Pay ID card fee (KES 500)
3. Visit ICT office with:
   - Receipt of payment
   - Admission letter
   - 2 passport photos
4. Photo capture (if needed)
5. Collect ID after 3-5 working days

REPLACEMENT (Lost/Damaged):
1. Report to Security office (get police abstract if lost outside campus)
2. Pay replacement fee (KES 1,000)
3. Visit ICT office with receipt
4. Bring 2 passport photos
5. Fill replacement form
6. Collect after 5-7 working days

ID CARD USES:
- Library access
- Exam identification
- Campus facility access
- Student discounts
- Official identification

IMPORTANT: Always carry your ID on campus. Report lost cards immediately.

Contact: ICT Support Desk, ICT Block Ground Floor''',
                'keywords': 'student id, id card, replacement id, lost id',
                'priority': 75
            },
            {
                'category': general_cat,
                'title': 'University Contacts',
                'question': 'What are the main university contacts?',
                'answer': '''MURANG'A UNIVERSITY OF TECHNOLOGY
Main Campus: Murang'a Town, Kenya

MAIN CONTACTS:
- Main Line: +254 712 345 500
- Email: info@mut.ac.ke
- Website: www.mut.ac.ke

KEY OFFICES:
- Vice Chancellor: vc@mut.ac.ke | +254 712 345 500
- Academic Registrar: registrar@mut.ac.ke | +254 712 345 600
- Finance Office: finance@mut.ac.ke | +254 712 345 650
- Admissions: admissions@mut.ac.ke | +254 712 345 550
- Examinations: exams@mut.ac.ke | +254 712 345 620
- ICT Support: ict.support@mut.ac.ke | +254 712 345 900
- Student Affairs: student.affairs@mut.ac.ke | +254 712 345 800
- Library: library@mut.ac.ke | +254 712 345 950
- Health Center: health@mut.ac.ke | +254 712 345 850

EMERGENCY:
- Security: +254 712 345 999
- Medical Emergency: +254 712 345 850

WORKING HOURS:
Monday - Friday: 8:00 AM - 5:00 PM
Saturday: 9:00 AM - 1:00 PM (Selected offices)''',
                'keywords': 'contacts, phone numbers, email addresses, reach university',
                'priority': 80
            },
            {
                'category': services_cat,
                'title': 'Accommodation Services',
                'question': 'How do I apply for university accommodation?',
                'answer': '''UNIVERSITY ACCOMMODATION APPLICATION:

HOSTELS AVAILABLE:
- Male Hostels: Block A, B, C
- Female Hostels: Block D, E, F
- Capacity: 2-4 students per room

FEES:
- KES 12,000 per semester
- Refundable deposit: KES 3,000

APPLICATION PROCESS:
1. Log into student portal
2. Go to Services > Accommodation
3. Select preferred hostel
4. Pay accommodation fee
5. Submit application
6. Await allocation (usually within 1 week)
7. Collect room keys from Accommodation Office

REQUIREMENTS:
- Must be a registered student
- Clear fee balance
- Valid student ID
- Sign hostel rules agreement

WHAT'S PROVIDED:
- Bed and mattress
- Study desk and chair
- Wardrobe
- 24/7 electricity
- Wi-Fi access
- Security

RULES:
- No visitors after 10 PM
- No cooking in rooms
- Maintain cleanliness
- No subletting

Contact: accommodation@mut.ac.ke | +254 712 345 820''',
                'keywords': 'hostel, accommodation, room, boarding, campus housing',
                'priority': 70
            },
            {
                'category': academic_cat,
                'title': 'Academic Transcripts',
                'question': 'How do I get my academic transcript?',
                'answer': '''TO REQUEST ACADEMIC TRANSCRIPT:

REQUIREMENTS:
- Completed transcript request form
- Copy of ID
- Fee clearance certificate
- Processing fee: KES 1,000 (per copy)

PROCESS:
1. Visit Academic Registrar's Office
2. Fill transcript request form
3. Get fee clearance from Finance
4. Pay processing fee
5. Submit all documents
6. Collect after 7-14 working days

PROVISIONAL TRANSCRIPT:
- Available immediately after graduation
- Free of charge
- Valid for 6 months

OFFICIAL TRANSCRIPT:
- Processed after 1 month of graduation
- Includes university seal and signatures
- Can be collected or mailed

DELIVERY OPTIONS:
- Self-collection: Free
- Courier within Kenya: KES 500
- International courier: KES 3,000

FOR URGENT PROCESSING:
- Additional fee: KES 2,000
- Ready in 3 working days

Contact: registrar@mut.ac.ke | +254 712 345 600''',
                'keywords': 'transcript, academic records, grades, documents',
                'priority': 65
            },
            {
                'category': general_cat,
                'title': 'University Location and Directions',
                'question': 'Where is Murang\'a University located?',
                'answer': '''MURANG'A UNIVERSITY OF TECHNOLOGY LOCATION:

ADDRESS:
Main Campus
Murang'a Town
Murang'a County, Kenya
P.O. Box 75-10200, Murang'a

GPS COORDINATES:
-0.7167° S, 37.1500° E

HOW TO GET THERE:

FROM NAIROBI:
- By Road: 80km via Thika-Murang'a Highway
- Travel time: 1.5 - 2 hours
- Matatu: Board at Muthurwa or Githurai (KES 150-200)
- By Car: Follow Thika Road to Murang'a

FROM THIKA:
- Distance: 40km
- Travel time: 45 minutes
- Matatu available (KES 100)

FROM NYERI:
- Distance: 55km via Karatina
- Travel time: 1 hour

LANDMARKS NEARBY:
- Murang'a County Headquarters (2km)
- Murang'a Level 5 Hospital (1km)
- Murang'a Stadium (500m)

ON CAMPUS:
- Main Gate on Murang'a-Nyeri Road
- Ample parking available
- Boda boda/taxi readily available

PUBLIC TRANSPORT:
Matatus from Nairobi drop at Murang'a Town
Campus is 10 minutes walk from town center''',
                'keywords': 'location, where is mut, directions, how to get, address',
                'priority': 60
            },
        ]
        
        for kb_data in knowledge_entries:
            KnowledgeBase.objects.create(**kb_data)
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {len(knowledge_entries)} knowledge base entries'))

    def seed_faqs(self):
        """Seed frequently asked questions"""
        self.stdout.write('Seeding FAQs...')
        
        # Get categories
        fees_cat = KnowledgeCategory.objects.get(slug='fees-payments')
        academic_cat = KnowledgeCategory.objects.get(slug='academic')
        exams_cat = KnowledgeCategory.objects.get(slug='examinations')
        admissions_cat = KnowledgeCategory.objects.get(slug='admissions')
        general_cat = KnowledgeCategory.objects.get(slug='general')
        
        faqs = [
            {
                'category': fees_cat,
                'question': 'Can I pay my fees in installments?',
                'answer': 'Yes, MUT offers a flexible payment plan. You must pay at least 60% of your tuition fees before sitting for examinations. Visit the Finance Office to arrange a payment plan. Contact: finance@mut.ac.ke',
                'order': 1,
                'is_featured': True
            },
            {
                'category': fees_cat,
                'question': 'What happens if I don\'t clear my fee balance?',
                'answer': 'If you have outstanding fees: 1) You cannot sit for examinations, 2) You cannot register for the next semester, 3) Your results will be withheld, 4) You cannot graduate. However, you can arrange a payment plan with the Finance Office.',
                'order': 2
            },
            {
                'category': fees_cat,
                'question': 'How long does it take for fee payment to reflect?',
                'answer': 'M-PESA and bank payments typically reflect within 24-48 hours. If your payment hasn\'t reflected after 48 hours, visit the Finance Office with your payment receipt.',
                'order': 3
            },
            {
                'category': academic_cat,
                'question': 'When does registration open each semester?',
                'answer': 'Course registration opens 2 weeks before the semester starts and closes 2 weeks after semester begins. Late registration attracts a penalty fee of KES 1,000. Check the academic calendar on the student portal for exact dates.',
                'order': 1,
                'is_featured': True
            },
            {
                'category': academic_cat,
                'question': 'How many units can I register for per semester?',
                'answer': 'Normal course load is 15-18 units per semester. Minimum is 12 units, maximum is 21 units. Taking more than 18 units requires approval from your Dean.',
                'order': 2
            },
            {
                'category': academic_cat,
                'question': 'Can I defer my studies?',
                'answer': 'Yes, you can defer for valid reasons (medical, financial, etc.). Submit a deferment application to the Academic Registrar with supporting documents. Maximum deferment period is usually 2 semesters.',
                'order': 3
            },
            {
                'category': exams_cat,
                'question': 'What is the minimum attendance required for exams?',
                'answer': 'You must attend at least 75% of all lectures to be eligible to sit for examinations. Lecturers submit attendance lists to the Examination Office.',
                'order': 1,
                'is_featured': True
            },
            {
                'category': exams_cat,
                'question': 'How do I get my exam card?',
                'answer': 'Exam cards are downloaded from the student portal 2 weeks before examinations begin. You must have paid at least 60% of your fees to access your exam card.',
                'order': 2
            },
            {
                'category': exams_cat,
                'question': 'When are exam results released?',
                'answer': 'Results are typically released 4-6 weeks after the examination period ends. You can view them on the student portal. Physical result slips can be collected from the Academic Registrar\'s Office.',
                'order': 3
            },
            {
                'category': admissions_cat,
                'question': 'What are the minimum entry requirements?',
                'answer': 'Minimum requirements: KCSE C+ (Plus) or equivalent. Specific programs have additional requirements. For diplomas: KCSE C- (Minus). Check the website or contact admissions@mut.ac.ke for detailed requirements.',
                'order': 1,
                'is_featured': True
            },
            {
                'category': admissions_cat,
                'question': 'When do applications open?',
                'answer': 'Applications for September intake open in March-May. January intake (if available) opens in September-November. Check www.mut.ac.ke for specific dates.',
                'order': 2
            },
            {
                'category': admissions_cat,
                'question': 'Can I transfer from another university?',
                'answer': 'Yes, transfers are accepted. Requirements: 1) Good academic standing, 2) Letter from current institution, 3) Transcripts, 4) Meet MUT\'s entry requirements. Contact admissions@mut.ac.ke',
                'order': 3
            },
            {
                'category': general_cat,
                'question': 'Is there Wi-Fi on campus?',
                'answer': 'Yes, free Wi-Fi is available across campus. Use your student portal credentials to connect. Network name: MUT-Student. For connection issues, contact ICT Support.',
                'order': 1
            },
            {
                'category': general_cat,
                'question': 'Are there computer labs available?',
                'answer': 'Yes, several computer labs are available in the ICT Block. Labs are open Monday-Friday: 7:00 AM - 9:00 PM, Saturday: 8:00 AM - 6:00 PM. Your student ID is required for access.',
                'order': 2
            },
            {
                'category': general_cat,
                'question': 'Does the university offer medical services?',
                'answer': 'Yes, the Health Center provides basic medical services Monday-Friday 8:00 AM - 5:00 PM. Emergency services available 24/7. Most services are free for registered students. Complex cases referred to Murang\'a Level 5 Hospital.',
                'order': 3
            },
        ]
        
        for faq_data in faqs:
            FAQ.objects.create(**faq_data)
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {len(faqs)} FAQs'))

    def seed_announcements(self):
        """Seed announcements"""
        self.stdout.write('Seeding announcements...')
        
        admin_user = User.objects.filter(is_staff=True).first()
        now = timezone.now()
        
        announcements = [
            {
                'title': 'Semester Registration Now Open',
                'content': '''Course registration for the current semester is now open.

All students are required to register their courses through the student portal by the deadline.

Important:
- Ensure fees are paid (minimum 60%)
- Register within the first 2 weeks
- Late registration attracts penalty

Visit the Academic Registrar for any issues.''',
                'priority': 'high',
                'target_audience': 'students',
                'start_date': now - timedelta(days=2),
                'end_date': now + timedelta(days=14),
                'created_by': admin_user
            },
            {
                'title': 'Supplementary Exam Applications',
                'content': '''Applications for supplementary examinations are now being accepted.

Application Deadline: Two weeks from today
Exam Fee: KES 1,500 per unit

Apply through the student portal under Examinations section.

For inquiries, contact the Examination Office.''',
                'priority': 'high',
                'target_audience': 'students',
                'start_date': now - timedelta(days=1),
                'end_date': now + timedelta(days=14),
                'created_by': admin_user
            },
            {
                'title': 'Library Extended Hours During Exam Period',
                'content': '''The university library will operate extended hours during the examination period:

Monday - Friday: 6:00 AM - 11:00 PM
Saturday - Sunday: 7:00 AM - 10:00 PM

Take advantage of the quiet study spaces and resources.

Remember to carry your student ID for access.''',
                'priority': 'medium',
                'target_audience': 'all',
                'start_date': now,
                'end_date': now + timedelta(days=30),
                'created_by': admin_user
            },
            {
                'title': 'Career Fair - Next Month',
                'content': '''MUT Career Fair 2025

Date: Next Month
Venue: University Grounds
Time: 9:00 AM - 5:00 PM

Meet with top employers, learn about internship opportunities, and get career guidance.

Over 50 companies confirmed!

Registration opens next week through the Career Services Office.''',
                'priority': 'medium',
                'target_audience': 'students',
                'start_date': now,
                'end_date': now + timedelta(days=45),
                'created_by': admin_user
            },
            {
                'title': 'New Student Orientation',
                'content': '''Calling all new students!

New Student Orientation Week begins next Monday.

Program includes:
- Campus tour
- Introduction to facilities
- Academic requirements briefing
- Student life activities
- Meet your lecturers

Attendance is mandatory. Check your email for detailed schedule.''',
                'priority': 'urgent',
                'target_audience': 'students',
                'start_date': now,
                'end_date': now + timedelta(days=7),
                'created_by': admin_user
            },
            {
                'title': 'Payment Deadline Reminder',
                'content': '''Reminder: Fee Payment Deadline

Date: End of this month

All students must clear at least 60% of their tuition fees to be eligible for examinations.

Payment Options:
- M-PESA Paybill: 247247
- Bank Deposit: Equity Bank
- Student Portal

Contact Finance Office for payment plans.''',
                'priority': 'high',
                'target_audience': 'students',
                'start_date': now - timedelta(days=10),
                'end_date': now + timedelta(days=20),
                'created_by': admin_user
            },
            {
                'title': 'ICT System Maintenance',
                'content': '''Scheduled System Maintenance

Date: This Saturday
Time: 11:00 PM - 5:00 AM Sunday

Services Affected:
- Student Portal
- Email
- Wi-Fi (may be intermittent)

Plan accordingly and download any materials you need beforehand.

We apologize for any inconvenience.''',
                'priority': 'medium',
                'target_audience': 'all',
                'start_date': now + timedelta(days=3),
                'end_date': now + timedelta(days=5),
                'created_by': admin_user
            },
        ]
        
        for announcement_data in announcements:
            Announcement.objects.create(**announcement_data)
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {len(announcements)} announcements'))