from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from publisher.models import Book, BookPage, BookImage, BookComment, Translation, LayoutTemplate, Publisher
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.contrib.auth.mixins import UserPassesTestMixin
from django.conf import settings
from captcha.image import ImageCaptcha
from django.urls import reverse
from django.db.models import Count, Max, Q
from django.views import View
from polli.decorators import restrict_access
from django.core.exceptions import SuspiciousOperation
from django.http import JsonResponse
from django.http import FileResponse
from django.http import Http404
from users.models import User
from polli import constants
from zipfile import ZipFile
from django.core.mail import send_mail
from django.conf import settings
import csv
import string
import random
import urllib2
import json
import time
import boto3


class BaseView(UserPassesTestMixin, View):

    def get_book_list(self):
        user = self.request.user

        # Get Books
        if user.user_type == User.PUBLISHER:
            books = user.publisher.books.all()
        elif user.user_type == User.STAFF:
            books = Book.objects.all()

        # Annotate Books with Unread Comments
        book_ids = [b.id for b in books]
        unresolved_comments = BookComment.objects.filter(book_id__in=book_ids, parent_comment__isnull=True)
        unresolved_comments = unresolved_comments.filter(status=BookComment.OPEN_STATUS).values_list('book_id', flat=True)

        unresolved_map = {}
        for book_id in unresolved_comments:
            if book_id not in unresolved_map:
                unresolved_map[book_id] = 1
            else:
                unresolved_map[book_id] += 1

        for b in books:
            b.unresolved_comments = unresolved_map[b.id] if b.id in unresolved_map else 0

        return books

    def get_book(self, book_id):
        user = self.request.user
        if user.user_type == User.STAFF:
            return Book.objects.get(pk=book_id)
        else:
            book_qs = Book.objects.filter(pk=book_id, publisher=user.publisher)
            if book_qs.exists():
                return book_qs.first()
            else:
                raise Http404('You can not access this book')

    def test_func(self):
        user_type = self.request.user.user_type
        return user_type == User.PUBLISHER or user_type == User.STAFF


# Book - Views
class PublisherDashboard(BaseView):
    def get(self, request):

        # Get Layout Templates
        if request.user.user_type == User.PUBLISHER:
            publisher = request.user.publisher
            templates = LayoutTemplate.objects.filter(Q(publisher=publisher)|Q(publisher__isnull=True))
        else:
            templates = LayoutTemplate.objects.filter(publisher__isnull=True)
        templates = [t for t in templates if t.layout['elements']]

        context = {
            'books': self.get_book_list(),
            'templates': templates
        }
        return render(request, 'publisher/dashboard.html', context)


class GeneralEditor(BaseView):
    def get(self, request, book_id):
        context = {
            'book': self.get_book(book_id)
        }
        return render(request, 'publisher/general_editor.html', context)


class BookAnalytics(BaseView):
    def get(self, request, book_id):
        book = self.get_book(book_id)
        context = {
            'book': book,
            'total_downloads': book.downloads.count()
        }
        return render(request, 'publisher/book_analytics.html', context)


class PageListEditor(BaseView):
    def get(self, request, book_id):
        book = self.get_book(book_id)
        user = request.user
        context = {
            'book': book,
            'pages': book.get_pages(user=user),
        }
        return render(request, 'publisher/list_editor.html', context)


class BookComments(BaseView):
    def get(self, request, book_id):
        book = self.get_book(book_id)
        user = request.user
        context = {
            'book': book,
            'comments': book.get_comments(user=user)
        }
        return render(request, 'publisher/book_comments.html', context)


class PageEditor(BaseView):
    def get(self, request, book_id, page_id):
        book = self.get_book(book_id)
        page = book.pages.get(pk=page_id)
        user = request.user
        comments = book.get_comments(page_id=page_id, user=user)

        # Get Layout Templates
        if request.user.user_type == User.PUBLISHER:
            publisher = request.user.publisher
            templates = LayoutTemplate.objects.filter(Q(publisher=publisher) | Q(publisher__isnull=True))
        else:
            templates = LayoutTemplate.objects.filter(publisher__isnull=True)

        templates = [t for t in templates if t.layout['elements']]
        layouts = [{'id': t.id, 'name': t.name, 'layout': t.layout} for t in templates]

        context = {
            'book': book,
            'page': page,
            'layouts': json.dumps(layouts),
            'content': json.dumps(page.content),
            'languages': json.dumps(book.languages),
            'page_id': page_id,
            'paging': page.get_paging_context(),
            'blend_levels': json.dumps(constants.BLEND_LEVELS),
            'comments': comments,
            'has_new_comments': any([c['has_unread_comments'] for c in comments])
        }
        return render(request, 'publisher/page_editor.html', context)


class BookTranslations(BaseView):
    def get(self, request, book_id):
        book = self.get_book(book_id)

        if request.user.user_type == User.PUBLISHER:
            translations = book.translations.all()
        else:
            translations = book.translations.exclude(status=Translation.REJECTED)

        context = {
            'book': book,
            'languages': constants.LANGUAGES,
            'translations': translations
        }
        return render(request, 'publisher/book_translations.html', context)


class BookPreview(BaseView):
    def get(self, request, book_id, secondary_language):
        book = self.get_book(book_id)
        pages = book.get_blended_pages(secondary_language=secondary_language)

        context = {
            'book': book,
            'pages': pages
        }
        return render(request, 'publisher/book_preview.html', context)


# Layout Templates - Views
class LayoutTemplateList(BaseView):
    def get(self, request):
        user = request.user

        if user.user_type == User.PUBLISHER:
            templates = user.publisher.templates.all()
        else:
            templates = LayoutTemplate.objects.filter(publisher__isnull=True)

        context = {
            'templates': templates
        }
        return render(request, 'publisher/layout_template_list.html', context)


class LayoutTemplateEditor(BaseView):
    def get(self, request, template_id):
        template = LayoutTemplate.objects.get(pk=template_id)
        context = {
            'template': template,
            'layout': json.dumps(template.layout),
        }
        return render(request, 'publisher/layout_template_editor.html', context)


# Translation - Views
class ReviewTranslation(BaseView):
    def get(self, request, translation_id):
        translation = Translation.objects.get(pk=translation_id)
        context = {
            'book': translation.book,
            'translation': translation,
            'lines': json.dumps(translation.get_translation_lines())
        }
        return render(request, 'publisher/translation_review.html', context)


class ReviewBlend(BaseView):
    def get(self, request, translation_id):
        translation = Translation.objects.get(pk=translation_id)
        translation.status = Translation.BLEND_REVIEW
        translation.save()

        context = {
            'book': translation.book,
            'translation': translation,
            'lines': json.dumps(translation.get_translation_lines())
        }
        return render(request, 'publisher/blend_review.html', context)