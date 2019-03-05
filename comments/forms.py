# -*- coding: utf-8 -*-
from django import forms
from .models import Comment
from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper


class CommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.post_id = kwargs.pop('post_id', None)
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', '提交'))

    class Meta:
        model = Comment
        fields = ('content',)
        labels = {
            'content': '',
        }

    def save(self, commit=True):
        inst = super(CommentForm, self).save(commit=False)
        inst.user = self.user
        inst.post_id = self.post_id
        if commit:
            inst.save()
            self.save_m2m()
        return inst
