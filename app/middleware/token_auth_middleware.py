from django.http import JsonResponse

from app.json_encoder import MyJSONEncoder
from app.models.account import Account
from app.models.session import Session


class TokenAuthMiddleware:
    EXEMPT_PATHS = {
        '/api/account/login',
        '/api/account/register',
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path.rstrip('/')
        if path.startswith('/api/') and path not in self.EXEMPT_PATHS:
            token = request.headers.get('token')
            if not token:
                return self.auth_failed()

            session = Session.objects.getByToken(token)
            if not session:
                return self.auth_failed()

            account = Account.objects.filter(pk=session.account).first()
            if not account:
                Session.objects.deleteByToken(token)
                return self.auth_failed()

            request.account_id = account.id
            request.user_id = account.user_id
            request.auth_token = token

        return self.get_response(request)

    def auth_failed(self):
        return JsonResponse({
            'code': -3,
            'msg': '登录超时',
            'data': {}
        }, encoder=MyJSONEncoder)
