from datetime import datetime

from core.security.models import Dashboard


def system_information(request):
    dashboard = Dashboard.objects.first()
    parameters = {
        'dashboard': dashboard,
        'date_joined': datetime.now(),
        'menu': 'hztbody.html' if dashboard is None else dashboard.get_template_from_layout()
    }
    return parameters
