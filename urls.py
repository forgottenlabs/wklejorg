from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.conf.urls.defaults import include
from django.conf import settings
from django.contrib import admin
admin.autodiscover()


from userstuff.models import UserProfile
from wklej.xmlrpc import rpc_handler

###############################################################################
###############################################################################
urlpatterns = patterns(
    '',
    (r'^admin/', include(admin.site.urls)),

    # serving statics:
    (r'^f/(.*)', 'django.views.static.serve',
     {'document_root': settings.FILES_ROOT}),
    (r'^static/(.*)', 'django.views.static.serve',
     {'document_root': settings.STATIC_ROOT}),

    # 403
    (r'^403/$', 'django.views.generic.simple.direct_to_template',
     {'template': '403.html'}),

    ### homepage
    (r'^$', 'wklejorg.homepage.homepage'),

    ### single paste:
    url(r'^id/(?P<id>\d+)/$', 'wklej.views.single', name="single"),
    # and it's txt version:
    url(r'^id/(?P<id>\d+)/txt/$', 'wklej.views.txt', name="txt"),
    # and it's downloadable:
    url(r'^id/(?P<id>\d+)/dl/$', 'wklej.views.download', name="download"),
    # responses
    url(r'^id/(?P<id>\d+)/re/$', 'wklej.views.re', name="reply"),
    # deletion
    url(r'^id/(?P<id>\d+)/delete/$', 'wklej.views.delete', name="delete"),


    ### single private paste:
    url(r'^hash/(?P<hash>\w+)/$', 'wklej.views.single', name="single"),
    # and it's txt version:
    url(r'^hash/(?P<hash>\w+)/txt/$', 'wklej.views.txt', name="txt"),
    # and it's downloadable:
    url(r'^hash/(?P<hash>\w+)/dl/$', 'wklej.views.download', name="download"),
    # and it's downloadable:
    url(r'^hash/(?P<hash>\w+)/delete/$', 'wklej.views.delete', name="delete"),


    ### list
    url(r'^own/$', 'wklej.views.own', name="own"),
    #(r'^wklejki/$', 'wklej.views.wklejki'),
    #url(r'^tag/(?P<tag>\w+)/$', 'wklej.views.with_tag', name="with_tag"),

    ### registartion stuff
    url(r'^accounts/register/$', 'registration.views.register',
        {'profile_callback': UserProfile.objects.create},
        name='registration_register'),

    url(r'^accounts/', include('registration.urls')),

    ### bunch of redirects
    url(r'^accounts/profile/$', 'django.views.generic.simple.redirect_to',
        {'url': '/'}),
    url(r'^logout/$', 'django.views.generic.simple.redirect_to',
        {'url': '/accounts/logout/'}),
    url(r'^login/$', 'django.views.generic.simple.redirect_to',
        {'url': '/accounts/login/'}),
    url(r'^zaloguj/$', 'django.views.generic.simple.redirect_to',
        {'url': '/accounts/login/'}),
    url(r'^register/$', 'django.views.generic.simple.redirect_to',
        {'url': '/accounts/register/'}),
    url(r'^rejestracja/$', 'django.views.generic.simple.redirect_to',
        {'url': '/accounts/register/'}),

    url(r'^reset/$',
        'django.contrib.auth.views.password_reset',
        {"template_name": 'registration/password_reset_form.dhtml'},
        name="password_reset"),

    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'template_name': 'registration/password_reset_confirm.dhtml'},
        name="password_reset_confirm"),

    url(r'^reset/done/$',
        'django.contrib.auth.views.password_reset_done',
        {"template_name": 'registration/password_reset_done.dhtml'},
        name="password_reset_done"),

    url(r'^reset/complete/$',
        'django.contrib.auth.views.password_reset_complete',
        {"template_name": 'registration/password_reset_complete.dhtml'},
        name="password_reset_complete"),

    url(r'^own/password/$', 'django.contrib.auth.views.password_change',
        {"template_name": 'registration/password_change_form.dhtml'},
        name="password_change"),

    url(r'^own/password/done/$',
        'django.contrib.auth.views.password_change_done',
        {"template_name": 'registration/password_change_done.dhtml'},
        name="password_change_done"),


    ## API:
    (r'^xmlrpc/$', rpc_handler),


    ### SALT:
    url(r'^salt/$', 'wklej.views.salt', name="salt"),

    ### Flatpages
    url(r'^regulamin/$', 'django.views.generic.simple.direct_to_template', {
        'template': 'flatpages/regulamin.html'
        }),
    url(r'^terms-of-use/$',
        'django.views.generic.simple.direct_to_template', {
            'template': 'flatpages/terms_of_service.html'
        }),
    url(r'^contact/$',
        'django.views.generic.simple.direct_to_template', {
            'template': 'flatpages/contact.html',
        }),
    url(r'^kontakt/$',
        'django.views.generic.simple.direct_to_template', {
            'template': 'flatpages/kontakt.html',
        }),
)
