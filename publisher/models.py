from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models import Count, Avg
from PyPDF2 import PdfFileReader
from PIL import Image
from django.core.files.base import ContentFile
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.contrib.postgres.fields import JSONField, ArrayField
from django.template.loader import render_to_string
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.templatetags.static import static
from nltk.tokenize import sent_tokenize
from django.core.mail import send_mail
from django.urls import reverse
from bs4 import BeautifulSoup
from zipfile import ZipFile
from polli import constants
from sets import Set
from itertools import islice
import math
import json
import re
import cStringIO
import copy
import csv
import os
import subprocess
import random
import shutil
import urllib2


class Publisher(models.Model):
    name = models.CharField(max_length=30, unique=True)


def book_pdf_path(instance, filename):
    publisher_id = instance.publisher.id if instance.publisher else 'polli'
    return 'publisher/{}/book_pdfs/{}'.format(publisher_id, filename)


def book_cover_path(instance, filename):
    publisher_id = instance.publisher.id if instance.publisher else 'polli'
    return 'publisher/{}/book_covers/{}'.format(publisher_id, filename)


def book_image_path(instance, filename):
    publisher_id = instance.book.publisher.id if instance.book.publisher else 'polli'
    return 'publisher/{}/book_images/{}'.format(publisher_id, filename)


def book_thumbnail_image_path(instance, filename):
    publisher_id = instance.book.publisher.id if instance.book.publisher else 'polli'
    return 'publisher/{}/book_thumbnail_images/{}'.format(publisher_id, filename)


class Book(models.Model):
    FLAGGED_STATUS = 'flagged'
    PUBLISHED_STATUS = 'published'
    PENDING_STATUS = 'pending'
    DRAFT_STATUS = 'draft'
    STATUSES = [
        (FLAGGED_STATUS, FLAGGED_STATUS),
        (PUBLISHED_STATUS, PUBLISHED_STATUS),
        (PENDING_STATUS, PENDING_STATUS),
        (DRAFT_STATUS, DRAFT_STATUS),
    ]

    ENGLISH = 'english'
    SPANISH = 'spanish'
    LANGUAGE_CHOICES = [
        (ENGLISH, ENGLISH),
        (SPANISH, SPANISH)
    ]

    processing_completed = models.IntegerField(default=0)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True, default=None, related_name='books')
    status = models.CharField(max_length=30, choices=STATUSES, default=DRAFT_STATUS)
    template = models.ForeignKey('publisher.LayoutTemplate', null=True, default=None)
    name = models.CharField(max_length=50, default="")
    author = models.CharField(max_length=100, default="")
    description = models.TextField(default="")
    cover_image = models.ImageField(upload_to=book_cover_path, null=True, default=None)
    cover_thumbnail = ProcessedImageField(upload_to=book_cover_path,
                                           processors=[ResizeToFill(300, 300)],
                                           format='JPEG',
                                           options={'quality': 80},
                                           null=True,
                                           default=None)

    book_pdf = models.FileField(upload_to=book_pdf_path, null=True, default=None)
    ave_rating = models.FloatField(null=True, default=None)
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def languages(self):
        lang_list = list(self.translations.filter(status='published').values_list('language', flat=True))
        lang_list.append('english')
        return lang_list

    def send_upload_notification(self, subject='Content Uploaded', heading='Content Uploaded', request=None):
        from users.models import User
        book_url = request.build_absolute_uri(reverse('publisher_general_editor', args=[self.id])) if request else ''
        context = {
            'book': self,
            'book_url': book_url,
            'heading': heading
        }
        message = render_to_string('emails/book_uploaded.html', context)
        from_email = 'noreply@polli.com'
        to_emails = User.objects.filter(user_type='staff').values_list('email', flat=True)
        send_mail(subject, message, from_email, to_emails, html_message=message)

    def set_cover_image(self, image_url):
        image_data = urllib2.urlopen(image_url).read()
        self.cover_image.save('book_{}.jpg'.format(self.id), ContentFile(image_data))
        self.cover_thumbnail.save('book_{}_thumbnail.jpg'.format(self.id), ContentFile(image_data))
        self.save()

    def update_rating(self):
        print 'Updating Book Average Rating'
        self.ave_rating = BookRating.objects.filter(book_id=56).aggregate(ave_rating=Avg('rating'))['ave_rating']
        self.save()

    def get_tokenized_page_text(self, language='english'):
        print 'Get Tokenized Page Text'
        pages = self.pages.order_by()
        page_list = []
        for p in pages:
            page_dict = {
                'page': p.order,
                'text': '',
                'sentences': []
            }

            elements = p.content['elements']
            for e in elements:
                if e['type'] == 'text':
                    page_dict['text'] += e['data'][language]

            page_dict['sentences'] = sent_tokenize(page_dict['text'])
            page_dict['sentences'] = [s.replace('\n', ' ').replace('\r', '') for s in page_dict['sentences']]

            page_list.append(page_dict)
        page_list = sorted(page_list, key=lambda page: page['page'])
        return page_list

    @staticmethod
    def clean_style(style):
        for key, value in style.iteritems():
            if type(value) == str and 'px' in value:
                style[key] = int(value.replace('px', ''))

    def get_blended_pages(self, primary_language='english', secondary_language='spanish'):
        # Get Translation
        translation = self.translations.get(language=secondary_language)

        # Create L1 Sentence Map
        l1_sent_map = {}
        lines = translation.get_translation_lines()
        for l in lines:
            l1_sent_map[l['L1']] = l['Blend']

        pages = self.pages.order_by('order')
        for p in pages:
            for element in p.content['elements']:
                if element['type'] == 'text':
                    # Tokenize Sentences
                    l1_sents = sent_tokenize(element['data'][primary_language])

                    # Aggregate the Blends
                    blends = ''
                    for l in l1_sents:
                        l_blend = l1_sent_map.get(l)
                        if l_blend:
                            print 'Blend Found'
                            blends += ' {}'.format(l_blend)
                        else:
                            print 'Blend Not Found'

                    element['blends'] = blends.strip()

        return pages

    def generate_bundle(self, primary_language='english', secondary_language='spanish'):
        print 'Generating Bundle'
        bundle_name = 'book_bundle_{}.zip'.format(self.id)
        bundle = ZipFile(bundle_name, 'w')

        # Get Translation
        translation = self.translations.get(language=secondary_language)

        # Create L1 Sentence Map
        l1_sent_map = {}
        lines = translation.get_translation_lines()
        for l in lines:
            l1_sent_map[l['L1']] = l['Blend']

        # Bundle All Images
        images = self.images.all()
        for img in images:
            img_name = img.image.name.split('/')[-1]
            img_path = 'images/{}'.format(img_name)
            print 'Storing - {}'.format(img_path)
            bundle.writestr(img_path, img.image.read())

        # Bundle All Fonts
        fonts = os.listdir('polli/static/fonts')
        for f in fonts:
            font_files = os.listdir('polli/static/fonts/'+f)
            for f_file in font_files:
                print 'Storing - {}'.format(f_file)
                file_path = 'fonts/{}/{}'.format(f, f_file)
                bundle.write('polli/static/'.format(file_path), file_path)

        # Add Cover Images to Bundle
        cover_image_path = 'images/' + self.cover_image.name.split('/')[-1]
        bundle.writestr(cover_image_path, self.cover_image.read())

        cover_thumbnail_path = 'images/' + self.cover_thumbnail.name.split('/')[-1]
        bundle.writestr(cover_thumbnail_path, self.cover_thumbnail.read())

        # Store Pages
        book_json = {
            'title': self.name,
            'author': self.author,
            'cover_image': cover_image_path,
            'cover_image_thumbnail': cover_thumbnail_path,
            'pages': []
        }

        pages = self.pages.order_by('order')
        for p in pages:
            page = {
                'style': Book.clean_style(p.content['style']),
                'content': [],
            }

            for element in p.content['elements']:
                page_element = {
                    'style': Book.clean_style(element['style']),
                    'containerStyle': Book.clean_style(element['containerStyle'])
                }
                if element['type'] == 'image':
                    page_element['type'] = 'image'
                    page_element['src'] = 'images/' + element['data']['url'].split('/')[-1]
                else:
                    page_element['type'] = 'paragraph'

                    # Tokenize Sentences
                    l1_sents = sent_tokenize(element['data'][primary_language])

                    # Aggregate the Blends
                    blends = ''
                    for l in l1_sents:
                        l_blend = l1_sent_map.get(l)
                        if l_blend:
                            print 'Blend Found'
                            blends += ' {}'.format(l_blend)
                        else:
                            print 'Blend Not Found'

                    blends = blends.strip()

                    # Parse Blend String
                    matches = re.findall("(\[[^\|\n]*\|[^\|\n]*\|[^\|\n]*\])*", blends)
                    matches = [m for m in matches if m]
                    blend_items = []
                    for m in matches:
                        item = m.replace('[', '').replace(']', '').split('|')
                        item[2] = int(item[2])
                        blend_items.append(item)

                    # Add Blend Items to Content
                    page_element['content'] = []
                    for b in blend_items:
                        if b[0]:
                            item = {
                                        'type': 'text',
                                        'content': {
                                            'L1': b[0],
                                            'L2': b[1]
                                        },
                                        'blends': self.get_blend_levels(b[2])
                                    }
                            page_element['content'].append(item)

                page['content'].append(page_element)

            book_json['pages'].append(page)

        # Store Book.json in bundle
        bundle.writestr('book.json', json.dumps(book_json))
        bundle.close()

        return bundle_name

    def get_blend_levels(self, blend_level):
        if blend_level == 1:
            blends = {'A': 'L2', 'B': 'L2', 'C': 'L2', 'D': 'L2', 'E': 'L2'}
        elif blend_level == 2:
            blends = {'A': 'L1', 'B': 'L2', 'C': 'L2', 'D': 'L2', 'E': 'L2'}
        elif blend_level == 3:
            blends = {'A': 'L1', 'B': 'L1', 'C': 'L2', 'D': 'L2', 'E': 'L2'}
        elif blend_level == 4:
            blends = {'A': 'L1', 'B': 'L1', 'C': 'L1', 'D': 'L2', 'E': 'L2'}
        elif blend_level == 5:
            blends = {'A': 'L1', 'B': 'L1', 'C': 'L1', 'D': 'L1', 'E': 'L2'}

        return blends

    def split_tagged_text(self, tagged_text=''):
        tagged_text = tagged_text.replace('<p>', '').replace('</p>', '')
        pattern = '(<span [\w\s"=-]*>[\w\s]*</span>)'
        parts = [p for p in re.split(pattern, tagged_text) if p]

        results = []
        for p in parts:
            soup = BeautifulSoup(p, 'html.parser')
            if soup.find_all('span'):
                tagged_element = soup.find_all('span')[0]
                results.append({
                    'tagged': True,
                    'feature_id': tagged_element.attrs['data-feature-id'],
                    'text': tagged_element.text
                })
            else:
                results.append({
                    'tagged': False,
                    'text': p
                })

        return results

    def get_pages(self, user=None):
        pages = self.pages.order_by('order')
        page_ids = [p.id for p in pages]
        unresolved_comments = BookComment.objects.filter(page_id__in=page_ids, parent_comment__isnull=True)
        unresolved_comments = unresolved_comments.filter(status=BookComment.OPEN_STATUS).values_list('page_id', flat=True)

        unresolved_map = {}
        for page_id in unresolved_comments:
            if page_id not in unresolved_map:
                unresolved_map[page_id] = 1
            else:
                unresolved_map[page_id] += 1

        for p in pages:
            p.unresolved_comments = unresolved_map[p.id] if p.id in unresolved_map else 0

        return pages

    def get_comments(self, page_id=None, user=None):

        if page_id is not None:
            comments = list(self.comments.filter(page_id=page_id, status=BookComment.OPEN_STATUS).select_related('creator').order_by('-date_created'))
        else:
            comments = list(self.comments.filter(status=BookComment.OPEN_STATUS).select_related('creator').order_by('-date_created'))

        root_comments = [c for c in comments if c.parent_comment is None]
        comment_map = {}
        for c in root_comments:
            comment_map[c.id] = {
                'id': c.id,
                'book_id': c.book_id,
                'page_id': c.page_id,
                'subject': c.subject,
                'type': c.type,
                'is_owner': c.creator_id == user.id,
                'messages': [],
                'date_created': c.date_created
            }

        # Append Comment Thread Messages
        for c in comments:
            parent_id = c.parent_comment_id if c.parent_comment else c.id
            comment_map[parent_id]['messages'].append({
                'msg': c.message,
                'date_created': c.date_created,
                'profile_pic': c.creator.get_profile_pic(),
                'username': c.creator.get_best_name()
            })

            if comment_map[parent_id]['date_created'] < c.date_created:
                comment_map[parent_id]['date_created'] = c.date_created

        # Mark read status for the comments
        unread_comments = self.comments.exclude(read_by=user)
        unread_map = {}
        for c in unread_comments:
            if c.parent_comment_id:
                unread_map[c.parent_comment_id] = c.parent_comment_id
            else:
                unread_map[c.id] = c.id

        for parent_id, comment in comment_map.iteritems():
            if comment['id'] in unread_map:
                comment_map[parent_id]['has_unread_comments'] = True
            else:
                comment_map[parent_id]['has_unread_comments'] = False

        # Sort Comments By Date
        comment_list = comment_map.values()
        comment_list = sorted(comment_list, key=lambda comment: comment['date_created'], reverse=True)

        return comment_list

    def get_info_json(self):
        info_json = json.dumps({
            'id': self.id,
            'status': self.status,
            'name': self.name,
            'description': self.description,
            'author': self.author,
            'cover_image_url': self.cover_image.url,
            'cover_thumbnail_url': self.cover_thumbnail.url,
            'images': self.get_images_dict_list()
        })
        return info_json

    def get_images_dict_list(self):
        images = self.images.all()
        book_images = []
        for img in images:
            book_images.append({
                'id': img.id,
                'url': img.image.url,
                'thumbnail_url': img.thumbnail.url
            })
        return book_images

    def process_book_pdf(self):
        print 'Processing Book PDF'

        # Remove Pre-Existing Pages
        print 'Remove Pre-Existing Pages'
        self.pages.all().delete()

        # Read Pdf
        cover_image_set = False
        pdf = PdfFileReader(self.book_pdf)
        for page_num in range(pdf.numPages):
            page = pdf.getPage(page_num)

            # Prepare Page Content
            content = copy.deepcopy(BookPage.DEFAULT_CONTENT)
            if self.template:
                content = copy.deepcopy(self.template.layout)

            # Replace Single and Double Quotes
            raw_content = page.extractText().replace(u'\ufb01', '"').replace(u'\ufb02', '"').replace(u'\u2122', "'")
            text_elements = [e for e in content['elements'] if e['type'] == 'text']
            if not text_elements:
                text_element = copy.deepcopy(BookPage.DEFAULT_TEXT_DATA)
                text_element['data']['english'] = raw_content
                content['elements'].append(text_element)
            else:
                text_elements[0]['data']['english'] = raw_content

            # Get Page Images
            if '/XObject' in page['/Resources']:
                xObject = page['/Resources']['/XObject'].getObject()
                img_count = 0
                for obj in xObject:
                    if xObject[obj]['/Subtype'] == '/Image':

                        # Increment Image Count
                        img_count += 1

                        filter = xObject[obj]['/Filter']
                        data = xObject[obj]._data if filter == '/FlateDecode' else xObject[obj]._data
                        img_data = ContentFile(data)

                        if filter == '/FlateDecode':
                            img_name = 'page_img_{}_{}_{}.png'.format(self.id, page_num, img_count)
                        elif filter == '/DCTDecode':
                            img_name = 'page_img_{}_{}_{}.jpg'.format(self.id, page_num, img_count)
                        elif filter == '/JPXDecode':
                            img_name = 'page_img_{}_{}_{}.jp2'.format(self.id, page_num, img_count)

                        # Save Book Image
                        book_image = BookImage.objects.create(book=self)
                        try:

                            # Save Book Cover Image
                            if cover_image_set is False:
                                self.cover_image.save('cover_{}'.format(img_name), img_data)
                                self.cover_thumbnail.save('cover_thumbnail_{}'.format(img_name), img_data)
                                cover_image_set = True

                            # Save Book Image
                            book_image.image.save(img_name, img_data)
                            book_image.thumbnail.save('thumbnail_{}'.format(img_name), img_data)

                            image_elements = [e for e in content['elements'] if e['type'] == 'image']
                            if self.template and image_elements:
                                image_elements[0]['data']['url'] = book_image.image.url
                                image_elements[0]['data']['thumbnail_url'] = book_image.thumbnail.url
                            else:
                                image_element = copy.deepcopy(BookPage.DEFAULT_IMAGE_DATA)
                                image_element['data']['url'] = book_image.image.url
                                image_element['data']['thumbnail_url'] = book_image.thumbnail.url
                                content['elements'].append(image_element)

                        except IOError as err:
                            print 'IO Error Occurred'
                            print err
                            book_image.delete()

            # Save Book Page
            processing_completed = int((page_num + 1)/float(pdf.numPages)*100)
            self.processing_completed = processing_completed
            self.save()

            page = BookPage.objects.create(book=self, raw_content=raw_content, content=content, order=page_num)
            page.save()


@receiver(post_save, sender=Book)
def book_post_save(sender, instance, **kwargs):
    print 'Book Post Save'
    if len(instance.available_languages) == 0:
        instance.available_languages.append(Book.ENGLISH)
        instance.save()


class BookDownload(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='downloads')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, default=None, related_name='downloads')
    primary_language = models.CharField(max_length=50, null=True, default=None)
    secondary_language = models.CharField(max_length=50, null=True, default=None)
    date_created = models.DateTimeField(auto_now_add=True)


class BookRating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, default=None, related_name='ratings')
    rating = models.FloatField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=BookRating)
def rating_post_save(sender, instance, **kwargs):
    print 'Rating Post Save'
    instance.book.update_rating()


class BookPage(models.Model):

    # PAGE DEFAULTS
    IMAGE_TYPE = 'image'
    TEXT_TYPE = 'text'

    DEFAULT_TEXT_DATA = {
        'type': TEXT_TYPE,
        'data': {
            'english': ''
        },
        'containerStyle': {

        },
        'style': {
            'display': 'flex',
            'flex': 1,
        }
    }

    DEFAULT_IMAGE_DATA = {
        'type': IMAGE_TYPE,
        'data': {
            'url': '',
            'thumbnail_url': ''
        },
        'containerStyle': {
            'flex': 1
        },
        'style': {
            'height': '100%',
            'width': 'auto'
        }
    }

    DEFAULT_CONTENT = {
        'style': {
            'flexDirection': 'column',
            'backgroundColor': '#ffffff',
            'padding': '0px'
        },
        'elements': [],
    }

    FLAGGED_STATUS = 'flagged'
    PUBLISHED_STATUS = 'published'
    PENDING_STATUS = 'pending'
    DRAFT_STATUS = 'draft'
    STATUSES = [
        (FLAGGED_STATUS, FLAGGED_STATUS),
        (PUBLISHED_STATUS, PUBLISHED_STATUS),
        (PENDING_STATUS, PENDING_STATUS),
        (DRAFT_STATUS, DRAFT_STATUS),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='pages')
    status = models.CharField(max_length=30, choices=STATUSES, default=DRAFT_STATUS)
    raw_content = models.TextField(default="")
    content = JSONField(null=True, default=DEFAULT_CONTENT)
    order = models.IntegerField(default=0)

    @property
    def edit_url(self):
        return reverse('publisher_page_editor', args=[self.book_id, self.id])

    def get_paging_context(self):
        pages = list(self.book.pages.order_by('order').values_list('id', flat=True))
        index = pages.index(self.id)
        prev_page_id = pages[index-1] if index > 0 else None
        next_page_id = pages[index + 1] if index < (len(pages)-1) else None

        context = {
            'page_number': self.order + 1,
            'prev_page_id': prev_page_id,
            'next_page_id': next_page_id
        }
        return context

    def get_page_thumbnail(self):
        image_url = static('images/samples/empty_square.jpg')
        for element in self.content['elements']:
            if element['type'] == self.IMAGE_TYPE:
                return element['data']['thumbnail_url']
        return image_url


class BookComment(models.Model):
    # Statuses
    OPEN_STATUS = 'open'
    CLOSED_STATUS = 'closed'
    STATUSES = [
        (OPEN_STATUS, OPEN_STATUS),
        (CLOSED_STATUS, CLOSED_STATUS),
    ]

    # Types
    SUGGESTION_TYPE = 'suggestion'
    WARNING_TYPE = 'warning'
    ERROR_TYPE = 'translation',

    TYPES = [
        (SUGGESTION_TYPE, SUGGESTION_TYPE),
        (WARNING_TYPE, WARNING_TYPE),
        (ERROR_TYPE, ERROR_TYPE),
    ]

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, default=None, related_name='comments')
    book = models.ForeignKey(Book, null=True, default=None, related_name='comments')
    page = models.ForeignKey(BookPage, null=True, default=None, related_name='comments')
    parent_comment = models.ForeignKey('self', null=True, default=None)
    subject = models.CharField(max_length=300, blank=True, default='')
    message = models.TextField()
    status = models.CharField(max_length=50, choices=STATUSES, default=OPEN_STATUS)
    type = models.CharField(max_length=50, choices=TYPES, default=SUGGESTION_TYPE)
    read_by = models.ManyToManyField(settings.AUTH_USER_MODEL)
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def profile_pic(self):
        return self.creator.get_profile_pic()

    @property
    def username(self):
        return self.creator.get_best_name()


class BookImage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=book_image_path, null=True, default=None)
    thumbnail = ProcessedImageField(upload_to=book_thumbnail_image_path,
                                          processors=[ResizeToFill(300, 300)],
                                          format='JPEG',
                                          options={'quality': 80},
                                          null=True,
                                          default=None)


def translation_path(instance, filename):
    return 'book/{}/translations/{}/{}'.format(instance.book_id, instance.id, filename)


def blend_path(instance, filename):
    return 'book/{}/blends/{}/{}'.format(instance.book_id, instance.id, filename)


class Translation(models.Model):
    ENGLISH = 'english'
    SPANISH = 'spanish'
    FRENCH = 'french'
    ITALIAN = 'italian'
    RUSSIAN = 'russian'
    LANGUAGES = [
        (ENGLISH, ENGLISH),
        (SPANISH, SPANISH),
        (FRENCH, FRENCH),
        (ITALIAN, ITALIAN),
        (RUSSIAN, RUSSIAN)
    ]

    REQUESTED = 'requested'
    REJECTED = 'rejected'
    APPROVED = 'approved'
    TRANSLATION = 'translation'
    TRANSLATION_REVIEW = 'translation_review'
    BLEND = 'blend'
    BLEND_REVIEW = 'blend_review'
    PUBLISHED = 'published'

    STATUSES = [
        (REQUESTED, REQUESTED),
        (REJECTED, REJECTED),
        (APPROVED, APPROVED),
        (TRANSLATION, TRANSLATION),
        (TRANSLATION_REVIEW, TRANSLATION_REVIEW),
        (BLEND, BLEND),
        (BLEND_REVIEW, BLEND_REVIEW),
        (PUBLISHED, PUBLISHED)
    ]

    # Blend Statuses
    BLEND_LEVELS = 5
    BLEND_NOT_STARTED = 'not started'
    BLEND_PENDING = 'pending'
    BLEND_PROCESSING = 'processing'
    BLEND_COMPLETE = 'complete'

    BLEND_STATUSES = [
        (BLEND_NOT_STARTED, BLEND_NOT_STARTED),
        (BLEND_PENDING, BLEND_PENDING),
        (BLEND_PROCESSING, BLEND_PROCESSING),
        (BLEND_COMPLETE, BLEND_COMPLETE)
    ]

    book = models.ForeignKey(Book, related_name='translations')
    language = models.CharField(max_length=50, choices=LANGUAGES)
    status = models.CharField(max_length=50, choices=STATUSES, default=REQUESTED)
    rejection_reason = models.TextField(default='')

    translation = models.FileField(upload_to=translation_path, null=True, default=None)
    translation_review_progress = JSONField(null=True, default=list)

    blends = models.FileField(upload_to=blend_path, null=True, default=None)
    blend_status = models.CharField(max_length=100,  choices=BLEND_STATUSES, default=BLEND_NOT_STARTED)
    blend_percentage = models.IntegerField(default=0)

    blend_review_progress = JSONField(null=True, default=list)

    # Time Tracking
    date_created = models.DateTimeField(auto_now_add=True)
    date_approved = models.DateTimeField(null=True, default=None)

    translation_start_time = models.DateTimeField(null=True, default=None)
    translation_finish_time = models.DateTimeField(null=True, default=None)

    translation_review_start_time = models.DateTimeField(null=True, default=None)
    translation_review_finish_time = models.DateTimeField(null=True, default=None)

    blend_start_time = models.DateTimeField(null=True, default=None)
    blend_finish_time = models.DateTimeField(null=True, default=None)

    blend_review_start_time = models.DateTimeField(null=True, default=None)
    blend_review_finish_time = models.DateTimeField(null=True, default=None)

    date_published = models.DateTimeField(null=True, default=None)

    def generate_blends(self):
        print 'generating the blends'

        # Create L1 & L2 Files
        l1_filename = '/tmp/Translation_{}_L1.txt'.format(self.id)
        l2_filename = '/tmp/Translation_{}_L2.txt'.format(self.id)
        l1_file = open(l1_filename, 'w')
        l2_file = open(l2_filename, 'w')

        reader = csv.DictReader(self.translation)
        for row in reader:
            l1_file.write(row['L1']+'\n')
            l2_file.write(row['L2']+'\n')
            print 'L1: {}, L2: {}'.format(row['L1'], row['L2'])

        l1_file.close()
        l2_file.close()

        # Tokenize and Align L1 & L2
        command = "sh polli/blend_generator/blender.sh {} en {} es {} 2> /tmp/blend_output_{}.txt".format(self.id, l1_filename, l2_filename, self.id)
        subprocess.call(command, shell=True)

        # Get Aligned L1 & L2 Files
        output_dir = "/tmp/output_final_{}".format(self.id)
        aligned_text_file = output_dir + '/L2.A3.final'

        blended_lines = []
        with open(aligned_text_file) as f:
            read_complete = False
            while not read_complete:
                next_3 = list(islice(f, 3))
                read_complete = True if not next_3 else False

                if next_3:
                    l1 = next_3[1]
                    l2 = next_3[2]

                    align_toks = re.findall(r'(.*?) \(\{([\d ]+)\}\)', l2)
                    align_toks = [[t[0].strip(), t[1].strip(), False] for t in align_toks]
                    for t in align_toks:
                        t[1] = [int(j) for j in t[1].split(' ')] if t[1] != '' else []

                    l1_parts = l1.split(' ')
                    blends = []

                    for i in range(len(l1_parts)):

                        blends.append({
                            'l1': l1_parts[i],
                            'l2': l1_parts[i],
                            'blend_level': random.randint(1, Translation.BLEND_LEVELS)
                        })

                        t_index = None
                        for j in range(len(align_toks)):
                            if align_toks[j][1] != '' and (i + 1) in align_toks[j][1]:
                                align_toks[j][2] = True
                                t_index = j
                                blends[i]['l2'] = align_toks[j][0] if align_toks[j][0] != 'NULL' else ''

                        # Check Item to the Right
                        if t_index is not None and t_index < (len(align_toks) - 1):
                            if not align_toks[t_index + 1][1] and align_toks[t_index + 1][2] == False:
                                align_toks[t_index + 1][2] = True
                                blends[i]['l2'] += ' {}'.format(align_toks[t_index + 1][0])

                        # Check Item to the Left
                        if t_index is not None and (t_index - 1) > 0:
                            if not align_toks[t_index - 1][1] and align_toks[t_index - 1][2] == False:
                                align_toks[t_index - 1][2] = True
                                blends[i]['l2'] = '{} {}'.format(align_toks[t_index - 1][0], blends[i]['l2'])

                    # Group Blends
                    current_l2 = ''
                    final_blends = []
                    for b in blends:
                        if len(final_blends) == 0 or b['l2'] != current_l2:
                            final_blends.append(b)
                            current_l2 = b['l2']
                        else:
                            final_blends[-1]['l1'] += ' {}'.format(b['l1'])

                    print final_blends

                    blended_lines.append(final_blends)

        # Write Blends to Translation File
        csv_name = '/tmp/translation_{}.csv'.format(self.id)
        csv_file = open(csv_name, 'w')
        writer = csv.DictWriter(csv_file, fieldnames=['Page', 'Line', 'L1', 'L2', 'ReviewStatus', 'Blend', 'BlendStatus'])
        reader = csv.DictReader(self.translation)

        writer.writeheader()
        i = 0
        for row in reader:
            blend = ''
            line = blended_lines[i]

            for item in line:
                l1 = item['l1'].replace('&quot;', '"').replace('&apos;', "'")
                l2 = item['l2'].replace('&quot;', '"').replace('&apos;', "'")
                blend += '[{}|{}|{}] '.format(l1, l2, item['blend_level'])

            row['Blend'] = blend
            row['BlendStatus'] = ''
            writer.writerow(row)
            i += 1

        csv_file.close()
        self.translation.save(csv_name, ContentFile(open(csv_name).read()))
        os.remove(csv_name)

        # Update Blend Status
        self.blend_status = Translation.BLEND_COMPLETE
        self.save()

        # Remove Output Directory
        shutil.rmtree(output_dir)

        return blended_lines

    def generate_translation_csv(self, file=None):

        if file:
            writer = csv.writer(file)
            writer.writerow(['Page', 'Line', 'L1', 'L2'])
            page_list = self.book.get_tokenized_page_text()
            for p in page_list:
                sentences = p['sentences']
                page = p['page']

                line = 0
                for s in sentences:
                    writer.writerow([page, line, s, ''])
                    line += 1

        self.status = self.TRANSLATION
        self.save()

    def set_translation_csv(self, csv_data):
        self.translation.save('translation_{}.csv'.format(self.id), csv_data)

        # Add Review Status Column to CSV
        csv_name = 'translation_{}.csv'.format(self.id)
        csv_file = open(csv_name, 'w')
        writer = csv.DictWriter(csv_file, fieldnames=['Page', 'Line', 'L1', 'L2', 'ReviewStatus'])
        reader = csv.DictReader(self.translation)

        writer.writeheader()
        for row in reader:
            row['ReviewStatus'] = ''

            if row['L1'] and not row['L2']:
                row['L2'] = row['L1']

            writer.writerow(row)

        csv_file.close()
        self.translation.save(csv_name, ContentFile(open(csv_name).read()))
        os.remove(csv_name)

        self.status = self.TRANSLATION_REVIEW
        self.save()

    def update_translation_review(self, page_num, line_num, l2, complete):
        csv_name = 'translation_{}.csv'.format(self.id)
        csv_file = open(csv_name, 'w')
        writer = csv.DictWriter(csv_file, fieldnames=['Page', 'Line', 'L1', 'L2', 'ReviewStatus'])
        writer.writeheader()

        lines = self.get_translation_lines()
        for l in lines:
            if l['Page'] == page_num and l['Line'] == line_num:
                l['ReviewStatus'] = 'complete' if complete == 'true' else ''
                l['L2'] = l2.encode('utf-8')
            writer.writerow(l)
        csv_file.close()

        self.translation.save(csv_name, ContentFile(open(csv_name).read()))
        os.remove(csv_name)

    def update_blend_review(self, page_num, line_num, blend, complete):
        csv_name = 'translation_{}.csv'.format(self.id)
        csv_file = open(csv_name, 'w')
        writer = csv.DictWriter(csv_file, fieldnames=['Page', 'Line', 'L1', 'L2', 'ReviewStatus', 'Blend', 'BlendStatus'])
        writer.writeheader()

        lines = self.get_translation_lines()
        for l in lines:
            if l['Page'] == page_num and l['Line'] == line_num:
                print 'Update Line'
                l['Blend'] = blend.encode('utf-8')
                l['BlendStatus'] = 'complete' if complete == 'true' else ''
            writer.writerow(l)
        csv_file.close()

        self.translation.save(csv_name, ContentFile(open(csv_name).read()))
        os.remove(csv_name)

    def get_translation_lines(self):
        return [l for l in csv.DictReader(self.translation)]

    def process_translation_csv(self):
        # Update Book Translations
        reader = csv.DictReader(self.translation)
        page_map = {}
        for row in reader:
            if row['Page'] not in page_map:
                page_map[row['Page']] = {
                    'page': row['Page'],
                    'lines': [row]
                }
            else:
                page_map[row['Page']]['lines'].append(row)

        page_list = page_map.values()
        for p in page_list:
            p['lines'] = sorted(p['lines'], key=lambda ln: ln['Line'])

        # Clear Previous Translations Set For Language
        pages = self.book.pages.all()
        for page in pages:
            elements = page.content['elements']
            for e in elements:
                e['data'][self.language] = ''

            page.content['elements'] = elements
            page.save()

        # Set Translation
        for p in page_list:
            page = self.book.pages.get(order=p['page'])
            elements = page.content['elements']
            for l in p['lines']:
                for e in elements:
                    if e['type'] == 'text' and l['L1'] in str(e['data']['english']).strip():
                        e['data'][self.language] += unicode(l['L2'].decode('utf-8'))

            page.save()

        return page_list

    def get_percentage_completed(self):
        increment = 16.6
        percentage = 0
        if self.status == self.APPROVED:
            percentage = increment * 1
        elif self.status == self.TRANSLATION:
            percentage = increment * 2
        elif self.status == self.TRANSLATION_REVIEW:
            percentage = increment * 3
        elif self.status == self.BLEND:
            percentage = increment * 4
        elif self.status == self.BLEND_REVIEW:
            percentage = increment * 5
        elif self.status == self.PUBLISHED:
            percentage = increment * 6

        return percentage

    def get_stage_class(self, stage):
        css_class = ''

        if stage == self.REQUESTED:
            css_class = 'green'
        elif stage == self.APPROVED and self.status in [self.APPROVED, self.TRANSLATION, self.TRANSLATION_REVIEW, self.BLEND, self.BLEND_REVIEW, self.PUBLISHED]:
            css_class = 'green'
        elif stage == self.TRANSLATION and self.status in [self.TRANSLATION, self.TRANSLATION_REVIEW, self.BLEND, self.BLEND_REVIEW, self.PUBLISHED]:
            css_class = 'green'
        elif stage == self.TRANSLATION_REVIEW and self.status in [self.TRANSLATION_REVIEW, self.BLEND, self.BLEND_REVIEW, self.PUBLISHED]:
            css_class = 'green'
        elif stage == self.BLEND and self.status in [self.BLEND, self.BLEND_REVIEW, self.PUBLISHED]:
            css_class = 'green'
        elif stage == self.BLEND_REVIEW and self.status in [self.BLEND_REVIEW, self.PUBLISHED]:
            css_class = 'green'
        elif stage == self.PUBLISHED and self.status in [self.PUBLISHED]:
            css_class = 'green'

        return css_class


class LayoutTemplate(models.Model):
    DEFAULT_LAYOUT = {
        'style': {
            'flexDirection': 'column',
            'backgroundColor': '#ffffff',
            'padding': '0px'
        },
        'elements': [],
    }

    name = models.CharField(max_length=100, default="")
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True, default=None, related_name='templates')
    layout = JSONField(null=True, default=DEFAULT_LAYOUT)

    def get_thumbnail(self):
        image_url = static('images/samples/empty_square.jpg')
        return image_url





















