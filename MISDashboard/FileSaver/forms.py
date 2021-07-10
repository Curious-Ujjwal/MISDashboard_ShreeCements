from django import forms
from .models import *

# OBSERVATION_CHOICES = [
# 	("Choice-1", _("Choice-1")),
# 	("Choice-2", _("Choice-2")),
# 	("Choice-3", _("Choice-3")),
# 	("Choice-4", _("Choice-4")),
# 	("Choice-5", _("Choice-5")),
# 	("Choice-6", _("Choice-6")),
# 	("Choice-7", _("Choice-7")),
# ]

class EntryForm(forms.ModelForm):
	entries = forms.ModelMultipleChoiceField(queryset=Operator_Entry.objects, widget=forms.CheckboxSelectMultiple(), required=False)
	# entries = forms.ChoiceField(choices=OBSERVATION_CHOICES, label=_("ListExample"), required=False)