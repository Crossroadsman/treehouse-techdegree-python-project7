
import json

from PIL import Image

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def cropper(request):
    template = 'image_edit/cropper.html'
    context = {}
    return render(request, template, context)


def upload_image(request):
    # Using AJAX

    image_file = request.FILES.get('image')
    msg = ""
    status = 0

    if image_file:
        # unedited image is passed in as a file attached to the form
        print("Image is in request.FILES")

        image_object = Image.open(image_file)

        print("getting user:")
        user = get_object_or_404(get_user_model(), pk=request.user.pk)
        print(user)

        print("checking for userprofile...")
        if hasattr(user, 'userprofile'):
            up_instance = user.userprofile
            print(up_instance)

            print("saving image:")
            up_instance.avatar = image_file
            up_instance.save()
            
            status = 1
            msg = "Ok"
        else:
            msg = "No user profile"
            print(msg)

    else:
        msg = "No image file"
        print(msg)
    
    url = reverse('accounts:profile')
    response = {
        'status': status,
        'message': msg,
        'url': url,
    }
    json_response = json.dumps(response)

    return HttpResponse(
        json_response,
        content_type="application/json"
    )
