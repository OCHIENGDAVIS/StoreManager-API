import unittest
import json
from app import flask_app


class TestSetUp(unittest.TestCase):
    """Initialize the app with test data"""
    def setUp(self):
        self.app = flask_app.test_client()
        self.login_url = '/api/v1/auth/login'
        self.user = dict(email="testuser@gmail.com", password="testpass1234")
        self.unknown = dict(email="username@gmail.com", password="password")
        self.register = self.app.post('/api/v1/auth/register',
                                      data=json.dumps(self.user),
                                      headers={"content-type": "application/json"})
        self.login = self.app.post(self.login_url, data=json.dumps(self.user), content_type='application/json')
        self.data = json.loads(self.login.get_data(as_text=True))
        self.token = self.data['token']
        self.app.post("/api/v1/auth/register", data=json.dumps(self.unknown),content_type="application/json")
        self.missing_email = dict(email="", password="testpass")
        self.product = dict(name="Shoe Polish", description="Kiwi Shoe Polish", price=1200, quantity=30)
        self.new_product = dict(name="Kiatu mzuri", description="Ni kiatu tu", price=1200,
                                quantity=30)
        self.empty_product = dict(name="", description="", price="", quantity=0)
        self.missing_prod_quantity = dict(name="Shoe", description="Ni kiatu tu", price=1200,
                                          quantity=0)
        self.quantity_string = dict(name="Shoe", description="Ni kiatu tu", price=1200,
                                    quantity="50")

        self.missing_prod_description = dict(name="Kiatu mzuri", description="", price="1200",
                                             quantity=10)
        self.missing_prod_price = dict(name="Kiatu mzuri", description="Kiatu tu", price=0,
                                       quantity=50)
        self.prod_price_string = dict(name="Kiatu mzuri", description="kiatu", price="100",
                                      quantity=50)
        self.new_product = dict(name="Kiatu mzuri", description="Ni kiatu tu", price=1200,
                                quantity=40)
        self.sale = dict(prod_id=1, quantity=20)
        self.new_sale = dict(prod_id=1, quantity=10)
        self.empty_sale = dict(quantity=0, prod_id=0)
        self.zero_sale_quantity = dict(quantity=0, prod_id=1)
        self.sale_quantity_string = dict(quantity="", prod_id=1)
        self.sale_prod_id_string = dict(quantity=20, prod_id="")
        self.wrong_email_format = dict(email="1234.xxx", password="testpass")
        self.invalid_email = dict(emaile="testuser.gmail.com", password="invalid")
        self.invalid_password = dict(email="testuser3@gmail.com", password="t")
        self.password_spaced = dict(email="testuser5@gmail.com", password="  ")
        self.unknown_login = self.app.post("/api/v1/auth/login", data=json.dumps(self.unknown),
                                           content_type="application/json")
        self.data = json.loads(self.unknown_login.get_data(as_text=True))
        self.unknown_token = self.data['token']
