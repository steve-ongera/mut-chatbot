# MUT AI Database Seeding Guide

This guide explains how to populate your MUT AI database with realistic Murang'a University of Technology data.

## 📋 Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Seeded Data](#seeded-data)
- [Test Users](#test-users)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

The `seed_data` management command populates your database with comprehensive Murang'a University information including:

- ✅ System settings
- ✅ Test users (students, staff, admin)
- ✅ Knowledge base categories and entries
- ✅ Financial information and bank accounts
- ✅ Academic years and exam schedules
- ✅ University officials and office locations
- ✅ FAQs and announcements
- ✅ Discontinuation procedures

**No external dependencies required** - All data is hardcoded and realistic!

---

## 🚀 Installation

### Step 1: Create the Management Command Directory

```bash
mkdir -p your_app/management/commands
touch your_app/management/__init__.py
touch your_app/management/commands/__init__.py
```

### Step 2: Add the Seed Script

Place `seed_data.py` in:
```
your_app/
└── management/
    └── commands/
        └── seed_data.py
```

### Step 3: Update the Script

Open `seed_data.py` and update the import path on line 13:

```python
# Change this line:
from your_app.models import (...)

# To your actual app name, for example:
from chat.models import (...)
# or
from mutai.models import (...)
```

---

## 💻 Usage

### Basic Usage

Run the seed command:

```bash
python manage.py seed_data
```

### Clear Existing Data

To clear all existing data before seeding:

```bash
python manage.py seed_data --clear
```

⚠️ **Warning**: This will delete ALL data from the affected models!

### Expected Output

```
Seeding system settings...
  ✓ Created 5 system settings
Seeding users...
  ✓ Created 4 users
Seeding knowledge categories...
  ✓ Created 10 categories
Seeding bank accounts...
  ✓ Created 3 bank accounts
...
✅ Database seeding completed successfully!
```

---

## 📊 Seeded Data

### System Settings (5 records)

| Key | Value | Description |
|-----|-------|-------------|
| ANTHROPIC_API_KEY | your-api-key-here | API key for Claude AI |
| UNIVERSITY_NAME | Murang'a University of Technology | Official name |
| UNIVERSITY_ACRONYM | MUT | Short name |
| SUPPORT_EMAIL | support@mut.ac.ke | Support contact |
| SUPPORT_PHONE | +254 712 345 678 | Support phone |

**Post-Seeding Action**: Update `ANTHROPIC_API_KEY` with your actual API key:

```python
# In Django admin or shell
from your_app.models import SystemSettings
setting = SystemSettings.objects.get(key='ANTHROPIC_API_KEY')
setting.value = 'sk-ant-your-actual-key'
setting.save()
```

### Knowledge Categories (10 categories)

1. Admissions
2. Fees & Payments
3. Academic Information
4. Examinations
5. Student Services
6. Campus Life
7. Library
8. IT Services
9. Administration
10. General Information

### Bank Accounts (3 accounts)

| Type | Bank | Account Number | Paybill |
|------|------|----------------|---------|
| Fees | Equity Bank | 0360291234567 | 247247 |
| Accommodation | Co-operative Bank | 01129123456789 | 400200 |
| Main | KCB Bank | 1234567890 | - |

### Financial Information (7 fee structures)

Includes tuition fees for:
- Computer Science (KES 52,000/semester)
- Business IT (KES 48,000/semester)
- Registration fees (KES 5,000/year)
- Examination fees (KES 3,000/semester)
- Accommodation (KES 12,000/semester)

### University Officials (8 officials)

- Vice Chancellor: Prof. James Kinyua Mwaura
- DVC Academic: Prof. Mary Wanjiku Kamau
- DVC Admin: Prof. David Kimani Njoroge
- Academic Registrar: Dr. Sarah Muthoni Githinji
- Dean Computing: Dr. Peter Kariuki Mwangi
- Dean Business: Dr. Agnes Nyambura Ndung'u
- Director Student Affairs: Mr. John Kamau Kiarie
- Director Finance: Ms. Lucy Wanjiru Kimemia

### Office Locations (10 offices)

Including:
- Finance Office
- Academic Registrar's Office
- Examination Office
- Student Affairs Office
- ICT Support Desk
- University Library
- Health Services
- Admissions Office
- Accommodation Office
- Career Services Office

### Knowledge Base (10 comprehensive entries)

Topics covered:
- How to pay school fees
- Fee structures
- Supplementary examinations
- Course registration
- Student portal access
- Student ID cards
- University contacts
- Accommodation services
- Academic transcripts
- Location and directions

### FAQs (15 frequently asked questions)

Covering:
- Fee payment and installments
- Registration procedures
- Exam requirements
- Admission criteria
- Campus facilities
- Medical services

### Announcements (7 active announcements)

Including:
- Semester registration notices
- Exam schedules
- Library hours
- Career fair
- Payment deadlines
- System maintenance

---

## 👥 Test Users

### Admin User
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: admin@mut.ac.ke
- **Type**: Administrator (Full access)

### Student Users

#### Student 1
- **Username**: `john.doe`
- **Password**: `student123`
- **Email**: john.doe@student.mut.ac.ke
- **Student ID**: MUT/01/2021/001
- **Department**: Computer Science
- **Year**: 3

#### Student 2
- **Username**: `jane.smith`
- **Password**: `student123`
- **Email**: jane.smith@student.mut.ac.ke
- **Student ID**: MUT/01/2022/002
- **Department**: Business IT
- **Year**: 2

### Staff User
- **Username**: `staff.member`
- **Password**: `staff123`
- **Email**: staff@mut.ac.ke
- **Type**: Staff

### Testing the App

1. **Login as admin**:
   ```
   URL: http://localhost:8000/login/
   Username: admin
   Password: admin123
   ```

2. **Test student features**:
   ```
   Username: john.doe
   Password: student123
   ```

3. **Test guest mode**:
   - Just click "Continue as guest" on login page

---

## 🔧 Customization

### Adding More Data

Edit `seed_data.py` and add to the respective functions:

#### Add a Knowledge Base Entry

```python
def seed_knowledge_base(self):
    # ... existing code ...
    
    knowledge_entries.append({
        'category': your_category,
        'title': 'Your Title',
        'question': 'Your question?',
        'answer': 'Your detailed answer...',
        'keywords': 'keyword1, keyword2, keyword3',
        'priority': 70
    })
```

#### Add an Office Location

```python
def seed_office_locations(self):
    # ... existing code ...
    
    offices.append({
        'name': 'Your Office Name',
        'office_type': 'administrative',
        'building': 'Building Name',
        'floor': 'Ground Floor',
        'room_number': 'A-G-01',
        'description': 'What this office does',
        'services_offered': 'Service 1, Service 2',
        'contact_person': 'Mr./Ms. Name',
        'email': 'email@mut.ac.ke',
        'phone': '+254 712 345 XXX',
        'opening_hours': 'Monday - Friday: 8:00 AM - 5:00 PM'
    })
```

### Modifying Existing Data

1. Find the relevant function (e.g., `seed_bank_accounts`)
2. Update the dictionary values
3. Run `python manage.py seed_data --clear` to refresh

---

## 🐛 Troubleshooting

### Error: "No module named 'your_app'"

**Solution**: Update the import statement with your actual app name:

```python
from chat.models import (...)  # Change 'chat' to your app name
```

### Error: "User matching query does not exist"

**Solution**: The admin user creation might have failed. Create manually:

```bash
python manage.py createsuperuser
```

### Error: "Duplicate key value violates unique constraint"

**Solution**: Clear existing data first:

```bash
python manage.py seed_data --clear
```

### Data Not Showing in Chat

**Possible causes**:

1. **API Key not set**: Update the `ANTHROPIC_API_KEY` in SystemSettings
2. **Search not working**: Check that knowledge base entries were created:
   ```bash
   python manage.py shell
   >>> from your_app.models import KnowledgeBase
   >>> KnowledgeBase.objects.count()
   10  # Should show 10
   ```

### Performance Issues

If seeding takes too long:

1. Use `--clear` only when necessary
2. Comment out sections you don't need
3. Reduce the number of entries in large lists

---

## 📝 Database Schema

### Tables Populated

| Model | Records | Purpose |
|-------|---------|---------|
| SystemSettings | 5 | Configuration |
| User | 4 | Test accounts |
| KnowledgeCategory | 10 | Organization |
| KnowledgeBase | 10 | AI training data |
| BankAccount | 3 | Payment info |
| FinancialInformation | 7 | Fee structures |
| AcademicYear | 2 | Calendar info |
| ExamInformation | 3 | Exam schedules |
| UniversityOfficial | 8 | Leadership |
| OfficeLocation | 10 | Campus map |
| FAQ | 15 | Quick answers |
| Announcement | 7 | Notices |
| Discontinuation | 1 | Procedures |

**Total Records**: ~84 records across 13 models

---

## 🔄 Updating Seed Data

To update with new university information:

1. Edit `seed_data.py`
2. Clear old data: `python manage.py seed_data --clear`
3. Seed new data: `python manage.py seed_data`

Or update specific records via Django admin.

---

## 📚 Next Steps

After seeding:

1. ✅ Update API key in SystemSettings
2. ✅ Test login with provided credentials
3. ✅ Try asking questions in the chat
4. ✅ Customize data for your needs
5. ✅ Add more knowledge base entries
6. ✅ Configure Google OAuth (if needed)

---

## 🤝 Contributing

To add more realistic data:

1. Research actual MUT information
2. Update the seed script
3. Test thoroughly
4. Share with the team

---

## 📞 Support

If you encounter issues:

1. Check this README
2. Review error messages
3. Check Django logs
4. Verify model imports

---

## ⚖️ License

This seed data is for development and testing purposes. Replace with actual university data in production.

---

**Happy Coding! 🚀**

*Last Updated: 2024*