from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid


class User(AbstractUser):
    """Extended user model for authentication"""
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
        ('guest', 'Guest'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='guest')
    student_id = models.CharField(max_length=50, blank=True, null=True, unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    year_of_study = models.IntegerField(blank=True, null=True)
    is_guest = models.BooleanField(default=False)
    google_oauth_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    profile_picture = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_active = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.username} ({self.user_type})"


class ChatSession(models.Model):
    """Represents a conversation session"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions', null=True, blank=True)
    session_token = models.CharField(max_length=255, unique=True, blank=True, null=True)  # For guest users
    title = models.CharField(max_length=255, default="New Chat")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.title} - {self.user or 'Guest'}"


class Message(models.Model):
    """Individual messages in a chat session"""
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tokens_used = models.IntegerField(default=0)
    response_time = models.FloatField(null=True, blank=True)  # in seconds
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."


class KnowledgeCategory(models.Model):
    """Categories for organizing university information"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Knowledge Categories"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class KnowledgeBase(models.Model):
    """University information that the AI can reference"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(KnowledgeCategory, on_delete=models.CASCADE, related_name='knowledge_items')
    title = models.CharField(max_length=255)
    question = models.TextField()  # Common question format
    answer = models.TextField()
    keywords = models.TextField(help_text="Comma-separated keywords for search")
    priority = models.IntegerField(default=0, help_text="Higher priority shown first")
    is_active = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)
    helpful_count = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_knowledge')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Knowledge Base Entry"
        ordering = ['-priority', '-updated_at']
    
    def __str__(self):
        return self.title


class FinancialInformation(models.Model):
    """Fee structures and payment information"""
    PAYMENT_TYPE_CHOICES = [
        ('tuition', 'Tuition Fee'),
        ('accommodation', 'Accommodation'),
        ('registration', 'Registration'),
        ('exam', 'Examination Fee'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPE_CHOICES)
    program = models.CharField(max_length=100, blank=True, help_text="Specific program or 'All'")
    year_of_study = models.IntegerField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='KES')
    description = models.TextField()
    academic_year = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Financial Information"
        verbose_name_plural = "Financial Information"
    
    def __str__(self):
        return f"{self.payment_type} - {self.program} - {self.academic_year}"


class BankAccount(models.Model):
    """University bank account details"""
    ACCOUNT_TYPE_CHOICES = [
        ('main', 'Main Account'),
        ('fees', 'Fees Account'),
        ('accommodation', 'Accommodation Account'),
        ('other', 'Other'),
    ]
    
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPE_CHOICES)
    bank_name = models.CharField(max_length=100)
    account_name = models.CharField(max_length=200)
    account_number = models.CharField(max_length=50)
    branch = models.CharField(max_length=100, blank=True)
    swift_code = models.CharField(max_length=20, blank=True)
    paybill_number = models.CharField(max_length=20, blank=True, help_text="For M-Pesa")
    account_reference = models.CharField(max_length=50, blank=True, help_text="Student ID or reference")
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.bank_name} - {self.account_type}"


class ExamInformation(models.Model):
    """Supplementary and regular exam information"""
    EXAM_TYPE_CHOICES = [
        ('regular', 'Regular Exam'),
        ('supplementary', 'Supplementary Exam'),
        ('special', 'Special Exam'),
        ('retake', 'Retake Exam'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exam_type = models.CharField(max_length=50, choices=EXAM_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    academic_year = models.CharField(max_length=20)
    semester = models.CharField(max_length=20)
    application_start_date = models.DateField(null=True, blank=True)
    application_deadline = models.DateField(null=True, blank=True)
    exam_start_date = models.DateField(null=True, blank=True)
    exam_end_date = models.DateField(null=True, blank=True)
    application_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    requirements = models.TextField()
    application_process = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.exam_type} - {self.title}"


class AcademicYear(models.Model):
    """Academic year and semester information"""
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('current', 'Current'),
        ('past', 'Past'),
    ]
    
    year = models.CharField(max_length=20, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    registration_start = models.DateField()
    registration_end = models.DateField()
    semester_1_start = models.DateField()
    semester_1_end = models.DateField()
    semester_2_start = models.DateField()
    semester_2_end = models.DateField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"Academic Year {self.year}"


class Discontinuation(models.Model):
    """Information about discontinuation procedures"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    reason_types = models.TextField(help_text="Types of discontinuation reasons")
    process_steps = models.TextField()
    required_documents = models.TextField()
    contact_office = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    fees_refund_policy = models.TextField()
    timeline = models.TextField(help_text="Expected processing time")
    important_notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


class UniversityOfficial(models.Model):
    """Key university officials and their information"""
    POSITION_CHOICES = [
        ('vc', 'Vice Chancellor'),
        ('dvc_academic', 'Deputy VC - Academic'),
        ('dvc_admin', 'Deputy VC - Administration'),
        ('registrar', 'Registrar'),
        ('dean', 'Dean'),
        ('hod', 'Head of Department'),
        ('director', 'Director'),
        ('other', 'Other'),
    ]
    
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    position_title = models.CharField(max_length=200)
    full_name = models.CharField(max_length=200)
    department = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    office_location = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    photo_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'position']
    
    def __str__(self):
        return f"{self.full_name} - {self.position_title}"


class OfficeLocation(models.Model):
    """University offices and their locations"""
    OFFICE_TYPE_CHOICES = [
        ('academic', 'Academic Office'),
        ('administrative', 'Administrative Office'),
        ('student_services', 'Student Services'),
        ('financial', 'Financial Services'),
        ('it', 'IT Services'),
        ('library', 'Library'),
        ('health', 'Health Services'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    office_type = models.CharField(max_length=50, choices=OFFICE_TYPE_CHOICES)
    building = models.CharField(max_length=100)
    floor = models.CharField(max_length=50, blank=True)
    room_number = models.CharField(max_length=50, blank=True)
    description = models.TextField()
    services_offered = models.TextField()
    contact_person = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    opening_hours = models.TextField()
    map_coordinates = models.CharField(max_length=100, blank=True, help_text="Latitude,Longitude")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.building}"


class FAQ(models.Model):
    """Frequently Asked Questions"""
    category = models.ForeignKey(KnowledgeCategory, on_delete=models.CASCADE, related_name='faqs')
    question = models.TextField()
    answer = models.TextField()
    order = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    helpful_count = models.IntegerField(default=0)
    not_helpful_count = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "FAQ"
        ordering = ['order', '-views_count']
    
    def __str__(self):
        return self.question[:100]


class ChatFeedback(models.Model):
    """User feedback on chat responses"""
    RATING_CHOICES = [
        (1, 'Very Poor'),
        (2, 'Poor'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excellent'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    is_helpful = models.BooleanField(null=True, blank=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback: {self.rating}/5"


class AITrainingData(models.Model):
    """Training data for improving AI responses"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_query = models.TextField()
    ai_response = models.TextField()
    correct_response = models.TextField(blank=True, help_text="Admin-provided correct response")
    context = models.TextField(blank=True)
    knowledge_refs = models.ManyToManyField(KnowledgeBase, blank=True, related_name='training_data')
    is_approved = models.BooleanField(default=False)
    feedback_score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "AI Training Data"
        verbose_name_plural = "AI Training Data"
    
    def __str__(self):
        return f"Training: {self.user_query[:50]}..."


class Announcement(models.Model):
    """Important university announcements"""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    target_audience = models.CharField(max_length=100, help_text="students, staff, all")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-priority', '-start_date']
    
    def __str__(self):
        return self.title


class SearchLog(models.Model):
    """Log of search queries for analytics"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session = models.ForeignKey(ChatSession, on_delete=models.SET_NULL, null=True, blank=True)
    query = models.TextField()
    results_found = models.BooleanField(default=False)
    results_count = models.IntegerField(default=0)
    response_time = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Search Log"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Search: {self.query[:50]}..."


class SystemSettings(models.Model):
    """System-wide configuration settings"""
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = "System Setting"
        verbose_name_plural = "System Settings"
    
    def __str__(self):
        return self.key