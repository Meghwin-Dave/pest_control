// Copyright (c) 2025, Meghwin Dave and contributors
// For license information, please see license.txt

frappe.ui.form.on("Customer", {
	refresh: function(frm) {
		// Ensure Trade Name visibility is updated
		if (frm.doc.custom_client_type === "Commercial") {
			frm.set_df_property("custom_trade_name_", "hidden", 0);
		} else {
			frm.set_df_property("custom_trade_name_", "hidden", 1);
		}
	},
	
	custom_client_type: function(frm) {
		// Update Trade Name visibility when Client Type changes
		if (frm.doc.custom_client_type === "Commercial") {
			frm.set_df_property("custom_trade_name_", "hidden", 0);
		} else {
			frm.set_df_property("custom_trade_name_", "hidden", 1);
			frm.set_value("custom_trade_name_", "");
		}
	}
});

