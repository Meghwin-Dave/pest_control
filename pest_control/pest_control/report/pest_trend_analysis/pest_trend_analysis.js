// Copyright (c) 2025, Meghwin Dave and contributors
// For license information, please see license.txt

frappe.query_reports["Pest Trend Analysis"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 0
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 0
		},
		{
			"fieldname": "customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"reqd": 0
		},
		{
			"fieldname": "premise_address",
			"label": __("Premise Address"),
			"fieldtype": "Link",
			"options": "Address",
			"reqd": 0,
			"get_query": function() {
				return {
					"filters": {
						"link_doctype": "Customer",
						"link_name": frappe.query_report.get_filter_value("customer")
					}
				};
			}
		}
	],
	
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		
		// Highlight high activity level
		if (column.fieldname === "max_activity_level") {
			if (value === "High") {
				value = `<span style="color: red; font-weight: bold;">${value}</span>`;
			} else if (value === "Medium") {
				value = `<span style="color: orange; font-weight: bold;">${value}</span>`;
			}
		}
		
		return value;
	},
	
	"onload": function(report) {
		// Set default date range if not provided
		if (!report.get_filter_value("from_date") && !report.get_filter_value("to_date")) {
			report.set_filter_value("from_date", frappe.datetime.add_months(frappe.datetime.get_today(), -1));
			report.set_filter_value("to_date", frappe.datetime.get_today());
		}
	}
};

