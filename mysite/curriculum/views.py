from django.template import RequestContext
from django.shortcuts import render_to_response
from curriculum.query_processor import QueryProcesser


def analyze_request(request):
    processor = QueryProcesser()
    response_dict = {}

    if request.method == 'POST':
        response_dict.update(
            server_response=processor._process_user_request(
                request.POST['query']
                ),
            )

    return render_to_response(
        'curriculum/interface.html',
        response_dict,
        context_instance=RequestContext(request),
        )
