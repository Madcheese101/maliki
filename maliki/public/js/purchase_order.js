frappe.ui.form.on('Purchase Order', {
	async refresh(frm) {

		settings = await frappe.db.get_doc('Maliki Settings', null);

        if(!frm.doc.__islocal){
            return;
        }
        if(!frm.doc.set_warehouse){
            frm.set_value('set_warehouse', settings["ly_warehouse"]);
        }
        if(!frm.doc.schedule_date){
            let dateString = frm.doc.transaction_date;
            frm.set_value('schedule_date', frappe.datetime.add_days(dateString, 3));
        }
        
	}
})