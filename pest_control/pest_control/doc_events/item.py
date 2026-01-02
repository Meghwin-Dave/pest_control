# Copyright (c) 2025, Meghwin Dave and contributors
# For license information, please see license.txt

import frappe

def validate(self, method=None):
    """Validate Item configuration based on Item Group"""
    stock_setting = frappe.get_single("Stock Settings")
    
    # Get item groups from Stock Settings
    service_item_group = stock_setting.get("custom_service_item_group")
    chemical_item_group = stock_setting.get("custom_chemical_item_group")
    equipment_item_group = stock_setting.get("custom_equipment_item_group")
    
    # Validate Maintain Stock setting based on Item Group
    if self.item_group == service_item_group:
        # Service items should NOT maintain stock
        if self.is_stock_item:
            frappe.throw(
                f"Service items (Item Group: {self.item_group}) should have 'Maintain Stock' unchecked. "
                "Please uncheck 'Is Stock Item' for this item."
            )
    
    elif self.item_group in [chemical_item_group, equipment_item_group]:
        # Chemicals and Equipment MUST maintain stock
        if not self.is_stock_item:
            frappe.throw(
                f"Chemical/Equipment items (Item Group: {self.item_group}) must have 'Maintain Stock' checked. "
                "Please check 'Is Stock Item' for this item."
            )

