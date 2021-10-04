# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "appointment"
app_title = "Appointment"
app_publisher = "Lonius Health & MTRH and contributors"
app_description = "Appointment"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@motire.co.ke"
app_license = "MIT"

# Includes in <head>
# ------------------
fixtures =["Client Script"]
# include js, css files in header of desk.html
# app_include_css = "/assets/appointment/css/appointment.css"
# app_include_js = "/assets/appointment/js/appointment.js"

# include js, css files in header of web template
# web_include_css = "/assets/appointment/css/appointment.css"
# web_include_js = "/assets/appointment/js/appointment.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "appointment/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "appointment.install.before_install"
# after_install = "appointment.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "appointment.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	# "*": {
	# 	"on_update": "method",
	# 	"on_cancel": "method",
	# 	"on_trash": "method"
	# }
	"Lab Test": {
		"before_save":"appointment.appointment.utils.lab_test_consumables.sync_template_consumables",
		"before_submit": "appointment.appointment.utils.lab_test_consumables.post_lab_stock_transactions",
		"before_update_after_submit": "appointment.appointment.utils.lab_utils.lab_test_alert"
	},
	"Sales Invoice":{
		"before_save":"appointment.api.utils.sales_invoice_on_save"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"appointment.tasks.all"
# 	],
# 	"daily": [
# 		"appointment.tasks.daily"
# 	],
# 	"hourly": [
# 		"appointment.tasks.hourly"
# 	],
# 	"weekly": [
# 		"appointment.tasks.weekly"
# 	]
# 	"monthly": [
# 		"appointment.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "appointment.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "appointment.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "appointment.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

