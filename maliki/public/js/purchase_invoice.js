let settings;

frappe.ui.form.on('Purchase Invoice', {

	async refresh(frm) {
		settings = await frappe.db.get_doc('Maliki Settings', null);
	},

    is_paid(frm) {
        if(frm.doc.docstatus !== 0 || !frm.is_new() || !settings){
            return;
        }
        if(frm.doc.is_paid){
            frm.set_value('mode_of_payment', settings["mode_of_payment_ly"]);
            frm.refresh_field('mode_of_payment');
        }else{
            frm.set_value('mode_of_payment', null);
            frm.refresh_field('mode_of_payment');
        }
    }
})