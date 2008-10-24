from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.cache import cache_control
from cStringIO import StringIO
import Image,ImageDraw,ImageFont
from random import random

def image(request):
    """ Create new image using python image library """

    numbers = (int(random()*40)+10,int(random()*40)+10)
    text = "%d+%d" % numbers
    answer = sum(numbers)

    # text = token_id
    # Create new image
    ablue = (0, 0, 0)
    aorange = (0, 255, 2525)
    image = Image.new('RGB', (90, 30), ablue)
    # Set font and its size
    font = ImageFont.truetype(settings.CAPTCHA_FONT_PATH,\
                              settings.CAPTCHA_FONT_SIZE)

    # Draw the text, starting from (2,2) so the text won't be edge
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font, fill=aorange)
    # create grid
    size = 8
    offset = 0
    draw = ImageDraw.Draw(image)
    for i in xrange(image.size[0] / size + 1):
        draw.line((i*size+offset, 0, i*size+offset, image.size[1]), \
                  fill=aorange)

    for i in xrange(image.size[0] / size + 1):
        draw.line((0, i*size+offset, image.size[0], i*size+offset), \
                  fill=aorange)
    # Saves the image in a StringIO object, so you can write the response
    # in a HttpResponse object

    out = StringIO()
    image.save(out, "JPEG")
    out.seek(0)
    request.session['captcha_answer'] = answer
    response = HttpResponse()
    response['Content-Type'] = 'image/jpeg'
    response.write(out.read())
    return response
