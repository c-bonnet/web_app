from flask_wtf import FlaskForm
from wtforms import StringField, FileField, IntegerField, SubmitField, BooleanField, TextAreaField, FormField, SelectField, FloatField, PasswordField
from wtforms.validators import ValidationError, DataRequired, InputRequired, NumberRange, Email


class CommercialForm(FlaskForm):
    description = StringField("Title of the Assessment")
    site_type = SelectField("Site Type *", choices=[("wind", "Wind"), ("solar", "Solar"), ("hydro", "Hydro"), ("wind_solar", "Wind + Solar")])
    rated_power = FloatField("Rated Power (kW) *", default=2000, validators=[NumberRange(min=1, message="Please enter a positive power."), InputRequired()])
    export_capacity = IntegerField("Export Capacity (kW) *", default=150, validators=[NumberRange(min=0, message="Please enter a positive integer."), InputRequired()])
    import_capacity = IntegerField("Import Capacity (kW) *", default=50, validators=[NumberRange(min=0, message="Please enter a positive integer."), InputRequired()])
    spill = FloatField("Spill due to data resolution (%) *", default=3, validators=[NumberRange(min=0, max=100, message="Please enter a positive percentage."), InputRequired()])
    winter_op_hours = FloatField("Winter Off-Peak Hours per Week *", default=5*12+2*24, validators=[NumberRange(min=0, max=7*24, message="Please enter a number of hours between %(min)d and %(max)d."), InputRequired()])
    winter_op_price = FloatField("Winter Off-Peak Price (£/MWh) *", default=50, validators=[NumberRange(min=0, message="Please enter a positive price."), InputRequired()])
    winter_p_hours = FloatField("Winter Peak Hours per Week *", default=5*12, validators=[NumberRange(min=0, max=7*24, message="Please enter a number of hours between %(min)d and %(max)d."), InputRequired()])
    winter_p_price = FloatField("Winter Peak Price (£/MWh) *", default=50, validators=[NumberRange(min=0, message="Please enter a positive price."), InputRequired()])
    summer_op_hours = FloatField("Summer Off-Peak Hours per Week *", default=5*12+2*24, validators=[NumberRange(min=0, max=7*24, message="Please enter a number of hours between %(min)d and %(max)d."), InputRequired()])
    summer_op_price = FloatField("Summer Off-Peak Price (£/MWh) *", default=50, validators=[NumberRange(min=0, message="Please enter a positive price."), InputRequired()])
    summer_p_hours = FloatField("Summer Peak Hours per Week *", default=5*12, validators=[NumberRange(min=0, max=7*24, message="Please enter a number of hours between %(min)d and %(max)d."), InputRequired()])
    summer_p_price = FloatField("Summer Peak Price (£/MWh) *", default=50, validators=[NumberRange(min=0, message="Please enter a positive price."), InputRequired()])
    miner_power = FloatField("Power Draw of One Miner (W) *", default=3340, validators=[NumberRange(min=0, message="Please enter a positive integer."), InputRequired()])
    miner_hashing = FloatField("Miner Hashing (TH/s)", default=88, validators=[NumberRange(min=0, message="Please enter a positive integer."), InputRequired()])
    miner_price = FloatField("Miner Price (£)", default=1200, validators=[NumberRange(min=0, message="Please enter a positive integer."), InputRequired()])
    miner_number = FloatField("Number of Miners", default=150, validators=[NumberRange(min=0, message="Please enter a positive integer."), InputRequired()])
    powerbox_shell_cost = FloatField("PowerBox Shell Cost (£)", default=150000, validators=[NumberRange(min=0, message="Please enter a positive integer."), InputRequired()])
    powerbox_maintenance = FloatField("PowerBox Maintenance Cost (£/year)", default=822, validators=[NumberRange(min=0, message="Please enter a positive integer."), InputRequired()])
    generation_data = FileField("Generation Data")
    submit = SubmitField("Run Commercial Assessment")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # does not work because is called only at form creation
        # initialise the export capacity to 5% of the rated power
        if self.rated_power.data and not self.export_capacity.data:
            self.export_capacity.data = 1*self.rated_power.data
        # initialise the import capacity to 5% of the rated power
        if self.rated_power.data and not self.import_capacity.data:
            self.import_capacity.data = 0.05*self.rated_power.data

    def validate_winter_op_hours(self, winter_op_hours):
        # check whether the sum of winter hours is 7*24=168 hours in a week
        if self.winter_p_hours.data + winter_op_hours.data != 168:
            raise ValidationError("The sum of winter peak and off-peak hours must be equal to 168 (7 days of 24 hours)")

    def validate_summer_op_hours(self, summer_op_hours):
        # check whether the sum of summer hours is 7*24=168 hours in a week
        if self.summer_p_hours.data + summer_op_hours.data != 168:
            raise ValidationError("The sum of summer peak and off-peak hours must be equal to 168 (7 days of 24 hours)")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")