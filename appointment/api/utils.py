import frappe

def sync_ids():
    all_tests = frappe.get_all("Lab Test", fields =["patient","name"])
    for j in all_tests:
        id = frappe.get_value("Patient", j.get("patient"),"identification_number")
        doc = frappe.get_doc("Lab Test", j.get("name"))
        
        doc.db_set("identification_number", id)
        print("updated", j.get("name"))
def sync_invoices():
    for j in frappe.get_all("Sales Invoice", filters=dict(creation=[">","2021-08-25"])):
        invoice = frappe.get_doc("Sales Invoice",j.get("name"))
        invoice.db_set("customer_name", invoice.get("customer"))
        invoice.db_set("title", invoice.get("customer"))
        print("Worked on", invoice.get("name"))
def sales_invoice_on_save(doc, state):
    pass
#     for d in doc.get("items"):
#         if d.get("target_warehouse") and d.get("warehouse") == d.get("target_warehouse"):
#             d.get("target_warehouse") = None
