from ambassadors.models import PromoCode
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=PromoCode)
def make_other_promo_codes_inactive(sender, instance, **kwargs):
    if instance.status == 'active':
        PromoCode.objects.filter(
            ambassador=instance.ambassador
        ).exclude(
            id=instance.id
        ).update(
            status='inactive'
        )
