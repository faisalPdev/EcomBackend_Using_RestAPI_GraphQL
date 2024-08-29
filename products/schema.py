import graphene
from graphene_django import DjangoObjectType
from . import models
# from .mutation import CustomObtainJSONWebToken
import graphql_jwt
from graphql_jwt.decorators import login_required,permission_required,staff_member_required

class ProductImagesType(DjangoObjectType):
    image1_url = graphene.String()
    image2_url = graphene.String()
    image3_url = graphene.String()
    class Meta:
        model = models.ProductImages
        fields = ('image1','image2','image3','id')

    def resolve_image1_url(self,info):
        if self.image1:
            return self.image1.url
        return None

    def resolve_image2_url(self,info):
        if self.image2:
            return self.image2.url
        return None

    def resolve_image3_url(self,info):
        if self.image3:
            return self.image3.url
        return None

class ProductType(DjangoObjectType):
    images=graphene.List(ProductImagesType)
    class Meta:
        model = models.Product
        interfaces = (graphene.relay.Node,)  # Use relay Node for pagination support
        fields = '__all__'

    def resolve_images(self,info):
        return self.images.all()

class Query(graphene.ObjectType):
    all_products = graphene.List(ProductType)

    def resolve_all_products(root,info):
        return models.Product.objects.prefetch_related('images').all()

 
    
