import frappe
from frappe.model.mapper import get_mapped_doc
from erpnext.stock.doctype.stock_entry.stock_entry import (StockEntry)
from frappe.utils import flt

class CustomStockEntry(StockEntry):
    def on_submit(self):
        self.register_additional_costs_je()
        super().on_submit()
    
    def on_cancel(self):
        super().on_cancel()
        if self.additional_costs_je:
            doc = frappe.get_doc("Journal Entry", self.additional_costs_je)
            doc.cancel()

    def before_submit(self):
        tr_warehouse = frappe.db.get_single_value("Maliki Settings", "tr_warehouse")

        if self.to_warehouse == tr_warehouse and self.total_additional_costs == 0:
            frappe.throw('يجب تحديد تكلفة النقل')

    @frappe.whitelist()
    def set_custom_status(self):
        total_qty = sum([d.qty for d in self.items])
        parent_doc = frappe.get_doc("Stock Entry", self.outgoing_stock_entry)
        issues_qty = total_qty + parent_doc.issues_qty

        parent_doc.db_set('issues_qty', issues_qty, commit=True)
        parent_doc.db_set('transfer_status', self.transfer_status, commit=True)

        parent_doc.add_comment('Comment', f'تم نحويل عدد {total_qty} من المنتجات لمخزن الأضرار بسبب {self.issue_type}')
        frappe.db.commit()
    
    @frappe.whitelist()
    def register_additional_costs_je(self):
        if self.total_additional_costs > 0:
            settings_doc = frappe.get_doc("Maliki Settings")
            shipping_account = settings_doc.shipping_account
            tr_account = settings_doc.tr_account

            if not shipping_account:
                frappe.throw("Shipping Costs Account must be set in Maliki Settings")
            if not tr_account:
                frappe.throw("Turkey Account must be set in Maliki Settings")
            
            doc = frappe.new_doc('Journal Entry')
            doc.title = f"مصاريف شحن {self.name}"

            doc.voucher_type = "Journal Entry"
            # doc.user_remark = self.notes
            doc.posting_date = self.posting_date

            # money to account
            to_ = {"account":shipping_account,
                    # "cost_center": self.cost_center,
                    "debit_in_account_currency": self.total_additional_costs}
            # money from account
            from_ = {"account":tr_account,
                    # "cost_center": self.cost_center,
                    "credit_in_account_currency": self.total_additional_costs}
            
            doc.append("accounts",to_)
            doc.append("accounts",from_)

            doc.save(ignore_permissions=True)
            doc.submit()

            self.db_set('additional_costs_je', doc.name)
            frappe.msgprint(f"Journal Entry {doc.name} created")
        else:
            frappe.msgprint("لا يوجد تكلفة شحن")


@frappe.whitelist()
def make_dmg_stock_in_entry(source_name, target_doc=None):
    to_warehouse = frappe.db.get_single_value("Maliki Settings", "damaged_warehouse")
    def set_missing_values(source, target):
        target.stock_entry_type = "Material Transfer"
        target.set_missing_values()

        if not frappe.db.get_single_value("Stock Settings", "use_serial_batch_fields"):
            target.make_serial_and_batch_bundle_for_transfer()

    def update_item(source_doc, target_doc, source_parent):
        target_doc.t_warehouse = to_warehouse

        if source_doc.material_request_item and source_doc.material_request:
            add_to_transit = frappe.db.get_value("Stock Entry", source_name, "add_to_transit")
            if add_to_transit:
                warehouse = frappe.get_value(
                    "Material Request Item", source_doc.material_request_item, "warehouse"
                )
                target_doc.t_warehouse = warehouse

        target_doc.s_warehouse = source_doc.t_warehouse
        target_doc.qty = source_doc.qty - source_doc.transferred_qty

    doclist = get_mapped_doc(
        "Stock Entry",
        source_name,
        {
            "Stock Entry": {
                "doctype": "Stock Entry",
                "field_map": {"name": "outgoing_stock_entry", 
                  "to_warehouse": "from_warehouse",
                },
                "validation": {"docstatus": ["=", 1]},
            },
            "Stock Entry Detail": {
                "doctype": "Stock Entry Detail",
                "field_map": {
                    "name": "ste_detail",
                    "parent": "against_stock_entry",
                    "serial_no": "serial_no",
                    "batch_no": "batch_no",
                },
                "postprocess": update_item,
                "condition": lambda doc: flt(doc.qty) - flt(doc.transferred_qty) > 0.00001,
            },
        },
        target_doc,
        set_missing_values,
    )
    doclist.to_warehouse = to_warehouse
    
    return doclist