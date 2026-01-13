# Copyright (c) 2025, Meghwin Dave and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	"""
	Execute the Technical Inspection Audit Report
	
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
			"fieldname": "visit_id",
			"label": _("Visit ID"),
			"fieldtype": "Link",
			"options": "Maintenance Visit",
			"width": 150
		},
		{
			"fieldname": "visit_date",
			"label": _("Visit Date"),
			"fieldtype": "Date",
			"width": 120
		},
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
			"fieldname": "contact_person",
			"label": _("Contact Person"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "time_in",
			"label": _("Time In"),
			"fieldtype": "Datetime",
			"width": 150
		},
		{
			"fieldname": "time_out",
			"label": _("Time Out"),
			"fieldtype": "Datetime",
			"width": 150
		},
		{
			"fieldname": "general_rec_followed",
			"label": _("General Rec. Followed"),
			"fieldtype": "Check",
			"width": 120
		},
		{
			"fieldname": "pest_trend_entries",
			"label": _("Pest Trend Entries"),
			"fieldtype": "Int",
			"width": 130
		},
		{
			"fieldname": "chemicals_used_count",
			"label": _("Chemicals Used Count"),
			"fieldtype": "Int",
			"width": 150
		},
		{
			"fieldname": "equipment_actions_count",
			"label": _("Equipment Actions Count"),
			"fieldtype": "Int",
			"width": 160
		},
		{
			"fieldname": "recommendations_count",
			"label": _("Recommendations Count"),
			"fieldtype": "Int",
			"width": 150
		},
		{
			"fieldname": "highest_activity_level",
			"label": _("Highest Activity Level"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "completion_status",
			"label": _("Completion Status"),
			"fieldtype": "Data",
			"width": 130
		},
		{
			"fieldname": "maintenance_type",
			"label": _("Maintenance Type"),
			"fieldtype": "Data",
			"width": 130
		}
	]


def get_data(filters):
	"""Get report data based on filters"""
	conditions = get_conditions(filters)
	
	query = """
		SELECT 
			mv.name as visit_id,
			mv.mntc_date as visit_date,
			mv.customer,
			mv.customer_address as premise_address,
			mv.contact_person,
			mv.status,
			mv.custom_time_in as time_in,
			mv.custom_timeout as time_out,
			mv.custom_general_recommendations_followed as general_rec_followed,
			COUNT(DISTINCT ptd.name) as pest_trend_entries,
			COUNT(DISTINCT cu.name) as chemicals_used_count,
			COUNT(DISTINCT ea.name) as equipment_actions_count,
			COUNT(DISTINCT sr.name) as recommendations_count,
			CASE 
				WHEN COUNT(DISTINCT CASE WHEN ptd.activity_level = 'High' THEN ptd.name END) > 0 THEN 'High'
				WHEN COUNT(DISTINCT CASE WHEN ptd.activity_level = 'Medium' THEN ptd.name END) > 0 THEN 'Medium'
				WHEN COUNT(DISTINCT CASE WHEN ptd.activity_level = 'Low' THEN ptd.name END) > 0 THEN 'Low'
				ELSE 'None'
			END as highest_activity_level,
			mv.completion_status,
			mv.maintenance_type
		FROM 
			`tabMaintenance Visit` mv
			LEFT JOIN `tabPest Trend Detail` ptd ON ptd.parent = mv.name
			LEFT JOIN `tabChemicals Used` cu ON cu.parent = mv.name
			LEFT JOIN `tabEquipment Action` ea ON ea.parent = mv.name
			LEFT JOIN `tabSpecific Recommendations` sr ON sr.parent = mv.name
		WHERE 
			mv.docstatus = 1
			{conditions}
		GROUP BY 
			mv.name, mv.mntc_date, mv.customer, mv.customer_address, mv.contact_person, 
			mv.status, mv.custom_time_in, mv.custom_timeout, mv.custom_general_recommendations_followed,
			mv.completion_status, mv.maintenance_type
		ORDER BY 
			mv.mntc_date DESC, mv.customer
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
	
	if filters.get("status"):
		conditions.append("mv.status = %(status)s")
	
	return " AND " + " AND ".join(conditions) if conditions else ""

