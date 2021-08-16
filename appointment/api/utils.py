import frappe

def sync_ids():
    all_tests = frappe.get_all("Lab Test", fields =["patient","name"])
    for j in all_tests:
        id = frappe.get_value("Patient", j.get("patient"),"identification_number")
        doc = frappe.get_doc("Lab Test", j.get("name"))
        
        doc.db_set("identification_number", id)
        print("updated", j.get("name"))