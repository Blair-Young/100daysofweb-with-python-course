from typing import List
import json
from apistar import App, Route, types, validators
from apistar.http import JSONResponse


def _load_contacts_data():
    with open('bojack-contacts.json') as f:
        contacts = json.loads(f.read())
    return {c["email"]: c for c in contacts}

contacts = _load_contacts_data()
all_emails = [c for c in contacts.keys()]
CONTACT_NOT_FOUND = 'Contact not found'

class Contact(types.Type):
    scientific_name = validators.String(min_length=4)
    common_name = validators.String(min_length=3)
    full_name = validators.String(min_length=2)
    email = validators.String()
    city = validators.String()


def get_all_contacts() -> List:
    return contacts

def create_contact(contact:Contact) -> JSONResponse:
    contact = Contact(contact)
    contacts[contact['email']] = contact
    return JSONResponse(contact, status_code=201)


def get_contact(email:str) ->JSONResponse:
    contact = contacts.get(email)
    if not contact:
        error = {'error': CONTACT_NOT_FOUND}
        return JSONResponse(error, status_code=404)
    details = contacts[email]
    return JSONResponse(details, status_code=200)


def edit_contact(email:str, update_contact:Contact) -> JSONResponse:
    contact = contacts.get(email)
    if not contact:
        error = {'error':CONTACT_NOT_FOUND}
        return JSONResponse(error, 404)
    contacts[email] = update_contact
    return JSONResponse(update_contact, status_code=200)


def delete_contact(email:str) -> JSONResponse:
    contact = contacts.get(email)
    if not contact:
        error = {'error':CONTACT_NOT_FOUND}
        return JSONResponse(error, status_code=404)
    deleted_contact = contacts.pop(email)
    return JSONResponse(deleted_contact, status_code=204)




routes = [Route('/', method='GET', handler=get_all_contacts),
          Route('/', method='POST', handler=create_contact),
          Route('/{email}/', method='GET', handler=get_contact),
          Route('/{email}/', method='PUT', handler=edit_contact),
          Route('/{email}/', method='DELETE', handler=delete_contact)
         ]


app = App(routes=routes)

if __name__ =='__main__':
    app.serve('127.0.0.1', 5000)