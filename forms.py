from django.forms import Form
from django.forms import fields
from django.forms import widgets
from django.core.exceptions import ValidationError
class FamousForm(Form):
    name = fields.CharField(error_messages={
        "required":"名字不能为空"},
        widget=widgets.TextInput(attrs={'class':'form-control'})
    )
    cname = fields.CharField(required=False,
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    cfname = fields.CharField(required=False,
                             widget=widgets.TextInput(attrs={'class': 'form-control'})
                             )
    ename = fields.CharField(required=False,
                             widget=widgets.TextInput(attrs={'class': 'form-control'})
                             )
    efname = fields.CharField(required=False,
                             widget=widgets.TextInput(attrs={'class': 'form-control'})
                             )
    othername = fields.CharField(required=False,
                             widget=widgets.TextInput(attrs={'class': 'form-control'})
                             )
    describe = fields.CharField(required=False,
                             widget=widgets.TextInput(attrs={'class': 'form-control'})
                             )
    introduction = fields.CharField(required=False,
                                widget=widgets.Textarea(attrs={'class': 'form-control'})
                                )
    content = fields.CharField(error_messages={
        "required":"名言不能为空"},widget=widgets.Textarea(attrs={'class': 'form-control'}))
    tag = fields.CharField(required=False,
                                widget=widgets.TextInput(attrs={'class': 'form-control'})
                                )







