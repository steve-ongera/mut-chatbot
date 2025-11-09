from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Count
from django.utils import timezone
from django.core.paginator import Paginator
import json
import uuid
import requests
from datetime import datetime, timedelta

from .models import (
    User, ChatSession, Message, KnowledgeBase, KnowledgeCategory,
    FinancialInformation, BankAccount, ExamInformation, AcademicYear,
    Discontinuation, UniversityOfficial, OfficeLocation, FAQ,
    ChatFeedback, AITrainingData, Announcement, SearchLog, SystemSettings
)


# ============= HOME & AUTH VIEWS =============

def home(request):
    """Main chat interface"""
    if request.user.is_authenticated:
        sessions = ChatSession.objects.filter(user=request.user, is_active=True)[:10]
    else:
        # Get guest sessions from cookie
        session_token = request.COOKIES.get('guest_session_token')
        if session_token:
            sessions = ChatSession.objects.filter(session_token=session_token, is_active=True)[:10]
        else:
            sessions = []
    
    context = {
        'sessions': sessions,
        'recent_announcements': Announcement.objects.filter(
            is_active=True,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        )[:5]
    }
    return render(request, 'chat/home.html', context)


@require_http_methods(["POST"])
def guest_session_create(request):
    """Create a guest session"""
    session_token = str(uuid.uuid4())
    session = ChatSession.objects.create(
        session_token=session_token,
        title="New Guest Chat"
    )
    
    response = JsonResponse({
        'success': True,
        'session_id': str(session.id),
        'session_token': session_token
    })
    response.set_cookie('guest_session_token', session_token, max_age=30*24*60*60)  # 30 days
    return response


def login_view(request):
    """Login page"""
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'auth/login.html')


@require_http_methods(["POST"])
def login_submit(request):
    """Handle login submission"""
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return JsonResponse({'success': True, 'redirect': '/'})
    
    return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=400)


def register_view(request):
    """Registration page"""
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'auth/register.html')


@require_http_methods(["POST"])
def register_submit(request):
    """Handle registration submission"""
    data = json.loads(request.body)
    
    try:
        user = User.objects.create_user(
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password'),
            user_type=data.get('user_type', 'student'),
            student_id=data.get('student_id'),
            phone_number=data.get('phone_number'),
            department=data.get('department'),
            year_of_study=data.get('year_of_study')
        )
        login(request, user)
        return JsonResponse({'success': True, 'redirect': '/'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def logout_view(request):
    """Logout user"""
    logout(request)
    return redirect('login')


# ============= CHAT VIEWS =============

@require_http_methods(["POST"])
def chat_session_create(request):
    """Create a new chat session"""
    data = json.loads(request.body)
    title = data.get('title', 'New Chat')
    
    if request.user.is_authenticated:
        session = ChatSession.objects.create(user=request.user, title=title)
    else:
        session_token = request.COOKIES.get('guest_session_token')
        if not session_token:
            session_token = str(uuid.uuid4())
        session = ChatSession.objects.create(session_token=session_token, title=title)
    
    return JsonResponse({
        'success': True,
        'session_id': str(session.id),
        'title': session.title,
        'created_at': session.created_at.isoformat()
    })


@require_http_methods(["GET"])
def chat_session_list(request):
    """Get all chat sessions for current user"""
    if request.user.is_authenticated:
        sessions = ChatSession.objects.filter(user=request.user, is_active=True)
    else:
        session_token = request.COOKIES.get('guest_session_token')
        if not session_token:
            return JsonResponse({'success': True, 'sessions': []})
        sessions = ChatSession.objects.filter(session_token=session_token, is_active=True)
    
    sessions_data = [{
        'id': str(s.id),
        'title': s.title,
        'created_at': s.created_at.isoformat(),
        'updated_at': s.updated_at.isoformat(),
        'message_count': s.messages.count()
    } for s in sessions]
    
    return JsonResponse({'success': True, 'sessions': sessions_data})


@require_http_methods(["GET"])
def chat_session_detail(request, session_id):
    """Get messages for a specific session"""
    try:
        session = ChatSession.objects.get(id=session_id, is_active=True)
        
        # Verify access
        if request.user.is_authenticated:
            if session.user != request.user:
                return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
        else:
            session_token = request.COOKIES.get('guest_session_token')
            if session.session_token != session_token:
                return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
        
        messages = Message.objects.filter(session=session)
        messages_data = [{
            'id': str(m.id),
            'role': m.role,
            'content': m.content,
            'created_at': m.created_at.isoformat()
        } for m in messages]
        
        return JsonResponse({
            'success': True,
            'session': {
                'id': str(session.id),
                'title': session.title,
                'created_at': session.created_at.isoformat()
            },
            'messages': messages_data
        })
    except ChatSession.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Session not found'}, status=404)


@require_http_methods(["DELETE"])
def chat_session_delete(request, session_id):
    """Delete a chat session"""
    try:
        session = ChatSession.objects.get(id=session_id)
        
        # Verify access
        if request.user.is_authenticated:
            if session.user != request.user:
                return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
        else:
            session_token = request.COOKIES.get('guest_session_token')
            if session.session_token != session_token:
                return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
        
        session.is_active = False
        session.save()
        return JsonResponse({'success': True})
    except ChatSession.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Session not found'}, status=404)


@require_http_methods(["PUT"])
def chat_session_rename(request, session_id):
    """Rename a chat session"""
    try:
        data = json.loads(request.body)
        session = ChatSession.objects.get(id=session_id)
        
        # Verify access
        if request.user.is_authenticated:
            if session.user != request.user:
                return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
        else:
            session_token = request.COOKIES.get('guest_session_token')
            if session.session_token != session_token:
                return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
        
        session.title = data.get('title', session.title)
        session.save()
        return JsonResponse({'success': True, 'title': session.title})
    except ChatSession.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Session not found'}, status=404)


@require_http_methods(["POST"])
def chat_send_message(request):
    """Send a message and get AI response"""
    import time
    start_time = time.time()
    
    data = json.loads(request.body)
    session_id = data.get('session_id')
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return JsonResponse({'success': False, 'error': 'Message cannot be empty'}, status=400)
    
    try:
        session = ChatSession.objects.get(id=session_id, is_active=True)
        
        # Verify access
        if request.user.is_authenticated:
            if session.user != request.user:
                return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
        else:
            session_token = request.COOKIES.get('guest_session_token')
            if session.session_token != session_token:
                return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
        
        # Save user message
        user_msg = Message.objects.create(
            session=session,
            role='user',
            content=user_message
        )
        
        # Log search
        SearchLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            session=session,
            query=user_message
        )
        
        # Search knowledge base
        knowledge_context = search_knowledge_base(user_message)
        
        # Generate AI response
        ai_response = generate_ai_response(user_message, knowledge_context, session)
        
        # Save AI response
        response_time = time.time() - start_time
        ai_msg = Message.objects.create(
            session=session,
            role='assistant',
            content=ai_response,
            response_time=response_time
        )
        
        # Update session
        session.updated_at = timezone.now()
        
        # Auto-generate title from first message
        if session.messages.filter(role='user').count() == 1:
            session.title = user_message[:50] + ('...' if len(user_message) > 50 else '')
        
        session.save()
        
        return JsonResponse({
            'success': True,
            'user_message': {
                'id': str(user_msg.id),
                'content': user_msg.content,
                'created_at': user_msg.created_at.isoformat()
            },
            'assistant_message': {
                'id': str(ai_msg.id),
                'content': ai_msg.content,
                'created_at': ai_msg.created_at.isoformat()
            },
            'session_title': session.title
        })
        
    except ChatSession.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Session not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def chat_stream_response(request):
    """Stream AI response for real-time typing effect"""
    # This would integrate with OpenAI's streaming API
    # For now, returning a placeholder
    def event_stream():
        response = "This is a streaming response simulation..."
        for char in response:
            yield f"data: {json.dumps({'content': char})}\n\n"
            import time
            time.sleep(0.05)
        yield f"data: {json.dumps({'done': True})}\n\n"
    
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')


# ============= KNOWLEDGE BASE HELPERS =============

def search_knowledge_base(query):
    """Search knowledge base for relevant information"""
    # Search in KnowledgeBase
    kb_results = KnowledgeBase.objects.filter(
        Q(question__icontains=query) |
        Q(answer__icontains=query) |
        Q(keywords__icontains=query),
        is_active=True
    ).order_by('-priority')[:5]
    
    # Search in FAQs
    faq_results = FAQ.objects.filter(
        Q(question__icontains=query) | Q(answer__icontains=query),
        is_active=True
    )[:3]
    
    context = {
        'knowledge_base': [{'question': kb.question, 'answer': kb.answer} for kb in kb_results],
        'faqs': [{'question': faq.question, 'answer': faq.answer} for faq in faq_results]
    }
    
    # Check for specific topics
    query_lower = query.lower()
    
    # Fees information
    if any(word in query_lower for word in ['fee', 'payment', 'cost', 'pay', 'tuition']):
        context['financial_info'] = list(FinancialInformation.objects.filter(is_active=True).values())
        context['bank_accounts'] = list(BankAccount.objects.filter(is_active=True).values())
    
    # Exam information
    if any(word in query_lower for word in ['exam', 'supplementary', 'sup', 'test']):
        context['exam_info'] = list(ExamInformation.objects.filter(is_active=True).values())
    
    # Academic year
    if any(word in query_lower for word in ['academic year', 'semester', 'registration']):
        context['academic_years'] = list(AcademicYear.objects.filter(is_active=True).values())
    
    # Discontinuation
    if any(word in query_lower for word in ['discontinue', 'withdraw', 'leave', 'defer']):
        context['discontinuation'] = list(Discontinuation.objects.filter(is_active=True).values())
    
    # Officials
    if any(word in query_lower for word in ['vc', 'vice chancellor', 'dean', 'registrar', 'hod']):
        context['officials'] = list(UniversityOfficial.objects.filter(is_active=True).values())
    
    # Office locations
    if any(word in query_lower for word in ['office', 'location', 'where is', 'find']):
        context['offices'] = list(OfficeLocation.objects.filter(is_active=True).values())
    
    return context


def generate_ai_response(query, context, session):
    """Generate AI response using Anthropic Claude or OpenAI"""
    # Get conversation history
    previous_messages = Message.objects.filter(session=session).order_by('created_at')[:10]
    conversation_history = [
        {"role": msg.role, "content": msg.content}
        for msg in previous_messages
    ]
    
    # Build system prompt with context
    system_prompt = f"""You are MUT AI, an intelligent assistant for Murang'a University of Technology.
You help students, staff, and visitors with information about the university.

Available Information:
{json.dumps(context, indent=2, default=str)}

Guidelines:
- Be helpful, accurate, and concise
- If you find relevant information in the context, use it
- If information is not available, politely say so and suggest who to contact
- Always be professional and friendly
- For financial information, always provide exact amounts and account details
- For procedures, provide step-by-step guidance
"""
    
    try:
        # Using Anthropic Claude API (you'll need to add your API key)
        api_key = SystemSettings.objects.get(key='ANTHROPIC_API_KEY').value
        
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers={
                'x-api-key': api_key,
                'anthropic-version': '2023-06-01',
                'content-type': 'application/json',
            },
            json={
                'model': 'claude-sonnet-4-20250514',
                'max_tokens': 1024,
                'system': system_prompt,
                'messages': conversation_history + [{'role': 'user', 'content': query}]
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['content'][0]['text']
        else:
            return "I apologize, but I'm having trouble processing your request right now. Please try again."
            
    except SystemSettings.DoesNotExist:
        # Fallback to simple pattern matching
        return generate_fallback_response(query, context)
    except Exception as e:
        return f"I apologize for the inconvenience. Please contact the IT support office for assistance."


def generate_fallback_response(query, context):
    """Generate a simple response without AI API"""
    query_lower = query.lower()
    
    # Fees
    if 'fee' in query_lower or 'payment' in query_lower:
        if context.get('bank_accounts'):
            bank = context['bank_accounts'][0]
            return f"""To pay school fees, use the following account details:

Bank: {bank['bank_name']}
Account Name: {bank['account_name']}
Account Number: {bank['account_number']}
Paybill: {bank.get('paybill_number', 'N/A')}

For M-Pesa payments:
1. Go to M-Pesa menu
2. Select Lipa na M-Pesa
3. Select Paybill
4. Enter Paybill number: {bank.get('paybill_number', 'N/A')}
5. Enter your Student ID as account number
6. Enter amount
7. Enter your M-Pesa PIN

For more information, visit the Finance Office."""
    
    # Exams
    if 'exam' in query_lower or 'supplementary' in query_lower:
        if context.get('exam_info'):
            exam = context['exam_info'][0]
            return f"""Supplementary Exam Information:

Application Period: {exam.get('application_start_date', 'TBA')} to {exam.get('application_deadline', 'TBA')}
Exam Period: {exam.get('exam_start_date', 'TBA')} to {exam.get('exam_end_date', 'TBA')}
Application Fee: KES {exam.get('application_fee', 'TBA')}

Requirements:
{exam.get('requirements', 'Contact the Examination Office')}

Application Process:
{exam.get('application_process', 'Visit the Examination Office for guidance')}"""
    
    # Officials
    if 'vc' in query_lower or 'vice chancellor' in query_lower:
        if context.get('officials'):
            officials = [o for o in context['officials'] if o['position'] == 'vc']
            if officials:
                official = officials[0]
                return f"""The Vice Chancellor of Murang'a University of Technology is {official['full_name']}.

Position: {official['position_title']}
Email: {official['email']}
Office: {official.get('office_location', 'Administration Block')}"""
    
    # Default response
    return """I'm here to help you with information about Murang'a University of Technology. 

I can assist with:
- School fees and payment information
- Exam schedules and supplementary exams
- Academic calendar and registration dates
- Discontinuation procedures
- University officials and contacts
- Office locations

What would you like to know?"""


# ============= FEEDBACK VIEWS =============

@require_http_methods(["POST"])
def message_feedback(request, message_id):
    """Submit feedback for a message"""
    data = json.loads(request.body)
    
    try:
        message = Message.objects.get(id=message_id)
        
        feedback = ChatFeedback.objects.create(
            message=message,
            user=request.user if request.user.is_authenticated else None,
            rating=data.get('rating'),
            is_helpful=data.get('is_helpful'),
            comment=data.get('comment', '')
        )
        
        return JsonResponse({'success': True, 'feedback_id': str(feedback.id)})
    except Message.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Message not found'}, status=404)


# ============= INFORMATION VIEWS =============

def knowledge_base_view(request):
    """Knowledge base page"""
    categories = KnowledgeCategory.objects.filter(is_active=True, parent=None)
    return render(request, 'info/knowledge_base.html', {'categories': categories})


@require_http_methods(["GET"])
def knowledge_search(request):
    """Search knowledge base via AJAX"""
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    
    results = KnowledgeBase.objects.filter(is_active=True)
    
    if query:
        results = results.filter(
            Q(question__icontains=query) |
            Q(answer__icontains=query) |
            Q(keywords__icontains=query)
        )
    
    if category_id:
        results = results.filter(category_id=category_id)
    
    results = results.order_by('-priority')[:20]
    
    data = [{
        'id': str(r.id),
        'title': r.title,
        'question': r.question,
        'answer': r.answer,
        'category': r.category.name
    } for r in results]
    
    return JsonResponse({'success': True, 'results': data})


def faqs_view(request):
    """FAQs page"""
    categories = KnowledgeCategory.objects.filter(is_active=True)
    featured_faqs = FAQ.objects.filter(is_featured=True, is_active=True)
    return render(request, 'info/faqs.html', {
        'categories': categories,
        'featured_faqs': featured_faqs
    })


@require_http_methods(["GET"])
def faq_by_category(request, category_id):
    """Get FAQs by category"""
    faqs = FAQ.objects.filter(category_id=category_id, is_active=True).order_by('order')
    
    data = [{
        'id': str(f.id),
        'question': f.question,
        'answer': f.answer,
        'helpful_count': f.helpful_count
    } for f in faqs]
    
    return JsonResponse({'success': True, 'faqs': data})


def announcements_view(request):
    """Announcements page"""
    announcements = Announcement.objects.filter(
        is_active=True,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).order_by('-priority', '-start_date')
    
    return render(request, 'info/announcements.html', {'announcements': announcements})


# ============= PROFILE & SETTINGS =============

@login_required
def profile_view(request):
    """User profile page"""
    return render(request, 'user/profile.html')


@login_required
@require_http_methods(["PUT"])
def profile_update(request):
    """Update user profile"""
    data = json.loads(request.body)
    user = request.user
    
    user.email = data.get('email', user.email)
    user.phone_number = data.get('phone_number', user.phone_number)
    user.department = data.get('department', user.department)
    user.year_of_study = data.get('year_of_study', user.year_of_study)
    user.save()
    
    return JsonResponse({'success': True, 'message': 'Profile updated successfully'})


@login_required
def settings_view(request):
    """Settings page"""
    return render(request, 'user/settings.html')


# ============= ADMIN ANALYTICS =============

@login_required
def analytics_view(request):
    """Analytics dashboard (admin only)"""
    if not request.user.is_staff:
        return redirect('home')
    
    # Get statistics
    total_users = User.objects.count()
    total_sessions = ChatSession.objects.count()
    total_messages = Message.objects.count()
    active_today = User.objects.filter(last_active__gte=timezone.now() - timedelta(days=1)).count()
    
    # Top searches
    top_searches = SearchLog.objects.values('query').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    context = {
        'total_users': total_users,
        'total_sessions': total_sessions,
        'total_messages': total_messages,
        'active_today': active_today,
        'top_searches': top_searches
    }
    
    return render(request, 'admin/analytics.html', context)