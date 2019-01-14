from django import forms
from django.contrib.auth.models import User
from .models import Client
from .models import SocialNetwork


"""
Constants
"""

"""Function
"""

def must_be_gt(value_password):

  if len(value_password) < 5:
    raise forms.ValidationError('el pass es muy corta')
  return value_password


"""
Class
"""




class LoginForm(forms.Form):
  username = forms.CharField(max_length=20)
  password = forms.CharField(max_length=20, widget = forms.PasswordInput() )

  def __init__(self, *args, **kwargs):
    super(LoginForm, self).__init__(*args, **kwargs)
    self.fields['username'].widget.attrs.update( { 'class':'username_login' } )
    self.fields['password'].widget.attrs.update( { 'class':'password_login', 'id':'id_pwd_login' } )

class createUserForm(forms.ModelForm):

  username = forms.CharField(max_length=20)
  password = forms.CharField(max_length=20, widget = forms.PasswordInput() )
  email = forms.CharField()
  

  def clean_email(self):
    email = self.cleaned_data.get('email')
    var = User.objects.filter(email=email)

    if var.exists().count():
      raise forms.ValidationError('Email debe ser unico')

    return email

  class Meta:
    #siempre especificar atributos cuando se trabajan en formulario de clase
    model = User
    fields = ('username', 'password', 'email')

class EditUserForm(forms.ModelForm):
  username = forms.CharField(max_length=20)
  email = forms.CharField()


  class Meta:
    model = User
    fields = ('username', 'email', 'first_name', 'last_name')

  def clean_email(self):
    email = self.cleaned_data.get('email')
    var = User.objects.filter(email=email)

    if var.exclude(pk = self.instance.id).count():
      raise forms.ValidationError('Email debe ser unico')

    return email


class EditPasswordForm(forms.Form):
  password = forms.CharField(max_length=20, widget = forms.PasswordInput() )
  new_password = forms.CharField(max_length=20, widget = forms.PasswordInput(), validators = [must_be_gt] )
  repeate_password = forms.CharField(max_length=20, widget = forms.PasswordInput(), validators = [must_be_gt] )

  def clean(self):
    clean_data = super(EditPasswordForm, self).clean()
    password1 = clean_data.get('new_password')
    password2 = clean_data.get('repeate_password')

    if(password1 != password2):
      raise forms.ValidationError('las pass no coinciden')


class EditClientForm(forms.ModelForm):
  class Meta:
    model = Client
    exclude = ['user']



class EditSocialNetwork(forms.ModelForm):
    class Meta:
      model = SocialNetwork
      exclude = ['user'] 

