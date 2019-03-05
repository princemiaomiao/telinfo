# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Fieldset, HTML, Div
from crispy_forms.bootstrap import TabHolder, Tab
from .models import Post


class LoginForm(forms.Form):
    uid = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'uid', 'placeholder': 'Username'}))
    pwd = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'pwd', 'placeholder': 'Password'}))


class SearchForm(forms.Form):
    keyword = forms.CharField(widget=forms.TextInput)


class PostForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', "Submit", css_class="btn-success"))
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset('Basic Info',
                     Field('company_name', title='company name', css_class="span6 m-wrap"),
                     Field('tel_no', title="input telephone number", css_class="span6 m-wrap"),
                     Field('consultee', title='caller name', css_class="span6 m-wrap"),
                     Field('title', title='mainframe', css_class="span6 m-wrap"),
                     Field('content', title='information', css_class="span6 m-wrap"),
                     ),
            Fieldset('Contact data',
                     Field('pricing', title='pricing', css_class="span6 m-wrap"),
                     Field('assign_person', title='personnel', css_class="span6 m-wrap"),
                     style="color: brown;"),
            Fieldset('Category Infos',
                     Field('category', title='categories', css_class="span6 m-wrap"),
                     Field('tags', title='tags', css_class="span6 m-wrap"),
                     Field('published', title='published'),
                     ),
            Fieldset('Result Field',
                     TabHolder(Tab('results', 'result'),
                               Tab('remarks', 'remarks'))
                     )
        )

    class Meta:
        model = Post
        fields = ['category', 'tags', 'title', 'company_name', 'tel_no', 'consultee', 'content', 'assign_person',
                  'result', 'pricing', 'published', 'remarks']
        labels = {
            'category': '类别',
            'tags': '标签',
            'title': '标题',
            'company_name': '公司名称',
            'tel_no': '电话号码',
            'consultee': '咨询者',
            'content': '咨询内容',
            'assign_person': '上门人员',
            'result': '沟通结果',
            'pricing': '协议价单号',
            'published': '录入完成',
            'remarks': '备注',
        }

    def save(self, commit=True):
        inst = super(PostForm, self).save(commit=False)
        inst.user = self.user
        if commit:
            inst.save()
            self.save_m2m()
        return inst


class PostEditForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(PostEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', "提交", css_class="btn-success"))
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(u"基本信息",
                     Field('company_name', title='company name', css_class="span6 m-wrap"),
                     Field('tel_no', title="input telephone number", css_class="form-control input-mask-phone"),
                     Field('consultee', title='caller name', css_class="span6 m-wrap"),
                     ),
            Fieldset(u"咨询内容",
                     Field('title', title='mainframe', css_class="span6 m-wrap"),
                     Field('content', title='information', css_class="span6 m-wrap"),
                     Field('pricing', title='pricing', css_class="span6 m-wrap"),
                     Field('assign_person', title='personnel', css_class="span6 m-wrap"),
                     style="color: brown;"),
            Fieldset(u"咨询范围",
                     Field('category', title='categories', css_class="span6 m-wrap"),
                     Field('tags', title='按住Ctrl多选', css_class="span6 m-wrap"),
                     Field('published', title='published'),
                     ),
            Fieldset(u"咨询结果",
                     TabHolder(Tab('results', 'result'),
                               Tab('remarks', 'remarks'))
                     )
        )

    class Meta:
        model = Post
        fields = ['category', 'tags', 'title', 'company_name', 'tel_no', 'consultee', 'content', 'assign_person',
                  'result', 'pricing', 'published', 'remarks']
        labels = {
            'category': '类别',
            'tags': '标签',
            'title': '标题',
            'company_name': '公司名称',
            'tel_no': '电话号码',
            'consultee': '咨询者',
            'content': '咨询内容',
            'assign_person': '上门人员',
            'result': '沟通结果',
            'pricing': '协议价单号',
            'published': '录入完成',
            'remarks': '备注',
        }


class StepOneForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(StepOneForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(u"基本信息",
                     Field('tel_no', title="输入来电号码", css_class="form-control input-mask-phone"),
                     HTML(""u"<p>提示用语:您好,这里是景鸿物流,很高兴为您服务</p>"""),
                     Div(css_class="span12"),
                     Field('consultee', title='咨询对象', css_class="span6 m-wrap"),
                     HTML(""u"<p>提示用语:您方便告诉我您服务的公司全称吗?</p>"""),
                     Div(css_class="span12"),
                     Field('company_name', title='公司名称', css_class="span6 m-wrap"),
                     HTML(""u"<p>提示用语:请问有什么可以帮到您?</p>"""),
                     ),
        )

    class Meta:
        model = Post
        fields = ['company_name', 'tel_no', 'consultee']
        labels = {
            'company_name': '公司名称',
            'tel_no': '电话号码',
            'consultee': '咨询者',
        }


class StepTwoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(StepTwoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(u"咨询内容",
                     HTML(""u"<p>提示用语:请问您的企业所处的行业?</p>"""),
                     Field('category', title='所处行业', css_class="span6 m-wrap"),
                     Div(css_class="span12"),
                     HTML(""u"<p>提示用语:需要本公司供哪些物流服务?</p>"""),
                     Field('tags', title='按住Ctrl多选', css_class="span6 m-wrap"),
                     Div(css_class="span12"),
                     HTML(""u"<p>提示用语:请问需要咨询哪些方面的内容?</p>"""),
                     Field('title', title='mainframe', css_class="span6 m-wrap"),
                     Div(css_class="span12"),
                     HTML(""u"<p>提示用语:能否留下更具体的咨询内容和联系方式。</p>"""),
                     Field('content', title='information', css_class="span6 m-wrap"),
                     Div(css_class="span12"),
                     HTML(""u"<p>提示用语:是否需要报价?</p>"""),
                     Field('pricing', title='pricing', css_class="span6 m-wrap"),
                     ),
        )

    class Meta:
        model = Post
        fields = ['category', 'tags', 'title', 'content', 'pricing']
        labels = {
            'category': '类别',
            'tags': '标签',
            'title': '标题',
            'content': '咨询内容',
            'pricing': '协议价单号',
        }


class StepThreeForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(StepThreeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(u"咨询结果",
                     HTML(""u"<p>提示用语:是否需要上门进一步沟通?</p>"""),
                     Field('assign_person', title='上门人员', css_class="span6 m-wrap"),
                     HTML(""u"<p>提示用语:感谢您的来电，我们会马上安排上门人员和您联系，后续如果有其他需要仍可致电我司。</p>"""),
                     Div(css_class="span12"),
                     Field('published', title='是否填写完成，勾选成将无法再更改'),
                     Div(css_class="span12"),
                     Field('result', title='结果', css_class="span6 m-wrap"),
                     HTML(""u"<p>提示用语:感谢您的来电。</p>"""),
                     Div(css_class="span12"),
                     Field('remarks', title='备注', css_class="span6 m-wrap"),
                     HTML(""u"<p>提示用语:还有没有其他别的需要咨询。</p>"""),
                     style="color: brown;"),
        )

    class Meta:
        model = Post
        fields = ['assign_person', 'result', 'published', 'remarks']
        labels = {
            'assign_person': '上门人员',
            'result': '沟通结果',
            'published': '录入完成',
            'remarks': '备注',
        }
