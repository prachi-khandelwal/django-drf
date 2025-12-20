from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class BurstRateThrottle(UserRateThrottle):
    """
    Throttle class for expensive/burst operations.
    Allows only 3 requests per minute regardless of user type.
    """
    scope = 'burst'


class StrictAnonRateThrottle(AnonRateThrottle):
    """
    Extra strict throttle for anonymous users on sensitive endpoints.
    Useful for login, signup, password reset to prevent brute force attacks.
    """
    scope = 'strict_anon'

