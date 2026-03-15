"""Database models for CryptoLab application."""

from django.db import models
from django.contrib.auth.models import User


class CryptoHistory(models.Model):
    """Stores encryption/decryption history for authenticated users."""
    
    OPERATION_CHOICES = [
        ('encrypt', 'Encrypt'),
        ('decrypt', 'Decrypt'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crypto_history')
    cipher = models.CharField(max_length=50)
    operation = models.CharField(max_length=10, choices=OPERATION_CHOICES)
    input_text = models.TextField()
    output_text = models.TextField()
    key_used = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Crypto histories'
    
    def __str__(self):
        return f"{self.user.username} - {self.cipher} ({self.operation}) at {self.timestamp}"


class UploadedKeyFile(models.Model):
    """Stores uploaded key files for authenticated users."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='key_files')
    file = models.FileField(upload_to='key_files/')
    original_filename = models.CharField(max_length=255)
    cipher_type = models.CharField(max_length=50, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.original_filename}"
