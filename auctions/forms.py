from django.forms import ModelForm,TextInput
from .models import User,Listing,Bid,Comment

class CreateBid(ModelForm):
    class Meta:
        model=Listing
        fields=('title',
                'image',
                'description',
                'initial_bid'
        )
        widgets={'title':TextInput(attrs={'class': 'form-control form-group',
                                            'placeholder': 'Give it a title'}),
                'image':TextInput(attrs={'class': 'form-control form-group',
                                        'placeholder': 'Image URL (optional)',}),
                'description':TextInput(attrs={'class': 'form-control form-group',
                                                'id':"exampleFormControlTextarea1",
                                                'placeholder': 'Tell more about the product',
                                                'rows': "4",}),
                'initial_bid':TextInput(attrs={'class': 'form-control form-group',
                                                'placeholder': 'Starting bid',

                })
            }
class CommentForm(ModelForm):
    class Meta:
        model=Comment
        fields=['text',
            ]

# class BidForm(ModelForm):
#     class Meta:
#         model=Bid
#         fields=['amount'
#         ]