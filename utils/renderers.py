from rest_framework import renderers

class CountRenderer(renderers.JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = {'count': len(data), 'results': data}
        return super().render(response_data, accepted_media_type, renderer_context)