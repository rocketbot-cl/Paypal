# coding: utf-8
"""
Base para desarrollo de modulos externos.
Para obtener el modulo/Funcion que se esta llamando:
     GetParams("module")

Para obtener las variables enviadas desde formulario/comando Rocketbot:
    var = GetParams(variable)
    Las "variable" se define en forms del archivo package.json

Para modificar la variable de Rocketbot:
    SetVar(Variable_Rocketbot, "dato")

Para obtener una variable de Rocketbot:
    var = GetVar(Variable_Rocketbot)

Para obtener la Opcion seleccionada:
    opcion = GetParams("option")


Para instalar librerias se debe ingresar por terminal a la carpeta "libs"

    pip install <package> -t .

"""


import os
import sys
base_path = tmp_global_obj["basepath"]
cur_path = base_path + "modules" + os.sep + "paypal" + os.sep + "libs" + os.sep
if cur_path not in sys.path:
    sys.path.append(cur_path)
from paypal import PayPal

module = GetParams("module")

global mod_paypal

if module == "login":
    try:
        client_id = GetParams("client_id")
        client_secret = GetParams("client_secret")
        mod_paypal = PayPal(client_id, client_secret)
        mod_paypal.login()

    except Exception as e:
        print("\x1B[" + "31;40mError\x1B[" + "0m")
        PrintException()
        raise e

if module == "add_person":
    name = GetParams("name")
    email = GetParams("email")
    billing_name = GetParams("billing_name")
    given_name = GetParams("given_name")
    billing_surname = GetParams("billing_surname")
    given_surname = GetParams("given_surname")
    address_line_1 = GetParams("address_line_1")
    address_line_2 = GetParams("address_line_2")
    admin_area_1 = GetParams("admin_area_1")
    admin_area_2 = GetParams("admin_area_2")
    postal_code = GetParams("postal_code")
    country_code_1 = GetParams("country_code_1")
    country_code_2 = GetParams("country_code_2")
    phone_number = GetParams("phone_number")
    phone_type = GetParams("phone_type")

    try:
        name1 = {"given_name": billing_name, "surname": billing_surname}
        data = {"address_line_1": address_line_1, "address_line_2": address_line_2, "admin_area_2": admin_area_2, "admin_area_1": admin_area_1, "postal_code": postal_code, "country_code": country_code_1}
        address = {key: value for key, value in data.items() if value}
        phones = [{"country_code": country_code_2, "national_number": phone_number, "phone_type": phone_type}]

        billing_info = {"name": name1, "address": address, "email_address": email, "phones": phones}

        name2 = {"given_name": given_name, "given_surname": given_surname}
        data = {"address_line_1": address_line_1, "address_line_2": address_line_2, "admin_area_2": admin_area_2,
                "admin_area_1": admin_area_1, "postal_code": postal_code, "country_code": country_code_1}
        address = {key: value for key, value in data.items() if value}
        shipping_info = {"name": name2, "address": address}
        person = {"billing_info": billing_info, "shipping_info": shipping_info}
        mod_paypal.addPerson(person)


    except Exception as e:
        print("\x1B[" + "31;40mError\x1B[" + "0m")
        PrintException()
        raise e

if module == "add_invoicer":
    name = GetParams("name")
    surname = GetParams("surname")
    address_line_1 = GetParams("address_line_1")
    address_line_2 = GetParams("address_line_2")
    admin_area_1 = GetParams("admin_area_1")
    admin_area_2 = GetParams("admin_area_2")
    postal_code = GetParams("postal_code")
    country_code_1 = GetParams("country_code_1")
    country_code_2 = GetParams("country_code_2")
    phone_number = GetParams("phone_number")
    phone_type = GetParams("phone_type")
    email = GetParams("email")

    try:
        name = {"given_name": name, "surname": surname}
        data = {"address_line_1": address_line_1, "address_line_2": address_line_2, "admin_area_2": admin_area_2,
                "admin_area_1": admin_area_1, "postal_code": postal_code, "country_code": country_code_1}
        address = {key: value for key, value in data.items() if value}
        phones = [{"country_code": country_code_2, "national_number": phone_number, "phone_type": phone_type}]
        invoicer = {"name": name, "address": address, "email_address": email, "phones": phones}
        mod_paypal.addInvoicer(invoicer)

    except Exception as e:
        print("\x1B[" + "31;40mError\x1B[" + "0m")
        PrintException()
        raise e



if module == "create_draft":

    date = GetParams("date")
    currency_code = GetParams("currency_code")
    note = GetParams("note")
    term = GetParams("term")
    memo = GetParams("memo")
    term_type = GetParams("term_type")
    due_date = GetParams("due_date")


    try:
        response = mod_paypal.createInvoiceDraft(date, currency_code, note, term, memo, term_type, due_date)
        print(response.json())
    except Exception as e:
        print("\x1B[" + "31;40mError\x1B[" + "0m")
        PrintException()
        raise e


if module == "share":
    try:

        headers = {'Authorization': 'Zoho-oauthtoken ' + mod_zoho.access_token}
        respjson = mod_zoho.response

        req_data = {}
        respjson = respjson['requests']
        request_id = respjson['request_id']
        #field_info = eval(field_info)
        a = mod_zoho.submitDocument(request_id, respjson, mod_zoho.access_token, mod_zoho.field_info)
        if a["status"] == "failure":
            raise Exception(a["message"])

    except Exception as e:
        print("\x1B[" + "31;40mError\x1B[" + "0m")
        PrintException()
        raise e

if module == "add_item":
    item = GetParams("item")
    description = GetParams("description")
    quantity = GetParams("quantity")
    currency_code = GetParams("currency_code")
    value = GetParams("value")
    tax_name = GetParams("tax_name")
    tax_percent = GetParams("tax_percent")
    discount = GetParams("discount")

    try:
        unit_amount = {"currency_code": currency_code, "value": value}
        tax = {"name": tax_name, "percent": tax_percent}
        discount = {"percent": discount}
        data = {}
        data["name"] = item
        data["description"] = description
        data["quantity"] = quantity
        data["unit_amount"] = unit_amount
        data["tax"] = tax
        data["discount"] = discount
        data["unit_of_measure"] = quantity
        mod_paypal.addItem(data)


    except Exception as e:
        print("\x1B[" + "31;40mError\x1B[" + "0m")
        PrintException()
        raise e

