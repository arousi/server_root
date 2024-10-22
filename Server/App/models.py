from django.db import models
from django.contrib.auth.models import User  # Import the User model

#4 DB

# Create your models here.
class PromptModel(models.Model):
    gemini_response = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt_text = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    yes_count = models.IntegerField()
    no_count = models.IntegerField()
    score = models.IntegerField()

    def __str__(self):
        return f"{self.user.username}'s Prompt"


class AppUser(models.Model):
    id = models.AutoField(primary_key=True)  # This must be an integer field
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, default = "Anon")  # Make sure to define this field
    email = models.EmailField("Email", max_length=254, default ="Anon@email.com")  # Corrected this line
    sector = models.CharField(max_length=100, default = "CODING")  # E.g., coding, creative writing, etc.
    region = models.CharField(max_length=100, default = "WorldWide")  # E.g., organization, country, etc.
    total_score = models.IntegerField(default=1)

    def __str__(self):
        return self.nickname