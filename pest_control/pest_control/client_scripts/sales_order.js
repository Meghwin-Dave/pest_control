// Copyright (c) 2025, Meghwin Dave and contributors
// For license information, please see license.txt

frappe.ui.form.on("Sales Order", {
	refresh: function(frm) {
		// Ensure field visibility is updated on refresh
		toggle_conditional_fields(frm);
	},
	
	custom_sale_type: function(frm) {
		// Update field visibility when Sale Type changes
		toggle_conditional_fields(frm);
	}
});

function toggle_conditional_fields(frm) {
	// Show/hide Emergency Call Outs based on Sale Type
	if (frm.doc.custom_sale_type === "Contract") {
		frm.set_df_property("custom_emergency_call_outs", "hidden", 0);
	} else {
		frm.set_df_property("custom_emergency_call_outs", "hidden", 1);
	}
	
	// Show/hide Call Back Visits based on Sale Type
	if (frm.doc.custom_sale_type === "Job" || frm.doc.custom_sale_type === "One-Off") {
		frm.set_df_property("custom_call_back_visits", "hidden", 0);
	} else {
		frm.set_df_property("custom_call_back_visits", "hidden", 1);
	}
}

