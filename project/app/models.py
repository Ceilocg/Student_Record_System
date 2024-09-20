from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)

class RequestNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
class CertificateRequest(models.Model):
    CERTIFICATE_CHOICES = [
        ('Certification', 'Certification'),
        ('Form 137', 'Form 137'),
        ('Form 138', 'Form 138'),
        ('Good_Moral', 'Good Moral Certificate'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    lrn = models.CharField(max_length=12)
    certificate_type = models.CharField(max_length=50, choices=CERTIFICATE_CHOICES)
    request_purpose = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')  # e.g., 'Pending', 'Approved', 'Rejected'

    def __str__(self):
        return f"{self.name} - {self.certificate_type}"
    
class ExcelFile(models.Model):
    file = models.FileField(upload_to='excel_files/')  # Stores the file in the 'media/excel_files/' folder
    name = models.CharField(max_length=255)  # Name of the file
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Automatically sets the upload date

    def __str__(self):
        return self.name

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} - Read: {self.is_read}"
    