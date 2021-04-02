import frappe
import erpnext

# frappe.logger("frappe.web").debug(kwargs)

# practit
api_secret = 'd610d167fd1159a'
api_key = '06af9757a946c06'

@frappe.whitelist(allow_guest=True)
def bookAppointment(*args, **kwargs):

    data = kwargs

    slot = data['slot']


    if len(frappe.db.get_list('Patient', {'email': data['email']})) < 1:
        frappe.local.response.update({   
                'message': 'Failed to book patient', 
                'status':'error', 
                'error': "Patient doesn't exist yet"
        })
    


    # appointment = frappe.get_doc({
    #     'doctype':'Patient Appointment',
    #     'patient': 
    # })




    # frappe.local.response.update(response)



@frappe.whitelist(allow_guest=True)
def createPatient(*args, **kwargs):

    data = kwargs #request data

    try:
        # if len(frappe.db.get_list('Patient', {'email': data['email']})) > 0:
            # frappe.local.response.update({'message': 'Failed to create patient', 'error': 'Patient already exists','status':'error'})

        patient = frappe.get_doc({
            'doctype': "Patient", 'email': data['email'],
            'sex': data['sex'], 'first_name': (data['name']).split(' ')[0],
            'last_name': (data['name']).split(' ')[1], 'mobile': data['mobile']
        })
        patient.run_method('set_missing_values')
        patient.insert(ignore_permissions=True, ignore_links=True, ignore_mandatory=True)
        patient.submit()
        frappe.db.commit()
        patient.notify_update()
        frappe.local.response.update({'message': 'Patient {} created successfully'.format(patient.name), 'status':'success'})
    except Exception as e:
        frappe.local.response.update({'message': 'Failed to create patient', 'status':'error', 'error': str(e)})

        

@frappe.whitelist()
def getAppointments(*args, **kwargs):

    data = kwargs
    p = frappe.db.get_list('Patient', {'email': data['email']})
    if len(_p) < 1:
        frappe.local.response.update({'error': "A patient with that email doesn't exist", 'status':'error'})

    patient = frappe.get_doc('Patient', p[0]['name'])]

    # appointments = 
    



    frappe.local.response.update({'args': args, 'kw': kwargs})



@frappe.whitelist(allow_guest=True)
def getAvailableSlots(*args, **kwargs):

    # schedule = frappe.get_doc('Practitioner Schedule', 'Default Schedule')

    slots = frappe.db.get_list(
        'Healthcare Schedule Time Slot',
        fields=['day', 'name', 'from_time', 'to_time',],
        order_by='from_time desc', page_length=20
    )

    frappe.local.response.update({'availableSlots': slots})



@frappe.whitelist(allow_guest=True)
def ping(*args, **kwargs):
    frappe.local.response.update({'ping':'pong'})