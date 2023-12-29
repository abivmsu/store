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
from .models import Category, Book, Item, Store

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['category', 'book_name', 'description', 'grade', 'pages', 'subject','image']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['category', 'item_name','description','image']

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['books', 'items', 'quantity']

    books = forms.ModelMultipleChoiceField(
        queryset=Book.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2' }),required = False,
    )

    items = forms.ModelMultipleChoiceField(
        queryset=Item.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),required = False,
    )

    def __init__(self, *args, **kwargs):
        super(StoreForm, self).__init__(*args, **kwargs)
        self.fields['books'].queryset = Book.objects.all()
        self.fields['items'].queryset = Item.objects.all()
