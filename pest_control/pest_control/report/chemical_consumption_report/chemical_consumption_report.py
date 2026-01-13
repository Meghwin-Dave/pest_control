# Copyright (c) 2025, Meghwin Dave and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	"""
	Execute the Chemical Consumption Report
	
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
			"fieldname": "date",
			"label": _("Date"),
			"fieldtype": "Date",
			"width": 120
		},
		{
			"fieldname": "item_code",
			"label": _("Chemical Item"),
			"fieldtype": "Link",
			"options": "Item",
			"width": 200
		},
		{
			"fieldname": "item_name",
			"label": _("Item Name"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "total_quantity_consumed",
			"label": _("Total Quantity Consumed"),
			"fieldtype": "Float",
			"width": 150,
			"precision": 2
		},
		{
			"fieldname": "uom",
			"label": _("UOM"),
			"fieldtype": "Link",
			"options": "UOM",
			"width": 80
		},
		{
			"fieldname": "number_of_visits",
			"label": _("Number of Visits"),
			"fieldtype": "Int",
			"width": 120
		}
	]


def get_data(filters):
	"""Get report data based on filters"""
	conditions = get_conditions(filters)
	
	query = """
		SELECT 
			DATE(se.posting_date) as date,
			sei.item_code,
			sei.item_name,
			SUM(sei.qty) as total_quantity_consumed,
			sei.uom,
			COUNT(DISTINCT se.custom_maintenance_visit) as number_of_visits
		FROM 
			`tabStock Entry` se
			INNER JOIN `tabStock Entry Detail` sei ON sei.parent = se.name
		WHERE 
			se.docstatus = 1
			AND se.stock_entry_type = 'Material Issue'
			{conditions}
		GROUP BY 
			DATE(se.posting_date), sei.item_code, sei.uom
		ORDER BY 
			DATE(se.posting_date) DESC, sei.item_code
	""".format(conditions=conditions)
	
	data = frappe.db.sql(query, filters, as_dict=1)
	return data


def get_conditions(filters):
	"""Build WHERE clause conditions"""
	conditions = []
	
	if filters.get("from_date"):
		conditions.append("se.posting_date >= %(from_date)s")
	
	if filters.get("to_date"):
		conditions.append("se.posting_date <= %(to_date)s")
	
	if filters.get("item_code"):
		conditions.append("sei.item_code = %(item_code)s")
	
	return " AND " + " AND ".join(conditions) if conditions else ""

