def create_response(message, data, error):
    response =  {
        "message": message,
        "data": data
    }
    if(error):
        response["error"] = error

    return response


user_details_steps = [
    {
        '$lookup': {
            'from': 'Users',
            'localField': 'userId',
            'foreignField': '_id',
            'as': 'user_object'
        }
    },
    {
        '$set': {
            'userDetails': {
                'username': {'$arrayElemAt': ['$user_object.username', 0]}
            }
        }
    },
    {
        '$unset': 'user_object'
    }
]
