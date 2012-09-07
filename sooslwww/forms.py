# -*- coding: utf-8 -*-
from django import forms

class AddSignForm(forms.Form):
    videoFile = forms.FileField(
	label='Please choose a video file to upload.'
    )

class AddGlossForm(forms.Form):
    gloss_text = forms.CharField(
	       widget=forms.TextInput(attrs={'size':'10',
					     'max_lenth': '128'})
    )
