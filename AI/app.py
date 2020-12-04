response = {
    'success': True,
    'message': ''
}

def main(event, context):
    payload = event
    isFor = payload.isFor
    data = payload.data

    if isFor == 'get_user_recommendations':
        # Call the corresponding Function

    return response

