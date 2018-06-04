from publisher.models import LayoutTemplate, Book, BookDownload, BookRating, BookPage, BookImage, BookComment, Translation,  Publisher
from serializers import LayoutTemplateSerializer, BookSerializer, BookPageSerializer, TranslationSerializer
from serializers import ImageSerializer, CommentSerializer
from rest_framework.decorators import detail_route, list_route, permission_classes
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from django.http import HttpResponse
from django.core.files.base import ContentFile
from rest_framework import viewsets
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import JsonResponse, FileResponse, Http404
from rest_framework import generics
from rest_framework.decorators import api_view, parser_classes
from django.db.models import Count, Max, Q
from django.conf import settings
from polli import constants
from users.models import User
import csv
import string
import random
import urllib2
import json
import time
import boto3
import json


# Layout Template - API
class LayoutTemplateViewSet(viewsets.ModelViewSet):
    queryset = LayoutTemplate.objects.all()
    serializer_class = LayoutTemplateSerializer

    def create(self, request):
        serializer = LayoutTemplateSerializer(data=request.data)
        if serializer.is_valid():
            user = self.request.user
            publisher = user.publisher if user.user_type == User.PUBLISHER else None
            serializer.save(publisher=publisher)
            return Response(serializer.data)


# Book - API Views
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def create(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            user = self.request.user
            publisher = user.publisher if user.user_type == User.PUBLISHER else None
            book = serializer.save(publisher=publisher)
            translation = request.data['translation']
            if translation:
                Translation.objects.create(book=book, language=translation)

            # Send Notification Email
            subject = 'Book Uploaded: ({}) {}'.format(book.id, book.name)
            heading = 'New Book Uploaded'
            book.send_upload_notification(subject=subject, heading=heading, request=request)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def list(self, request):
        books = Book.objects.filter(translations__status='published')
        page = self.paginate_queryset(books)
        serializer = BookSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @detail_route(methods=['get'])
    def get_book_bundle(self, request, pk=None):
            # Record Download
            primary_language = request.query_params['primary_language']
            secondary_language = request.query_params['secondary_language']
            BookDownload.objects.create(
                user=request.user,
                book_id=pk,
                primary_language=primary_language,
                secondary_language=secondary_language
            )

            # Get Bundle
            book = Book.objects.get(pk=pk)
            bundle_file_path = book.generate_bundle(primary_language=primary_language, secondary_language=secondary_language)
            return FileResponse(open(bundle_file_path, 'rb'), content_type='application/octet-stream')

    @detail_route(methods=['post'])
    def rate_book(self, request, pk):
            book_rating, created = BookRating.objects.get_or_create(user=request.user, book_id=pk)
            book_rating.rating = float(request.data['rating'])
            book_rating.save()
            return Response('Rate Book Complete')

    @detail_route(methods=['post'])
    def process_book(self, request, pk=None):
        book = Book.objects.get(pk=pk)
        book.process_book_pdf()
        serializer = BookSerializer(instance=book)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def get_book_processing_status(self, request, pk):
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(instance=book)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def update_book_cover(self, request, pk=None):
        book = Book.objects.get(pk=pk)
        book.set_cover_image(image_url=request.data['image_url'])
        serializer = BookSerializer(instance=book)
        return Response(serializer.data)


# Page - API Views
class PageViewSet(viewsets.ModelViewSet):
    queryset = BookPage.objects.all()
    serializer_class = BookPageSerializer

    def create(self, request):
        serializer = BookPageSerializer(data=request.data)
        if serializer.is_valid():
            book_id = request.data['book']
            order = Book.objects.get(pk=book_id).pages.aggregate(Max('order'))['order__max'] + 1
            serializer.save(order=order)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    @list_route(methods=['post'])
    def update_page_sorting(self, request):
        for page in json.loads(request.data['pages']):
            BookPage.objects.filter(id=int(page['id'])).update(order=int(page['order']))
        return Response('Page Sorting Updated')


# Translation - API Views
class TranslationViewSet(viewsets.ModelViewSet):
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer

    def create(self, request):
        serializer = TranslationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    @detail_route(methods=['get'])
    def get_translation_csv(self, request, pk):
        translation_csv = HttpResponse(content_type='text/csv')
        translation_csv['Content-Disposition'] = 'attachment; filename="translation_{}.csv"'.format(pk)
        translation = Translation.objects.get(pk=pk)
        translation.generate_translation_csv(translation_csv)
        return translation_csv

    @detail_route(methods=['post'])
    def upload_translation_csv(self, request, pk=None):
        translation = Translation.objects.get(pk=pk)
        csv_data = ContentFile(request.FILES['csv'].read())
        translation.set_translation_csv(csv_data)
        translation.process_translation_csv()
        return Response('upload translation complete')

    @detail_route(methods=['post'])
    def update_translation_review(self, request, pk):
        data = request.data
        translation = Translation.objects.get(pk=pk)
        translation.update_translation_review(page_num=data['page_num'], line_num=data['line_num'], l2=data['l2'], complete=data['complete'])
        return Response('update translation review complete')

    @detail_route(methods=['post'])
    def update_blend_review(self, request, pk):
        data = request.data
        translation = Translation.objects.get(pk=pk)
        translation.update_blend_review(page_num=data['page_num'], line_num=data['line_num'], blend=data['blend'], complete=data['complete'])
        return Response('update blend review complete')

    @detail_route(methods=['post'])
    def create_blend_request(self, request, pk):
        # Update Translation
        translation = Translation.objects.get(pk=pk)
        translation.status = Translation.BLEND
        translation.blend_status = Translation.BLEND_PENDING
        translation.save()

        # Add Blend Request to SQS
        sqs = boto3.resource('sqs', region_name='us-east-1', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        queue = sqs.get_queue_by_name(QueueName=settings.AWS_SQS_NAME)
        queue.send_message(MessageBody=json.dumps({'translation_id': pk}))
        return Response('create blend request')

    @list_route(permission_classes=[permissions.AllowAny], methods=['post'])
    def generate_blends(self, request):
        translation = Translation.objects.get(pk=request.data['translation_id'])
        translation.generate_blends()
        return Response('Generate Blends')


# Images - API Views
class ImageViewSet(viewsets.ModelViewSet):
    queryset = BookImage.objects.all()
    serializer_class = ImageSerializer

    def create(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.save()

            # Send Notification Email
            book = image.book
            subject = 'Image Uploaded: ({}) {}'.format(book.id, book.name)
            heading = 'New Image Uploaded'
            book.send_upload_notification(subject=subject, heading=heading, request=request)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


# Comment - API Views
class CommentViewSet(viewsets.ModelViewSet):
    queryset = BookComment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    @detail_route(methods=['post'])
    def mark_comment_read(self, request, pk):
        comments = BookComment.objects.filter(Q(id=pk)|Q(parent_comment_id=pk))
        for c in comments:
            c.read_by.add(request.user)
        return Response('Comment Read')

    @detail_route(methods=['post'])
    def resolve_comment(self, request, pk):
        BookComment.objects.filter(Q(id=pk) | Q(parent_comment_id=pk)).update(status=BookComment.CLOSED_STATUS)
        comments.update(status=BookComment.CLOSED_STATUS)
        return Response('Comment Resolved')
