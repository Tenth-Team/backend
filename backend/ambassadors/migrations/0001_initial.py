# Generated by Django 4.2.10 on 2024-03-10 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ambassador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, verbose_name='Полное имя')),
                ('gender', models.CharField(choices=[('М', 'Мужской'), ('Ж', 'Женский')], max_length=1, verbose_name='Пол')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес проживания')),
                ('postal_code', models.CharField(max_length=20, verbose_name='Индекс')),
                ('email', models.CharField(max_length=255, verbose_name='Адрес проживания')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Номер телефона')),
                ('telegram', models.CharField(max_length=100, verbose_name='Ник в телеграме')),
                ('edu', models.TextField(max_length=1000, verbose_name='Образование')),
                ('work', models.TextField(max_length=1000, verbose_name='Место работы')),
                ('study_goal', models.TextField(max_length=1000, verbose_name='Цель обучения')),
                ('blog_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ссылка на блоги')),
                ('clothing_size', models.CharField(choices=[('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')], max_length=3, verbose_name='Размер одежды')),
                ('shoe_size', models.CharField(max_length=50, verbose_name='Размер обуви')),
                ('additional_comments', models.TextField(blank=True, max_length=2000, null=True, verbose_name='Дополнительная информация')),
                ('status', models.CharField(choices=[('active', 'Активный'), ('paused', 'На паузе'), ('not_ambassador', 'Не амбассадор'), ('pending', 'Уточняется')], default='pending', max_length=50, verbose_name='Статус амбассадора')),
                ('reg_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')),
            ],
            options={
                'verbose_name': 'Амбассадор',
                'verbose_name_plural': 'Амбассадоры',
            },
        ),
        migrations.CreateModel(
            name='AmbassadorGoal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название цели')),
            ],
            options={
                'verbose_name': 'Цель амбассадорства',
                'verbose_name_plural': 'Цели амбассадорства',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название города')),
            ],
            options={
                'verbose_name': 'город',
                'verbose_name_plural': 'города',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название страны')),
            ],
            options={
                'verbose_name': 'страна',
                'verbose_name_plural': 'страны',
            },
        ),
        migrations.CreateModel(
            name='Merchandise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('hoody', 'Толстовка'), ('coffee', 'Кофе'), ('stickers', 'Стикеры'), ('plus', 'Плюс'), ('arzamas', 'Арзамас'), ('shopper', 'Шоппер'), ('backpack', 'Рюкзак'), ('cross_bag', 'Сумка кросс'), ('socks', 'Носки'), ('50%_discount', 'Скидка 50%'), ('alice_mini', 'Алиса мини'), ('alice_big', 'Алиса биг'), ('student_club_at_night', 'Клуб учащихся ночью')], max_length=25, verbose_name='Название мерча')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость мерча')),
            ],
            options={
                'verbose_name': 'Мерч',
                'verbose_name_plural': 'Мерч',
            },
        ),
        migrations.CreateModel(
            name='TrainingProgram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название программы')),
            ],
            options={
                'verbose_name': 'Программа обучения',
                'verbose_name_plural': 'Программы обучения',
            },
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Промокод')),
                ('status', models.CharField(choices=[('active', 'Активный'), ('inactive', 'Неактивный')], default='active', max_length=10, verbose_name='Статус промокода')),
                ('ambassador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='promo_code', to='ambassadors.ambassador', verbose_name='Амбассадор')),
            ],
            options={
                'verbose_name': 'Промокод',
                'verbose_name_plural': 'Промокоды',
            },
        ),
        migrations.CreateModel(
            name='MerchandiseShippingRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_send', models.CharField(choices=[('new', 'Новая заявка'), ('address_verified', 'Адрес проверен'), ('sent_to_logisticians', 'Отправлена логистам')], default='new', max_length=25, verbose_name='Статус отправки')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('comment', models.TextField(max_length=200, verbose_name='Комментарий менеджера')),
                ('ambassador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='merch_shipping_requests', to='ambassadors.ambassador', verbose_name='Амбассадор')),
                ('name_merch', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ambassadors.merchandise', verbose_name='Название мерча')),
            ],
            options={
                'verbose_name': 'Заявка на отправку мерча',
                'verbose_name_plural': 'Заявки на отправку мерча',
            },
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, verbose_name='Имя и Фамилия')),
                ('telegram', models.CharField(max_length=100, verbose_name='Ник в телеграме')),
                ('link', models.CharField(max_length=200, verbose_name='Ссылка на контент')),
                ('guide', models.BooleanField(verbose_name='В рамках Гайда?')),
                ('status', models.CharField(choices=[('new', 'Новая публикация'), ('approved', 'Одобрена'), ('rejected', 'Не одобрена')], default='new', max_length=50, verbose_name='Статус контента')),
                ('comment', models.TextField(blank=True, max_length=200, null=True, verbose_name='Комментарий менеджера')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('ambassador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='content', to='ambassadors.ambassador', verbose_name='амбассадор')),
            ],
            options={
                'verbose_name': 'Контент',
                'verbose_name_plural': 'Контент',
            },
        ),
        migrations.AddField(
            model_name='ambassador',
            name='amb_goals',
            field=models.ManyToManyField(related_name='ambassadors', to='ambassadors.ambassadorgoal', verbose_name='Цель амбассадорства'),
        ),
        migrations.AddField(
            model_name='ambassador',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ambassadors.city', verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='ambassador',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ambassadors', to='ambassadors.country', verbose_name='Страна'),
        ),
        migrations.AddField(
            model_name='ambassador',
            name='ya_edu',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ambassadors', to='ambassadors.trainingprogram', verbose_name='Программа обучения'),
        ),
    ]
