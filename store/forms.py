# from django import forms
# from django_select2.forms import ModelSelect2MultipleWidget
# from .models import Category, Book, Item, Store

# class CategoryForm(forms.ModelForm):
#     class Meta:
#         model = Category
#         fields = ['name']

# class BookForm(forms.ModelForm):
#     class Meta:
#         model = Book
#         fields = ['category', 'book_name', 'grade', 'pages', 'subject']

# class ItemForm(forms.ModelForm):
#     class Meta:
#         model = Item
#         fields = ['category', 'item_name']

# class StoreForm(forms.ModelForm):
#     class Meta:
#         model = Store
#         fields = ['books', 'items', 'quantity']

#     books = forms.ModelMultipleChoiceField(
#         queryset=Book.objects.all(),
#         widget=ModelSelect2MultipleWidget(
#             model=Book,
#             search_fields=['book_name__icontains'],
#         ),
#     )

#     items = forms.ModelMultipleChoiceField(
#         queryset=Item.objects.all(),
#         widget=ModelSelect2MultipleWidget(
#             model=Item,
#             search_fields=['item_name__icontains'],
#         ),
#     )

#     def __init__(self, *args, **kwargs):
#         super(StoreForm, self).__init__(*args, **kwargs)
#         self.fields['books'].queryset = Book.objects.all()
#         self.fields['items'].queryset = Item.objects.all()


from django import forms
from .models import Category, Book, Item, Store, Order

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_name', 'description', 'grade', 'pages', 'subject', 'image']

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    book_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    grade = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    pages = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input'}))
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    item_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control custom-file-input'}))

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['unit', 'quantity', 'subunit', 'subunit_quantity', 'price', 'tax']
        widgets = {
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'subunit': forms.Select(attrs={'class': 'form-control', 'onchange': 'updateSubunitQuantity()'}), # Add onchange event to trigger JavaScript function
            'subunit_quantity': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}), # Set readonly attribute initially
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'tax': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        # Customize the form if needed
        self.fields['subunit'].required = False
        self.fields['subunit_quantity'].required = False

        # Add JavaScript function to update subunit_quantity based on subunit selection
        self.fields['subunit'].widget.attrs['onchange'] = 'updateSubunitQuantity();'

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['quantity']

    # books = forms.ModelMultipleChoiceField(
    #     queryset=Book.objects.all(),
    #     widget=forms.SelectMultiple(attrs={'class': 'select2' }),required = False,
    # )

    # items = forms.ModelMultipleChoiceField(
    #     queryset=Item.objects.all(),
    #     widget=forms.SelectMultiple(attrs={'class': 'select2'}),required = False,
    # )

    # def __init__(self, *args, **kwargs):
    #     super(StoreForm, self).__init__(*args, **kwargs)
    #     self.fields['books'].queryset = Book.objects.all()
    #     self.fields['items'].queryset = Item.objects.all()
