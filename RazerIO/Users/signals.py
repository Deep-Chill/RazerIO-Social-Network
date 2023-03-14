from django.dispatch import receiver
from .models import CustomUser
from allauth.account.signals import email_confirmed, email_changed, email_added, email_removed
from allauth.account.models import EmailAddress


@receiver(email_confirmed)
@receiver(email_added)
@receiver(email_removed)
def updatecompanyverifiedstatus(sender, request, email_address, **kwargs):
    user = email_address.user
    domain = user.Company.Email_Domain
    users_emails = EmailAddress.objects.filter(user=user, verified=True, email__endswith='@'+domain)
    user.Company_Verified_Email = users_emails.exists()
    user.save()
    if user.Company_Verified_Email:
        user.earn_badge('Verified_Company')
        user.save()

@receiver(email_changed)
def update_company_verified_email_on_change(sender, request, user, from_email_address, to_email_address, **kwargs):
    user = to_email_address.user
    domain = user.Company.Email_Domain
    users_emails = EmailAddress.objects.filter(user=user, verified=True, email__endswith='@'+domain)
    user.Company_Verified_Email = users_emails.exists()
    user.save()
    if user.Company_Verified_Email:
        user.earn_badge('Verified_Company')
        user.save()
