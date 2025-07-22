from django import forms
from .models import Order, Review, CartItem, RATE_CHOICES
from .bulma_mixin import BulmaMixin


class OrderForm(BulmaMixin, forms.ModelForm):
    name = forms.CharField(label='Имя')
    phone = forms.CharField(label='Номер телефона')
    address = forms.CharField(label='Адрес доставки')

    class Meta:
        model = Order
        fields = ['name', 'phone', 'address']

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone')
        name = cleaned_data.get('name')
        address = cleaned_data.get('address')

        if phone:
            if not phone.startswith('+998'):
                self.add_error('phone', forms.ValidationError('Номер телефона должен начинаться с +998'))
            if len(phone) < 13:
                self.add_error('phone', forms.ValidationError('Некорректная длина номера телефона.'))
        
        if name and len(name) < 3:
            self.add_error('name', forms.ValidationError('Имя должно содержать не менее трех символов.'))
        
        return cleaned_data


class RateForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'input'}), label='Оставить отзыв')
    rate = forms.ChoiceField(
        choices=RATE_CHOICES,
        required=True,
        label='Оцените блюдо от 1 до 5',
    )

    class Meta:
        model = Review
        fields = ['text', 'rate']


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']
