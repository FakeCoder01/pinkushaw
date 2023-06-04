from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Profile, ProfileImage

from .forms import ImageUploadForm, ProfilePicUploadForm

# @api_view(['POST'])
# @authentication_classes([SessionAuthentication, TokenAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def profile_pic_upload(request):
    print("hhhhh")
    if "profile_pic" in request.FILES:
        p = Profile.objects.get(user=request.user)
        p.profile_pic = request.FILES['profile_pic']
        p.save()
        return Response({'message': 'profile pic uploaded'}, status=200)
    return Response({"detail" : "image invalid"}, status=400)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def profile_image_upload(request):
    form = ImageUploadForm(data=request.data)
    if form.is_valid():
        form.save(user=request.user.userprofile)
        return Response({'message': 'image uploaded'}, status=200)
    return Response({"detail" : "image invalid"}, status=400)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def profile_image_delete(self, request, id):
    if ProfileImage.objects.filter(id=id, user=self.request.user.userprofile).exists():
        ProfileImage.objects.get(id=id, user=self.request.user.userprofile).delete()
        return Response({'message': 'image deleted'}, status=200)
    return Response({"detail" : "image invalid"}, status=400)

