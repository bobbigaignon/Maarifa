from django.template import Context, loader
from django.shortcuts import render_to_response

def index(request):
    loader.get_template('curriculum/interface.html')
    return render_to_response('curriculum/interface.html', {})
