from rest_framework.throttling import SimpleRateThrottle

class OncePerDayThrottleForAnonymous(SimpleRateThrottle):
    scope = 'once_per_day_for_anonymous'

    def get_cache_key(self, request, view):
        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }

    def get_rate(self):
        return '1/day'