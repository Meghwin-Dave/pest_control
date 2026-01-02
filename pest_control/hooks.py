app_name = "pest_control"
app_title = "Pest Control"
app_publisher = "Meghwin Dave"
app_description = "Pest Control"
app_email = "meghwindave04@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "pest_control",
# 		"logo": "/assets/pest_control/logo.png",
# 		"title": "Pest Control",
# 		"route": "/pest_control",
# 		"has_permission": "pest_control.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/pest_control/css/pest_control.css"
# app_include_js = "/assets/pest_control/js/pest_control.js"

# include js, css files in header of web template
# web_include_css = "/assets/pest_control/css/pest_control.css"
# web_include_js = "/assets/pest_control/js/pest_control.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "pest_control/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Sales Order": "pest_control/public/js/pest_control/sales_order.js",
	"Customer": "pest_control/public/js/pest_control/customer.js"
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_tree.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "pest_control/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "pest_control.utils.jinja_methods",
# 	"filters": "pest_control.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "pest_control.install.before_install"
# after_install = "pest_control.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "pest_control.uninstall.before_uninstall"
# after_uninstall = "pest_control.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "pest_control.utils.before_app_install"
# after_app_install = "pest_control.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "pest_control.utils.before_app_uninstall"
# after_app_uninstall = "pest_control.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "pest_control.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Sales Order": {
		"on_submit": "pest_control.pest_control.doc_events.sales_order.on_submit",
	},
	"Maintenance Visit": {
		"on_submit": "pest_control.pest_control.doc_events.maintenance_visit.on_submit",
		"onload": "pest_control.pest_control.doc_events.maintenance_visit.onload",
	},
	"Item": {
		"validate": "pest_control.pest_control.doc_events.item.validate",
	}
}

fixtures = [
    {
    "doctype": "Custom Field",
        "filters": {
            "module": [ "in", ["Pest Control"] ]
            }
        },
    {
        "doctype": "Role",
        "filters": {
            "name": ["in", ["Technician", "Technical Inspector", "Operations Manager", "Technical Manager"]]
        }
    },
    ]

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"pest_control.tasks.all"
# 	],
# 	"daily": [
# 		"pest_control.tasks.daily"
# 	],
# 	"hourly": [
# 		"pest_control.tasks.hourly"
# 	],
# 	"weekly": [
# 		"pest_control.tasks.weekly"
# 	],
# 	"monthly": [
# 		"pest_control.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "pest_control.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "pest_control.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "pest_control.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["pest_control.utils.before_request"]
# after_request = ["pest_control.utils.after_request"]

# Job Events
# ----------
# before_job = ["pest_control.utils.before_job"]
# after_job = ["pest_control.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"pest_control.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

