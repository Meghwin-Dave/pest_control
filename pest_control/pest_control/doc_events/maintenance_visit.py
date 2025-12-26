import frappe
from frappe import msgprint


def on_submit(self, method=None):
    stock_setting = frappe.get_single("Stock Settings")

    if not stock_setting.custom_from_warehouse or not stock_setting.custom_to_warehouse:
        frappe.throw("Please set From / To Warehouse in Stock Settings")

    # 1. Create Material Issue for Chemical Consumption
    if self.custom_chemicals_used:
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
            f"Stock Entry <b>{stock_entry.name}</b> created for chemical consumption."
        )

    # 2. Create Material Transfer for Equipment Demobilization (Job/One-Off only)
    # Get Sale Type from linked Sales Order
    sale_type = None
    if self.purposes:
        for purpose in self.purposes:
            if purpose.prevdoc_doctype == "Sales Order" and purpose.prevdoc_docname:
                sales_order = frappe.get_doc("Sales Order", purpose.prevdoc_docname)
                sale_type = sales_order.get("custom_sale_type")
                break

    if sale_type in ["Job", "One-Off"] and self.custom_equipment_action:
        demobilize_items = []
        for row in self.custom_equipment_action:
            if row.action in ["Demobilize", "Remove"] and row.item and row.quantity:
                demobilize_items.append({
                    "item": row.item,
                    "qty": row.quantity
                })

        if demobilize_items:
            # Get Main Store warehouse (assuming it's the default warehouse or from settings)
            main_store = frappe.db.get_value("Warehouse", {"is_group": 0}, "name")
            if not main_store:
                frappe.throw("Please set up Main Store warehouse")

            stock_entry_transfer = frappe.new_doc("Stock Entry")
            stock_entry_transfer.stock_entry_type = "Material Transfer"
            stock_entry_transfer.company = self.company

            for item_data in demobilize_items:
                stock_item = stock_entry_transfer.append("items", {})
                stock_item.s_warehouse = stock_setting.custom_from_warehouse  # Technician's Van
                stock_item.t_warehouse = main_store  # Main Store
                stock_item.item_code = item_data["item"]
                stock_item.qty = item_data["qty"]

            stock_entry_transfer.custom_maintenance_visit = self.name
            stock_entry_transfer.insert(ignore_permissions=True)
            frappe.msgprint(
                f"Stock Entry <b>{stock_entry_transfer.name}</b> created for equipment demobilization."
            )


def onload(self, method=None):
    """Carry forward open specific recommendations from previous visits"""
    if self.is_new():
        # Get previous maintenance visits for the same customer
        previous_visits = frappe.get_all(
            "Maintenance Visit",
            filters={
                "customer": self.customer,
                "docstatus": 1,
                "name": ["!=", self.name]
            },
            fields=["name"],
            order_by="mntc_date desc, creation desc",
            limit=1
        )

        if previous_visits:
            prev_visit = frappe.get_doc("Maintenance Visit", previous_visits[0].name)
            if prev_visit.custom_specific_recommendations:
                # Copy only open recommendations
                for rec in prev_visit.custom_specific_recommendations:
                    if rec.status == "Open":
                        new_rec = self.append("custom_specific_recommendations", {})
                        new_rec.recommendation = rec.recommendation
                        new_rec.category = rec.category
                        new_rec.priority = rec.priority
                        new_rec.status = "Open"
                        new_rec.first_noted_on = rec.first_noted_on
                        new_rec.remarks = rec.remarks
