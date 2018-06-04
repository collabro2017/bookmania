from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
import api_views
import views


router = routers.SimpleRouter()
router.register(r'layout-template', api_views.LayoutTemplateViewSet)
router.register(r'book', api_views.BookViewSet)
router.register(r'page', api_views.PageViewSet)
router.register(r'translation', api_views.TranslationViewSet)
router.register(r'image', api_views.ImageViewSet)
router.register(r'comment', api_views.CommentViewSet)

urlpatterns = [

    # Book - Views
    url(r'^dashboard/$', views.PublisherDashboard.as_view(), name='publisher_dashboard'),
    url(r'^editor/(?P<book_id>[0-9]+)/general/$', views.GeneralEditor.as_view(), name='publisher_general_editor'),
    url(r'^editor/(?P<book_id>[0-9]+)/analytics/$', views.BookAnalytics.as_view(), name='publisher_book_analytics'),
    url(r'^editor/(?P<book_id>[0-9]+)/list/$', views.PageListEditor.as_view(), name='publisher_list_editor'),
    url(r'^editor/(?P<book_id>[0-9]+)/comments/$', views.BookComments.as_view(), name='publisher_book_comments'),
    url(r'^editor/(?P<book_id>[0-9]+)/page/(?P<page_id>[0-9]+)/$', views.PageEditor.as_view(), name='publisher_page_editor'),
    url(r'^editor/(?P<book_id>[0-9]+)/translations/$', views.BookTranslations.as_view(), name='book_translations'),
    url(r'^editor/(?P<book_id>[0-9]+)/preview/(?P<secondary_language>[a-z]+)/$', views.BookPreview.as_view(), name='book_preview'),

    # Layout Templates - Views
    url(r'^layout-template/list/$', views.LayoutTemplateList.as_view(), name='layout_template_list'),
    url(r'^layout-template/editor/(?P<template_id>[0-9]+)/$', views.LayoutTemplateEditor.as_view(), name='layout_template_editor'),

    # Translation - Views
    url(r'^review-translation/(?P<translation_id>[0-9]+)/$', views.ReviewTranslation.as_view(), name='review_translation'),
    url(r'^review-blend/(?P<translation_id>[0-9]+)/$', views.ReviewBlend.as_view(), name='review_blend'),

    # API Views
    url(r'^', include(router.urls)),
]
