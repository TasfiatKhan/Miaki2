from django.http import JsonResponse

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import NoteSerializer, TagSerializer
from note.models import Note, Tag
from users.models import User
from .utils import updateNote, getNoteDetail, deleteNote, getNotesList, createNote

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer





@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def getNotes(request):

    if request.method == 'GET':
        return getNotesList(request)

    if request.method == 'POST':
        return createNote(request)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def getNote(request, pk):

    if request.method == 'GET':
        return getNoteDetail(request, pk)

    if request.method == 'PUT':
        return updateNote(request, pk)

    if request.method == 'DELETE':
        return deleteNote(request, pk)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getTags(request):
    tags = Tag.objects.all()
    serializer = TagSerializer(tags, many=True)
    return Response(serializer.data)



















'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getNotes(request):
    user = request.user
    notes = user.note_set.all()
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getNoteDetail(request, pk):
    user = request.user
    notes = user.note_set.all()
    note = notes.get(id=pk)
    serializer = NoteSerializer(note, many=False)
    return Response(serializer.data)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteNote(request, pk):
    user = request.user
    notes = user.note_set.all()
    note = notes.get(id=pk)
    note.delete()
    return Response('Note was deleted!')

'''



































@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
    ]
    
    return Response(routes)