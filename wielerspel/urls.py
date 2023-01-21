from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
#import debug_toolbar


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('results.urls', 'results'), namespace='results')),
    path('auction/', include(('auction.urls', 'auction'), namespace='auction')),
    #path('veiling/', include('veiling.urls')),
    #path('veiling-tweede-ronde/', include('veilingeentjes.urls')),
    

    #path('__debug__/', include(debug_toolbar.urls)),
    path('accounts/',include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns