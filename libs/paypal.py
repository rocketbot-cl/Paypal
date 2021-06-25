import requests


class PayPal:

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.recipients = []
        self.items = []

    def login(self):
        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en_US',
        }
        data = {
            'grant_type': 'client_credentials'
        }
        response = requests.post('https://api-m.sandbox.paypal.com/v1/oauth2/token', headers=headers, data=data,
                                 auth=(self.client_id, self.client_secret))
        respjson = response.json()
        print(respjson)
        self.access_token = respjson['access_token']

    def addPerson(self, person):
        self.recipients.append(person)

    def addItem(self, item):
        self.items.append(item)

    def addInvoicer(self, invoicer):
        self.invoicer = invoicer

    def createInvoiceDraft(self, date, currency_code, note, term, memo, term_type, due_date):
        authorization = "Bearer " + self.access_token
        headers = {
            'Content-Type': 'application/json',
            'Authorization': authorization,
        }

        response = requests.post('https://api-m.sandbox.paypal.com/v2/invoicing/generate-next-invoice-number',
                                 headers=headers)
        respjson = response.json()
        invoice_number = respjson['invoice_number']

        payment_term = {}
        payment_term['term_type'] = term_type
        payment_term['due_date'] = due_date

        detail = {}
        detail['invoice_number'] = invoice_number
        detail['reference'] = 'deal-ref'
        detail['currency_code'] = currency_code
        detail['note'] = note
        detail['invoice_date'] = date
        detail['term'] = term
        detail['memo'] = memo
        detail['payment_term'] = payment_term

        datajson = {}
        datajson['detail'] = detail
        datajson['invoicer'] = self.invoicer
        datajson['primary_recipients'] = self.recipients
        datajson['items'] = self.items

        data = datajson
        print(data)
        response = requests.post('https://api-m.sandbox.paypal.com/v2/invoicing/invoices', headers=headers, data=data)
        return response


"""
client_id = 'ATgijFs8JZWdAPxMsNhN_Vl3VgZhIvzmPDwUCXjzMHdOFoOjM_mqXua1AaaKhiiEnyHlk8_tXoYsRZbc'
secret = 'ENu6GbuB-Fzc6Y0F7w1ouYhqQnkpyTUXEu3k7utvo3bqkjikJLk1GZKuolkR7Ymy2hNPpZUhXdW0Zf39'

headers = {
    'Accept': 'application/json',
    'Accept-Language': 'en_US',
}

data = {
    'grant_type': 'client_credentials'
}

response = requests.post('https://api-m.sandbox.paypal.com/v1/oauth2/token', headers=headers, data=data,
                         auth=(client_id, secret))

respjson = response.json()
access_token = respjson['access_token']
print(access_token)
"""
