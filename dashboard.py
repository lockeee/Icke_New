from django.utils.translation import ugettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard
from jet.dashboard.dashboard_modules import google_analytics

class CustomIndexDashboard(Dashboard):
    columns = 2