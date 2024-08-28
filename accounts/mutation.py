# import graphene
# import graphql_jwt
# from graphql_jwt import JSONWebTokenMutation
# from graphql_jwt.decorators import login_required
# from .schema import UserType  # Import your UserType

# class CustomObtainJSONWebToken(JSONWebTokenMutation):
#     user = graphene.Field(UserType)

#     @classmethod
#     def resolve(cls, root, info, **kwargs):
#         # Call the original method
#         result = super().resolve(root, info, **kwargs)
        
#         # Add custom payload or fields
#         if result:
#             user = info.context.user
#             result.user = user
#             # You can also add custom payload modifications here if needed
#         return result
