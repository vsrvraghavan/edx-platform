from .models import UserProfileExtraInfo
from django.forms import ModelForm

class UserProfileExtraInfoForm(ModelForm):
    """
    The fields on this form are derived from the UserProfileExtraInfo model in models.py.
    """
    def __init__(self, *args, **kwargs):
        super(UserProfileExtraInfoForm, self).__init__(*args, **kwargs)
        self.fields['favorite_language'].error_messages = {
            "required": u"Please tell us your favorite programming language.",
            "invalid": u"It's an invalid entry.",
        }

    class Meta(object):
        model = UserProfileExtraInfo
        fields = ('favorite_editor', 'favorite_language')
