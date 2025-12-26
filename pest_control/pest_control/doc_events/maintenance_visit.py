import frappe
from frappe import msgprint


def on_submit(self, method=None):

    # If no chemicals used → inform user and exit
    if not self.custom_chemicals_used:
        frappe.msgprint(
            "No chemicals were added. Stock Entry was not created."
        )
        return

    stock_setting = frappe.get_single("Stock Settings")

    if not stock_setting.custom_from_warehouse or not stock_setting.custom_to_warehouse:
        frappe.throw("Please set From / To Warehouse in Stock Settings")

    stock_entry = frappe.new_doc("Stock Entry")
    stock_entry.stock_entry_type = "Material Issue"
    stock_entry.company = self.company

    for row in self.custom_chemicals_used:
        if not row.item or not row.quantity:
            continue

        stock_item = stock_entry.append("items", {})
        stock_item.s_warehouse = stock_setting.custom_from_warehouse
        stock_item.t_warehouse = stock_setting.custom_to_warehouse
        stock_item.item_code = row.item
        stock_item.qty = row.quantity
    stock_entry.custom_maintenance_visit = self.name
    stock_entry.insert(ignore_permissions=True)


    frappe.msgprint(
        f"Stock Entry <b>{stock_entry.name}</b> created successfully."
    )
