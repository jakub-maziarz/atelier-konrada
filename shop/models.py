import uuid
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField('slug', max_length=255, blank=True, unique=False)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _("Categories")

    def save(self, *args, **kwargs):
        if not self.slug:
            pl_letters = 'ąćęłńóśźż'
            letters = 'acelnoszz'
            translator = ''.maketrans(pl_letters, letters)
            name_to_slug = self.name.lower().translate(translator)
            self.slug = slugify(name_to_slug)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


@receiver(pre_save, sender=Category)
def update_slug(sender, instance, **kwargs):
    if (sender.objects.filter(id=instance.id).count() > 0):
        if (sender.objects.get(id=instance.id).name != instance.name):
            pl_letters = 'ąćęłńóśźż'
            letters = 'acelnoszz'
            translator = ''.maketrans(pl_letters, letters)
            name_to_slug = instance.name.lower().translate(translator)
            instance.slug = slugify(name_to_slug)


class Product(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    slug = models.SlugField('slug', max_length=255, blank=True, unique=True)
    price = models.DecimalField(_('price'), max_digits=7, decimal_places=2)
    description = models.TextField(_('description'), max_length=800)
    quantity = models.IntegerField(_('quantity'), blank=True, default=0)
    categories = models.ManyToManyField(Category, through='CategoryProduct')
    recommended = models.BooleanField(_('recommended'), default=False)
    status = models.BooleanField(
        _('status'), default=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _("Products")

    def save(self, *args, **kwargs):
        if not self.slug:
            pl_letters = 'ąćęłńóśźż'
            letters = 'acelnoszz'
            translator = ''.maketrans(pl_letters, letters)
            name_to_slug = self.name.lower().translate(translator)
            self.slug = slugify(name_to_slug)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)

    @property
    def get_thumbnail_image(self):
        image = Image.objects.filter(product_id=self.id).first().image_path.url
        return image


@receiver(pre_save, sender=Product)
def update_slug(sender, instance, **kwargs):
    if (sender.objects.filter(id=instance.id).count() > 0):
        if (sender.objects.get(id=instance.id).name != instance.name):
            pl_letters = 'ąćęłńóśźż'
            letters = 'acelnoszz'
            translator = ''.maketrans(pl_letters, letters)
            name_to_slug = instance.name.lower().translate(translator)
            instance.slug = slugify(name_to_slug)


class CategoryProduct(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('CategoryProduct')
        verbose_name_plural = _("CategoryProducts")

    def __str__(self):
        return str(self.category.name) + " : " + str(self.product.name)


class Image(models.Model):
    product = models.ForeignKey(
        Product, related_name='images', on_delete=models.CASCADE)
    image_path = models.ImageField(_('image_path'), upload_to='uploads/')

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _("Images")

    def __str__(self):
        return str(self.product.name)


@receiver(post_delete, sender=Image)
def update_image(sender, instance, **kwargs):
    instance.image_path.delete(save=False)


STATUS_CHOICES = (
    ('ordered', _('ordered')),
    ('paid', _('paid')),
    ('shipped', _('shipped')),
    ('finished', _('finished'))
)


class Order(models.Model):
    customer_name = models.CharField(_('customer name'), max_length=100)
    customer_phone = models.CharField(_('customer phone'), max_length=100)
    customer_email = models.CharField(_('customer email'), max_length=100)
    to_zip = models.CharField(_('zip code'), max_length=50)
    to_city = models.CharField(_('city'), max_length=100)
    to_street = models.CharField(_('street'), max_length=100)
    to_house_number = models.CharField(
        _('house number'), max_length=50, default="")
    address = models.TextField(_('address'), null=True, blank=True)
    products = models.ManyToManyField(Product, through='OrderProduct')
    transaction_id = models.UUIDField(
        _('transaction id'), default=uuid.uuid4)
    client_id = models.CharField(_('client id'), max_length=100)
    order_number = models.CharField(
        _('order_number'), max_length=30, default="", null=True, blank=True)
    customer_name_other = models.CharField(
        _('other customer name'), max_length=100, null=True, blank=True)
    customer_phone_other = models.CharField(
        _('other customer phone'), max_length=100, null=True, blank=True)
    customer_email_other = models.CharField(
        _('other customer email'), max_length=100, null=True, blank=True)
    to_zip_other = models.CharField(
        _('other zip code'), max_length=50, null=True, blank=True)
    to_city_other = models.CharField(
        _('other city'), max_length=100, null=True, blank=True)
    to_street_other = models.CharField(
        _('other street'), max_length=100, null=True, blank=True)
    to_house_number_other = models.CharField(
        _('other house number'), max_length=50, null=True, blank=True)
    address_other = models.TextField(_('other address'), null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    status = models.CharField(_('status'),
                              max_length=50, choices=STATUS_CHOICES, default="ordered")

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _("Orders")

    def __str__(self):
        return str("Zamówienie: " + self.order_number)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(_('quantity'), default=1)

    class Meta:
        verbose_name = _('OrderProduct')
        verbose_name_plural = _("OrderProducts")

    def __str__(self):
        return str(self.order.order_number) + " : " + str(self.product.name)


class Cart(models.Model):
    client_id = models.CharField(_('client id'), max_length=100)
    products = models.ManyToManyField(Product, through='CartProduct')
    customer_name = models.CharField(
        _('customer name'), max_length=100, null=True, blank=True)
    customer_phone = models.CharField(
        _('customer phone'), max_length=100, null=True, blank=True)
    customer_email = models.CharField(
        _('customer email'), max_length=100, null=True, blank=True)
    to_zip = models.CharField(
        _('zip code'), max_length=50, null=True, blank=True)
    to_city = models.CharField(
        _('city'), max_length=100, null=True, blank=True)
    to_street = models.CharField(
        _('street'), max_length=100, null=True, blank=True)
    to_house_number = models.CharField(
        _('house number'), max_length=50, null=True, blank=True)
    address = models.TextField(_('address'), null=True, blank=True)
    customer_name_other = models.CharField(
        _('other customer name'), max_length=100, null=True, blank=True)
    customer_phone_other = models.CharField(
        _('other customer phone'), max_length=100, null=True, blank=True)
    customer_email_other = models.CharField(
        _('other customer email'), max_length=100, null=True, blank=True)
    to_zip_other = models.CharField(
        _('other zip code'), max_length=50, null=True, blank=True)
    to_city_other = models.CharField(
        _('other city'), max_length=100, null=True, blank=True)
    to_street_other = models.CharField(
        _('other street'), max_length=100, null=True, blank=True)
    to_house_number_other = models.CharField(
        _('other house number'), max_length=50, null=True, blank=True)
    address_other = models.TextField(_('other address'), null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _("Carts")

    def __str__(self):
        return str(self.client_id)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(_('quantity'), default=1)

    class Meta:
        verbose_name = _('CartProduct')
        verbose_name_plural = _("CartProducts")

    def __str__(self):
        return str(self.cart.client_id) + " : " + str(self.product.name)


class Newsletter(models.Model):
    customer_email = models.CharField(_('customer email'), max_length=100)

    class Meta:
        verbose_name = _('Newsletter')
        verbose_name_plural = _("Newsletters")

    def __str__(self):
        return str(self.customer_email)
