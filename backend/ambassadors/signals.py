from ambassadors.models import PromoCode
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=PromoCode)
def make_other_promo_codes_inactive(sender, instance, **kwargs):
    """
    Сигнал, который деактивирует все остальные промокоды
    при определении активного.
    """
    if instance.status == 'active':
        PromoCode.objects.filter(
            ambassador=instance.ambassador
        ).exclude(
            id=instance.id
        ).update(
            status='inactive'
        )
