let settings;
let parent_per_transferred_value;

frappe.ui.form.on('Stock Entry', {
    before_save(frm) {
        if(frm.doc.outgoing_stock_entry){
            if(frm.doc.to_warehouse === settings['damaged_warehouse']){
                frm.set_value('stock_title', 'الى مخزن الأضرار')
            }
            else{
                frm.set_value('stock_title', 'استلام في تركيا')
            }
        }
        else{
            frm.set_value('stock_title', 'الى النقل')
        }
    },
    async before_submit(frm) {
        if(!frm.doc.outgoing_stock_entry && frm.doc.add_to_transit){
            frm.set_value('transfer_status', "انتظار");
            return;
        }
        if(frm.doc.outgoing_stock_entry && (parent_per_transferred_value > 0 && parent_per_transferred_value < 100)){
            const status = await prompt_user();
            frm.set_value('issue_type', status);
            frm.set_value('transfer_status', 'استلام جزئي');
        }
    },
    async on_submit(frm) {
        if(frm.doc.outgoing_stock_entry){
            const parent_per_transferred = await frappe.db.get_value('Stock Entry', frm.doc.outgoing_stock_entry, 'per_transferred');
            const parent_per_transferred_value = parent_per_transferred.message.per_transferred;

            if(parent_per_transferred_value > 0 && parent_per_transferred_value < 100){
                parent_doc = await frappe.db.get_doc('Stock Entry', frm.doc.outgoing_stock_entry);
                frappe.confirm('يوجد أصناف غير مستلمة, هل تريد تحويلها لمخزن الأضرار؟',
                    () => {
                        // action to perform if Yes is selected
                        const parentfrm = frm;
                        parentfrm.doc = parent_doc;
                        parentfrm.docname = parent_doc.name;

                        frappe.model.open_mapped_doc({
                            method: "maliki.maliki.overrides.stock_entry.make_dmg_stock_in_entry",
                            frm: parentfrm,
                        });
                    }, () => {
                        // action to perform if No is selected
                    })
            }
        }
        if(['ضرر', 'ضياع'].includes(frm.doc.issue_type)){
            frm.call('set_custom_status')
        }
    },

    onload(frm) {
        if(!frm.doc.outgoing_stock_entry && frm.doc.__islocal && !frm.doc.stock_entry_type){
            frm.set_value('stock_entry_type', "Material Transfer");
        }
    },
    add_to_transit(frm) {
        if(frm.is_new() && settings){
            if(frm.doc.add_to_transit && !frm.doc.outgoing_stock_entry){
                frm.set_value('to_warehouse', settings["transit_warehouse"]);
            }else{
                frm.set_value('to_warehouse', settings["tr_warehouse"]);
            }
        }
    },
	async refresh(frm) {
        if(!frm.doc.additional_costs_je && frm.doc.docstatus === 1){
            frm.add_custom_button(__("تسجيل مصاريف الشحن"), function () {
                frm.call('register_additional_costs_je').then(() => {
                    frm.refresh();
                })
            });
        }

		settings = await frappe.db.get_doc('Maliki Settings', null);
        
        const per_transferred = frm.doc.per_transferred;
        const parent_per_transferred = await frappe.db.get_value('Stock Entry', frm.doc.outgoing_stock_entry, 'per_transferred');
        parent_per_transferred_value = parent_per_transferred.message.per_transferred;

        if(per_transferred > 0 && per_transferred < 100 && !frm.doc.__islocal){
            frm.add_custom_button(__("ارسال لمخزن الأضرار"), function () {
                
                frappe.model.open_mapped_doc({
                    method: "maliki.maliki.overrides.stock_entry.make_dmg_stock_in_entry",
                    frm: frm,
                });
            });
        }

        if(!frm.doc.__islocal){
            return;
        }
        
        if(parent_per_transferred_value > 0){
            return;
        }
        
        if(!frm.doc.outgoing_stock_entry){
            frm.set_value('add_to_transit', 1);
            frm.set_value('from_warehouse', settings["ly_warehouse"]);
        }else{
            frm.set_value('from_warehouse', settings["transit_warehouse"]);
            frm.set_value('to_warehouse', settings["tr_warehouse"]);
            if(frm.doc.additional_costs.length === 0){
                let new_row = frm.add_child('additional_costs');
                frappe.model.set_value(new_row.doctype, new_row.name, "expense_account", settings["shipping_account"]);
                frappe.model.set_value(new_row.doctype, new_row.name, "description", 'تكلفة النقل');
                frappe.model.set_value(new_row.doctype, new_row.name, "amount", 0);
                frm.refresh_field('additional_costs');
            }
            
        }
	}
})

function prompt_user() {
    return new Promise((resolve) => {
        frappe.prompt(
            [
                {
                    label: 'الحالة',
                    fieldname: 'custom_status',
                    fieldtype: 'Select',
                    options: ['ضرر', 'ضياع']
                }
            ],
            function(values) {
                resolve(values.custom_status);
            },
            'الرجاء ادخال نوع الاستلام',
            "حفظ"
        );
    });
}