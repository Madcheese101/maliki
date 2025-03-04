import frappe
from frappe.model.mapper import get_mapped_doc
from erpnext.accounts.doctype.sales_invoice.sales_invoice import (SalesInvoice)
from frappe.utils import flt


class CustomSalesInvoice(SalesInvoice):

    def on_submit(self):
        self.register_handling_fee()
        super().on_submit()

    def on_cancel(self):
        super().on_cancel()
        if self.handling_fee_je:
            doc = frappe.get_doc("Journal Entry", self.handling_fee_je)
            doc.cancel()

    @frappe.whitelist()
    def register_handling_fee(self):
        amount = sum([d.handling_fee_rate * d.qty for d in self.items])
        
        if amount > 0:
            settings_doc = frappe.get_doc("Maliki Settings")
            handling_fee_account = settings_doc.handling_fee_account
            tr_account = settings_doc.tr_account

            if not handling_fee_account:
                frappe.throw("Handling Fee Account must be set in Maliki Settings")
            if not tr_account:
                frappe.throw("Turkey Account must be set in Maliki Settings")
            
            doc = frappe.new_doc('Journal Entry')
            title = f"عمولة {self.name}"

            doc.voucher_type = "Journal Entry"
            # doc.user_remark = self.notes
            doc.posting_date = self.posting_date

            # money to account
            to_ = {"account":handling_fee_account,
                    "cost_center": self.cost_center,
                    "debit_in_account_currency": amount}
            # money from account
            from_ = {"account":tr_account,
                    "cost_center": self.cost_center,
                    "credit_in_account_currency": amount}
            
            doc.append("accounts",to_)
            doc.append("accounts",from_)

            doc.save(ignore_permissions=True)
            doc.submit()

            self.db_set('handling_fee_je', doc.name)
            frappe.msgprint(f"Journal Entry {doc.name} created")
        else:
            frappe.msgprint("No handling fee to register")