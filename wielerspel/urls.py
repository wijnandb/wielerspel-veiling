from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
import debug_toolbar


urlpatterns = [
    path('', RedirectView.as_view(url='/results/', permanent=False)),
    path('', include('auction.urls')),
    path('veiling/', include('veiling.urls')),
    #path('veiling-tweede-ronde/', include('veilingeentjes.urls')),
    path('results/', include('results.urls')),
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
]
