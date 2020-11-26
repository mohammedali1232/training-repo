# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

# This is the main class of Bista Training Module
class BistaTraining(models.Model):
    _name = 'bista_training.bista_training'
    _description = 'Bista Training'

    name = fields.Char('Name')
    value = fields.Integer('Exam Score')
    date = fields.Date('Date of Exam',required=1)
    trainee_ids = fields.One2many('bista.trainee','training_batch_id',string="Trainee")

class Trainee(models.Model):
    _name = 'bista.trainee'
    _description = 'Trainee Master'

    #def create(self,vals):
    #def write(self,vals):
    #def unlink(self,vals):  unimplemented

    @api.model
    def create(self,vals):
        print("@@@@@",vals)
        return super(Trainee,self).create(vals)

    def write(self,vals):
        print("This is from write method",vals)
        return super(Trainee,self).write(vals)

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {})
        default.update(
            email= _("%s (copy)") % (self.email or ''))

        return super(Trainee,self).copy(default)

    def action_employed(self):
        #Actions
       # import pdb;
       #  pdb.set_trace()
        for record in self:
            record.state = 'employed'
        return True

    @api.constrains('email_2')
    def _check_email_2_values(self):
        if self.email_2 == 'ali@gmail.com':
            raise ValidationError(_('You are not allowed to enter this value'))


    name = fields.Char(compute='concat_name',store="True")
    first_name = fields.Char('First Name',required="True")
    last_name = fields.Char('Last Name')
    email_2 = fields.Char("Email2")
    email = fields.Char("Email",required="True")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('transgender', 'Transgender')], default='male')
    date_of_birth = fields.Date('Date of Birth')
    date_of_joining = fields.Date('Date of Joining')
    emp_code = fields.Integer('EMP code')
    trainee_id = fields.Char(string="Trainee ID", default=lambda self: self.env['ir.sequence'].next_by_code('trainee.id'))
    training_batch_id = fields.Many2one('bista_training.bista_training',string="Batch",
                                        help='this field is to fill up batch details')

    image_1 = fields.Image(String="Image")
    status = fields.Selection([('new','New'),('employed','Employed'),('training','Training'),
                              ('rejected','Rejected')],string="Status",default='new')

    _sql_constraints = [
        ('email_uniq','unique(email)','Email ID should be unique')
    ]


    @api.depends('first_name', 'last_name')
    def concat_name(self):
        self.name = (self.first_name or '') + ' ' + (self.last_name or '')