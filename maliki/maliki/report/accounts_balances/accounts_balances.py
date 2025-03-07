# Copyright (c) 2025, MaxIT and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from erpnext.accounts.utils import get_balance_on

def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_data(filters):

	data = []

	data.extend(get_cash_accounts(filters))
	data.extend(get_supplier_accounts(filters))
	data.extend(get_customer_accounts(filters))
	data.extend(get_loans_and_advances_accounts(filters))

	return data
def get_loans_and_advances_accounts(filters):
	loans = [{"account": "ديون و سلف خارجية", "indent": 0, "has_value": 1}]
	from_ = [{"account": "دائنين", "indent": 1, "has_value": 1}]
	to_ = [{"account": "مدينين", "indent": 1, "has_value": 1}]
	total_from = 0
	total_to = 0

	parent_account = frappe.db.get_value("Account", {"account_number": 1600}, "name")
	accounts = frappe.db.get_list("Account",
                       filters={
                           'is_group': 0,
                           'parent_account': parent_account
                           },
                       fields=['name', "account_currency"])
	
	for d in accounts:
		balance = get_balance_on(d.name, date=filters.report_date)
		if balance < 0:
			from_.append({"account": d.name, "balance": balance, "currency": d.account_currency, "indent": 2, "has_value": 1})
			total_from += balance
		if balance > 0:
			to_.append({"account": d.name, "balance": balance, "currency": d.account_currency, "indent": 2, "has_value": 1})
			total_to += balance
	loans.extend(from_)
	loans.extend(to_)

	return loans
	
	

def get_cash_accounts(filters):
	cash_accounts = [{"account": "خزائن النقدي", "indent": 0, "has_value": 1}]
	parent_account = frappe.db.get_value("Account", {"account_number": 1100}, "name")
	accounts = frappe.db.get_list("Account",
                       filters={
                           'is_group': 0,
                           'parent_account': parent_account
                           },
                       fields=['name', "account_currency"])
	
	for d in accounts:
		balance = get_balance_on(d.name, date=filters.report_date)
		cash_accounts.append({"account": d.name, "balance": balance, "currency": d.account_currency, "indent": 1, "has_value": 1})

	return cash_accounts

def get_customer_accounts(filters):
	customers = [{"account": "حسابات الزبائن", "indent": 0, "has_value": 1}]
	customer_names = frappe.db.get_list("Customer", fields=["name"])

	for d in customer_names:
		balance = get_balance_on(party_type="Customer", party=d.name, date=filters.report_date)
		if balance != 0:
			customers.append({"account": d.name, "balance": balance, "indent": 1, "has_value": 1})

	return customers

def get_supplier_accounts(filters):
	suppliers = [{"account": "حسابات الموردين", "indent": 0, "has_value": 1}]
	supplier_names = frappe.db.get_list("Supplier", fields=["name"])

	for d in supplier_names:
		balance = get_balance_on(party_type="Supplier", party=d.name, date=filters.report_date)
		if balance != 0:
			suppliers.append({"account": d.name, "balance": balance, "indent": 1, "has_value": 1})

	return suppliers

def get_columns():
	columns = [
		{
			"label": _("Account"),
			"fieldtype": "Link",
			"fieldname": "account",
			"options": "Account",
			"width": 400,
		},
		{
			"label": _("Currency"),
			"fieldtype": "Link",
			"fieldname": "currency",
			"options": "Currency",
			"hidden": 1,
			"width": 50,
		},
		{
			"label": _("Balance"),
			"fieldtype": "Currency",
			"fieldname": "balance",
			"options": "currency",
			"width": 200,
		},
	]

	return columns
