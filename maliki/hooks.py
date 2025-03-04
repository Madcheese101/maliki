app_name = "maliki"
app_title = "Maliki"
app_publisher = "MaxIT"
app_description = "Malik\'s business"
app_email = "info@MaxITly.com"
app_license = "bsl-1.0"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "maliki",
# 		"logo": "/assets/maliki/logo.png",
# 		"title": "Maliki",
# 		"route": "/maliki",
# 		"has_permission": "maliki.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/maliki/css/maliki.css"
# app_include_js = "/assets/maliki/js/maliki.js"

# include js, css files in header of web template
# web_include_css = "/assets/maliki/css/maliki.css"
# web_include_js = "/assets/maliki/js/maliki.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "maliki/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_js = {"Stock Entry" : "public/js/stock_entry.js",
              "Sales Invoice" : "public/js/sales_invoice.js",
              "Purchase Order" : "public/js/purchase_order.js",
            }
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "maliki/public/icons.svg"

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
# 	"methods": "maliki.utils.jinja_methods",
# 	"filters": "maliki.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "maliki.install.before_install"
# after_install = "maliki.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "maliki.uninstall.before_uninstall"
# after_uninstall = "maliki.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "maliki.utils.before_app_install"
# after_app_install = "maliki.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "maliki.utils.before_app_uninstall"
# after_app_uninstall = "maliki.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "maliki.notifications.get_notification_config"

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

override_doctype_class = {
	"Stock Entry": "maliki.maliki.overrides.stock_entry.CustomStockEntry",
	"Sales Invoice": "maliki.maliki.overrides.sales_invoice.CustomSalesInvoice"
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"maliki.tasks.all"
# 	],
# 	"daily": [
# 		"maliki.tasks.daily"
# 	],
# 	"hourly": [
# 		"maliki.tasks.hourly"
# 	],
# 	"weekly": [
# 		"maliki.tasks.weekly"
# 	],
# 	"monthly": [
# 		"maliki.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "maliki.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "maliki.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "maliki.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["maliki.utils.before_request"]
# after_request = ["maliki.utils.after_request"]

# Job Events
# ----------
# before_job = ["maliki.utils.before_job"]
# after_job = ["maliki.utils.after_job"]

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
# 	"maliki.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            
            [
                "name",
                "in",
                (
                    "Stock Entry-custom_additional_costs_je",
					"Sales Invoice-custom_handling_fee_je",
					"Sales Invoice-custom_total_handling_fees",
					"Sales Invoice Item-custom_handling_fee_rate",
					"Stock Entry-custom_issue_type",
					"Stock Entry-custom_issues_qty",
					"Stock Entry-custom_transfer_status",
					"Stock Entry-custom_mobile",
					"Stock Entry-custom_column_break_wa4ew",
					"Stock Entry-custom_flight_date",
					"Stock Entry-custom_passenger",
					"Stock Entry-custom_معلومات_الرحلة",
                ),
            ]
        ]
    },
    {
        "doctype": "Property Setter",
        "filters": [
            
            [
                "name",
                "in",
                (
                    "Sales Invoice-accounting_dimensions_section-hidden",
					"Sales Invoice-is_pos-default",
					"Sales Invoice-section_break_104-hidden",
					"Sales Invoice-time_sheet_list-hidden",
					"Sales Invoice-packing_list-hidden",
					"Sales Invoice-pricing_rule_details-hidden",
					"Sales Invoice-sec_tax_breakup-hidden",
					"Sales Invoice-section_break_43-hidden",
					"Sales Invoice-section_break_40-hidden",
					"Sales Invoice-taxes_section-hidden",
					"Sales Invoice-more_info_tab-hidden",
					"Sales Invoice-terms_tab-hidden",
					"Sales Invoice-loyalty_points_redemption-hidden",
					"Sales Invoice-advances_section-hidden",
					"Sales Invoice-payments_section-collapsible_depends_on",
					"Sales Invoice-payments_section-collapsible",
					"Sales Invoice-contact_and_address_tab-hidden",
					"Stock Entry-main-title_field",
					"Stock Entry-bom_info_section-hidden",
					"Stock Entry-section_break_7qsm-hidden",
					"Stock Entry-source_warehouse_address-hidden",
					"Stock Entry-source_address_display-hidden",
					"Stock Entry-target_warehouse_address-hidden",
					"Stock Entry-target_address_display-hidden",
					"Stock Entry-section_break_19-hidden",
					"Stock Entry-supplier_info_tab-hidden",
					"Stock Entry-accounting_dimensions_section-hidden",
					"Stock Entry-other_info_tab-hidden",
					"Stock Entry-tab_connections-hidden",
					"Stock Entry-per_transferred-in_list_view",
					"Stock Entry-from_warehouse-in_list_view",
					"Stock Entry-purpose-in_list_view",
					"Stock Entry-stock_entry_type-in_list_view",
					"Stock Entry-to_warehouse-in_list_view",
					"Stock Entry-is_return-in_list_view"
                ),
            ]
        ]
    }
]
