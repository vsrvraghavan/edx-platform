# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-13 17:34


import uuid

import django.utils.timezone
import django_countries.fields
import model_utils.fields
import opaque_keys.edx.django.models
import simple_history.models
from django.conf import settings
from django.db import migrations, models
from lms.djangoapps.experiments.models import ExperimentData
from common.djangoapps.student.models import CourseEnrollment, FBEEnrollmentExclusion

import openedx.core.djangolib.model_mixins
from common.djangoapps.course_modes import models as course_modes_models
from openedx.features.course_duration_limits.config import EXPERIMENT_DATA_HOLDBACK_KEY, EXPERIMENT_ID


# These data migrations do not require changes when building from scratch.
# student.migrations.0029_add_data_researcher
# student.migrations.0011_course_key_field_to_foreign_key

# student.migrations.0025_auto_20191101_1846
def populate_fbeenrollmentexclusion(apps, schema_editor):
    holdback_entries = ExperimentData.objects.filter(
        experiment_id=EXPERIMENT_ID,
        key=EXPERIMENT_DATA_HOLDBACK_KEY,
        value='True'
    )
    for holdback_entry in holdback_entries:
        enrollments = [FBEEnrollmentExclusion(enrollment=enrollment)
                       for enrollment in CourseEnrollment.objects.filter(user=holdback_entry.user)]
        if enrollments:
            FBEEnrollmentExclusion.objects.bulk_create(enrollments)


class Migration(migrations.Migration):

    replaces = [('student', '0001_initial'), ('student', '0002_auto_20151208_1034'), ('student', '0003_auto_20160516_0938'), ('student', '0004_auto_20160531_1422'), ('student', '0005_auto_20160531_1653'), ('student', '0006_logoutviewconfiguration'), ('student', '0007_registrationcookieconfiguration'), ('student', '0008_auto_20161117_1209'), ('student', '0009_auto_20170111_0422'), ('student', '0010_auto_20170207_0458'), ('student', '0011_course_key_field_to_foreign_key'), ('student', '0012_sociallink'), ('student', '0013_delete_historical_enrollment_records'), ('student', '0014_courseenrollmentallowed_user'), ('student', '0015_manualenrollmentaudit_add_role'), ('student', '0016_coursenrollment_course_on_delete_do_nothing'), ('student', '0017_accountrecovery'), ('student', '0018_remove_password_history'), ('student', '0019_auto_20181221_0540'), ('student', '0020_auto_20190227_2019'), ('student', '0021_historicalcourseenrollment'), ('student', '0022_indexing_in_courseenrollment'), ('student', '0023_bulkunenrollconfiguration'), ('student', '0024_fbeenrollmentexclusion'), ('student', '0025_auto_20191101_1846'), ('student', '0026_allowedauthuser'), ('student', '0027_courseenrollment_mode_callable_default'), ('student', '0028_historicalmanualenrollmentaudit'), ('student', '0029_add_data_researcher'), ('student', '0030_userprofile_phone_number'), ('student', '0031_auto_20200317_1122')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course_overviews', '0013_courseoverview_language'),
        ('experiments', '0001_initial'),
        ('sites', '0002_alter_domain_unique'),
        ('course_overviews', '0014_courseoverview_certificate_available_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnonymousUserId',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anonymous_user_id', models.CharField(max_length=32, unique=True)),
                ('course_id', opaque_keys.edx.django.models.CourseKeyField(blank=True, db_index=True, max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CourseAccessRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org', models.CharField(blank=True, db_index=True, max_length=64)),
                ('course_id', opaque_keys.edx.django.models.CourseKeyField(blank=True, db_index=True, max_length=255)),
                ('role', models.CharField(db_index=True, max_length=64)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CourseEnrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='course_overviews.CourseOverview')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('mode', models.CharField(default=b'honor', max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('user', 'course_id'),
            },
        ),
        migrations.CreateModel(
            name='CourseEnrollmentAllowed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(db_index=True, max_length=255)),
                ('course_id', opaque_keys.edx.django.models.CourseKeyField(db_index=True, max_length=255)),
                ('auto_enroll', models.BooleanField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseEnrollmentAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('namespace', models.CharField(help_text='Namespace of enrollment attribute', max_length=255)),
                ('name', models.CharField(help_text='Name of the enrollment attribute', max_length=255)),
                ('value', models.CharField(help_text='Value of the enrollment attribute', max_length=255)),
                ('enrollment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='student.CourseEnrollment')),
            ],
        ),
        migrations.CreateModel(
            name='DashboardConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_date', models.DateTimeField(auto_now_add=True, verbose_name='Change date')),
                ('enabled', models.BooleanField(default=False, verbose_name='Enabled')),
                ('recent_enrollment_time_delta', models.PositiveIntegerField(default=0, help_text="The number of seconds in which a new enrollment is considered 'recent'. Used to display notifications.")),
                ('changed_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Changed by')),
            ],
            options={
                'ordering': ('-change_date',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EnrollmentRefundConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_date', models.DateTimeField(auto_now_add=True, verbose_name='Change date')),
                ('enabled', models.BooleanField(default=False, verbose_name='Enabled')),
                ('refund_window_microseconds', models.BigIntegerField(default=1209600000000, help_text='The window of time after enrolling during which users can be granted a refund, represented in microseconds. The default is 14 days.')),
                ('changed_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Changed by')),
            ],
            options={
                'ordering': ('-change_date',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EntranceExamConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', opaque_keys.edx.django.models.CourseKeyField(db_index=True, max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('skip_entrance_exam', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LanguageProficiency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(choices=[['aa', 'Afar'], ['ab', 'Abkhazian'], ['af', 'Afrikaans'], ['ak', 'Akan'], ['sq', 'Albanian'], ['am', 'Amharic'], ['ar', 'Arabic'], ['an', 'Aragonese'], ['hy', 'Armenian'], ['as', 'Assamese'], ['av', 'Avaric'], ['ae', 'Avestan'], ['ay', 'Aymara'], ['az', 'Azerbaijani'], ['ba', 'Bashkir'], ['bm', 'Bambara'], ['eu', 'Basque'], ['be', 'Belarusian'], ['bn', 'Bengali'], ['bh', 'Bihari languages'], ['bi', 'Bislama'], ['bs', 'Bosnian'], ['br', 'Breton'], ['bg', 'Bulgarian'], ['my', 'Burmese'], ['ca', 'Catalan'], ['ch', 'Chamorro'], ['ce', 'Chechen'], ['zh', 'Chinese'], ['zh_HANS', 'Simplified Chinese'], ['zh_HANT', 'Traditional Chinese'], ['cu', 'Church Slavic'], ['cv', 'Chuvash'], ['kw', 'Cornish'], ['co', 'Corsican'], ['cr', 'Cree'], ['cs', 'Czech'], ['da', 'Danish'], ['dv', 'Divehi'], ['nl', 'Dutch'], ['dz', 'Dzongkha'], ['en', 'English'], ['eo', 'Esperanto'], ['et', 'Estonian'], ['ee', 'Ewe'], ['fo', 'Faroese'], ['fj', 'Fijian'], ['fi', 'Finnish'], ['fr', 'French'], ['fy', 'Western Frisian'], ['ff', 'Fulah'], ['ka', 'Georgian'], ['de', 'German'], ['gd', 'Gaelic'], ['ga', 'Irish'], ['gl', 'Galician'], ['gv', 'Manx'], ['el', 'Greek'], ['gn', 'Guarani'], ['gu', 'Gujarati'], ['ht', 'Haitian'], ['ha', 'Hausa'], ['he', 'Hebrew'], ['hz', 'Herero'], ['hi', 'Hindi'], ['ho', 'Hiri Motu'], ['hr', 'Croatian'], ['hu', 'Hungarian'], ['ig', 'Igbo'], ['is', 'Icelandic'], ['io', 'Ido'], ['ii', 'Sichuan Yi'], ['iu', 'Inuktitut'], ['ie', 'Interlingue'], ['ia', 'Interlingua'], ['id', 'Indonesian'], ['ik', 'Inupiaq'], ['it', 'Italian'], ['jv', 'Javanese'], ['ja', 'Japanese'], ['kl', 'Kalaallisut'], ['kn', 'Kannada'], ['ks', 'Kashmiri'], ['kr', 'Kanuri'], ['kk', 'Kazakh'], ['km', 'Central Khmer'], ['ki', 'Kikuyu'], ['rw', 'Kinyarwanda'], ['ky', 'Kirghiz'], ['kv', 'Komi'], ['kg', 'Kongo'], ['ko', 'Korean'], ['kj', 'Kuanyama'], ['ku', 'Kurdish'], ['lo', 'Lao'], ['la', 'Latin'], ['lv', 'Latvian'], ['li', 'Limburgan'], ['ln', 'Lingala'], ['lt', 'Lithuanian'], ['lb', 'Luxembourgish'], ['lu', 'Luba-Katanga'], ['lg', 'Ganda'], ['mk', 'Macedonian'], ['mh', 'Marshallese'], ['ml', 'Malayalam'], ['mi', 'Maori'], ['mr', 'Marathi'], ['ms', 'Malay'], ['mg', 'Malagasy'], ['mt', 'Maltese'], ['mn', 'Mongolian'], ['na', 'Nauru'], ['nv', 'Navajo'], ['nr', 'Ndebele, South'], ['nd', 'Ndebele, North'], ['ng', 'Ndonga'], ['ne', 'Nepali'], ['nn', 'Norwegian Nynorsk'], ['nb', 'Bokmål, Norwegian'], ['no', 'Norwegian'], ['ny', 'Chichewa'], ['oc', 'Occitan'], ['oj', 'Ojibwa'], ['or', 'Oriya'], ['om', 'Oromo'], ['os', 'Ossetian'], ['pa', 'Panjabi'], ['fa', 'Persian'], ['pi', 'Pali'], ['pl', 'Polish'], ['pt', 'Portuguese'], ['ps', 'Pushto'], ['qu', 'Quechua'], ['rm', 'Romansh'], ['ro', 'Romanian'], ['rn', 'Rundi'], ['ru', 'Russian'], ['sg', 'Sango'], ['sa', 'Sanskrit'], ['si', 'Sinhala'], ['sk', 'Slovak'], ['sl', 'Slovenian'], ['se', 'Northern Sami'], ['sm', 'Samoan'], ['sn', 'Shona'], ['sd', 'Sindhi'], ['so', 'Somali'], ['st', 'Sotho, Southern'], ['es', 'Spanish'], ['sc', 'Sardinian'], ['sr', 'Serbian'], ['ss', 'Swati'], ['su', 'Sundanese'], ['sw', 'Swahili'], ['sv', 'Swedish'], ['ty', 'Tahitian'], ['ta', 'Tamil'], ['tt', 'Tatar'], ['te', 'Telugu'], ['tg', 'Tajik'], ['tl', 'Tagalog'], ['th', 'Thai'], ['bo', 'Tibetan'], ['ti', 'Tigrinya'], ['to', 'Tonga (Tonga Islands)'], ['tn', 'Tswana'], ['ts', 'Tsonga'], ['tk', 'Turkmen'], ['tr', 'Turkish'], ['tw', 'Twi'], ['ug', 'Uighur'], ['uk', 'Ukrainian'], ['ur', 'Urdu'], ['uz', 'Uzbek'], ['ve', 'Venda'], ['vi', 'Vietnamese'], ['vo', 'Volapük'], ['cy', 'Welsh'], ['wa', 'Walloon'], ['wo', 'Wolof'], ['xh', 'Xhosa'], ['yi', 'Yiddish'], ['yo', 'Yoruba'], ['za', 'Zhuang'], ['zu', 'Zulu']], help_text='The ISO 639-1 language code for this language.', max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='LinkedInAddToProfileConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_date', models.DateTimeField(auto_now_add=True, verbose_name='Change date')),
                ('enabled', models.BooleanField(default=False, verbose_name='Enabled')),
                ('company_identifier', models.TextField(help_text='The company identifier for the LinkedIn Add-to-Profile button e.g 0_0dPSPyS070e0HsE9HNz_13_d11_')),
                ('dashboard_tracking_code', models.TextField(blank=True, default='')),
                ('trk_partner_name', models.CharField(blank=True, default='', help_text="Short identifier for the LinkedIn partner used in the tracking code.  (Example: 'edx')  If no value is provided, tracking codes will not be sent to LinkedIn.", max_length=10)),
                ('changed_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Changed by')),
            ],
            options={
                'ordering': ('-change_date',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LoginFailures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('failure_count', models.IntegerField(default=0)),
                ('lockout_until', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Login Failures',
                'verbose_name': 'Login Failure',
            },
        ),
        migrations.CreateModel(
            name='ManualEnrollmentAudit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrolled_email', models.CharField(db_index=True, max_length=255)),
                ('time_stamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('state_transition', models.CharField(choices=[('from unenrolled to allowed to enroll', 'from unenrolled to allowed to enroll'), ('from allowed to enroll to enrolled', 'from allowed to enroll to enrolled'), ('from enrolled to enrolled', 'from enrolled to enrolled'), ('from enrolled to unenrolled', 'from enrolled to unenrolled'), ('from unenrolled to enrolled', 'from unenrolled to enrolled'), ('from allowed to enroll to enrolled', 'from allowed to enroll to enrolled'), ('from unenrolled to unenrolled', 'from unenrolled to unenrolled'), ('N/A', 'N/A')], max_length=255)),
                ('reason', models.TextField(null=True)),
                ('enrolled_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('enrollment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.CourseEnrollment')),
                ('role', models.CharField(blank=True, max_length=64, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PendingEmailChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_email', models.CharField(blank=True, db_index=True, max_length=255)),
                ('activation_key', models.CharField(db_index=True, max_length=32, unique=True, verbose_name='activation key')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PendingNameChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_name', models.CharField(blank=True, max_length=255)),
                ('rationale', models.CharField(blank=True, max_length=1024)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activation_key', models.CharField(db_index=True, max_length=32, unique=True, verbose_name='activation key')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'auth_registration',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, db_index=True, max_length=255)),
                ('meta', models.TextField(blank=True)),
                ('courseware', models.CharField(blank=True, default='course.xml', max_length=255)),
                ('language', models.CharField(blank=True, db_index=True, max_length=255)),
                ('location', models.CharField(blank=True, db_index=True, max_length=255)),
                ('year_of_birth', models.IntegerField(blank=True, db_index=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('m', 'Male'), ('f', 'Female'), ('o', 'Other/Prefer Not to Say')], db_index=True, max_length=6, null=True)),
                ('level_of_education', models.CharField(blank=True, choices=[('p', 'Doctorate'), ('m', "Master's or professional degree"), ('b', "Bachelor's degree"), ('a', 'Associate degree'), ('hs', 'Secondary/high school'), ('jhs', 'Junior secondary/junior high/middle school'), ('el', 'Elementary/primary school'), ('none', 'No formal education'), ('other', 'Other education')], db_index=True, max_length=6, null=True)),
                ('mailing_address', models.TextField(blank=True, null=True)),
                ('city', models.TextField(blank=True, null=True)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('goals', models.TextField(blank=True, null=True)),
                ('allow_certificate', models.BooleanField(default=1)),
                ('completed_registration_assesment', models.BooleanField(default=0)),
                ('bio', models.CharField(blank=True, max_length=3000, null=True)),
                ('profile_image_uploaded_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'auth_userprofile',
                'permissions': (('can_deactivate_users', 'Can deactivate, but NOT delete users'),),
            },
        ),
        migrations.CreateModel(
            name='UserSignupSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site', models.CharField(db_index=True, max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserStanding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_status', models.CharField(blank=True, choices=[('disabled', 'Account Disabled'), ('enabled', 'Account Enabled')], max_length=31)),
                ('standing_last_changed_at', models.DateTimeField(auto_now=True)),
                ('changed_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='standing', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserTestGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=32)),
                ('description', models.TextField(blank=True)),
                ('users', models.ManyToManyField(db_index=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='languageproficiency',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='language_proficiencies', to='student.UserProfile'),
        ),
        migrations.AddField(
            model_name='courseenrollmentallowed',
            name='user',
            field=models.ForeignKey(blank=True, help_text="First user which enrolled in the specified course through the specified e-mail. Once set, it won't change.", null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='courseenrollmentallowed',
            unique_together=set([('email', 'course_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='languageproficiency',
            unique_together=set([('code', 'user_profile')]),
        ),
        migrations.AlterUniqueTogether(
            name='entranceexamconfiguration',
            unique_together=set([('user', 'course_id')]),
        ),
        migrations.AlterField(
            model_name='courseenrollment',
            name='mode',
            field=models.CharField(default='audit', max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='courseenrollment',
            unique_together=set([('user', 'course_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='courseaccessrole',
            unique_together=set([('user', 'org', 'course_id', 'role')]),
        ),
        migrations.CreateModel(
            name='UserAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(help_text='Name of this user attribute.', max_length=255)),
                ('value', models.CharField(help_text='Value of this user attribute.', max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='userattribute',
            unique_together=set([('user', 'name')]),
        ),
        migrations.AlterField(
            model_name='userattribute',
            name='name',
            field=models.CharField(db_index=True, help_text='Name of this user attribute.', max_length=255),
        ),
        migrations.CreateModel(
            name='LogoutViewConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_date', models.DateTimeField(auto_now_add=True, verbose_name='Change date')),
                ('enabled', models.BooleanField(default=False, verbose_name='Enabled')),
                ('changed_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Changed by')),
            ],
            options={
                'ordering': ('-change_date',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegistrationCookieConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_date', models.DateTimeField(auto_now_add=True, verbose_name='Change date')),
                ('enabled', models.BooleanField(default=False, verbose_name='Enabled')),
                ('utm_cookie_name', models.CharField(help_text='Name of the UTM cookie', max_length=255)),
                ('affiliate_cookie_name', models.CharField(help_text='Name of the affiliate cookie', max_length=255)),
                ('changed_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Changed by')),
            ],
            options={
                'ordering': ('-change_date',),
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='courseenrollment',
            options={'ordering': ('user', 'course')},
        ),
        migrations.AlterUniqueTogether(
            name='courseenrollment',
            unique_together=set([('user', 'course')]),
        ),
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(max_length=30)),
                ('social_link', models.CharField(blank=True, max_length=100)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_links', to='student.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='AccountRecovery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secondary_email', models.EmailField(help_text='Secondary email address to recover linked account.', max_length=254, unique=True, verbose_name='Secondary email address')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account_recovery', to=settings.AUTH_USER_MODEL)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'auth_accountrecovery',
            },
        ),
        migrations.CreateModel(
            name='PendingSecondaryEmailChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_secondary_email', models.CharField(blank=True, db_index=True, max_length=255)),
                ('activation_key', models.CharField(db_index=True, max_length=32, unique=True, verbose_name='activation key')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=(openedx.core.djangolib.model_mixins.DeletableByUserValue, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalCourseEnrollment',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, db_index=True, editable=False, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('mode', models.CharField(default='audit', max_length=100)),
                ('history_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('course', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='course_overviews.CourseOverview')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'history_date',
                'ordering': ('-history_date', '-history_id'),
                'db_table': 'student_courseenrollment_history',
                'verbose_name': 'historical course enrollment',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AddIndex(
            model_name='courseenrollment',
            index=models.Index(fields=['user', '-created'], name='student_cou_user_id_b19dcd_idx'),
        ),
        migrations.CreateModel(
            name='BulkUnenrollConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_date', models.DateTimeField(auto_now_add=True, verbose_name='Change date')),
                ('enabled', models.BooleanField(default=False, verbose_name='Enabled')),
                ('csv_file', models.FileField(help_text='It expect that the data will be provided in a csv file format with                     first row being the header and columns will be as follows:                     user_id, username, email, course_id, is_verified, verification_date', upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['csv'])])),
                ('changed_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Changed by')),
            ],
            options={
                'ordering': ('-change_date',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FBEEnrollmentExclusion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrollment', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='student.CourseEnrollment')),
            ],
        ),
        migrations.RunPython(
            code=populate_fbeenrollmentexclusion,
            reverse_code=migrations.operations.special.RunPython.noop,
        ),
        migrations.CreateModel(
            name='AllowedAuthUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('email', models.EmailField(help_text="An employee (a user whose email has current site's domain name) whose email exists in this model, can be able to login from login screen through email and password. And if any employee's email doesn't exist in this model then that employee can login via third party authentication backend only.", max_length=254, unique=True)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allowed_auth_users', to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='courseenrollment',
            name='mode',
            field=models.CharField(default=course_modes_models.CourseMode.get_default_mode_slug, max_length=100),
        ),
        migrations.AlterField(
            model_name='historicalcourseenrollment',
            name='mode',
            field=models.CharField(default=course_modes_models.CourseMode.get_default_mode_slug, max_length=100),
        ),
        migrations.CreateModel(
            name='HistoricalManualEnrollmentAudit',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('enrolled_email', models.CharField(db_index=True, max_length=255)),
                ('time_stamp', models.DateTimeField(blank=True, editable=False, null=True)),
                ('state_transition', models.CharField(choices=[('from unenrolled to allowed to enroll', 'from unenrolled to allowed to enroll'), ('from allowed to enroll to enrolled', 'from allowed to enroll to enrolled'), ('from enrolled to enrolled', 'from enrolled to enrolled'), ('from enrolled to unenrolled', 'from enrolled to unenrolled'), ('from unenrolled to enrolled', 'from unenrolled to enrolled'), ('from allowed to enroll to enrolled', 'from allowed to enroll to enrolled'), ('from unenrolled to unenrolled', 'from unenrolled to unenrolled'), ('N/A', 'N/A')], max_length=255)),
                ('reason', models.TextField(null=True)),
                ('role', models.CharField(blank=True, max_length=64, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('enrolled_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('enrollment', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='student.CourseEnrollment')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'history_date',
                'ordering': ('-history_date', '-history_id'),
                'verbose_name': 'historical manual enrollment audit',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=50, null=True, validators=[django.core.validators.RegexValidator(message='Phone number can only contain numbers.', regex='^\\+?1?\\d*$')]),
        ),
        migrations.CreateModel(
            name='AccountRecoveryConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_date', models.DateTimeField(auto_now_add=True, verbose_name='Change date')),
                ('enabled', models.BooleanField(default=False, verbose_name='Enabled')),
                ('csv_file', models.FileField(help_text='It expect that the data will be provided in a csv file format with                     first row being the header and columns will be as follows:                     username, email, new_email', upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['csv'])])),
                ('changed_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Changed by')),
            ],
            options={
                'ordering': ('-change_date',),
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='courseenrollment',
            name='course',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING,
                                    to='course_overviews.CourseOverview'),
        ),
    ]
