from .tracked_groups import TrackedGroupsFilter
from .admins import AdminsFilter
from loader import dp

if __name__ == "filters":
    dp.filters_factory.bind(TrackedGroupsFilter, event_handlers=[
        dp.message_handlers
    ])
    dp.filters_factory.bind(AdminsFilter, event_handlers=[
        dp.message_handlers, 
        dp.callback_query_handlers
    ])
