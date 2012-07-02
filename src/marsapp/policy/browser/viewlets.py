#-*- coding: utf-8 -*-
from plone.app.layout.links.viewlets import FaviconViewlet as BaseFavViewlet

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class FaviconViewlet(BaseFavViewlet):

    _template = ViewPageTemplateFile('templates/favicon.pt')

