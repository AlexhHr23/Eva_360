from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token
from django.views.generic import TemplateView

from core.security.models import Dashboard


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'panel.html'

    def get(self, request, *args, **kwargs):
        request.user.set_group_session()
        request.session['module'] = None
        data = self.get_context_data()
        dashboard = Dashboard.objects.filter()
        if dashboard.exists():
            if dashboard[0].layout == 1:
                return render(request, 'vtcpanel.html', data)
        return render(request, 'hztpanel.html', data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Panel de administración'
        return context


@requires_csrf_token
def error_404(request, exception):
    return render(request, '404.html', {})


@requires_csrf_token
def error_500(request, exception):
    return render(request, '500.html', {})
