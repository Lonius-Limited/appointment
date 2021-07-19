// Copyright (c) 2021, Lonius Health & MTRH and contributors and contributors
// For license information, please see license.txt

frappe.ui.form.on('OSHA Form', {
	populate_audiometry_values: (frm) => {
		var existing_values = []
		if (frm.doc.audiometry_measure) {
			frm.doc.audiometry_measure.forEach(row => {
				existing_values.push(row.frequency)
			})
		}
		// if (!frm.doc.audiometry_measure) {	
		const frequencies = [ "2000Hz", "3000Hz", "4000Hz"]
		var missing_frequencies = frequencies.filter(value => !existing_values.includes(value))
		missing_frequencies.forEach(value => {
			var rowitem = frm.add_child("audiometry_measure");
			rowitem.frequency = value
			// rowitem.noise_level_db = 0
			// rowitem.description = item_obj.description
		})

		// }
		// }
		refresh_field("audiometry_measure")
	},
	onload_post_render: function (frm) {
		frm.trigger('date_of_birth');
		frm.trigger('date_of_birth');

	},
	date_of_birth: (frm) => {
		if (frm.doc.date_of_birth) {
			console.log("Age", get_age(frm.doc.date_of_birth))
			frm.doc.age = get_age(frm.doc.date_of_birth, false)
			refresh_field("age")
		}

	},
	date_of_employment: (frm) => {
		if (frm.doc.date_of_employment) {
			console.log("Years of Service", get_age(frm.doc.date_of_employment))
			frm.doc.years_of_service = get_age(frm.doc.date_of_employment, true)
			refresh_field("years_of_service")
		}

	},
	//CALCULATIONS
	fev_o: (frm) => {
		let percent = parseFloat(frm.doc.fev_o) / parseFloat(frm.doc.fvc_o)
		frm.doc.fev_fvc_ratio_o = percent
		refresh_field('fev_fvc_ratio_o')
	},
	fev_w: (frm) => {
		let percent = parseFloat(frm.doc.fev_w) / parseFloat(frm.doc.fvc_w)
		frm.doc.fev_fvc_ratio_w = percent
		refresh_field('fev_fvc_ratio_w')
	},
	fev_wc: (frm) => {
		let percent = parseFloat(frm.doc.fev_wc) / parseFloat(frm.doc.fvc_wc)
		frm.doc.fev_fvc_ratio_wc = percent
		refresh_field('fev_fvc_ratio_wc')
	},
	fev_cw: (frm) => {
		let percent = parseFloat(frm.doc.fev_cw) / parseFloat(frm.doc.fvc_cw)
		frm.doc.fev_fvc_ratio_cw = percent
		refresh_field('fev_fvc_ratio_cw')
	},

});
let get_age = function (birth, yearsOnly) {
	let ageMS = Date.parse(Date()) - Date.parse(birth);
	let age = new Date();
	age.setTime(ageMS);
	let years = age.getFullYear() - 1970;
	if (yearsOnly) {
		return years + ' Year(s) '
	}
	return years + ' Year(s) ' + age.getMonth() + ' Month(s) ' + age.getDate() + ' Day(s)';
};