from django import forms
from post.models import BlogPost


class CreateBlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'image', 'price']


class UpdateBlogPostForm(forms.ModelForm):
    class Meta:  # define metadata for the form
        model = BlogPost
        fields = ['title', 'body', 'image', 'price']

    def save(self, commit=True):
        # Instance of the BlogPost model associated with the form
        blog_post = self.instance
        # Update the attributes of the BlogPost instance with cleaned data from the form
        blog_post.title = self.cleaned_data['title']
        blog_post.body = self.cleaned_data['body']
        blog_post.price = self.cleaned_data['price']

        # If a new image is provided in the form
        if self.cleaned_data['image']:
            blog_post.image = self.cleaned_data['image']

        # Save the changes to the BlogPost instance
        if commit:
            blog_post.save()
        # Return the updated BlogPost instance
        return blog_post
