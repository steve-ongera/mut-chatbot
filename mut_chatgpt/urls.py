from django.urls import path
from . import views

urlpatterns = [
    # ============= HOME & AUTH =============
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Auth API endpoints
    path('api/auth/login/', views.login_submit, name='api_login'),
    path('api/auth/register/', views.register_submit, name='api_register'),
    path('api/guest/session/create/', views.guest_session_create, name='guest_session_create'),
    
    # ============= CHAT SESSIONS =============
    path('api/chat/session/create/', views.chat_session_create, name='chat_session_create'),
    path('api/chat/sessions/', views.chat_session_list, name='chat_session_list'),
    path('api/chat/session/<uuid:session_id>/', views.chat_session_detail, name='chat_session_detail'),
    path('api/chat/session/<uuid:session_id>/delete/', views.chat_session_delete, name='chat_session_delete'),
    path('api/chat/session/<uuid:session_id>/rename/', views.chat_session_rename, name='chat_session_rename'),
    
    # ============= MESSAGES =============
    path('api/chat/message/send/', views.chat_send_message, name='chat_send_message'),
    path('api/chat/stream/', views.chat_stream_response, name='chat_stream'),
    path('api/message/<uuid:message_id>/feedback/', views.message_feedback, name='message_feedback'),
    
    # ============= KNOWLEDGE BASE =============
    path('knowledge/', views.knowledge_base_view, name='knowledge_base'),
    path('api/knowledge/search/', views.knowledge_search, name='knowledge_search'),
    
    # ============= FAQs =============
    path('faqs/', views.faqs_view, name='faqs'),
    path('api/faq/category/<uuid:category_id>/', views.faq_by_category, name='faq_by_category'),
    
    # ============= ANNOUNCEMENTS =============
    path('announcements/', views.announcements_view, name='announcements'),
    
    # ============= PROFILE & SETTINGS =============
    path('profile/', views.profile_view, name='profile'),
    path('api/profile/update/', views.profile_update, name='profile_update'),
    path('settings/', views.settings_view, name='settings'),
    
    # ============= ANALYTICS (Admin) =============
    path('analytics/', views.analytics_view, name='analytics'),
]