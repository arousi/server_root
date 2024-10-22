from django.middleware.csrf import CsrfViewMiddleware

class DisableCSRFMiddleware(CsrfViewMiddleware):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        if request.path.startswith('/signup'):  # Replace with your desired URL pattern
            return None
        return super().process_view(request, callback, callback_args, callback_kwargs)