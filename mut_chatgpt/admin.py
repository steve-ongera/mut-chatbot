from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import (
    User, ChatSession, Message, KnowledgeCategory, KnowledgeBase,
    FinancialInformation, BankAccount, ExamInformation, AcademicYear,
    Discontinuation, UniversityOfficial, OfficeLocation, FAQ,
    ChatFeedback, AITrainingData, Announcement, SearchLog, SystemSettings
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'user_type', 'student_id', 'department', 'is_active', 'last_active']
    list_filter = ['user_type', 'is_active', 'is_staff', 'department', 'year_of_study']
    search_fields = ['username', 'email', 'student_id', 'first_name', 'last_name', 'phone_number']
    ordering = ['-created_at']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'student_id', 'phone_number', 'department', 
                      'year_of_study', 'is_guest', 'google_oauth_id', 'profile_picture', 'last_active')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'student_id', 'phone_number', 'department', 'year_of_study')
        }),
    )


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ['created_at', 'tokens_used', 'response_time']
    fields = ['role', 'content', 'tokens_used', 'response_time', 'created_at']
    can_delete = False


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at', 'updated_at', 'is_active', 'message_count']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['title', 'user__username', 'session_token']
    readonly_fields = ['id', 'created_at', 'updated_at']
    inlines = [MessageInline]
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'role', 'content_preview', 'tokens_used', 'response_time', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['content', 'session__title']
    readonly_fields = ['id', 'created_at']
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content'


@admin.register(KnowledgeCategory)
class KnowledgeCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'order', 'is_active', 'item_count']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    
    def item_count(self, obj):
        return obj.knowledge_items.count()
    item_count.short_description = 'Items'


@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'priority', 'views_count', 'helpful_count', 'is_active', 'updated_at']
    list_filter = ['is_active', 'category', 'priority', 'created_at']
    search_fields = ['title', 'question', 'answer', 'keywords']
    readonly_fields = ['id', 'views_count', 'helpful_count', 'created_at', 'updated_at']
    list_editable = ['priority', 'is_active']
    ordering = ['-priority', '-updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'title', 'question', 'answer')
        }),
        ('Search & Display', {
            'fields': ('keywords', 'priority', 'is_active')
        }),
        ('Statistics', {
            'fields': ('views_count', 'helpful_count', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FinancialInformation)
class FinancialInformationAdmin(admin.ModelAdmin):
    list_display = ['payment_type', 'program', 'year_of_study', 'amount', 'currency', 'academic_year', 'is_active']
    list_filter = ['payment_type', 'academic_year', 'is_active', 'year_of_study']
    search_fields = ['program', 'description']
    list_editable = ['is_active']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['account_type', 'bank_name', 'account_number', 'paybill_number', 'is_active']
    list_filter = ['account_type', 'bank_name', 'is_active']
    search_fields = ['bank_name', 'account_name', 'account_number', 'paybill_number']
    list_editable = ['is_active']


@admin.register(ExamInformation)
class ExamInformationAdmin(admin.ModelAdmin):
    list_display = ['title', 'exam_type', 'academic_year', 'semester', 'application_deadline', 'exam_start_date', 'is_active']
    list_filter = ['exam_type', 'academic_year', 'semester', 'is_active']
    search_fields = ['title', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'application_deadline'


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ['year', 'status', 'start_date', 'end_date', 'registration_start', 'registration_end', 'is_active']
    list_filter = ['status', 'is_active']
    search_fields = ['year']
    ordering = ['-start_date']


@admin.register(Discontinuation)
class DiscontinuationAdmin(admin.ModelAdmin):
    list_display = ['title', 'contact_office', 'contact_email', 'contact_phone', 'is_active', 'updated_at']
    list_filter = ['is_active', 'updated_at']
    search_fields = ['title', 'contact_office']
    readonly_fields = ['id', 'updated_at']


@admin.register(UniversityOfficial)
class UniversityOfficialAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'position_title', 'position', 'department', 'email', 'phone', 'is_active']
    list_filter = ['position', 'is_active', 'department']
    search_fields = ['full_name', 'position_title', 'email', 'department']
    ordering = ['order', 'position']
    list_editable = ['is_active']
    
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.photo_url:
            return ['photo_preview'] + list(self.readonly_fields or [])
        return self.readonly_fields or []
    
    def photo_preview(self, obj):
        if obj.photo_url:
            return format_html('<img src="{}" style="max-width: 200px; max-height: 200px;" />', obj.photo_url)
        return "No photo"
    photo_preview.short_description = 'Photo Preview'


@admin.register(OfficeLocation)
class OfficeLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'office_type', 'building', 'floor', 'room_number', 'email', 'phone', 'is_active']
    list_filter = ['office_type', 'building', 'is_active']
    search_fields = ['name', 'building', 'description', 'services_offered']
    list_editable = ['is_active']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question_preview', 'category', 'views_count', 'helpful_count', 'not_helpful_count', 'is_featured', 'is_active']
    list_filter = ['category', 'is_featured', 'is_active', 'created_at']
    search_fields = ['question', 'answer']
    readonly_fields = ['views_count', 'helpful_count', 'not_helpful_count', 'created_at', 'updated_at']
    list_editable = ['is_featured', 'is_active']
    ordering = ['order', '-views_count']
    
    def question_preview(self, obj):
        return obj.question[:100] + '...' if len(obj.question) > 100 else obj.question
    question_preview.short_description = 'Question'


@admin.register(ChatFeedback)
class ChatFeedbackAdmin(admin.ModelAdmin):
    list_display = ['message_preview', 'user', 'rating', 'is_helpful', 'created_at']
    list_filter = ['rating', 'is_helpful', 'created_at']
    search_fields = ['comment', 'message__content']
    readonly_fields = ['id', 'created_at']
    
    def message_preview(self, obj):
        content = obj.message.content
        return content[:50] + '...' if len(content) > 50 else content
    message_preview.short_description = 'Message'


@admin.register(AITrainingData)
class AITrainingDataAdmin(admin.ModelAdmin):
    list_display = ['query_preview', 'is_approved', 'feedback_score', 'created_at', 'updated_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['user_query', 'ai_response', 'correct_response']
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_editable = ['is_approved']
    filter_horizontal = ['knowledge_refs']
    
    def query_preview(self, obj):
        return obj.user_query[:100] + '...' if len(obj.user_query) > 100 else obj.user_query
    query_preview.short_description = 'Query'


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'target_audience', 'start_date', 'end_date', 'is_active', 'created_by']
    list_filter = ['priority', 'target_audience', 'is_active', 'start_date']
    search_fields = ['title', 'content']
    readonly_fields = ['id', 'created_at']
    date_hierarchy = 'start_date'
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = ['query_preview', 'user', 'results_found', 'results_count', 'response_time', 'timestamp']
    list_filter = ['results_found', 'timestamp']
    search_fields = ['query', 'user__username']
    readonly_fields = ['id', 'timestamp']
    date_hierarchy = 'timestamp'
    
    def query_preview(self, obj):
        return obj.query[:100] + '...' if len(obj.query) > 100 else obj.query
    query_preview.short_description = 'Query'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ['key', 'value_preview', 'is_active', 'updated_at', 'updated_by']
    list_filter = ['is_active', 'updated_at']
    search_fields = ['key', 'value', 'description']
    readonly_fields = ['updated_at']
    list_editable = ['is_active']
    
    def value_preview(self, obj):
        return obj.value[:100] + '...' if len(obj.value) > 100 else obj.value
    value_preview.short_description = 'Value'
    
    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


# Customize admin site header and title
admin.site.site_header = "University Chatbot Administration"
admin.site.site_title = "Chatbot Admin Portal"
admin.site.index_title = "Welcome to University Chatbot Administration"