# Copyright (c) 2025, Meghwin Dave and contributors
# For license information, please see license.txt

import frappe


def execute():
	"""
	Update reports from Query Report to Script Report type
	and remove old query fields
	"""
	reports_to_update = [
		"Pest Trend Analysis",
		"Group Contract Summary",
		"Chemical Consumption Report",
		"Technical Inspection Audit Report"
	]
	
	for report_name in reports_to_update:
		if frappe.db.exists("Report", report_name):
			try:
				# Update directly using SQL to avoid link validation issues
				frappe.db.sql("""
					UPDATE `tabReport`
					SET report_type = 'Script Report', query = NULL
					WHERE name = %s
				""", (report_name,))
				frappe.db.commit()
				print(f"Updated {report_name} to Script Report")
			except Exception as e:
				print(f"Error updating {report_name}: {str(e)}")
				# Try using set_value as fallback
				try:
					frappe.db.set_value(
						"Report",
						report_name,
						{
							"report_type": "Script Report",
							"query": None
						},
						update_modified=False,
						validate_links=False
					)
					frappe.db.commit()
					print(f"Updated {report_name} using set_value")
				except Exception as e2:
					print(f"Failed to update {report_name}: {str(e2)}")
		else:
			print(f"Report {report_name} not found, skipping...")

