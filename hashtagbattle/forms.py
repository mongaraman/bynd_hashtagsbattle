from django import forms

from .models import Battle

class BattleForm(forms.ModelForm):
    ''' Battle Form class. This will create auto form depending upon model.'''

    class Meta:
        model = Battle
        fields = [
            "battle_name",
            "hashtag1",
            "hashtag2",
        ]
