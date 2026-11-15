from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=150, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Application(models.Model):
    class Status(models.TextChoices):
        WISHLIST = "Wishlist"
        APPLIED = "Applied"
        INTERVIEW = "Interview"
        OFFER = "Offer"
        REJECTED = "Rejected"

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="applications"
    )
    position = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    job_url = models.URLField(blank=True)
    location = models.CharField(max_length=150, blank=True)
    application_date = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.WISHLIST
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.position


class InterviewRound(models.Model):
    class Outcome(models.TextChoices):
        PENDING = "Pending"
        PASSED = "Passed"
        FAILED = "Failed"

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="interview_rounds",
    )
    round_name = models.CharField(max_length=100)
    interview_date = models.DateTimeField(blank=True, null=True)
    interview_type = models.CharField(max_length=50, blank=True)
    outcome = models.CharField(
        max_length=20,
        choices=Outcome.choices,
        default=Outcome.PENDING,
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.round_name
