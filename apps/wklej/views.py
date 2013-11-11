#coding: utf-8

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from wklej.forms import RotateSyntaxForm
from wklej.forms import WklejkaForm
from wklej.models import Wklejka, BANNED_LEXERS


def single(request, id=0, hash=''):
    """
    This is very important view because it displays a single paste.
    It's actually the most viewed view ever
    """

    if id:
        w = get_object_or_404(Wklejka, pk=id, is_private=False)
    elif hash:
        w = get_object_or_404(Wklejka, hash=hash, is_private=True)

    hl = request.GET.get('hl', w.syntax) or w.guessed_syntax or 'python'
    if hl in BANNED_LEXERS:
        hl = w.guessed_syntax or 'python'

    syntaxform = RotateSyntaxForm(label_suffix='', initial={'hl': hl})

    return TemplateResponse(
        request, "wklej/single.dhtml", {
            'w': w,
            'hl': hl,
            'rsform': syntaxform
        },
    )


def txt(request, id=0, hash=0):
    """
    This one tooks care of txt view for single paste.
    It display it's content without syntax highlighting, with mimetype
    text/plain which (by most browsers) should be taken care of
    as a plaintext document. It does both private (using hash) and public
    (using id) pastes.
    """

    if id:
        w = get_object_or_404(Wklejka, pk=id, is_private=False)
    elif hash:
        w = get_object_or_404(Wklejka, hash=hash, is_private=True)

    return HttpResponse(w.body, mimetype='text/plain; charset=utf-8')


def download(request, id=0, hash=0):
    """
    This view is responsible for downloading a single paste.
    It literally force (due to mime app/x-force-download) browser to download
    a specially prepared request.

    # New in wklej .v04: its adding proper extension based on hilighting
    (either chosen or guessed by pygments), insted of older .wklej extension
    """

    if id:
        w = get_object_or_404(Wklejka, pk=id, is_private=False)
    elif hash:
        w = get_object_or_404(Wklejka, hash=hash, is_private=True)

    # Based on w.body and w.hl i add special mimetype and return response
    response = HttpResponse(w.body, mimetype="application/x-force-download")
    final_ext = (w.syntax or w.guessed_syntax or "wklej")
    filename = 'attachment; filename=' + str(w.id) + "." + final_ext
    response['Content-Disposition'] = filename
    return response


def re(request, id=0):
    """
    This view represents a "respond" page, where users can add
    pastes 'in respond' to some other pastes.

    It works only with public pastes (since it would be hard to pass
    an url of private paste to the user, so he could see what paste this
    response is for.) ← actually, this is important because i couldn't figure
    out why i blocked respones for private pastes in 03 version :P

    Through the GET you can pass an optional argument ?s=True, where s is short
    for "source" which mean "display content of original paste in the form

    It doesn't count what you pass as value to s, since where you pass
    anything it is processed as a string, and so it has positive length
    it is considered as True.
    """

    w = get_object_or_404(Wklejka, pk=id, is_private=False)

    # then i check whether the s variable is passed:
    s = request.GET.get("s", '')

    form = WklejkaForm()

    return TemplateResponse(
        request, "homepage.dhtml", {
            'w': w,
            'form': form,
            'source': s,
        }
    )


@login_required
def delete(request, id=0, hash=''):
    """
    This view is responsible for deleting a single paste,
    both private and public one's.

    For safety reasons it displays a form with 'yes' and 'no' buttons
    and then check via POST which one was clicked.

    It's not idiot proof and far from perfect, but it's a lot better
    than just removing paste because someone just clicked on faked URL.

    template: wklej/delete.dhtml
    context: w - wklejka instance
    """

    if id:
        w = get_object_or_404(Wklejka, pk=id, is_private=False)
    elif hash:
        w = get_object_or_404(Wklejka, hash=hash, is_private=True)

    if request.method == 'POST':
        if request.POST.get('yes', ''):
            if w.user == request.user:
                w.is_deleted = True
                w.body = "[deleted]"
                w.save()

        return HttpResponseRedirect(w.get_absolute_url())

    return TemplateResponse(
        request, "delete.dhtml", {'w': w}
    )


@login_required
def own(request):
    """
    This view will list a list of users pastes.
    It's using generic view so it has it's own caching
    and pagination mechanism (which is cool)
    """
    qs = request.user.wklejka_set.filter(is_deleted=False)

    return TemplateResponse(
        request, "wklej/list.dhtml", {'qs': qs}
    )


#def wklejki(request):
    #"""
    #This view will list a list of users pastes.
    #It's using generic view so it has it's own caching
    #and pagination mechanism (which is cool)
    #"""

    #queryset = Wklejka.objects.order_by("-pub_date").filter(
        #is_deleted=False,
        #is_private=False,
        #is_spam=False,
    #)

    #return object_list(
        #request, queryset=queryset,
        #paginate_by=25,
        #template_name="wklej/list.dhtml",
        #template_object_name="w",
    #)


@login_required
def salt(request):
    """
    saves new salt to database
    """

    if request.method == 'POST':
        if request.POST['yes']:
            new_salt = request.user.get_profile().generate_new_salt()

            return TemplateResponse(
                request, "salt.dhtml", {
                    'salt': new_salt
                },
            )

    return TemplateResponse(request, "salt.dhtml")
