from quotesapp.views import button_pressed
from django.dispatch import receiver


import subprocess


@receiver(button_pressed)
def scrap_data(sender, **kwargs):
    command = 'python -m utils.scrap_and_load'
    sub = subprocess.run(command, shell=True)
    return sub
    