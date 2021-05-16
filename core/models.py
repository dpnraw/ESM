from django.core.cache import cache
from django.db import models
from model_utils.models import TimeStampedModel


class SingletonModel(models.Model):
    ''' Singleton Model '''
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.id = 1
        super(SingletonModel, self).save(*args, **kwargs)
        self.set_cache()

    def delete(self, *args, **kwargs):
        pass

    def set_cache(self):
        '''
        To reduce the amount of database requests,
        you can save settings to cache. For this let’s
        add method set_cache to the model.
        '''
        cache.set(self.__class__.__name__, self)

    @classmethod
    def load(cls):
        '''
        When we call load method, an object will be
        loaded from a database or, if the object does
        not exist in a database, it will be created.
        When you save an instance of the model, it
        always has the same primary key, so there is
        only one record for this model in the database.
        Thus, in order to create a class responsible
        for site settings, we will create a class
        based on an abstract SingletonModel.
        '''
        if cache.get(cls.__name__) is None:
            obj, created = cls.objects.get_or_create(id=1)
            if not created:
                obj.set_cache()
        return cache.get(cls.__name__)


class GeoCodingSettings(SingletonModel, TimeStampedModel):
    '''
    This is a base class for Singleton model.
    When we call load method, an object will be
    loaded from a database or, if the object does
    not exist in a database, it will be created.
    So, in order to create a class responsible for
    site settings we will create a class based
    on an abstract SingletonModel.
    '''

    customer_location = models.BooleanField(default=False)
    sale_location = models.BooleanField(default=False)

    def __str__(self) -> str:
        repr = 'Customer Location: {} and Sale Location: {}'
        return repr.format(
            self.customer_location,
            self.sale_location,
        )

    class Meta:
        verbose_name_plural = 'Reverse Geocoding Settings'
