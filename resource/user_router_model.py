from marshmallow import Schema, fields


# Schema
class UserGetSchema(Schema):
    name = fields.Str(example="string")

class UserPostSchema(Schema):
    name = fields.Str(doc="name", example="string", required=True)
    account = fields.Str(doc="account", example="string", required=True)
    passwd = fields.Str(doc="passwd", example="string", required=True)
    gender = fields.Bool(doc="gender", example="string", required=True)
    created_time = fields.Bool(doc="created_time", example="string", required=False)

# class UserPostSchema(Schema):
#     name = fields.Str(doc="name", example="string", required=True)
#     gender = fields.Str(doc="gender", example="string", required=True)
#     account = fields.Str(doc="account", example="string", required=True)
#     password = fields.Str(doc="password", example="string", required=True)
#     birth = fields.Str(doc="birth", example="string")
#     note = fields.Str(doc="note", example="string")


class UserPatchSchema(Schema):
    name = fields.Str(doc="name", example="string")
    gender = fields.Bool(doc="gender", example="string")
    account = fields.Str(doc="account", example="string")
    passwd = fields.Str(doc="passwd", example="string")
    


class LoginSchema(Schema):
    account = fields.Str(doc="account", example="string", required=True)
    password = fields.Str(doc="password", example="string", required=True)


# Response
class UserGetResponse(Schema):
    message = fields.Str(example="success")
    datatime = fields.Str(example="1970-01-01T00:00:00.000000")
    data = fields.List(fields.Dict())
    #data = fields.List(fields.Dict())  #強制輸出型態
    

class UserCommonResponse(Schema):
    message = fields.Str(example="success")


