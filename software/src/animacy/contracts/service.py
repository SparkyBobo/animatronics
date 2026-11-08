"""
DaBones

Service routine contracts.

Copyright (c) 2026 Sparky Bobo
"""

# An indication of service activity.
class ServiceResult:
    """Service ResultEnumeration"""
    IDLE = 0
    ACTIVITY = 1
    LOADED = 2
    EXIT = 100

# A service-able routine such as an event loop
class Service:
    def service(self) -> ServiceResult:
        return ServiceResult.IDLE
