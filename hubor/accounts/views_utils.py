'''
================ HELPER FUNCTIONS ================
'''
# is the request is sent by given id
def isSelf(request, id) -> bool:
    return request.user.id == id

# is the request is sent by him/herself or by a staff
def isSelfOrStaff(request, id) -> bool:
    # check if this request is authorized.
    # - only doctors, admins, and patient himself can post
    return request.user.user_type == 1 or request.user.user_type == 2 or request.user.id == id

# is the request is sent by staff
def isStaff(request) -> bool:
    return request.user.user_type == 1 or request.user.user_type == 2

# is the request is sent by admin
def isAdmin(request) -> bool:
    return request.user.user_type == 2