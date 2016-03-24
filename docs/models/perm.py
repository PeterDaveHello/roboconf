from django.db import models
from django.contrib.auth.models import User, Group

class Permission(models.Model):

    class Meta:
        app_label = 'docs'

    VIEW = '1'
    COMMENT = '2'
    EDIT = '3'

    ALLOW = 'A'
    DENY = 'D'

    PUBLIC = '0'
    INTERNAL = '1'
    PROTECTED = '2'
    PER_GROUP = 'G'
    PER_USER = 'U'

    TYPE_CHOICES = (
            (VIEW, 'View document'),
            (COMMENT, 'Comment on document'),
            (EDIT, 'Edit document'),
        )

    EFFECT_CHOICES = (
            (ALLOW, 'Allow'),
            (DENY, 'Deny'),
        )

    SCOPE_CHOICES = (
            (PUBLIC, 'Public'),
            (INTERNAL, 'Staff'),
            (PROTECTED, 'Administrators'),
            (PER_GROUP, 'Specify group'),
            (PER_USER, 'Specify user'),
        )

    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    effect = models.CharField(max_length=1, choices=EFFECT_CHOICES)
    scope = models.CharField(max_length=1, choices=SCOPE_CHOICES)
    target = models.IntegerField(blank=True, null=True)

    def target_user(self):
        if not self.scope == PER_USER:
            return None
        return User.objects.get(id=self.target)

    def target_group(self):
        if not self.scope == PER_GROUP:
            return None
        return Group.objects.get(id=self.target)

    def __key__(self):
        # Returns the sorting key for comparision functions
        # Permissions with lower priority (granularity) goes first
        return '%s%s%s' % (self.scope, self.type, self.effect)

    TYPE_NAMES = {
        VIEW: 'VIEW',
        COMMENT: 'COMMENT',
        EDIT: 'EDIT',
    }

    EFFECT_NAMES = {
        ALLOW: 'ALLOW',
        DENY: 'DENY',
    }

    SCOPE_NAMES = {
        PUBLIC: '*',
        INTERNAL: 'STAFF',
        PROTECTED: 'ADMIN',
        PER_GROUP: 'GROUP',
        PER_USER: 'USER',
    }

    def __str__(self):
        return '%s:%s %s%s %s' % (
                self.__key__(),
                Permission.EFFECT_NAMES.get(self.effect, '?'),
                Permission.SCOPE_NAMES.get(self.scope, '?'),
                (' %s' % self.target) if self.target else '',
                Permission.TYPE_NAMES.get(self.type, '?'),
            )

    TYPE_ENUMERATION = (
            (VIEW, 'view'),
            (COMMENT, 'comment'),
            (EDIT, 'edit'),
        )

    EFFECT_ENUMERATION = (
            (ALLOW, 'allow'),
            (DENY, 'deny'),
        )

    SCOPE_ENUMERATION = (
            (PUBLIC, '*'),
            (INTERNAL, 'staff'),
            (PROTECTED, 'admin'),
            (PER_GROUP, 'group'),
            (PER_USER, 'user'),
        )
