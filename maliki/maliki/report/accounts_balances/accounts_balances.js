// Copyright (c) 2025, MaxIT and contributors
// For license information, please see license.txt

frappe.query_reports["Accounts Balances"] = {
	"filters": [
		{
			fieldname:"report_date",
			label: __("Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			reqd: 1
		}
	],
	"tree":true,
	"name_field":"account",
	"parent_field":"account",
	"initial_depth":3
};
