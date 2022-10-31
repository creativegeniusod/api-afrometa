from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User


class SignUp(ModelForm):
	"""docstring for SignUp"""
	def __init__(self, *args, **kwargs):
		super(SignUp, self).__init__(*args, **kwargs)

		for visible in self.visible_fields():
			if 'checkbox' != visible.field.widget.input_type:
				visible.field.widget.attrs.update({'class': 'form-control  form-control-lg'})
				visible.field.help_text = None

	class Meta:
		model = User
		fields = ('username', 'email', 'password')



class EditProfile(ModelForm):

	def __init__(self, *args, **kwargs):
		super(EditProfile, self).__init__(*args, **kwargs)
		
		for visible in self.visible_fields():
			if 'checkbox' != visible.field.widget.input_type:
				visible.field.widget.attrs.update({'class': 'form-control'})
				visible.field.help_text = None


	class Meta:
		model = User
		fields = ('username', 'email', 'is_active', 'is_superuser')