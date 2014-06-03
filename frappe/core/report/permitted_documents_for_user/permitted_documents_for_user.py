# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, throw
import frappe.utils.user
from frappe.permissions import check_admin_or_system_manager

def execute(filters=None):
	user, doctype = filters.get("user"), filters.get("doctype")
	validate(user, doctype)

	columns, fields = get_columns_and_fields(doctype)
	data = frappe.get_list(doctype, fields=fields, as_list=True, user=user)

	return columns, data

def validate(user, doctype):
	# check if current user is System Manager
	check_admin_or_system_manager()

	if not user:
		throw(_("Please specify user"))

	if not doctype:
		throw(_("Please specify doctype"))

def get_columns_and_fields(doctype):
	columns = ["Name:Link/{}:200".format(doctype)]
	fields = ["name"]
	for df in frappe.get_meta(doctype).fields:
		if df.in_list_view:
			fields.append(df.fieldname)
			fieldtype = "Link/{}".format(df.options) if df.fieldtype=="Link" else df.fieldtype
			columns.append("{label}:{fieldtype}:{width}".format(label=df.label, fieldtype=fieldtype, width=df.width or 100))

	return columns, fields

def query_doctypes(doctype, txt, searchfield, start, page_len, filters):
	user = filters.get("user")
	user_obj = frappe.utils.user.User(user)
	user_obj.build_permissions()
	can_read = user_obj.can_read

	out = []
	for dt in can_read:
		if txt.lower().replace("%", "") in dt.lower():
			out.append([dt])

	return out
