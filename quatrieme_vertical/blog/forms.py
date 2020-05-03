from django import forms

class CommentForm(forms.Form):
	name = forms.CharField(
		label='Nom',
		max_length=100,
		widget=forms.TextInput(attrs={'class': 'form-control'}),
		required=True
	)
	email = forms.EmailField(
		label='Votre email',
		widget=forms.EmailInput(attrs={'class': 'form-control'}),
		required=True
	)
	message = forms.CharField(
		label='Commentaire',
		widget=forms.TextInput(attrs={'class': 'form-control'}),
		required=True
	) 