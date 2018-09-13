from django.shortcuts import render, redirect, reverse

from accounts.models import UserProfile, Avatar
from image_editor.forms import AvatarEditForm



# for edit avatar, we want to check if user has an avatar
# if they do, load it and supply it to the form as an initial value

# if they don't, display a blank form
# if any submission button except save is selected
# create (or edit) an Avatar instance with the loaded image set to the temp
# image attribute

# then pass the temp image to pillow to perform whichever operation was selected

# then reload the page with the pillow-edited temp image as the initial value

# when save is selected, set the avatar attribute to the temp image and the
# temp image to None

def edit_avatar(request):
    form = AvatarEditForm()
    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect(reverse('accounts:profile'))

        form = AvatarEditForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            print("image url: {}".format(cleaned_data['temp_image']))
            print("pos 1: ({}, {})".format(cleaned_data['x1'], cleaned_data['y1']))
            print("pos 2: ({}, {})".format(cleaned_data['x2'], cleaned_data['y2']))
            if 'save' in request.POST:
                # set the avatar to be the temp image
                return redirect(reverse('accounts:profile'))
            
            if 'crop' in request.POST:
                # do the crop operation
                # then reload the page
                print('crop')
            elif 'rotate-left' in request.POST:
                # do the rotate operation
                # then reload the page
                print('RL')
            elif 'rotate-right' in request.POST:
                # do the rotate operation
                # then reload the page
                print('RR')
            elif 'flip-horizontal' in request.POST:
                # do the flip operation
                # then reload the page
                print('FH')
            elif 'flip-vertical' in request.POST:
                # do the flip operation
                # then reload the page
                print('FV')
    context = {'form': form}
    template = 'image_editor/avatar.html'
    return render(request, template, context)