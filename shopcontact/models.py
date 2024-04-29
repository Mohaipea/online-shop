from django.db import models


class Contact(models.Model):
    name = models.CharField('نام و نام خانوادگی', max_length=100)
    email = models.EmailField('ایمیل')
    subject = models.CharField('موضوع', max_length=50)
    message = models.TextField('پیام')
    created = models.DateTimeField('زمان ثبت', auto_now_add=True)
    seen = models.BooleanField('خوانده شده/ نشده', default=False)

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'

    def __str__(self):
        return self.subject
