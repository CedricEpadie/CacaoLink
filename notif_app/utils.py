# utils.py

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
# from pyfcm import FCMNotification

def send_welcome_email(username, email):
    subject = 'Bienvenue sur CacaoLink!'
    html_message = render_to_string('notif_app/welcome_email.html', {'username': username})
    plain_message = "Bienvenue sur CacaoLink! Merci de vous être inscrit."
    
    send_mail(
        subject,
        plain_message,
        settings.EMAIL_HOST_USER,
        [email],
        html_message=html_message,  # Ajoutez le contenu HTML ici
    )

def send_new_offer_email(offer_title, offer_description, offer_price, offer_link, recipient_list):
    subject = 'Nouvelle offre disponible sur CacaoLink!'
    html_message = render_to_string('new_offer_email.html', {
        'offer_title': offer_title,
        'offer_description': offer_description,
        'offer_price': offer_price,
        'offer_link': offer_link,
    })
    plain_message = f"Une nouvelle offre est disponible : {offer_title}\n\nDescription : {offer_description}\nPrix : {offer_price} FCFA"
    
    send_mail(
        subject,
        plain_message,
        settings.EMAIL_HOST_USER,
        recipient_list,
        html_message=html_message,
    )

def send_new_message_email(sender_name, recipient_name, message_content, message_link, recipient_email):
    subject = 'Vous avez reçu un nouveau message sur CacaoLink'
    html_message = render_to_string('new_message_email.html', {
        'sender_name': sender_name,
        'recipient_name': recipient_name,
        'message_content': message_content,
        'message_link': message_link,
    })
    plain_message = f"Vous avez reçu un nouveau message de {sender_name} :\n\n{message_content}"
    
    send_mail(
        subject,
        plain_message,
        settings.EMAIL_HOST_USER,
        [recipient_email],
        html_message=html_message,
    )

# Configure FCM avec ta clé serveur
# push_service = FCMNotification(api_key="AIzaSyA153OlUfWZGZH3N4542M5UseOVBY415So")

# def send_push_notification(device_token, title, message):
#     """
#     Envoie une notification push à un appareil spécifique.
#     :param device_token: Le token FCM de l'appareil.
#     :param title: Le titre de la notification.
#     :param message: Le contenu de la notification.
#     """
#     result = push_service.notify_single_device(
#         registration_id=device_token,
#         message_title=title,
#         message_body=message,
#     )
#     return result