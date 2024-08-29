import graphene
from graphene_django import DjangoObjectType
from . import models
# from .mutation import CustomObtainJSONWebToken
import graphql_jwt
from graphql_jwt.decorators import login_required,permission_required,staff_member_required
from graphene_file_upload.scalars import Upload


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

    product_by_id=graphene.Field(ProductType,id=graphene.Int(required=True))

    product_by_slug=graphene.Field(ProductType,slug=graphene.String(required=True))

    def resolve_all_products(root,info):
        try:
            return models.Product.objects.prefetch_related('images').all()
        except Exception as e:
            raise Exception(f"An error occured: {str(e)}")


    def resolve_product_by_id(root,info,id):
        try:
            return models.Product.objects.prefetch_related('images').get(id=id)
        except models.Product.DoesNotExist:
            raise Exception("Product Not Exist")
        except Exception as e:
            raise Exception(f"An error occured: {str(e)}")

    def resolve_product_by_slug(root,info,slug):
        try:
            return models.Product.objects.prefetch_related('images').get(slug=slug)
        except models.Product.DoesNotExist: 
            raise Exception("Product Not Exist")
        except Exception as e:
            raise Exception(f"An error occured: {str(e)}")
        
class CreateProduct(graphene.Mutation):

    class Arguments:
        title=graphene.String(required=True)
        description=graphene.String(required=True)
        price=graphene.String(required=True)
        image1=Upload(required=True)
        image2=Upload(required=True)
        image3=Upload(required=True)


    product=graphene.Field(ProductType)
   

    def mutate(root,info,title,description,price,image1,image2,image3):
        try:
            product=models.Product.objects.create(title=title,description=description,price=price)

            product_images=models.ProductImages.objects.create(product=product,image1=image1,image2=image2,image3=image3)

            return CreateProduct(product=product)
        except Exception as e:
            raise Exception(f"An error occured: {str(e)}")
        
class DeleteProduct(graphene.Mutation):
    class Arguments:
        id=graphene.Int(required=True)

    success=graphene.Boolean()
    def mutate(root,info,id):
        try:
            product=models.Product.objects.get(id=id)
            product.delete()
            return DeleteProduct(success=True)
            
        except models.Product.DoesNotExist:
            raise Exception("Product Not Exist")
        except Exception as e:
            raise Exception(f"An error occured: {str(e)}")
        
class UpdateProduct(graphene.Mutation):
    class Arguments:
        id=graphene.Int(required=True)
        title=graphene.String()
        description=graphene.String()
        price=graphene.String()
        image1=Upload()
        image2=Upload()
        image3=Upload()

    product=graphene.Field(ProductType)

    def mutate(root,info,id,**kwargs):
        try:
            product=models.Product.objects.get(id=id)


            for key, value in kwargs.items():
                if key not in ['image1','image2','image3']:
                    if value is not None:
                        setattr(product,key,value)
            product.save()

            # handle image uploads
            images_updated = False  # Track if any images are updated
            product_images, created = models.ProductImages.objects.get_or_create(product=product)

            if 'image1' in kwargs and kwargs['image1'] is not None:
                product_images.image1 = kwargs['image1']
                images_updated = True
            if 'image2' in kwargs and kwargs['image2'] is not None:
                product_images.image2 = kwargs['image2']
                images_updated = True
            if 'image3' in kwargs and kwargs['image3'] is not None:
                product_images.image3 = kwargs['image3']
                images_updated = True
            
            if images_updated:
                product_images.save()

            return UpdateProduct(product=product)


            return UpdateProduct(product=product)
        except models.Product.DoesNotExist:
            raise Exception("Product Not Exist")
        except Exception as e:
            raise Exception(f"An error occured: {str(e)}")


        
class Mutation(graphene.ObjectType):

    create_product=CreateProduct.Field()
    delete_product=DeleteProduct.Field()
    update_product=UpdateProduct.Field()
        
        
        


       
        
 
    
