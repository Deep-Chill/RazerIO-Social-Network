from django.db.models import Aggregate

class CacheCompanyScore(Aggregate):
    function = None
    template = '%(function)s(%(expressions)s)'

    def as_sql(self, compiler, connection, function=None, template=None):
        self.function = connection.ops.quote_name('cache_company_score')
        return super().as_sql(compiler, connection, function, template)
