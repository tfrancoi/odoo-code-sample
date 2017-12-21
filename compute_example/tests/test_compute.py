# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from odoo import fields
from odoo.tests import common
from odoo.exceptions import ValidationError
import odoo

class TestComputeExampe(common.TransactionCase):
    
    @classmethod
    def setUpClass(cls):
        super(TestComputeExampe, cls).setUpClass()
        odoo.registry(common.get_db_name()).enter_test_mode()

    @classmethod
    def tearDownClass(cls):
        odoo.registry(common.get_db_name()).leave_test_mode()
        super(TestComputeExampe, cls).tearDownClass()
    
    def setUp(self):
        super(TestComputeExampe, self).setUp()
        self.partner = self.ref('compute_example.test_partner')
        self.partner = self.env['res.partner'].browse(self.partner)

    def test_01_compute(self):
        etudiant = self.env['etudiant'].create({'partner_id': self.partner.id})
        self.assertEqual(etudiant.name, self.partner.name, "Name should be the same")
        
    def test_02_inverse(self):
        etudiant = self.env['etudiant'].browse(self.ref('compute_example.test_etudiant'))
        etudiant.name = "Salut"
        self.assertEqual(etudiant.partner_id.name, "Salut")
        
    def test_03_search(self):
        import time
        st = time.time()
        etudiant_old = self.env['etudiant'].search([('majeur', '=', True)])
        self.env['etudiant'].create({'partner_id': self.partner.id, 'age': 20})
        self.env['etudiant'].create({'partner_id': self.partner.id, 'age': 19})
        etudiant = self.env['etudiant'].search([('majeur', '=', True)])
        
        self.assertEqual(len(etudiant), len(etudiant_old) + 2)
        print "Total Time", time.time() - st
    
    def test_04_constrains(self):
        with self.assertRaises(ValidationError):
            self.env['etudiant'].create({'partner_id': self.partner.id, 'age': 15})
    
    def test_05_mock(self):
        from odoo.addons.compute_example.models.test_compute import Etudiant
        old_method = Etudiant._get_majeur_value
        Etudiant._get_majeur_value = lambda *a: True
        st = self.env['etudiant'].create({'partner_id': self.partner.id, 'age': 17})
        self.assertTrue(st.majeur)
        Etudiant._get_majeur_value = old_method
