import frappe, json
import datetime, requests

LAB_TEST_DOCTYPE = "Lab Test"
NPHL_RESULT_DOCTYPE = "Lab Test NPHL Result"
USERNAME = frappe.db.get_single_value("OSH Settings", "nphl_user_name")
PASSWORD = frappe.db.get_single_value("OSH Settings", "nphl_password")
FACILITY_NAME = frappe.db.get_single_value("OSH Settings", "nphl_facility_name")
FACILITY_CODE = frappe.db.get_single_value("OSH Settings", "nphl_facility_code")
NPHL_URI = frappe.db.get_single_value("OSH Settings","nphl_uri")


def post_unsubmitted_request():
	unposted_cases = get_unposted_cases()
	for case in unposted_cases:
		case_id = case#"HLC-LAB-2021-00682"
		payload = get_case_from_lab_test(lab_test_name=case_id)[0]
		# return payload
		url = NPHL_URI
		x = requests.post(url, json=payload)
		print(x.content)
		frappe.get_doc(
			dict(
				doctype=NPHL_RESULT_DOCTYPE,
				lab_test=case_id,
				result="{0}".format(x.content),
				is_success=1 if "SUCCESS" in str(x.content) else 0,
				status = "Sent" if "SUCCESS" in str(x.content) else "Failed",
			)
		).insert()
def get_unposted_cases():
	return ["HLC-LAB-2021-00682"]
	query_str = '''SELECT name FROM `tabLabTest` WHERE name NOT IN (SELECT lab_test FROM `tabLab Test NPHL Result`)'''	
	unposted = frappe.db.sql(query_str, as_dict=1)
	return [x.get("name") for x in unposted]
def get_case_from_lab_test(lab_test_name=None):
	query_str = frappe.get_doc("Report", "Covid 19 Lab Tests").get("query")
	query_str += """ AND `tabLab Test`.name ='{0}'""".format(lab_test_name)
	lab_test = frappe.db.sql(query_str, as_dict=1)
	lab_test = sanitize_dict(lab_test)
	return lab_test


def sanitize_dict(the_dict):
	keys = list(the_dict[0].keys())
	seperator = ":"
	elem = the_dict[0]
	for j in keys:
		if isinstance(elem[j], datetime.date):
			print(j)
			acceptable_date = elem[j].strftime("%Y-%m-%d")
			elem[str(j.split(seperator, 1)[0]).upper()] = acceptable_date
			elem.pop(j)
			continue
		elem[str(j.split(seperator, 1)[0]).upper().replace(" ", "_")] = elem.pop(j)

	elem["USERNAME"] = USERNAME
	elem["PASSWORD"] = PASSWORD
	elem["TESTING_LAB"] = FACILITY_CODE
	# elem["COUNTY_OF_DIAGNOSIS"]=COUNTY_OF_DIAGNOSIS

	sanitized_elem = elem
	return [sanitized_elem]


def get_mandatory_params():
	params = []
	# return get_mandatory_params_and_data()[0].values()
	for param in get_mandatory_params_and_data():
		params.append(param.get("Parameter").lower())
	# print (params)
	return params


def get_mandatory_params_and_data():
	return [
		{"Parameter": "USERNAME", "Description": "Mandatory"},
		{"Parameter": "PASSWORD", "Description": "Mandatory"},
		{
			"Parameter": "TESTING_LAB",
			"Description": "Code of the testing lab(See lab codes below). Mandatory",
		},
		{"Parameter": "CASE_ID", "Description": ""},
		{
			"Parameter": "CASE_TYPE",
			"Description": "Either                                          Initial or                                         Repeat. Mandatory",
		},
		{
			"Parameter": "SAMPLE_TYPE",
			"Description": "One of:                                          NP Swab,                                         OP Swab,                                         Serum,                                         Sputum or                                         Tracheal Aspirate. Mandatory",
		},
		{
			"Parameter": "SAMPLE_NUMBER",
			"Description": "Unique identifier for the sample at the testing lab. Mandatory",
		},
		{
			"Parameter": "SAMPLE_COLLECTION_DATE",
			"Description": "Date format is Y-m-d e.g. 2020-05-31. Mandatory",
		},
		{
			"Parameter": "RECEIVED_ON",
			"Description": "Date format is Y-m-d e.g. 2020-05-31. Mandatory",
		},
		{
			"Parameter": "RESULT",
			"Description": "Negative or                                         Positive. Mandatory",
		},
		{
			"Parameter": "LAB_CONFIRMATION_DATE",
			"Description": "Date format is Y-m-d e.g. 2020-05-31. Mandatory",
		},
		{
			"Parameter": "FIRST_FOLLOW_UP_DATE",
			"Description": "Date format is Y-m-d e.g. 2020-05-31",
		},
		{"Parameter": "FIRST_FOLLOW_UP_RESULT", "Description": ""},
		{
			"Parameter": "SECOND_FOLLOW_UP_DATE",
			"Description": "Date format is Y-m-d e.g. 2020-05-31",
		},
		{"Parameter": "SECOND_FOLLOW_UP_RESULT", "Description": ""},
		{
			"Parameter": "THIRD_FOLLOW_UP_DATE",
			"Description": "Date format is Y-m-d e.g. 2020-05-31",
		},
		{"Parameter": "THIRD_FOLLOW_UP_RESULT", "Description": ""},
		{"Parameter": "PATIENT_NAMES", "Description": "Mandatory"},
		{"Parameter": "PATIENT_PHONE", "Description": ""},
		{"Parameter": "AGE", "Description": "Mandatory"},
		{"Parameter": "AGE_UNIT", "Description": "Years, months or days. Mandatory"},
		{
			"Parameter": "GENDER",
			"Description": "F for Female and                                         M for Male. Mandatory",
		},
		{"Parameter": "OCCUPATION", "Description": ""},
		{"Parameter": "NATIONALITY", "Description": "Mandatory"},
		{
			"Parameter": "NATIONAL_ID",
			"Description": "National ID / Passport Number / Alien ID",
		},
		{"Parameter": "COUNTY", "Description": "County of residence. Mandatory"},
		{"Parameter": "SUB_COUNTY", "Description": "Mandatory"},
		{"Parameter": "WARD", "Description": ""},
		{"Parameter": "VILLAGE", "Description": "Mandatory"},
		{
			"Parameter": "HAS_TRAVEL_HISTORY",
			"Description": "Either                                          Yes or                                         No",
		},
		{"Parameter": "TRAVEL_FROM", "Description": ""},
		{
			"Parameter": "CONTACT_WITH_CASE",
			"Description": "Did the patient have contact with a confirmed case? Either                                          Yes or                                         No",
		},
		{"Parameter": "CONFIRMED_CASE_NAME", "Description": ""},
		{
			"Parameter": "SYMPTOMATIC",
			"Description": "Does the patient display symptoms? Either                                          Yes or                                         No",
		},
		{
			"Parameter": "SYMPTOMS",
			"Description": "Semi-colon delimited list of symptoms",
		},
		{
			"Parameter": "SYMPTOMS_ONSET_DATE",
			"Description": "Date format is Y-m-d e.g. 2020-05-31",
		},
		{
			"Parameter": "COUNTY_OF_DIAGNOSIS",
			"Description": "County where the case was isolated. Mandatory",
		},
		{
			"Parameter": "QUARANTINED_FACILITY",
			"Description": "The quarantine facility name (if quarantined)",
		},
		{
			"Parameter": "HOSPITALIZED",
			"Description": "Either                                          Yes,                                         No or                                         Unknown",
		},
		{
			"Parameter": "ADMISSION_DATE",
			"Description": "Date format is Y-m-d e.g. 2020-05-31",
		},
	]
