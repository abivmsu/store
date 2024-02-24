from django import forms
from .models import  Book, Item, Store, Order, Product, ProductGiven, ProductGivenDetail


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

# class StaffOrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['unit', 'quantity', 'subunit', 'subunit_quantity']
#         widgets = {
#             'unit': forms.Select(attrs={'class': 'form-control'}),
#             'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
#             'subunit': forms.Select(attrs={'class': 'form-control', 'onchange': 'updateSubunitQuantity()'}), # Add onchange event to trigger JavaScript function
#             'subunit_quantity': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}), # Set readonly attribute initially
#             }

#     def __init__(self, *args, **kwargs):
#         super(StaffOrderForm, self).__init__(*args, **kwargs)
#         # Customize the form if needed
#         self.fields['subunit'].required = False
#         self.fields['subunit_quantity'].required = False

#         # Add JavaScript function to update subunit_quantity based on subunit selection
#         self.fields['subunit'].widget.attrs['onchange'] = 'updateSubunitQuantity();'

class StaffOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['unit', 'quantity', 'subunit', 'subunit_quantity']
        widgets = {
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'subunit': forms.Select(attrs={'class': 'form-control', 'onchange': 'updateSubunitQuantity()'}),
            'subunit_quantity': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
        }
        error_messages = {
            'unit': {'required': 'Please select a unit.'},
            'quantity': {'required': 'Please enter a quantity.', 'invalid': 'Invalid quantity.'},
        }

    def __init__(self, *args, **kwargs):
        super(StaffOrderForm, self).__init__(*args, **kwargs)
        self.fields['subunit'].required = False
        self.fields['subunit_quantity'].required = False
        self.fields['subunit'].widget.attrs['onchange'] = 'updateSubunitQuantity();'

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control'})
            }

            
#############################################################################
#############################################################################
#############################################################################
#############################################################################

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name']


class ProductGivenForm(forms.ModelForm):
    class Meta:
        model = ProductGiven
        fields = ['provider', 'teacher', 'notes']
     

class ProductGivenDetailForm(forms.ModelForm):
    class Meta:
        model = ProductGivenDetail
        fields = ['product', 'quantity', 'date_given', 'notes']
        widgets = {
            'product': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_given': forms.DateInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super(ProductGivenDetailForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()  # Queryset for the product field