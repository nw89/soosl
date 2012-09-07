from django.template import Library, RequestContext

from sooslwww.models import WrittenLanguage

from sooslwww.LanguageChooser import CurrentLanguageID

register = Library()

def language_chooser(context):
    # If no language set, choose the default
    # TODO: browser based detection
    print context
    request = context['request']
    selectedLanguageID = CurrentLanguageID(request)

    #Get all languages
    languages = WrittenLanguage.objects.all();

    return {'languages': languages,
            'selected_language_id': int(selectedLanguageID),
            'url_prefix': request.path }

register.inclusion_tag('language_chooser.html', takes_context=True)(language_chooser)
