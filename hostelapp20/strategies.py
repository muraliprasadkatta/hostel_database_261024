from social_django.strategy import DjangoStrategy

class CustomSocialStrategy(DjangoStrategy):
    def start(self):
        # Capture the intent from the query parameters and store it in the session
        action = self.request.GET.get('action')
        if action:
            self.request.session['social_auth_action'] = action
        return super().start()
