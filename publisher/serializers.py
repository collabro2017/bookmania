from publisher.models import Book, LayoutTemplate, BookPage, Translation, BookImage, BookComment
from rest_framework import serializers


class LayoutTemplateSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source='get_thumbnail', read_only=True)

    class Meta:
        model = LayoutTemplate
        fields = ('id', 'name', 'publisher', 'layout', 'image')


class BookSerializer(serializers.ModelSerializer):
    languages = serializers.CharField(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'

    def validate_template(self, value):
        return value if value else None


class BookPageSerializer(serializers.ModelSerializer):
    edit_url = serializers.CharField(read_only=True)

    class Meta:
        model = BookPage
        fields = '__all__'


class TranslationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Translation
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookImage
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    profile_pic = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)

    class Meta:
        model = BookComment
        exclude = ('read_by',)
