from __future__ import unicode_literals
import frappe, json, regex, re
from frappe.core.doctype.sms_settings.sms_settings import send_sms
from frappe.utils import get_url, cint, file_lock
from frappe.utils.background_jobs import enqueue
from frappe import _


def lab_test_alert(doc, state):
    frappe.msgprint("Lab test status {0}".format(doc.get("status")))
    if doc.get("status") == "Approved":
        email_msg = "Dear {0}, Please find attached Lab Test Result from {1}".format(
            doc.get("patient"), doc.get("company")
        )
        frappe.msgprint(email_msg)

@frappe.whitelist()
def send_lab_alert(docname):
    doc = frappe.get_doc("Lab Test", docname)
    email_msg = "Dear {0}, Please find attached Lab Test Result from {1}".format(
        doc.get("patient"), doc.get("company")
    )
    sms_msg = "Hello {0} your {1} results have been emailed to {2}. {3}".format(
        doc.patient, doc.lab_test_name, doc.email, doc.company
    )
    pt_doc = frappe.get_doc("Patient", doc.patient)
    email, phone = pt_doc.get("email"), pt_doc.get("mobile") or pt_doc.get("phone")
    if phone:
        send_sms([phone], sms_msg)
    if email:
        send_notifications(
            [email],
            email_msg,
            "Lab Test Result {0}".format(doc.get("name")),
            doc.get("doctype"),
            doc.get("name"),
        )
def send_notifications(email_list, message, subject, doctype, docname):
    # template_args = get_common_email_args(None)
    attachments = [frappe.attach_print(doctype, docname, file_name=docname)]
    email_args = {
        "recipients": email_list,
        "message": _(message),
        "subject": subject,
        "attachments": attachments or None,
        "reference_doctype": doctype,
        "reference_name": docname,
    }
    enqueue(method=frappe.sendmail, queue="short", timeout=300, **email_args)
