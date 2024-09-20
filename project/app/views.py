from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import CertificateRequestForm, CustomUserCreationForm , UpdateUserForm , CustomUserChangeForm
from .models import CertificateRequest, Notification
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.models import User 
from django.http import  HttpResponse
from django.contrib.auth.models import User
from app.models import ExcelFile
from django.contrib.auth.decorators import login_required
from django.views import View


def student_dashboard(request):
    if request.method == 'POST':
        form = CertificateRequestForm(request.POST)
        if form.is_valid():
            form.save()  # Save data to the database
            return redirect('request_success')  # Redirect to success page after saving
    else:
        form = CertificateRequestForm()

    return render(request, 'student_dashboard.html', {'form': form})

def request_success(request):
    return render(request, 'request_success.html')

def notification_view(request):
    # Fetch all certificate requests
    requests = CertificateRequest.objects.all().order_by('-submitted_at')
    return render(request, 'dashboard/notifications.html', {'requests': requests})


class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

def index(request):
    return render(request, 'index.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after login
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def form_template_view(request):
    return render(request, 'dashboard/form_templates.html')

def settings(request):
    return render(request, 'settings.html')

def home_view(request):
    return render(request, 'dashboard/home.html')

def about_view(request):
    return render(request, 'dashboard/about.html')

def data_management_view(request):
    return render(request, 'dashboard/data_management.html')

@login_required
def settings_view(request):
    return render(request, 'dashboard/settings.html')


def password_reset(request):
    return render(request, 'password_reset.html')

def user_management_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Set password properly
            user.save()
            messages.success(request, "User added successfully.")
            return redirect('user_management')  # Redirect to the user management page
        else:
            messages.error(request, "Please correct the error(s).")
    else:
        form = CustomUserCreationForm()

    users = User.objects.all()  # Query all users from the database
    return render(request, 'user_management.html', {'form': form, 'users': users})


# View to delete a user
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('user_management')

# View to update a user
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            password1 = form.cleaned_data.get('password1')
            if password1:
                user.set_password(password1)
            user.save()
            return redirect('user_management')  # Redirect to a success page
    else:
        form = CustomUserChangeForm(instance=user)
    
    return render(request, 'update_user.html', {'form': form, 'user': user})

def list_excel_files(request):
    # Fetch all ExcelFile objects from the database
    excel_files = ExcelFile.objects.all()
    
    # Debugging: Print the QuerySet to ensure files are fetched
    print(excel_files)

    # Pass the data to the template
    return render(request, 'dashboard/form_templates.html', {'excel_files': excel_files})


# View to handle file download
def download_excel_file(request, file_id):
    excel_file = get_object_or_404(ExcelFile, pk=file_id)
    response = HttpResponse(excel_file.file, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{excel_file.name}"'
    return response

def form_template_view(request):
    excel_files = ExcelFile.objects.all()
    return render(request, 'dashboard/form_templates.html', {'excel_files': excel_files})

def dashboard(request):
    # Make sure user is authenticated
    if request.user.is_authenticated:
        unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()
    else:
        unread_notifications_count = 0

    context = {
        'unread_notifications_count': unread_notifications_count
    }

    return render(request, 'dashboard.html', context)

def notifications(request):
    # Logic to handle notifications
    return render(request, 'notifications.html')

class NotificationsView(View):
    def get(self, request):
        # Logic to handle notifications
        return render(request, 'notifications.html')
    
def dashboard_view(request):
    unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()
    context = {
        'unread_notifications_count': unread_notifications_count,
    }
    return render(request, 'dashboard.html', context)

def request_certificate(request):
    if request.method == 'POST':
        form = CertificateRequestForm(request.POST)
        if form.is_valid():
            # Handle the form submission
            pass
    else:
        form = CertificateRequestForm()

    return render(request, 'request_certificate.html', {'form': form})

