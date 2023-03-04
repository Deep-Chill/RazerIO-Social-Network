from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models import Q

# Create your models here.

User = settings.AUTH_USER_MODEL

PROGRAMMING_SKILLS = [
    ('python', 'Python'),
    ('java', 'Java'),
    ('csharp', 'C#'),
    ('cplus', 'C++'),
    ('php', 'PHP'),
    ('javascript', 'JavaScript'),
    ('ruby', 'Ruby'),
    ('swift', 'Swift'),
    ('objective_c', 'Objective-C'),
    ('go', 'Go'),
    ('kotlin', 'Kotlin'),
    ('scala', 'Scala'),
    ('rust', 'Rust'),
    ('typescript', 'TypeScript'),
    ('dart', 'Dart'),
    ('perl', 'Perl'),
    ('lua', 'Lua'),
    ('sql', 'SQL'),
    ('html', 'HTML'),
    ('css', 'CSS'),
    ('bash', 'Bash'),
    ('powershell', 'PowerShell'),
    ('assembly', 'Assembly'),
    ('matlab', 'MATLAB'),
    ('r', 'R'),
    ('swift', 'Swift'),
    ('visual_basic', 'Visual Basic'),
    ('delphi', 'Delphi'),
    ('cobol', 'COBOL'),
    ('fortran', 'FORTRAN'),
    ('lisp', 'Lisp'),
    ('prolog', 'Prolog'),
    ('scheme', 'Scheme'),
    ('smalltalk', 'Smalltalk'),
    ('haskell', 'Haskell'),
    ('erlang', 'Erlang'),
    ('fsharp', 'F#'),
    ('ocaml', 'OCaml'),
    ('groovy', 'Groovy'),
    ('perl6', 'Perl 6'),
    ('crystal', 'Crystal'),
    ('nim', 'Nim'),
    ('elixir', 'Elixir'),
    ('reasonml', 'ReasonML'),
    ('clojure', 'Clojure'),
    ('clojurescript', 'ClojureScript'),
    ('coffeescript', 'CoffeeScript'),
    ('haxe', 'Haxe'),
    ('dart', 'Dart'),
    ('reason', 'Reason'),
    ('elm', 'Elm'),
    ('graphql', 'GraphQL'),
    ('purescript', 'PureScript'),
    ('swift', 'Swift'),
    ('kotlin', 'Kotlin'),
    ('scala', 'Scala'),
    ('groovy', 'Groovy'),
    ('ruby_on_rails', 'Ruby on Rails'),
    ('django', 'Django'),
    ('flask', 'Flask'),
    ('express', 'Express.js'),
    ('angular', 'AngularJS'),
    ('react', 'ReactJS'),
    ('vue', 'Vue.js'),
    ('ember', 'Ember.js'),
    ('backbone', 'Backbone.js'),
    ('meteor', 'Meteor.js'),
    ('spring', 'Spring Framework'),
    ('laravel', 'Laravel'),
    ('codeigniter', 'CodeIgniter'),
    ('yii', 'Yii'),
    ('symfony', 'Symfony'),
    ('cakephp', 'CakePHP'),
    ('zend', 'Zend'),
    ('aspnet', 'ASP.NET'),
    ('nodejs', 'Node.js'),
    ('nextjs', 'Next.js'),
    ('gatsbyjs', 'Gatsby.js'),
    ('nuxtjs', 'Nuxt.js'),
    ('gridsome', 'Gridsome'),
    ('strapi', 'Strapi'),
    ('contentful', 'Contentful'),
    ('sanity', 'Sanity'),
    ('prismic', 'Prismic'),
    ('wordpress', 'WordPress'),
    ('drupal', 'Drupal'),
    ('joomla', 'Joomla')]

class CustomUser(AbstractUser):
    Bio = models.CharField(max_length=240, default='')
    Salary = models.IntegerField(default=0)
    Company = models.ForeignKey('Company.Company', on_delete=models.CASCADE,
                                   null=True, blank=True)
    Skills = models.ManyToManyField('Skill', blank=True)
    Country = models.CharField(choices=(('USA', 'USA'), ('Canada', 'Canada')),
                               max_length=50, default='USA')

    def __str__(self):
        return self.username



class Skill(models.Model):
    name = models.CharField(choices=PROGRAMMING_SKILLS, max_length=50)

    def __str__(self):
        return self.name


class UserFollowing(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    Following_User_ID = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['User', 'Following_User_ID'], name='unique_followers')
        ]
        ordering = ["-created"]
    def __str__(self):
        return f'{self.User}'

