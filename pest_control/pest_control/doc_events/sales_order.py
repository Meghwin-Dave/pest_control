import frappe
from datetime import timedelta

def on_submit(self, method):
    if self.custom_sale_type == "Contract":
        stock_setting = frappe.get_doc("Stock Settings")
        
        # Calculate number of visits based on Service Frequency
        frequency_days = {
            "Weekly": 7,
            "Monthly": 30,
            "Quarterly": 91,
            "Annually": 365,
            "One-Time": None
        }
        
        # -------------------------------
        # Create Maintenance Schedule
        # -------------------------------
        maintenance_schedule = frappe.new_doc("Maintenance Schedule")
        maintenance_schedule.customer = self.customer
        maintenance_schedule.customer_address = self.customer_address
        maintenance_schedule.contact_person = self.contact_person

        for item in self.items:
            schedule_item = maintenance_schedule.append("items")
            schedule_item.item_code = item.item_code
            schedule_item.item_name = item.item_name
            schedule_item.start_date = self.custom_contract_start_date
            schedule_item.end_date = self.custom_contract_end_date
            
            # Calculate number of visits based on Service Frequency
            if self.custom_service_frequency and self.custom_service_frequency != "One-Time":
                days = frequency_days.get(self.custom_service_frequency, 30)
                if days:
                    total_days = (self.custom_contract_end_date - self.custom_contract_start_date).days
                    no_of_visits = max(1, (total_days // days) + 1)  # +1 to include start date
                    schedule_item.no_of_visits = no_of_visits
                else:
                    schedule_item.no_of_visits = 1
            else:
                schedule_item.no_of_visits = 1
            
            schedule_item.sales_order = self.name

            # Generate schedule dates based on frequency
            if self.custom_service_frequency and self.custom_service_frequency != "One-Time":
                days = frequency_days.get(self.custom_service_frequency, 30)
                if days:
                    current_date = self.custom_contract_start_date
                    while current_date <= self.custom_contract_end_date:
                        schedule_date = maintenance_schedule.append("schedules")
                        schedule_date.item_code = item.item_code
                        schedule_date.item_name = item.item_name
                        schedule_date.scheduled_date = current_date
                        current_date = current_date + timedelta(days=days)
                else:
                    # One-Time or fallback
                    schedule_date = maintenance_schedule.append("schedules")
                    schedule_date.item_code = item.item_code
                    schedule_date.item_name = item.item_name
                    schedule_date.scheduled_date = self.delivery_date or self.custom_contract_start_date
            else:
                # One-Time or no frequency specified
                schedule_date = maintenance_schedule.append("schedules")
                schedule_date.item_code = item.item_code
                schedule_date.item_name = item.item_name
                schedule_date.scheduled_date = self.delivery_date or self.custom_contract_start_date

        maintenance_schedule.insert(ignore_mandatory=True)

        # -------------------------------
        # Create Maintenance Visit
        # -------------------------------
        maintenance_visit = frappe.new_doc("Maintenance Visit")
        maintenance_visit.maintenance_schedule = maintenance_schedule.name
        maintenance_visit.customer = self.customer
        maintenance_visit.customer_address = self.customer_address
        maintenance_visit.contact_person = self.contact_person

        for item in self.items:
            visit_item = maintenance_visit.append("purposes")
            visit_item.item_code = item.item_code
            visit_item.item_name = item.item_name
            visit_item.prevdoc_doctype = "Sales Order"
            visit_item.prevdoc_docname = self.name
            if stock_setting.custom_chemical_item_group == item.item_group:
                chemical_item = maintenance_visit.append("custom_chemicals_used")
                chemical_item.item = item.item_code
                chemical_item.quantity = item.qty
            if stock_setting.custom_equipment_item_group == item.item_group:
                equipment_item = maintenance_visit.append("custom_equipment_action")
                equipment_item.item = item.item_code
                equipment_item.quantity = item.qty

        maintenance_visit.insert(ignore_mandatory=True)

        
        

        # -------------------------------
        # Success Message
        # -------------------------------
        frappe.msgprint(
            msg=f"""
            <b>Maintenance records created successfully</b><br><br>
            • Maintenance Schedule: 
            <a href="/app/maintenance-schedule/{maintenance_schedule.name}">
                {maintenance_schedule.name}
            </a><br>
            • Maintenance Visit: 
            <a href="/app/maintenance-visit/{maintenance_visit.name}">
                {maintenance_visit.name}
            </a>
            """,
            title="Success",
            indicator="green"
        )
