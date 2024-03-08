from django.http import JsonResponse

class ServerExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # Customize the error response
        error_response = {
            'error': 'Something went wrong on the server'
        }
        return JsonResponse(error_response, status=500)
