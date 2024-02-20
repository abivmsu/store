from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class ProfileForm(UserCreationForm):
  
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={'class': 'form-control form-control-sm','placeholder': 'Email address'}))
    first_name = forms.CharField(max_length=30, label="",widget=forms.TextInput(attrs={'class': 'form-control form-control-sm ','placeholder':'first Name'}))
    last_name = forms.CharField(max_length=30, label="", widget=forms.TextInput(attrs={'class': 'form-control form-control-sm ','placeholder': 'Last Name'}))
    # password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control-sm '}))
    # confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control-sm '}))

    class Meta:
      model = User
      fields = ('username','first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__ (self, *args, **kwargs):

      super(ProfileForm, self).__init__(*args, **kwargs)

      self.fields['username'].widget.attrs['class'] = 'form-control form-control-sm'
      self.fields['username'].widget.attrs['placeholder'] = 'User Name'
      self.fields['username'].label = ''
      self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
      #self.fields['username'] = forms.CharField(help_text=mark_safe('<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'))
      
      
      self.fields['password1'].widget.attrs['class'] = 'form-control form-control-sm'
      self.fields['password1'].widget.attrs['placeholder'] = 'Password'
      self.fields['password1'].label = ''
      self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

      self.fields['password2'].widget.attrs['class'] = 'form-control form-control-sm'
      self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
      self.fields['password2'].label = ''
      self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email']

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )


class TeacherForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email']  # Customize fields as needed
      
