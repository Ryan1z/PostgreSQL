from marshmallow import Schema, fields


class UserGetSchema(Schema):
    name = fields.Str(example="string")


class UserPostSchema(Schema):
    name = fields.Str(doc="name", example="string", required=True)
    # own_id = fields.Str(doc="own_id", example="string")
    
# Response
class UserGetResponse(Schema):
    message = fields.Str(example="success")
    datatime = fields.Str(example="1970-01-01T00:00:00.000000")
    data = fields.List(fields.Dict())
    #data = fields.List(fields.Dict())  #強制輸出型態

class UsersGetResponse(Schema):
    message = fields.Str(example="success")
    datatime = fields.Str(example="1970-01-01T00:00:00.000000")
    data = fields.Dict()  
    # data = fields.List(fields.Dict()) #強制輸出型態
    
class UserCommonResponse(Schema):
    message = fields.Str(example="success")
    
    
class UserPatchSchema(Schema):
    name = fields.Str(doc="name", example="string", required=True)
    owner_id = fields.Str(doc="owner_id", example="string")
    

    