# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django import forms
from django.forms import widgets
from django.forms.fields import ChoiceField
from django.template import engines
from django.template.loader import select_template
from django.utils.translation import ugettext as _, ugettext
from entangled.forms import EntangledModelFormMixin
from cms.plugin_pool import plugin_pool
from cmsplugin_cascade.fields import GlossaryField
from shop.cascade.plugin_base import ShopPluginBase
from shop.conf import app_settings
from shop.cascade.catalog import ShopCatalogFrom


class ShopSearchResultsForm(EntangledModelFormMixin,forms.ModelForm):
    pagination = ChoiceField(
        label=_("Pagination"),
        choices=[('paginator', _("Use Paginator")), ('manual', _("Manual Infinite")), ('auto', _("Auto Infinite"))],
        help_text=_("Shall the product list view use a paginator or scroll infinitely?"),
    )

    class Meta:
        entangled_fields = {'glossary': ['pagination']}

    def clean(self):
        cleaned_data = super(ShopSearchResultsForm, self).clean()
        page = self.instance.placeholder.page if self.instance.placeholder_id else None
        if page and page.application_urls != 'CatalogSearchApp':
            raise ValidationError("This plugin can only be used on a CMS page with an application of type 'Search'.")
        return cleaned_data

class ShopSearchResultsPlugin(ShopPluginBase):
    name = _("Search Results")
    require_parent = True
    parent_classes = ['BootstrapColumnPlugin']
    form = ShopSearchResultsForm
    cache = False

    def get_render_template(self, context, instance, placeholder):
        if instance.placeholder.page.application_urls == 'CatalogSearchApp':
            return select_template([
                '{}/search/results.html'.format(app_settings.APP_LABEL),
                'shop/search/results.html',
            ])
        alert_msg = '''<div class="alert alert-danger">
        This {} plugin is used on a CMS page without an application of type "Search".
        </div>'''
        return engines['django'].from_string(alert_msg.format(self.name))

    def render(self, context, instance, placeholder):
        super(ShopSearchResultsPlugin, self).render(context, instance, placeholder)
        context['pagination'] = instance.glossary.get('pagination', 'paginator')
        return context

    @classmethod
    def get_identifier(cls, obj):
        pagination = obj.glossary.get('pagination')
        if pagination == 'paginator':
            return ugettext("Manual Pagination")
        return ugettext("Infinite Scroll")

plugin_pool.register_plugin(ShopSearchResultsPlugin)
