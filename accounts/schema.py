import graphene
from graphene_django import DjangoObjectType
from . import models
# from .mutation import CustomObtainJSONWebToken
import graphql_jwt
from graphql_jwt.decorators import login_required,permission_required,staff_member_required


class UserType(DjangoObjectType):
    class Meta:
        model = models.CustomUser
        fields = "__all__"


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)

    user_by_id=graphene.Field(UserType,id=graphene.Int(required=True))

    @login_required
    def resolve_all_users(root,info):
        return models.CustomUser.objects.all()
    
    # @staff_member_required
    def resolve_user_by_id(root,info,id):
        try:
            return models.CustomUser.objects.get(id=id)
        except models.CustomUser.DoesNotExist:
            raise Exception("User is Not Exist")
    


class RegisterUser(graphene.Mutation):
    class Arguments:
        username=graphene.String(required=True)
        email=graphene.String(required=True)
        password=graphene.String(required=True)

    user = graphene.Field(UserType)

    
    def mutate(root,info,username,email,password):

        user=models.CustomUser.objects.filter(username=username,email=email).first()

        if user:
            raise Exception("User already exists")

        user=models.CustomUser(username=username,email=email)
        user.set_password(password)
        user.save()

        return RegisterUser(user=user)
    
class DeleteUser(graphene.Mutation):
    class Arguments:
        id=graphene.Int(required=True)

    success=graphene.Boolean()

    def mutate(root,info,id):
        try:
            user=models.CustomUser.objects.get(id=id)
            user.delete()
            return DeleteUser(success=True)
        except models.CustomUser.DoesNotExist:
            raise Exception("User Not Exist")


class UpdateUser(graphene.Mutation):
    class Arguments:
        id=graphene.Int(required=True)
        username=graphene.String()
        email=graphene.String()
        firstname=graphene.String()
        lastname=graphene.String()
        phone_number=graphene.String()
        address=graphene.String()

    user = graphene.Field(UserType)

    def mutate(root,info,id,**kwargs):

        try:
            user=models.CustomUser.objects.get(id=id)
            for key, value in kwargs.items():
                if value is not None:
                    setattr(user,key,value)

            user.save()

            return UpdateUser(user=user)

        except models.CustomUser.DoesNotExist:
            raise Exception("User Not Exist")
        
        except Exception as e:
            raise Exception(f"An error occurred: {str(e)}")
        
    
# class PasswordReset(graphene.Mutation):
#     class Arguments:
#         email=graphene.String(required=True)

#     success=graphene.Boolean()

#     def mutate(root,info,email):

class Mutation(graphene.ObjectType):
    token_auth=graphql_jwt.ObtainJSONWebToken.Field()
    refresh_token=graphql_jwt.Refresh.Field()
    verify_token=graphql_jwt.Verify.Field()

    register_user=RegisterUser.Field()
    delete_user=DeleteUser.Field()
    update_user=UpdateUser.Field()

    