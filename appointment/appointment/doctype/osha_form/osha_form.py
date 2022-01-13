# Copyright (c) 2021, Lonius Health & MTRH and contributors and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class OSHAForm(Document):
	def before_save(self):
		if self.time_of_encounter: return
		self.time_of_encounter= self.creation
