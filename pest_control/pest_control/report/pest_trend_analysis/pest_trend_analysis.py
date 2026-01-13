# Copyright (c) 2025, Meghwin Dave and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	"""
	Execute the Pest Trend Analysis Report
	
	Args:
		filters: Dictionary of filters from the report filters
		
	Returns:
		columns: List of column definitions
		data: List of data rows
	"""
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	"""Define report columns"""
	return [
		{
			"fieldname": "customer",
			"label": _("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 200
		},
		{
			"fieldname": "premise_address",
			"label": _("Premise Address"),
			"fieldtype": "Link",
			"options": "Address",
			"width": 200
		},
		{
			"fieldname": "area_location",
			"label": _("Area/Location"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "pest_noticed",
			"label": _("Pest Noticed"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "total_count",
			"label": _("Total Count"),
			"fieldtype": "Int",
			"width": 100
		},
		{
			"fieldname": "occurrences",
			"label": _("Occurrences"),
			"fieldtype": "Int",
			"width": 100
		},
		{
			"fieldname": "max_activity_level",
			"label": _("Max Activity Level"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "visit_date",
			"label": _("Visit Date"),
			"fieldtype": "Date",
			"width": 120
		}
	]


def get_data(filters):
	"""Get report data based on filters"""
	conditions = get_conditions(filters)
	
	query = """
		SELECT 
			mv.customer,
			mv.customer_address as premise_address,
			ptd.area_location,
			ptd.pest_noticed,
			SUM(COALESCE(ptd.pest_count, 0)) as total_count,
			COUNT(*) as occurrences,
			MAX(ptd.activity_level) as max_activity_level,
			mv.mntc_date as visit_date
		FROM 
			`tabMaintenance Visit` mv
			INNER JOIN `tabPest Trend Detail` ptd ON ptd.parent = mv.name
		WHERE 
			mv.docstatus = 1
			{conditions}
		GROUP BY 
			mv.customer, mv.customer_address, ptd.area_location, ptd.pest_noticed, mv.mntc_date
		ORDER BY 
			ptd.pest_noticed, SUM(COALESCE(ptd.pest_count, 0)) DESC
	""".format(conditions=conditions)
	
	data = frappe.db.sql(query, filters, as_dict=1)
	return data


def get_conditions(filters):
	"""Build WHERE clause conditions"""
	conditions = []
	
	if filters.get("from_date"):
		conditions.append("mv.mntc_date >= %(from_date)s")
	
	if filters.get("to_date"):
		conditions.append("mv.mntc_date <= %(to_date)s")
	
	if filters.get("customer"):
		conditions.append("mv.customer = %(customer)s")
	
	if filters.get("premise_address"):
		conditions.append("mv.customer_address = %(premise_address)s")
	
	return " AND " + " AND ".join(conditions) if conditions else ""

