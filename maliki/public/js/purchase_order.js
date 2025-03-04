frappe.ui.form.on('Purchase Order', {
	async refresh(frm) {

		settings = await frappe.db.get_doc('Maliki Settings', null);

        if(!frm.doc.__islocal){
            return;
        }

        frm.set_value('set_warehouse', settings["ly_warehouse"]);
	}
})