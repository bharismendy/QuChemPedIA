from django import forms


class SearchUserForm(forms.Form):
    """
        The purpose of this form is to make research in the PostGreSQL database for user
    """
    CHOICES = (('ID', 'ID'),
               ('first_name', 'First name'),
               ('last_name', 'Last name'),
               ('affiliation', 'Affiliation'),
               ('mail', 'Mail')
               )

    search = forms.CharField(widget=forms.TextInput(attrs={'id': 'research_entry','class' : 'mb-1 col-12 col-lg-6 form-control'}),
                             max_length=500, label="", required=False)
    typeQuery = forms.CharField(widget=forms.Select(choices=CHOICES, attrs={'class': 'custom-select col-12 col-lg-3'}), label="",
                                required=False,)