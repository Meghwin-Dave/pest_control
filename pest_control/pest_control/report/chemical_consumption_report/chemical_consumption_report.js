// Copyright (c) 2025, Meghwin Dave and contributors
// For license information, please see license.txt

frappe.query_reports["Chemical Consumption Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.month_start(),
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.month_end(),
			"reqd": 1
		},
		{
			"fieldname": "item_code",
			"label": __("Chemical Item"),
			"fieldtype": "Link",
			"options": "Item",
			"reqd": 0,
			"get_query": function() {
				return {
					"filters": {
						"is_stock_item": 1,
						"item_group": frappe.boot.sysdefaults.custom_chemical_item_group || ""
					}
				};
			}
		}
	],
	
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		
		// Highlight high consumption
		if (column.fieldname === "total_quantity_consumed" && parseFloat(value) > 100) {
			value = `<span style="color: red; font-weight: bold;">${value}</span>`;
		}
		
		return value;
	},
	
	"onload": function(report) {
		// Set default date range to current month if not provided
		if (!report.get_filter_value("from_date") && !report.get_filter_value("to_date")) {
			report.set_filter_value("from_date", frappe.datetime.month_start());
			report.set_filter_value("to_date", frappe.datetime.month_end());
		}
	}
};

