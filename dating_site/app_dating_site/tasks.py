from .models import LikedUsers
from dating_site.celery import app
from django.contrib.auth import get_user_model
from django.db import transaction
from django.core.mail import send_mass_mail

User = get_user_model()


# Время до начала выполнения задачи 30 с, лимит повторов выполнения 10
@app.task(soft_time_limit=30, autoretry_for=(IOError,),
          retry_kwargs={'max_retries': 10})
def send_email_celery(current_user_pk, liked_user_pk):
    """
    Задача отправки писем с адресом электронной почты понравившегося
     пользователя, если возникла взаимная симпатия.
    """
    current_user = User.objects.filter(pk=current_user_pk).first()
    liked_user = User.objects.filter(pk=liked_user_pk).first()

    if current_user and liked_user:
        message_1 = (
            'Вы понравились {0}'.format(liked_user.first_name),
            'Здравствуйте, {0}! Вы понравились {1}.\n'
            'Почта участника: {2}'.format(
                current_user.first_name,
                liked_user.first_name,
                liked_user.email
            ),
            'artur.tokranov888@gmail.com',
            [current_user.email],
        )

        message_2 = (
            'Вы понравились {0}'.format(current_user.first_name),
            'Здравствуйте, {0}! Вы понравились {1}.\n'
            'Почта участника: {2}'.format(
                liked_user.first_name,
                current_user.first_name,
                current_user.email
            ),
            'artur.tokranov888@gmail.com',
            [liked_user.email],
        )
        result = send_mass_mail((message_1, message_2), fail_silently=False)

        if result == 2:
            data_current_user = LikedUsers.objects.filter(
                user_id=current_user_pk, liked_user_id=liked_user_pk
            ).first()
            data_liked_user = LikedUsers.objects.filter(
                user_id=liked_user.pk, liked_user_id=current_user.pk
            ).first()

            with transaction.atomic():
                data_current_user.send_email = True
                data_current_user.save(update_fields=['send_email'])
                data_liked_user.send_email = True
                data_liked_user.save(update_fields=['send_email'])
