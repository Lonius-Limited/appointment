from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import flt, nowdate, nowtime, cstr
from erpnext.healthcare.doctype.healthcare_settings.healthcare_settings import get_account

def sync_template_consumables(doc, state):
    test_template = frappe.get_doc("Lab Test Template", doc.template)
    consumables = test_template.get("lab_test_consumables")
    if consumables:
        def _map_items(consumable_item):
            existing_items =[x.get("item") for x in doc.get("lab_test_consumables")]
            if consumable_item.get("item") in existing_items: return
            consumable_item.name = frappe.utils.frappe.generate_hash(length=10)
            consumable_item.parenttype = doc.doctype
            consumable_item.parent = doc.name
            doc.append("lab_test_consumables",consumable_item)
        list(map(lambda x: _map_items(x), consumables))
def post_lab_stock_transactions(doc, state):
    if doc.get("lab_test_consumables"):
        make_stock_entry(doc)
@frappe.whitelist()
def make_stock_entry(doc):
	stock_entry = frappe.new_doc('Stock Entry')
	stock_entry = set_stock_items(stock_entry, doc.name, 'Lab Test')
	stock_entry.stock_entry_type = 'Material Issue'
	stock_entry.from_warehouse = doc.warehouse
	stock_entry.company = doc.company
	expense_account = get_account(None, 'expense_account', 'Healthcare Settings', doc.company)

	for item_line in stock_entry.items:
		cost_center = frappe.get_cached_value('Company',  doc.company,  'cost_center')
		item_line.cost_center = cost_center
		item_line.expense_account = expense_account

	stock_entry.save(ignore_permissions=True)
	stock_entry.submit()
	return stock_entry.name
def set_stock_items(doc, stock_detail_parent, parenttype):
	items = get_items('Lab Test Item', stock_detail_parent, parenttype)

	for item in items:
		se_child = doc.append('items')
		se_child.item_code = item.item_code
		se_child.item_name = item.item_name
		se_child.uom = item.uom
		se_child.stock_uom = item.stock_uom
		se_child.qty = flt(item.qty)
		# in stock uom
		se_child.transfer_qty = flt(item.transfer_qty)
		se_child.conversion_factor = flt(item.conversion_factor)
		if item.batch_no:
			se_child.batch_no = item.batch_no

	return doc

def get_items(table, parent, parenttype):
	items = frappe.db.get_all(table, filters={
		'parent': parent,
		'parenttype': parenttype
	}, fields=['*'])

	return items