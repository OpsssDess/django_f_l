from charity.forms import OfficeFormChoise

def officeFormChoise(request):
    return {
        'OfficeFormChoise': OfficeFormChoise(data={'officeChoise': request.session.get('office_id')})
    }

