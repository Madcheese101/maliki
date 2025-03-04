frappe.ui.form.on('Sales Invoice', {
	async refresh(frm) {
        if(!frm.doc.handling_fee_je && frm.doc.docstatus === 1){
            frm.add_custom_button(__("تسجيل العمولة"), function () {
                frm.call('register_handling_fee').then(() => {
                    frm.refresh();
                })
            });
        }
        
	}
})

frappe.ui.form.on('Sales Invoice Item', {
    handling_fee_rate:function(frm, cdt, cdn){

        var handling_fee_amount = 0;

        frm.doc.items.forEach((d) => {
            let amount = d.handling_fee_rate * d.qty;
            handling_fee_amount += amount;
        });

        frm.set_value('total_handling_fees', handling_fee_amount);
    },
    items_remove:function(frm){
        var handling_fee_amount = 0;

        frm.doc.items.forEach((d) => {
            var amount = d.handling_fee_rate * d.qty;
            handling_fee_amount += amount;
        });

        frm.set_value('total_handling_fees', handling_fee_amount);
    }
});