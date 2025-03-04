import frappe
from frappe.model.mapper import get_mapped_doc
from erpnext.stock.doctype.stock_entry.stock_entry import (StockEntry)
from frappe.utils import flt

class CustomStockEntry(StockEntry):
    @frappe.whitelist()
    def add_additional_costs(self):
        shipping_account = frappe.db.get_single_value("Maliki Settings", "shipping_account")
        # currency = frappe.db.get_value("Account", shipping_account, "currency")
        # frappe.msgprint(shipping_account)

        self.append("additional_costs", 
                    {
                        'expense_account': shipping_account,
                        'description': 'تكلفة النقل',
                        'amount': 0
                    })

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