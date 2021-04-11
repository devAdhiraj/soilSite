from django.http import HttpResponse
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
from django.shortcuts import render, redirect
from .forms import ImageForm
from .models import ImageModel


def home_view(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            a = identify_comp()
            print(a[1])
            return redirect(identify_comp())
    else:
        form = ImageForm()
    return render(request, 'pages/home.html', {'form': form})


def loam_view(request, comp):
    a = comp.split(',')
    context = {
        'iron': a[0],
        'magnesium': a[1],
        'water': a[2],
    }
    return render(request, 'pages/loam.html', context)


def silt_view(request, comp):
    a = comp.split(',')
    context = {
        'iron': a[0],
        'magnesium': a[1],
        'water': a[2],
    }
    return render(request, 'pages/silt.html', context)


def clay_view(request, comp):
    a = comp.split(',')
    context = {
        'iron': a[0],
        'magnesium': a[1],
        'water': a[2],
    }
    return render(request, 'pages/clay.html', context)


def loam_view2(request):
    context = {
        'iron': None,
        'magnesium': None,
        'water': None,
    }
    return render(request, 'pages/loam.html', context)


def silt_view2(request):
    context = {
        'iron': None,
        'magnesium': None,
        'water': None,
    }
    return render(request, 'pages/silt.html', context)


def clay_view2(request):
    context = {
        'iron': None,
        'magnesium': None,
        'water': None,
    }
    return render(request, 'pages/clay.html', context)


def identify_comp():
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = tensorflow.keras.models.load_model('pages/Composition.h5', compile=False)

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    imgSrc = str(ImageModel.objects.last().img.url)[1:]
    image = Image.open(imgSrc)
    # resize the image to a 224x224 with the same strategy as in TM2:
    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # display the resized image
    # image.show()

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    print("Iron " + str(prediction[0][0]) + "%\nMagnesium / Calcium " + str(
        prediction[0][1]) + "%\nWater Retention " + str(prediction[0][2]) + "%")

    comp = str(prediction[0][0]) + "," + str(prediction[0][1]) + "," + str(prediction[0][2])
    return identify_img(comp)


def identify_img(comp):
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    imgSrc = str(ImageModel.objects.last().img.url)[1:]
    model = tensorflow.keras.models.load_model('pages/keras_model.h5', compile=False)

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(imgSrc)

    # resize the image to a 224x224 with the same strategy as in TM2:
    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # display the resized image
    # image.show()

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    print("Loam " + str(prediction[0][0]) + "%\nSilt " + str(prediction[0][1]) + "%\nClay " + str(prediction[0][2]) + "%")

    if prediction[0][0] > prediction[0][1] and prediction[0][0] > prediction[0][2]:
        return '../loam-soil' + "/" + comp

    elif prediction[0][1] > prediction[0][0] and prediction[0][1] > prediction[0][2]:
        return '../silt-soil' + "/" + comp
    else:
        return '../clay-soil' + "/" + comp

