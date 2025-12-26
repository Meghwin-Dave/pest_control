# Copyright (c) 2025, Meghwin Dave and contributors
# For license information, please see license.txt

import frappe


def execute():
	"""
	Fix Sales Order custom fields: Convert custom_call_back_visits and 
	custom_emergency_call_outs from Data (varchar) to Int safely
	"""
	# Clean existing data - set non-numeric values to NULL or 0
	frappe.db.sql("""
		UPDATE `tabSales Order`
		SET custom_call_back_visits = NULL
		WHERE custom_call_back_visits IS NOT NULL
		AND (custom_call_back_visits = '' OR custom_call_back_visits NOT REGEXP '^[0-9]+$')
	""")
	
	frappe.db.sql("""
		UPDATE `tabSales Order`
		SET custom_emergency_call_outs = NULL
		WHERE custom_emergency_call_outs IS NOT NULL
		AND (custom_emergency_call_outs = '' OR custom_emergency_call_outs NOT REGEXP '^[0-9]+$')
	""")
	
	# Convert numeric string values to integers
	frappe.db.sql("""
		UPDATE `tabSales Order`
		SET custom_call_back_visits = CAST(custom_call_back_visits AS UNSIGNED)
		WHERE custom_call_back_visits IS NOT NULL
		AND custom_call_back_visits REGEXP '^[0-9]+$'
	""")
	
	frappe.db.sql("""
		UPDATE `tabSales Order`
		SET custom_emergency_call_outs = CAST(custom_emergency_call_outs AS UNSIGNED)
		WHERE custom_emergency_call_outs IS NOT NULL
		AND custom_emergency_call_outs REGEXP '^[0-9]+$'
	""")
	
	frappe.db.commit()

