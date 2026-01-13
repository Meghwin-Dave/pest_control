# Copyright (c) 2025, Meghwin Dave and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	"""
	Execute the Group Contract Summary Report
	
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
			"fieldname": "total_visits",
			"label": _("Total Visits"),
			"fieldtype": "Int",
			"width": 100
		},
		{
			"fieldname": "high_activity_visits",
			"label": _("High Activity Visits"),
			"fieldtype": "Int",
			"width": 130
		},
		{
			"fieldname": "medium_activity_visits",
			"label": _("Medium Activity Visits"),
			"fieldtype": "Int",
			"width": 150
		},
		{
			"fieldname": "low_activity_visits",
			"label": _("Low Activity Visits"),
			"fieldtype": "Int",
			"width": 140
		},
		{
			"fieldname": "highest_activity_level",
			"label": _("Highest Activity Level"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "total_pest_count",
			"label": _("Total Pest Count"),
			"fieldtype": "Int",
			"width": 130
		}
	]


def get_data(filters):
	"""Get report data based on filters"""
	if not filters.get("customer"):
		frappe.throw(_("Please select a Customer"))
	
	conditions = get_conditions(filters)
	
	query = """
		SELECT 
			mv.customer,
			mv.customer_address as premise_address,
			COUNT(DISTINCT mv.name) as total_visits,
			COUNT(DISTINCT CASE WHEN ptd.activity_level = 'High' THEN mv.name END) as high_activity_visits,
			COUNT(DISTINCT CASE WHEN ptd.activity_level = 'Medium' THEN mv.name END) as medium_activity_visits,
			COUNT(DISTINCT CASE WHEN ptd.activity_level = 'Low' THEN mv.name END) as low_activity_visits,
			MAX(ptd.activity_level) as highest_activity_level,
			SUM(COALESCE(ptd.pest_count, 0)) as total_pest_count
		FROM 
			`tabMaintenance Visit` mv
			LEFT JOIN `tabPest Trend Detail` ptd ON ptd.parent = mv.name
		WHERE 
			mv.docstatus = 1
			{conditions}
		GROUP BY 
			mv.customer, mv.customer_address
		ORDER BY 
			MAX(CASE WHEN ptd.activity_level = 'High' THEN 3 WHEN ptd.activity_level = 'Medium' THEN 2 ELSE 1 END) DESC,
			SUM(COALESCE(ptd.pest_count, 0)) DESC
	""".format(conditions=conditions)
	
	data = frappe.db.sql(query, filters, as_dict=1)
	return data


def get_conditions(filters):
	"""Build WHERE clause conditions"""
	conditions = ["mv.customer = %(customer)s"]
	
	if filters.get("from_date"):
		conditions.append("mv.mntc_date >= %(from_date)s")
	
	if filters.get("to_date"):
		conditions.append("mv.mntc_date <= %(to_date)s")
	
	return " AND " + " AND ".join(conditions)

