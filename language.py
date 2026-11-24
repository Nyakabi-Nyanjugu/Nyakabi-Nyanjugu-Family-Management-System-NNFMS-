from django.utils.deprecation import MiddlewareMixin

class FamilyLanguageMiddleware(MiddlewareMixin):
    def process_request(self, request):
        selected = request.GET.get('lang')
        if selected in ('sw', 'en'):
            request.session['family_language'] = selected
        request.family_language = request.session.get('family_language', 'sw')
