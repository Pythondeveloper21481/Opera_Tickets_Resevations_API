from django.shortcuts import render
from django.http.response import JsonResponse 
from.models import Guest, Opera, Reservation, Post
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import OperaSerializer, GuestSerializer, ResevationSerializer, PostSerializer
from rest_framework import status, filters
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import mixins, generics
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from .permissions import IsAuthorOrReadOnly 
# Create your views here.
# we will create some endpoints with methods
#function based view without restframework no model query
def no_rest_no_model(request):
    gests= [
        {
            'id':1,
            "name": "Rami",
            "Mobile": 2544112255,
        },
        {
            'id':2,
            "name": "Chedi",
            "Mobile": 10110012255,
        }
    ]
    return JsonResponse(gests, safe=False)


#function without rest

def no_rest_from_model(request):
    data = Guest.objects.all()
    response = {
        'guests':list(data.values('name', 'mobile'))
    }
    return JsonResponse(response)

#fuction based views GET POST
@api_view(['GET', 'POST'])
def fbv_list(request):
    #GET
    if request.method == 'GET':
        guest = Guest.objects.all()
        serializer = GuestSerializer(guest, many=True)
        return Response(serializer.data)
    #POST
    elif  request.method == 'POST':
        serializer = GuestSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def fbv_pk(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    #GET
    if request.method == 'GET':
        
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    #PUT
    elif  request.method == 'PUT':
        serializer = GuestSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #DELETE
    if request.method == 'DELETE':
        
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# Using class based views POST GET
class CBV_list(APIView):

    def get(self, request):
        guest = Guest.objects.all()
        serializer = GuestSerializer(guest, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED )
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


# Using class based views GET PUT DELET
   

class CBV_pk(APIView):

    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        guest= self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    
    def put(self, request, pk):
        guest= self.get_object(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#Mixins
#list
class mixins_list(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request):
        return self.list(request)
    def post(self, request):
        return self.create(request)
# mixinsGET PUT DELETE
class mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    def get(self, request, pk):
        return self.retrieve(request)
    def post(self, request, pk):
        return self.update(request)
    def delete(self, request, pk):
        return self.destroy(request)


#Generics GET POST
class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    # authentication_classes= [BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    authentication_classes= [TokenAuthentication]


#Generics GET PUT and DELETE
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    # authentication_classes= [BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    authentication_classes= [TokenAuthentication]


#viewsets 
#
class UserViewSet_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

class UserViewSet_opera(viewsets.ModelViewSet):
    queryset = Opera.objects.all()
    serializer_class = OperaSerializer
    filter_backends =[filters.SearchFilter]
    search_fields = ['opera']

class UserViewSet_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ResevationSerializer

#Search Opera
@api_view(['GET'])
def Search_opera(request):
    operas = Opera.objects.filter(opera=request.data['opera'], hall=request.data['hall'])
    serializer = OperaSerializer(operas, many=True)
    return Response(serializer.data)

#create new reservation
@api_view(['POST'])
def new_reservation(request):
    opera =Opera.objects.get(
        opera=request.data['opera'],
        hall=request.data['hall']
        )
    guest = Guest()  #create new guest new empty guest
    guest.name=request.data['name']
    guest.mobile=request.data['mobile']
    guest.save()

    reservation = Reservation() # new empty reservation
    reservation.guest =guest
    reservation.opera = opera
    reservation.save()
    serializer = OperaSerializer(opera)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

#Post author editor

class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer










#there is no security in this views
