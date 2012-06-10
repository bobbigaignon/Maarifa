from django.template import RequestContext
from django.shortcuts import render_to_response

def analyze_request(request):
    return render_to_response(
        'curriculum/interface.html',
        {},
        context_instance=RequestContext(request),
    )
