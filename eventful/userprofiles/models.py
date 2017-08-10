from django.contrib.auth.models import User
from django.db import models

from .managers import FriendRequestManager


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    timezone = models.CharField(max_length=35, blank=True)
    friends = models.ManyToManyField('self')

    def __str__(self):
        return str(self.user.pk)

    def are_friends(self, pk):
        return any(friend.pk == pk for friend in self.friends.all())

    def are_friends_by_filter(self, pk):
        return self.friends.filter(pk=pk).exists()

    def get_friends(self):
        return list(self.friends.all().select_related('user').values(
            pk=models.F('friends__user_id'),
            username=models.F('friends__user__username'),
            first_name=models.F('friends__user__first_name'),
            last_name=models.F('friends__user__last_name')
        ))

    def get_friends_pks(self):
        return self.friends.all().values_list('user_id', flat=True)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='friend_requests_sent',
                                  on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friend_requests_received',
                                on_delete=models.CASCADE)
    objects = FriendRequestManager()

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f'{self.from_user_id} sent request to {self.to_user_id}'
