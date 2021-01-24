import requests

"""
This exception is used when there is a problem with some of the data sent.
"""
class ValidationError(Exception):
    status_code = 400
    def __init__(self, message, payload):
        Exception.__init__(self)
        self.message = message
        self.payload = payload
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

"""
This exception is used when there is a problem with the access token.
"""
class AuthorizationError(Exception):
    status_code = 401
    def __init__(self, message, payload):
        Exception.__init__(self)
        self.message = message
        self.payload = payload
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

"""
This exception is used with generic errors.
"""
class FailedRequest(Exception):
    def __init__(self, message, status_code, payload):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv      

class PyPayPal:
    def __init__(self, client_id, secret, sandbox=False):
        self.client_id = client_id
        self.secret = secret

        self.api_url = 'https://api-m.paypal.com'
        if sandbox:
            self.api_url = 'https://api-m.sandbox.paypal.com'

        access_token = self.get_access_token()

        """
        Use this Session instance to query the API.
        """
        api = requests.Session()
        api.headers.update({ 'Authorization': f'Bearer {access_token}' })
        self.api = api

        """
        Use this dictionary to easily create routes
        to query specific API resources.
        """
        self.resources = {
            'products': self.url('/catalogs/products'),
            'plans': self.url('/billing/plans'),
            'subscriptions': self.url('/billing/subscriptions')
        }

    def url(self, path, version=1):
        """
        Use this function to easily create routes for
        query the API.
        """
        if version == 2:
            return self.api_url + '/v2' + path
        else:
            return self.api_url + '/v1' + path

    def get_access_token(self):
        """
        This function is used to obtain the access token.
        You probably don't need to use it at any time.
        """
        url = self.url('/oauth2/token')
        auth = (self.client_id, self.secret)
        result = requests.post(url, 'grant_type=client_credentials', auth=auth)
        if result.status_code == 200:
            return result.json()['access_token']
        else:
            return None

    def handle_response(self, response):
        """
        This function is used to handle API responses.
        You probably don't need to use it at any time.
        """
        status_code = response.status_code
        data = response.json()
        if status_code >= 200 and status_code < 300:
            return data
        else:
            if status_code == 401:
                message = data['error']
                payload = data['error_description']
                raise AuthorizationError(message, payload)
            message = data['message']
            payload = data['details']
            if status_code == 400:
                raise ValidationError(message, payload)
            raise FailedRequest(message, status_code, payload)


    def list_products(self):
        """
        Use this function to list the products.
        """
        url = self.resources['products']
        response = self.api.get(url)
        data = response.json()
        return self.handle_response(response)
    
    def list_plans(self):
        """
        Use this function to list the plans.
        """
        url = self.resources['plans']
        response = self.api.get(url)
        return self.handle_response(response)

    def show_plan_details(self, id):
        """
        Use this function to view the details of a plan.
        """
        url = self.resources['plans'] + f'/{id}'
        response = self.api.get(url)
        return self.handle_response(response)

    def show_subscription_details(self, id):
        """
        Use this function to view the details of a subscription.
        """
        url = self.resources['subscriptions'] + f'/{id}'
        response = self.api.get(url)
        return self.handle_response(response)

    def list_transactions_for_subscription(self, id):
        """
        Use this feature to view transactions for a subscription.
        """
        url = self.resources['subscriptions'] + f'/{id}/transactions'
        response = self.api.get(url)
        return self.handle_response(response)

    def create_subscription(self, plan_id):
        """
        Use this function to create a subscription.
        """
        url = self.resources['subscriptions']
        response = self.api.post(url, json={'plan_id': plan_id})
        return self.handle_response(response)

    def cancel_subscription(self, id, reason):
        """
        Use this function to cancel a subscription.
        """
        url = self.resources['subscriptions'] + f'/{id}/cancel'
        response = self.api.post(url, json={'reason': reason})
        return self.handle_response(response)

    def activate_subscription(self, id, reason):
        """
        Use this function to activate a subscription.
        """
        url = self.resources['subscriptions'] + f'/{id}/activate'
        response = self.api.post(url, json={'reason': reason})
        return self.handle_response(response)
