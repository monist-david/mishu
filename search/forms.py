from django import forms


class SearchForm(forms.Form):
    product_name = forms.CharField(label='product_name', max_length=100)
    # product_price_range_min = forms.FloatField(label='product_price_range_min')
    # product_price_range_max = forms.FloatField(label='product_price_range_max')
    product_style = forms.CharField(label='product_style', max_length=100)
    product_functionality = forms.CharField(label='product_style', max_length=100)
    product_comment = forms.CharField(label='product_comment', max_length=100)
