from django.db.models.signals import m2m_changed, post_delete
from django.dispatch import receiver
from project.models import Project


@receiver(m2m_changed, sender=Project.technologies.through)
def update_user_tech_on_project_tech_change(
        sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        if instance.user.tech_profile:
            instance.user.tech_profile.update_tech_with_approved()


@receiver(post_delete, sender=Project)
def update_user_tech_on_project_delete(sender, instance, **kwargs):
    user = instance.user
    if hasattr(user, 'tech_profile') and user.tech_profile:
        user.tech_profile.update_tech_with_approved()
