import frappe
import erpnext
import json
# frappe.logger("frappe.web").debug(kwargs)

# practit
api_secret = 'd610d167fd1159a'
api_key = '06af9757a946c06'

@frappe.whitelist(allow_guest=True)
def bookAppointment(*args, **kwargs):

    data = kwargs

    _slot = data['slot']
    slot = frappe.get_doc('Healthcare Schedule Time Slot', _slot)
    # frappe.local.response.update({'slot': json.loads(slot.as_json())})
    # return
    

    _p = frappe.db.get_all('Patient', {'email': data['patient']})
    if len(_p) < 1:
        frappe.local.response.update({   
                'message': 'Failed to book patient', 
                'status':'error', 
                'error': "Patient doesn't exist yet"
        })
    

    try:
        appointment = frappe.get_doc({
            'doctype':'Patient Appointment',
            'patient': frappe.get_doc('Patient', _p[0]['name']),
            'appointment_datetime': '' ,
            'appointment_type': '',
            'company': frappe.get_doc('Company','Motire Occupational Safety and Health Solutions'),
            'department': frappe.get_doc('Medical Department', 'General'),
            'practitioner': frappe.get_doc('Practitioner', 'Dr. Motire')
        })
        appointment.run_method('set_missing_values')
        appointment.insert(ignore_permissions=True, ignore_links=True, ignore_mandatory=True)
        appointment.submit()
        frappe.db.commit()
        appointment.notify_update()
        frappe.local.response.update({'message': 'appointment {} created successfully'.format(appointment.name), 'status':'success'})

    except Exception as e:
        frappe.local.response.update({'message': 'Failed to create appointment', 'status':'error', 'error': str(e)})


def _g():
    res = []
    for i in range(9, 16):
        _from = '{}:00'.format(i)
        _to = '{}:00'.format(i + 1)
        _d = {"from_time": _from, "to_time": _to}
        res.append(_d)
    return res



@frappe.whitelist(allow_guest=True)
def createPatient(*args, **kwargs):

    data = kwargs #request data
    _p = frappe.db.get_all('Patient', {'email': data['email']})
    try:
        if len(_p) > 0:
            frappe.local.response.update({'message': 'Failed to create patient', 'error': 'Patient already exists','status':'error'})
            return

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
        frappe.local.response.update(
            {
                'message': 'Patient {} created successfully'.format(patient.name), 
                'status':'success',
                'patient':{
                    'name': data['name'],
                    'sex': data['sex'],
                    'email': data['email']
                }
            }
        )
        return
    except Exception as e:
        frappe.local.response.update({'message': 'Failed to create patient', 'status':'error', 'error': str(e)})
        return

        

@frappe.whitelist()
def getAppointments(*args, **kwargs):

    data = kwargs
    # check for email parameter in url: ?email={patient_email}
    if not 'email' in kwargs:frappe.local.response.update({'error': "A patient email hasn't been specified", 'status':'error'})

    # check if the patient is registered
    _p = frappe.db.get_all('Patient', {'email': data['email']})
    if len(_p) < 1:frappe.local.response.update({'error': "A patient with that email doesn't exist", 'status':'error'})

    patient = frappe.get_doc('Patient', _p[0]['name'])

    appointments = frappe.get_all(
        'Patient Appointment',
        filters={'patient_name': patient.patient_name},
        fields=['practitioner_name', 'duration', 'status', 'name', 'patient_name', 
            'appointment_datetime', 'appointment_type', 'company'
        ]
    )
    frappe.local.response.update({'appointments': appointments})


@frappe.whitelist(allow_guest=True)
def getAvailableSlots(*args, **kwargs):

    data =  kwargs
    date = data['date'] 

    # schedule = frappe.get_doc('Practitioner Schedule', 'Default Schedule
    slots = frappe.db.get_all(
        'Healthcare Schedule Time Slot',
        fields=['day', 'name', 'from_time', 'to_time',],
        order_by='from_time desc', page_length=20
    )
    frappe.local.response.update({'availableSlots': slots})



@frappe.whitelist(allow_guest=True)
def ping(*args, **kwargs):
    frappe.local.response.update({'ping':'pong'})
    return


def get_available_slots():
    data = frappe.db.get_all(
        '''
            SELECT 
        '''
    )
    # data = frappe.db.sql()
    d = _g()

    c = frappe.get_all('Patient Appointment',
        filters={'appointment_date': '2021-04-05'}, 
        fields=['appointment_date', 'appointment_time',  'patient',]
    )
    for i in c:
        x = str(i['appointment_time'])
        int(x.split[':'][0])




# for i in appointments:

