from django.core.mail import send_mail

def send_activation_code(email, activation_code):
    messege = f"""
        Thank you for signing up!
        Your activation code is:
        {activation_code}
    """

    send_mail(
        "Activate your account",
        messege,
        "baielabdyllaev.00@gmail.com",
        [email, ],
        fail_silently=False,
    )