// Copyright (c) 2025, Meghwin Dave and contributors
// For license information, please see license.txt

frappe.query_reports["Group Contract Summary"] = {
	"filters": [
		{
			"fieldname": "customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"reqd": 1
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -3),
			"reqd": 0
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 0
		}
	],
	
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		
		// Highlight high activity levels
		if (column.fieldname === "highest_activity_level") {
			if (value === "High") {
				value = `<span style="color: red; font-weight: bold;">${value}</span>`;
			} else if (value === "Medium") {
				value = `<span style="color: orange; font-weight: bold;">${value}</span>`;
			}
		}
		
		// Highlight high activity visit counts
		if (column.fieldname === "high_activity_visits" && parseInt(value) > 0) {
			value = `<span style="color: red; font-weight: bold;">${value}</span>`;
		}
		
		return value;
	},
	
	"onload": function(report) {
		// Set default date range if not provided
		if (!report.get_filter_value("from_date") && !report.get_filter_value("to_date")) {
			report.set_filter_value("from_date", frappe.datetime.add_months(frappe.datetime.get_today(), -3));
			report.set_filter_value("to_date", frappe.datetime.get_today());
		}
	}
};

