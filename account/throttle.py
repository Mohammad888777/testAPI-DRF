from rest_framework.throttling import UserRateThrottle


class RegisterThrottle(UserRateThrottle):
    scope="register"
     


class ForBlockedForEverThottle(UserRateThrottle):
    scope="for-ever-block"