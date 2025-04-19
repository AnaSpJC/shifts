from django.db import models # type: ignore this is recommended by codespace for interpreter stuff
from django.contrib.auth.models import User # type: ignore

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.date} {self.time}"

